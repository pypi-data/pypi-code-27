"""Test settings."""
from __future__ import absolute_import, division, print_function, unicode_literals

SECRET_KEY = 'Use the force, Luke!'

DKIM_SELECTOR = 'selector'
DKIM_DOMAIN = 'example.com'
DKIM_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDQUTvs1Rqjw6Vq2/LRnI7LzycT1gM1G4ZRMdWiLFg7y4TEPwfW
r6RgR04f56L9PxM1B6gW+gTkm30dwxNbU60u7emcqu+mYCzyVBHx9a4uhI3Ts8sy
67zIIeXarmxh+V/jqmAbdRAzRzAvjs0S74di1mwCplxYvVOEsDOj7OIEDQIDAQAB
AoGAR2rSJIuaqnI0j8IAKSSHQBAw0XgZeWeKUOPI3eReC4HmbnE9eriUnf1UJ1P+
aNvq9c8+LUJh0w4LgtySEklJoaK6rqLsdQhriHRiYThctMlzoZiLuVo6MQdACHBj
5LvjQY+PSIkpdoQumQJAwngyG0Zkg+t2u57UINn+p3zBxoECQQDuaF5HBELdbu84
08UsiG+zvuGoKEjtr4EjRZ9hdgkErooO8SXbJT+ALwJ6M6awGvkxQiPYR39kgCcG
VpB744aFAkEA37Bx33DKOpbOju2IaF4nwJ/JBmz54EvFOTl2ImP9iHM2qfZo8ueg
/iOG2vifayt5FvgTN7I7rpo3oQcI1DLR6QJBANskYmyi9Rd3zjsNJfQeYZb2gZRB
m2+n4Gtcpvk+N2HvUgYUEfkTjwAztfJAIhtEYASwSCSY6/ekeLqxvVOzu8UCQQCm
F4eWF1OxiUS6j9kXVcJCnuJPKR+o0doRkX8MLh6U8KeIL/ThV+gMjCiX8r+8fb0d
tvneAzOZg90Gbgi6NznxAkAXQz0rYjnQwRjlCyS/KUG1fek/EfJBlgiDmMtYuUpq
UPPnqkzsGyB9LqzL4aoKg1LDsbVP0hSt97SYhB9TtcgO
-----END RSA PRIVATE KEY-----'''
