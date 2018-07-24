import conlog
import utils


def test_start_from_yaml_simple():
    """Test executing start_from_yaml with a simple YAML
    configuration. Will pass if it returns a Logger Without
    Exception.
    """
    log = conlog.start(yaml_file='test/yaml/simple.yml')
    log.info('Testing')


def test_start_from_yaml_complex(requires_tmp):
    """Test executing start_from_yaml with a complex YAML
    configuration. Will pass if it returns a Logger Without
    Exception.
    """
    log = conlog.start(yaml_file='test/yaml/complex.yml')
    log.info('Testing')
    # File below is specified in test/yaml/complex.yml
    utils.cleanup(log, 'test/tmp/test.log')
