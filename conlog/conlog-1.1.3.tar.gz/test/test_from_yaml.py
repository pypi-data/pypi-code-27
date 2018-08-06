import conlog
import utils


def test_start_from_yaml_simple():
    """Test executing start_from_yaml with a simple YAML
    configuration.

    Will pass if it returns a Logger Without Exception.
    """
    log = conlog.start(yaml_file='test/yaml/simple.yml')
    log.info('Testing')


def test_start_from_yaml_complex(requires_tmp):
    """Test executing start_from_yaml with a complex YAML
    configuration.

    Will pass if,
        A) It returns a Logger without Exception.
        B) Logger logs to file correctly
    """
    tmp_file = 'test/tmp/test.log' # Specified in test/yaml/complex.yml
    log = conlog.start(yaml_file='test/yaml/complex.yml')
    log.info('Testing')
    #
    # TODO: Add log output validation
    #
    utils.cleanup(log, tmp_file)
