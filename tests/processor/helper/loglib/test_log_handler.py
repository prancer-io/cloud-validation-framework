from processor.helper.loglib.log_handler import getlogger


def test_getlogger():
    logger = getlogger()
    assert logger is not None
    logger1 = getlogger()
    assert logger1 is not None
    assert id(logger) == id(logger1)