from .log import lprint, gprint, rprint
from .data import Cache, Info
from .setting import DB_FOFA


def search_in_db(key=None, *show_options):
    prepare_test_info = []
    DB_Handle = Cache(DB_FOFA)
    if not key:
        for i in DB_Handle.query(Info):
            lprint(title=i.title, os=i.os, ip=i.ip, ports=i.ports, time=i.ctime, geo=i.geo, body=i.body)
    else:
        
        if not show_options:
            def printer(i):
                
                lprint(title=i.title, os=i.os, ip=i.ip, ports=i.ports, time=i.ctime, geo=i.geo, body=i.body)
                prepare_test_info.append(i)
        else:
            def printer(i):
                
                prepare_test_info.append(i)
                f = {}
                for show in show_options:
                    if hasattr(i,show):
                        f[show] = getattr(i, show)
                    elif show == 'time':
                        f[show] = getattr(i, 'c' + show)
                lprint(**f)
            
        for i in DB_Handle.fuzzy_search(Info, key, printer=printer):
            pass
        
    gprint("set target: %d" % len(prepare_test_info))
    return prepare_test_info

