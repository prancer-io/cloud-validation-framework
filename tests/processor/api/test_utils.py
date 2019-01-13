from processor.api.utils import gettokentimeout

def test_json_record():
    val = gettokentimeout()
    assert type(val) is int
