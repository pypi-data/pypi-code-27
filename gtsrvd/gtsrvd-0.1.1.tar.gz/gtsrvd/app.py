from gtsrvd import aws, nginx

cloud = aws  # "eventually" will be cloud agnostic (?)


def create(domain, subdomain, port):
    cloud.create_record(domain, subdomain)
    nginx.create_proxy(domain, subdomain, port)


def delete(domain, subdomain, port):
    cloud.delete_record(domain, subdomain)
    nginx.delete_proxy(domain, subdomain, port)
