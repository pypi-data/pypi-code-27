import subprocess
import os
import codecs
import sys


def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(path, mode)


def rgbToAnsi(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16

        if r > 248:
            return 231

        return round(((r - 8) / 247) * 24) + 232

    ansi = 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

    return ansi


def executecmd(cmd):
    return subprocess.run([cmd], shell=True).returncode == 0


class ShellHandler:
    def __init__(self):
        pass

    def setPrompt(self, string, colorfront, colorback):

        prompt = '\\e[0;35m(' + string + ')\\e[m \\u@\W -> '

        if colorfront is None:
            prompt = '\\033[48;5;' + str(colorback) + 'm(' + string + ')\\033[0m \\u@\W -> '
        elif colorback is None:
            prompt = '\\033[38;5;' + str(colorfront) + 'm(' + string + ')\\033[0m \\u@\W -> '
        else:
            prompt = '\\033[48;5;' + str(colorback) + ';38;5;' + str(
                colorfront) + 'm(' + string + ')\\033[0m \\u@\W -> '

        os.environ['PS1'] = prompt

    def launchShell(self):
        process = subprocess.Popen(['/bin/bash', '-i'])
        process.wait()

    def addToEnv(self, name, value):
        if name in os.environ:
            os.environ[name] += ':' + value
        else:
            # print('Warning the env var ' + name + ' doesnt exist')
            os.environ[name] = value

    def setToEnv(self, name, value):
        os.environ[name] = value


class Verse:
    def __init__(self, rootdir, lines):
        self.rootdir = rootdir
        self.lines = lines
        self.shell = ShellHandler()
        self.foreground = None
        self.background = None
        self.name = None
        self.alias = dict()  # str name, (str cmd, str desc)
        self.runcmd = list()
        self.setupcmd = list()
        self.tmpDesc = None

    def createHelp(self):
        with open(os.path.join(self.rootdir, 'cache/aliases/help.txt'), 'w') as the_file:
            for n, t in self.alias.items():
                c, d = t
                the_file.write('Aliases:\n\n')
                if d is None:
                    the_file.write(n + '\n\t' + c + '\n')
                else:
                    the_file.write(n + ' - ' + str(d) + '\n\t\t' + c + '\n')

        self.writeAlias('vhelp', 'cat ' + os.path.join(self.rootdir, 'cache/aliases/help.txt'))

    def writeAlias(self, name, cmd):
        self.alias[name] = (cmd, self.tmpDesc)
        self.tmpDesc = None

        output = "#!/usr/bin/env bash\n\n" + cmd

        with open(os.path.join(self.rootdir, 'cache/aliases/' + name), 'w') as the_file:
            the_file.write(output)
        make_executable(os.path.join(self.rootdir, 'cache/aliases/') + name)

    def parseOneLine(self, line, isInfo=False):
        if len(line) <= 0:
            return

        elems = line.split(' ')

        token = elems[0]

        if token == 'NAME':
            self.name = line[len(token) + 1:]

        elif token == 'FORE':
            color = line[len(token) + 1:]
            color = color.split(' ')
            color = rgbToAnsi(int(color[0]), int(color[1]), int(color[2]))
            self.foreground = color

        elif token == 'BACK':
            color = line[len(token) + 1:]
            color = color.split(' ')
            color = rgbToAnsi(int(color[0]), int(color[1]), int(color[2]))
            self.background = color

        elif token == 'ALIAS':
            name = elems[1]
            cmd = line[len(token) + 1 + len(name) + 1:]
            self.writeAlias(name, cmd)

        elif token == 'ENV':
            if not isInfo:
                inst = elems[1]
                if inst == 'ADD':
                    v = elems[2]
                    val = line[len(token) + 1 + len(inst) + 1 + len(v) + 1:]
                    if val[0] != '/':
                        val = os.path.join(os.getcwd(), val)
                    self.shell.addToEnv(v, val)
                elif inst == 'SET':
                    v = elems[2]
                    val = line[len(token) + 1 + len(inst) + 1 + len(v) + 1:]
                    if val[0] != '/':
                        val = os.path.join(os.getcwd(), val)
                    self.shell.addToEnv(v, val)
                else:
                    print('Bad option for ENV: ' + line)


        elif token == 'PRINT':
            if not isInfo:
                p = line[len(token) + 1:]
                p = codecs.escape_decode(p)[0].decode()
                print(p)
        elif token == 'DESC':
            self.tmpDesc = line[len(token) + 1:]

        elif token == 'RUN':
            cmd = line[len(token) + 1:]
            self.runcmd.append(cmd)

        elif token == 'SETUP':
            cmd = line[len(token) + 1:]
            self.setupcmd.append(cmd)

        else:
            print('Command not found or bad syntax: ' + line)

    def parseLines(self, isInfo=False):
        i = 0
        for l in self.lines:
            try:
                self.parseOneLine(l, isInfo)
            except Exception as e:
                print('Error while parsing line ' + str(i) + ' -> ' + l)
                print(str(e))

    def shellmode(self):
        self.parseLines()
        self.addDefaultEnv()

        self.createHelp()

        self.shell.setPrompt(self.name, self.foreground, self.background)

        self.launchShell()

    def addDefaultEnv(self):
        if self.rootdir[0] == '/':
            self.shell.addToEnv('PATH', os.path.join(self.rootdir, 'scripts'))
            self.shell.addToEnv('PATH', os.path.join(self.rootdir, 'cache/aliases'))
            subprocess.Popen(['mkdir', '-p', os.path.join(self.rootdir, 'cache/aliases')])
        else:
            self.shell.addToEnv('PATH', os.path.join(os.getcwd(), self.rootdir, 'scripts'))
            self.shell.addToEnv('PATH', os.path.join(os.getcwd(), self.rootdir, 'cache/aliases'))
            subprocess.Popen(['mkdir', '-p', os.path.join(self.rootdir, 'cache/aliases')])

    def launchShell(self):
        self.shell.launchShell()

    def run(self):
        for l in self.lines:
            elems = l.split(' ')

            token = elems[0]

            if token == 'RUN':
                cmd = l[len(token) + 1:]
                executecmd(cmd)

    def setup(self):
        for l in self.lines:
            elems = l.split(' ')

            token = elems[0]

            if token == 'SETUP':
                cmd = l[len(token) + 1:]
                executecmd(cmd)


def shellmode(rootdir):
    try:
        lines = [line.rstrip('\n') for line in open(os.path.join(rootdir, 'Versefile'))]
    except FileNotFoundError:
        print('Error: no Versefile found at location: ' + rootdir)
        return 1
    else:
        v = Verse(rootdir, lines)
        v.shellmode()


def run(rootdir):
    try:
        lines = [line.rstrip('\n') for line in open(os.path.join(rootdir, 'Versefile'))]
    except FileNotFoundError:
        print('Error: no Versefile found at location: ' + rootdir)
        return 1
    else:
        v = Verse(rootdir, lines)
        v.run()


def setup(rootdir):
    try:
        lines = [line.rstrip('\n') for line in open(os.path.join(rootdir, 'Versefile'))]
    except FileNotFoundError:
        print('Error: no Versefile found at location: ' + rootdir)
        return 1
    else:
        v = Verse(rootdir, lines)
        v.setup()


def help():
    print('[USAGE] verse {ROOTDIR, default=./verse}')
    print('\tLaunch verse with a optional path to a dir containing a Versefile\n')
    print('- [arg] is mandatory, {arg} is optional\n')
    print('[USAGE] verse [OPTIONS]')
    print('\tOptions:')
    print('\t\trun {ROOTDIR}:\n\t\t\tExecute all RUN commands of Versefile\n')
    print('\t\tsetup {ROOTDIR}:\n\t\t\tExecute all SETUP commands of Versefile\n')
    print('\t\tlist {ROOTDIR}:\n\t\t\tDisplay all commands in Versefile\n')
    print('\t\tinfo {ROOTDIR}:\n\t\t\tDisplay Versefile info\n')
    print('\t\thelp:\n\t\t\tDisplay help\n')
    print('Commands in a Versefile:')
    print('\tNAME [name]: The name of the project (will be displayed in prompt)')
    print('\tFORE [r] [g] [b]: Color of prompt foreground')
    print('\tBACK [r] [g] [b]: Color of prompt background')
    print('\tPRINT [message]: Print a message')
    print(
        '\tALIAS [command]: Create a alias for a command.\n\t\tWARNING! The command will be executed in a subshell not like a real alias.')
    print(
        '\tDESC [description]: Put a description for an alias.\n\t\tWARNING! Must be placed before an ALIAS instruction.')
    print('\tENV [instruction]:')
    print('\t\tADD [key] [value]: Add value to env key (append)')
    print('\t\tSET [key] [value]: Set value to env key (replace)')
    print('\tRUN [command]: Command to execute when type verse run')
    print('\tRUN [SETUP]: Command to execute when type verse setup')


def info(rootdir):
    try:
        lines = [line.rstrip('\n') for line in open(os.path.join(rootdir, 'Versefile'))]
    except FileNotFoundError:
        print('Error: no Versefile found at location: ' + rootdir)
        return 1
    else:
        print('Actual info about Versefile located in ' + rootdir + ':\n')

        v = Verse(rootdir, lines)
        v.parseLines(True)

        print('Name: ' + v.name + '\n')

        print('Aliases:')
        for n, t in v.alias.items():
            c, d = t
            if d is None:
                print('\t' + n + '\n\t' + c + '\n')
            else:
                print('\t' + n + ' - ' + str(d) + '\n\t\t' + c + '\n')

        print('Run commands:')
        for c in v.runcmd:
            print('\t' + c)

        print('Setup commands:')
        for c in v.runcmd:
            print('\t' + c)


def main():
    rootdir = './verse'

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'run':
            if len(sys.argv) > 2:
                rootdir = sys.argv[2]
            run(rootdir)

        if cmd == 'setup':
            if len(sys.argv) > 2:
                rootdir = sys.argv[2]
            setup(rootdir)

        if cmd == 'info':
            if len(sys.argv) > 2:
                rootdir = sys.argv[2]
            info(rootdir)

        elif cmd == 'help':
            help()

        else:
            rootdir = sys.argv[1]
            shellmode(rootdir)

    else:
        shellmode(rootdir)


if __name__ == '__main__':
    main()
