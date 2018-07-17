import sqlite3

from typedtsv import dumps, loads

with sqlite3.connect('proxy_cache.db') as conn:
    with open('outfile.ttsv', 'w') as outfile:
        rows = list(conn.execute('SELECT url, timestamp, status, page FROM page_cache LIMIT 1000'))
        dumps(('url', 'timestamp', 'status', 'page'), rows, outfile)

with open('outfile.ttsv', 'r', newline='\n') as infile:
    header_info, rows2 = loads(infile)

for r1, r2 in zip(rows, rows2):
    diff = set(r1).difference(r2)
    if diff:
        print(diff)

