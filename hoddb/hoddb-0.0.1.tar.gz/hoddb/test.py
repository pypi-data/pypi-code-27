import client
c = client.Client()
res = c.query("SELECT * WHERE { ?x rdf:type/rdfs:subClassOf* brick:Point };")
s = c.search("Temperature")
import IPython; IPython.embed()
