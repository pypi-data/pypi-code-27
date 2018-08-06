import conlog
import utils


def test_start_from_args_no_args():
    """Test executing start_from_args with no arguments.

    Will pass if it returns a Logger without Exception.
    """
    log = conlog.start()
    log.info('Testing')


def test_start_from_args_simple_args(requires_tmp):
    """Test executing start_from_args with no arguments.

    Will pass if,
        A) It returns a Logger without Exception.
        B) Logger logs to file correctly
    """
    tmp_file = 'test/tmp/test.log'
    log = conlog.start(level='INFO', log_file=tmp_file)
    log.info('Testing')
    message = '     INFO -                 root - Testing'
    assert utils.read_log_entry(tmp_file) == message
    utils.cleanup(log, tmp_file)  # Cleanup log file


def test_start_from_args_complex_info(requires_tmp):
    """Test executing start_from_args with all available
    arguments.

    Will pass if,
        A) It returns a Logger without Exception.
        B) Logger logs to file correctly
    """
    tmp_file = 'test/tmp/test.log'
    log = conlog.start(
        log_file=tmp_file,
        log_format="%(asctime)22s : %(levelname)8s : %(name)20s : %(message)s",
        level='INFO',
        max_file_size='5 MB',
        max_retention=5,
    )
    log.info('Testing')
    message = '     INFO :                 root : Testing'
    assert utils.read_log_entry(tmp_file) == message
    utils.cleanup(log, tmp_file)


def test_start_from_args_complex_debug(requires_tmp):
    """Test executing start_from_args with all available
    arguments. Will pass if,
        A) It returns a Logger without Exception.
        B) Logger logs to file correctly
    """
    tmp_file = 'test/tmp/test.log'
    log = conlog.start(
        log_file=tmp_file,
        debug_format="%(asctime)22s : %(levelname)8s : %(name)20s : " \
                     "%(funcName)20s : %(message)s",
        level='DEBUG',
        max_file_size='5 MB',
        max_retention=5,
    )
    log.info('Testing Debug')
    message = '     INFO :                 root : ' \
              'test_start_from_args_complex_debug : Testing Debug'
    assert utils.read_log_entry(tmp_file) == message
    utils.cleanup(log, tmp_file)
