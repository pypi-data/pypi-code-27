# -*- coding: utf-8 -*-
# http://psutil.readthedocs.io/en/latest/
"""Main module."""
try:
    import psutil
except ImportError:
    installer = ['install', '--user', 'psutil']
    try:
        import pip
        pip.main(installer)  # pip old
    except AttributeError:
        try:
            from pip._internal import main  # pip new
            main(installer)
        except AttributeError as e1:
            pass

try:
    import psutil
except ImportError:
    import sys
    sys.exit(1)


try:
    import cpuinfo
except ImportError:
    installer = ['install', '--user', 'py-cpuinfo']
    try:
        import pip
        pip.main(installer)  # pip old
    except AttributeError:
        try:
            from pip._internal import main  # pip new
            main(installer)
        except AttributeError as e1:
            pass

try:
    import cpuinfo
except ImportError:
    import sys
    sys.exit(1)


class TBLuModule:

    def cpu_info(self):
        data = cpuinfo.get_cpu_info()
        data['hz_actual_raw'] = data['hz_actual_raw'][0]
        data['hz_advertised_raw'] = data['hz_advertised_raw'][0]
        data['cpuinfo_version'] = ".".join(
            str(x) for x in data['cpuinfo_version'])
        result = []
        result.append(data)
        return result

    def cpu_times(self):
        data = psutil.cpu_times(percpu=True)
        result = []
        for idx, val in enumerate(data):
            cpu = dict(val.__dict__)
            cpu['cpuIndex'] = idx
            result.append(cpu)
        return result

    def cpu_freq(self):
        data = psutil.cpu_freq(percpu=True)
        result = []
        for idx, val in enumerate(data):
            cpu = dict(val.__dict__)
            cpu['cpuIndex'] = idx
            result.append(cpu)
        return result

    def virtual_memory(self):
        data = psutil.virtual_memory()
        result = []
        result.append(dict(data.__dict__))
        return result

    def swap_memory(self):
        data = psutil.swap_memory()
        result = []
        result.append(dict(data.__dict__))
        return result

    def disk_usage(self):
        dataP = psutil.disk_partitions(all=True)
        result = []
        for val in dataP:
            d = psutil.disk_usage(val.mountpoint)
            if d.total != None and d.total > 0:
                d1 = dict(d.__dict__)
                d2 = dict(val.__dict__)
                d1.update(d2)
                result.append(d1)
        return result

    def disk_io_counters(self):
        data = psutil.disk_io_counters(perdisk=True)
        result = []
        for val in data:
            d = dict(data[val].__dict__)
            d['disk'] = val
            result.append(d)
        return result

    def net_io_counters(self):
        data = psutil.net_io_counters(pernic=True)
        result = []
        for val in data:
            d = dict(data[val].__dict__)
            d['if'] = val
            result.append(d)
        return result

    def net_if_addrs(self):
        data = psutil.net_if_addrs()
        dataS = psutil.net_if_stats()
        result = []
        for val in data:
            for j in dataS:
                if val == j:
                    d1 = {}
                    d1['if'] = val
                    d1['address'] = []
                    d2 = dict(dataS[val].__dict__)
                    d1.update(d2)
                    for add in data[val]:
                        address = dict(add.__dict__)
                        d1['address'].append(address)
                    result.append(d1)
        return result

    def call(self, method):
        return getattr(self, method)()
