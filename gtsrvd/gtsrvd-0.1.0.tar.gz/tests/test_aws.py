from unittest import mock, TestCase

from gtsrvd import aws


meta_ip_response = mock.MagicMock(text="192.168.1.100")


class TestAWS(TestCase):
    @mock.patch("gtsrvd.aws.client")
    @mock.patch("gtsrvd.aws.requests.get", return_value=meta_ip_response)
    def test_create(self, requests_get, client):
        aws.create_record("blastedstudios.com", "test1")
        self.assertTrue(client.change_resource_record_sets.called)

    @mock.patch("gtsrvd.aws.client")
    @mock.patch("gtsrvd.aws.requests.get", return_value=meta_ip_response)
    def test_delete(self, requests_get, client):
        aws.delete_record("blastedstudios.com", "test1")
        self.assertTrue(client.change_resource_record_sets.called)
