import time
import re

def get_hostdata_item(uid, timeout, warning_limit, report_callback):
    match = re.search(r"^([a-fA-F\d\.:]+) (.*)", uid)
    if match:
        host = match.group(1)
        desc = ' ' + match.group(2)
    else:
        host = uid
        desc = ''

    return HostData(uid, desc, host, timeout, warning_limit, report_callback)

class HostData():
    def __init__(self, uid, desc, host, timeout, warning_limit, report_callback):
        self.uid = uid
        self.desc = desc
        self.host = host
        self.desc_len = len(host) + len(desc)
        self.max_desc_len = self.desc_len
        self.warning_limit = warning_limit  # msec
        self.fault_limit = timeout * 1000  # msec
        self.last_value = None
        self.minute = Cache(60)
        self.hour = Cache(3600)
        self.total = Cache(0)
        self.future = None
        self.report_callback = report_callback
        self.first = True

    def update_max_desc_len(self, max_desc_len):
        self.max_desc_len = max_desc_len

    def update_value(self, utime, value):
        self.last_value = value
        # minute
        self.minute.calc(utime, value, value, 1 if value >= self.fault_limit else 0)

        # hour
        if (time.time() - self.minute.start) >= 60:
            self.hour.calc(self.minute.get_first(),self.minute.avg,self.minute.max,self.minute.err)

            if self.report_callback:
                if self.first:
                    self.first = False
                else:
                    assert callable(self.report_callback)
                    self.report_callback(self.uid, *self.minute.as_tuple())

            self.minute.reset(60)

        # total
        if (time.time() - self.hour.start) >= 3600:
            self.total.calc(self.hour.get_first(), self.hour.avg, self.hour.max, self.hour.err)
            self.hour.reset(3600)

class Cache():
    def __init__(self, subtract_time):
        self.time_cache = []
        self.cache = []
        self.reset(subtract_time)

    def as_tuple(self):
        return (
            self.start,
            self.avg,
            self.max,
            self.err,
            self.len
        )
    
    def get_first(self):
        return self.time_cache[0]

    def reset(self, subtract_time):
        self.time_cache.clear()
        self.cache.clear()
        self.len = 0
        self.avg = 0.0
        self.max = 0.0
        self.err = 0
        t = time.time()
        if subtract_time:
            self.start = t - (t % subtract_time)
        else:
            self.start = t
    
    def calc(self, utime, value, max_val, fault_count):
        self.calc_avg(utime, value)
        self.calc_max(max_val)
        self.calc_err(fault_count)

    def calc_avg(self, utime, value):
        self.time_cache.append(utime)
        self.cache.append(value)
        self.len = len(self.cache)
        self.avg = sum(self.cache) / self.len

    def calc_max(self, max_val):
        self.max = max(self.max, max_val)

    def calc_err(self, fault_count):
        self.err += fault_count
