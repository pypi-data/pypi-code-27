# Note: if you get 'ATE E0' messages you may want to disable ModemManager:
#       on ubuntu: 'systemctl stop ModemManager.service'

import time
import re
import threading
import glob
import sys
import signal
from os.path import basename

from . import serialconnection
from . import socketserver

# ==================================================================================================

def threadLocked(f):
    """decorator to make function thread exclusive"""
    lock = threading.Lock()
    def wrapper(*args, **kwargs):
        with lock:
            result = f(*args, **kwargs)
        return result
    return wrapper

# ==================================================================================================

@threadLocked
def log(msg):
    print(" -- {}".format(msg), file=sys.stderr)

@threadLocked
def output(msg):
    print(msg)
    socketServer.msgToAll(msg)

shutdown = False
def requestShutdown():
    global shutdown
    log("request global shutdown")
    shutdown = True

# TODO come on, this is not the way to do it
# enable debug logging for module
serialconnection.debug = lambda msg: log("(lc) {}".format(msg))
# shutdown all threads when a thread within this module crashes
serialconnection.onSubThreadCrash = requestShutdown

socketserver.debug = lambda msg: log("(ss) {}".format(msg))
socketserver.onSubThreadCrash = requestShutdown

# ==================================================================================================

def connectToAllttyACM(timeout = 1):
    paths = glob.glob("/dev/ttyACM*")
    paths.sort()

    if not paths:
        raise ConnectionError("could not find any /dev/ttyACM*")

    result = []
    try:
        for path in paths:
            # kudo's to piro and Claudiu on stackoverflow for the path = path trick
            # https://stackoverflow.com/questions/233673/how-do-lexical-closures-work
            handler = lambda msg, path = path: serialMsgHandler(msg, path)
            lc = serialconnection.Connection(path, handler, timeout = timeout)
            result.append(lc)
    except BaseException as e:
        for lc in result:
            lc.close()
        raise e

    return result

# ==================================================================================================

def listenOnStdin(handler, timeout = 1):
    global shutdown

    def raiseTimeout(_x,_y):
        raise TimeoutError()

    #note: cant use signal but in the main thread
    signal.signal(signal.SIGALRM, raiseTimeout)

    while not shutdown:
        signal.alarm(timeout)
        try:
            for line in sys.stdin:
                handler(line.strip())
            log("received EOF")
            requestShutdown()
        except TimeoutError as e:
            pass
        finally:
            signal.alarm(0)
    log("shut down stdin listener")

# ==================================================================================================

def serialMsgHandler(msg, path):
    log("{}: {}".format(path, msg))

    m = re.match("^([A-L]) ([01])$", msg)
    if m:
        laser_name, state = m.groups()
        for n, (b_lc, b_laser_name) in enumerate(beams):
            if b_lc.getPath() == path and b_laser_name == laser_name:
                output("{} {}".format(n, state))

# ==================================================================================================

beams = []

def command_reset():
    global lasikConns
    global beams

    beams = []

    for lc in lasikConns:
        lc.send("reset")

    for lc in lasikConns:
        for laser_name in "ABCDEFGHIJKL":
            beams.append((lc, laser_name))

def command_detect_beams():
    global lasikConns
    global beams

    beams = []

    for lc in lasikConns:
        response = lc.awaitResponse("get all", "all [01]{12}$")
        bits = re.match("^all ([01]{12})", response).group(1)
        for n,b in enumerate(bits):
            if b == "1":
                laser_name = chr(ord('A') + n)
                beams.append((lc, laser_name))
    logMsg = "detected {} beams:".format(len(beams))
    for n, (lc, laser_name) in enumerate(beams):
        logMsg += "\n    {:2} = {}: laser {}".format(n, lc.getPath(), laser_name)
    log(logMsg)

def command_disable_other_lasers():
    for lc in lasikConns:
        for l in "ABCDEFGHIJKL":
            detected = False
            for b_lc, b_laser_name in beams:
                if l == b_laser_name and lc.getPath() == b_lc.getPath():
                    detected = True
                    break
            if not detected:
                lc.send("set {} 0".format(l))
                # beware that this might result in a false beam detection
                lc.send("conf {} 0 0 0 0 0 1000 0".format(l))

def command_version():
    for lc in lasikConns:
        lc.send("version")

def argParse_set(args):
    beamNr, pwm = map(int,args)
    if not 0 <= pwm <= 255:
        log("pwm value must be in range 0-255")
        return None
    elif not 0 <= beamNr < len(beams):
        log("beamNr must be in range 0-{}".format(len(beams)-1))
        return None
    return (beamNr,pwm)

def command_set(beamNr, pwm):
    lc, laser_name = beams[beamNr]
    lc.send("set {} {}".format(laser_name, pwm))

def argParse_set_all(args):
    pwm, = map(int, args)
    if not 0 <= pwm <= 255:
        log("pwm value must be in range 0-255")
        return None
    return (pwm,)

def command_set_all(pwm):
    for lc, laser_name in beams:
        lc.send("set {} {}".format(laser_name, pwm))

def command_get_all():
    global lasikConns
    global beams

    allBeamStates = {}

    for lc in lasikConns:
        response = lc.awaitResponse("get all", "all [01]{12}$")
        bits = re.match("^all ([01]{12})", response).group(1)
        for n,b in enumerate(bits):
            laser_name = chr(ord('A') + n)
            allBeamStates[(lc.getPath(), laser_name)] = b

    bits = [allBeamStates[(lc.getPath(), laser_name)] for lc, laser_name in beams]

    output("all " + "".join(bits))

# ==================================================================================================

commandLock = threading.Lock()
def userCommandHandler(msg):
    # the argParse functions must take a tuple of strings and either return a tuple of valid
    # parameters its command_ or either return None if no valid parameters can be parsed from
    # the provided strings
    handlers = [
            ("set ([0-9]{1,3}) ([0-9]{1,3})$", argParse_set,        command_set),
            ("set all ([0-9]{1,3})$",          argParse_set_all,    command_set_all),
            ("reset$",                         lambda x:x,          command_reset),
            ("detect beams$|db$",              lambda x:x,          command_detect_beams),
            ("disable other lasers$|dol$",     lambda x:x,          command_disable_other_lasers),
            ("get all$",                       lambda x:x,          command_get_all),
            ("version$",                       lambda x:x,          command_version) ]

    success = False

    for regex, argParse, command in handlers:
        m = re.match(regex, msg)
        if m:
            args = argParse(m.groups())
            if args != None: # no arguments is (), thus != None
                with commandLock:
                    command(*args)
                success = True
            break

    if not success:
        log("bad command: '{}'".format(msg))

# ==================================================================================================

def init_lasiks():
    sleep_t = 0.2

    log("requesting firmware version number")
    command_version()
    log("waiting for {}s".format(sleep_t))
    time.sleep(sleep_t)

    log("resetting all lasers")
    command_reset()
    log("waiting for {}s".format(sleep_t))
    time.sleep(sleep_t)

    log("detecting beams")
    command_detect_beams()

    log("disabling the lasers that were not detected")
    command_disable_other_lasers()

# ==================================================================================================

lasikConns = None
socketServer = None

def main():
    global lasikConns
    global socketServer

    if len(sys.argv) == 1:
        host, port = "localhost", 1337
        log("no host and port specified, using defaults {}:{}".format(host,port))
    elif len(sys.argv) == 3:
        host, port = sys.argv[1], int(sys.argv[2])
    else:
        log("usage example: '{} HOST PORT'".format(basename(sys.argv[0])))
        exit(1)

    try: # TODO fix error handling
        # establish connections with lasik boards
        # be aware that this creates subthreads
        log("detecting and connecting to lasiks")
        lasikConns = connectToAllttyACM()

        log("initialising lasiks")
        init_lasiks()

        log("starting socket server")
        socketServer = socketserver.SocketServer(userCommandHandler, host = host, port = port)

        log("starting listening on stdin")
        listenOnStdin(userCommandHandler) # this blocks until EOF

    finally:
        requestShutdown()
        if "socketServer" in globals():
            socketServer.requestShutdown()
        if "lasikConns" in globals():
            for lc in lasikConns:
                lc.close()

if __name__ == "__main__":
    main()
