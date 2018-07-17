import unittest
from exoedge.exo_edge import ExoEdge, NoLocalConfigIO

class TestExoEdge(unittest.TestCase):
    def test_no_local_config(self):
        with self.assertRaises(NoLocalConfigIO):
            ExoEdge('', **{'local_strategy': True,
                           'config_io_file': '/file/dne'}).setup()
    
    def test_bool_init_logic(self):
        E = ExoEdge('', **{'local_strategy': True,
                           'config_io_file': '/file/dne',
                           'no_config_cache': True,
                           'no_config_sync': None})
        self.assertFalse(E.cache_config_io)
        self.assertTrue(E.config_io_sync)
        self.assertIsNotNone(E.config_io_watcher)

    def test_default_config_file(self):
        E = ExoEdge('', **{'murano_id': 'MYMURANOID'})
        self.assertEquals(E.config_io_file, 'MYMURANOID.json')


def main():
    unittest.main()

if __name__ == "__main__":
    main()
