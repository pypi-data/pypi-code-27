from concurrent.futures import ThreadPoolExecutor
import datetime
import re
import pathlib
import time
from functools import partial
from .hostdata import get_hostdata_item
from .ping import ping
from . import screen_layout

def ping_worker(cli, interrupt):
    default_layout = cli.layout.children.copy()
    hostdatalist = []
    threadpool = ThreadPoolExecutor(20)

    while cli._is_running:

        if cli.settings.hasChanged.is_set():
            cli.settings.hasChanged.clear()
            hostdatalist, timeout, interval, max_desc_len = init_hostdata(cli, default_layout, hostdatalist)

        cli.invalidate()
        duration = time.time()

        for hostdata in hostdatalist:
            hostdata.future = threadpool.submit(ping, hostdata.host, timeout)

        for hostdata in hostdatalist:
            if cli._is_running:
                value = hostdata.future.result()
                hostdata.update_max_desc_len(max_desc_len)
                hostdata.update_value(datetime.datetime.now(), value)

        cli.invalidate()
        interrupt.wait(interval - (time.time() - duration))
        interrupt.clear()

def init_hostdata(cli, default_layout, hostdatalist):
    layout = cli.layout
    screen_layout.clear(layout, default_layout)

    hosts = cli.settings.getlist("hosts")
    timeout = cli.settings.getfloat("general", "timeout")
    interval = cli.settings.getfloat("general", "interval")
    warning_limit = cli.settings.getfloat("general", "warning_limit")
    csvfilepath = cli.settings.getstr("general", "csvfilepath")

    if csvfilepath and not "!" in csvfilepath:
        csvfilecallback = partial(write_report_callback, csvfilepath)
    else:
        csvfilecallback = None

    for uid in hosts:
        for hostdata in hostdatalist:
            if uid == hostdata.uid:
                break
        else:
            hostdatalist.append(get_hostdata_item(uid, timeout, warning_limit, csvfilecallback))

    if hostdatalist:
        max_desc_len = max(item.desc_len for item in hostdatalist)
    else:
        max_desc_len = 0
    
    screen_layout.add_header(layout, max_desc_len)

    for hostdata in hostdatalist:
        # setup screen layout
        screen_layout.add_line_of_data(layout, hostdata)

    return hostdatalist, timeout, interval, max_desc_len

def write_report_callback(root_path, uid, time_v, avg_v, max_v, err_v, len_v):
    date_str = time.strftime("%Y-%m-%d", time.localtime(time_v))
    time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(time_v))
    cleanstr = re.compile(r'[^a-zA-Z0-9_\. ]')
    filename = "{} {}.csv".format(cleanstr.sub("", uid), date_str)
    filepath = pathlib.Path(root_path) / filename
    mode = "a" if filepath.exists() else "w"
    with filepath.open(mode=mode) as f:
        if mode == "w":
            print("name", "time", "avg", "max", "errors", "tries", sep="\t", end="\n", file=f)
        print(uid, time_str, avg_v, max_v, err_v, len_v, sep="\t", end="\n", file=f)
