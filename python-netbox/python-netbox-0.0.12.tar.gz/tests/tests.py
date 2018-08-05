import unittest
from netbox import NetBox


class TestNetBox(unittest.TestCase):

    def setUp(self):

        self.netbox = NetBox(host='127.0.0.1', port=80, use_ssl=False,
                             auth_token='21abdc9a716e3c2a4134834cd7909cee2022e404')

    def test_create_site(self):
        self.assertTrue(self.netbox.dcim.create_site('S1', 's-1'))

    def test_create_rack(self):
        self.assertTrue(self.netbox.dcim.create_rack('R1', 'S1000'))

    # def test_create_device_role(self):
    #     self.assertTrue(self.netbox.dcim.create_device_role('webserver', 'aa1409', 'webserver'))
    #
    # def test_create_manufacturer(self):
    #     self.assertTrue(self.netbox.dcim.create_manufacturer('manufacturer', 'manufacturer'))
    #
    # def test_create_device_type(self):
    #     self.assertTrue(self.netbox.dcim.create_device_type('server', 'server', 'manufacturer'))



