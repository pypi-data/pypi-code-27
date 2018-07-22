#!/usr/bin/env python

import requests
import xml.etree.ElementTree as et

mail = input('Adresse électronique : ')

domain = mail.split('@')[1]

result = requests.get('https://autoconfig.thunderbird.net/v1.1/' + domain)

if result.status_code == 404:
    print('Le domaine est introuvable')

else:
    xml = result.text
    root = et.fromstring(xml)
    outgoingServers = root.find('emailProvider').findall('outgoingServer')

    print(domain)
    print('##########')
    for server in outgoingServers:
        for i in server:
            print(i.tag.ljust(15), ':', i.text)
        print('------')