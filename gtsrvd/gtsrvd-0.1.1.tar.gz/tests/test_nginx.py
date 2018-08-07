import os
import shutil
import tempfile
from unittest import mock, TestCase

from gtsrvd import nginx


meta_ip_response = mock.MagicMock(text="192.168.1.100")


class TestNginx(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.subdomain = "test1"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    @mock.patch("gtsrvd.nginx.call")
    def test_create_proxy(self, call):
        with mock.patch("gtsrvd.nginx.NGINX_CONF_ROOT", self.temp_dir):
            conf_path = nginx.proxy_conf_path(self.subdomain)
            nginx.create_proxy("blastedstudios.com", self.subdomain, 8081)
            self.assertTrue(os.path.exists(conf_path))

    @mock.patch("gtsrvd.nginx.call")
    @mock.patch("gtsrvd.nginx.os")
    def test_delete_proxy(self, os, call):
        with mock.patch("gtsrvd.nginx.NGINX_CONF_ROOT", self.temp_dir):
            nginx.delete_proxy("blastedstudios.com", self.subdomain, 8081)
            self.assertTrue(call.called)
            self.assertTrue(os.remove.called)
