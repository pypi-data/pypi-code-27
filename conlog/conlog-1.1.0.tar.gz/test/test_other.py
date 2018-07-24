import conlog
# import utils


def test_module_defaults():
    """Test that no module defaults were altered. In the event
    that a default is actually being updated, this test should
    also be updated.
    """
    con = conlog.ConLog()
    assert con.log_file == None
    assert con.log_format == '%(asctime)22s - %(levelname)8s - %(name)20s - ' \
                             '%(message)s'
    assert con.debug_format == '%(asctime)22s - %(levelname)8s - ' \
                               '%(name)20s - %(funcName)20s - %(message)s'
    assert con.level == 'INFO'
    assert con.max_file_size == 5000000
    assert con.max_retention == 5
