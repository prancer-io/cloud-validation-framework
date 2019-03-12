from processor_enterprise.api.utils import gettokentimeout, parseint, parsebool

def test_gettokentimeout():
    val = gettokentimeout()
    assert type(val) is int

def test_parseint():
    assert 123 == parseint('123', 1)
    assert 2 == parseint('1.2', 2)
    assert 1 == parseint(True, 10)

def test_parsebool():
    assert True == parsebool('tRue', False)
    assert False == parsebool('False')
    assert True == parsebool(1)
    assert False == parsebool(None)
    assert True == parsebool(None, True)

