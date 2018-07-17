import client

c = client.Client("http://localhost:47808")
res = c.query("""SELECT ?s ?p ?o WHERE { ?s ?p ?o };""", timeout=60)
# number of results
print(res.count)
# loop through rows
for row in res.rows:
    print('?subject={0} ?predicate={1} ?object={2}'.format(row.s, row.p, row.o))
    print('?subject={0} ?predicate={1} ?object={2}'.format(row.values['?s'], row.values['?p'], row.values['?o']))

# simple group-by functionality
res = c.query("""SELECT ?s ?p ?o WHERE { ?s ?p ?o };""", timeout=60, groupby=['?s'])
# loop through rows
for s, groups in res.rows.items():
    print('?subject={0} has {1} groups'.format(s, len(groups)))
