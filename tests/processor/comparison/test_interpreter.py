
def mock_zero_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return []


def mock_get_documents(collection, query=None, dbname=None, sort=None, limit=10):
    return [{
        "structure": "azure",
        "reference": 'abcd',
        "source": 'snapshot',
        "path": '/a/b/c',
        "_id": "5c24af787456217c485ad1e6",
        "checksum": "7d814f2f82a32ea91ef37de9e11d0486",
        "collection": "microsoftcompute",
        "json":{
            "id": 124,
            "location": "eastus2",
            "name": "mno-nonprod-shared-cet-eastus2-tab-as03"
        },
        "queryuser": "ajeybk1@kbajeygmail.onmicrosoft.com",
        "snapshotId": 1,
        "timestamp": 1545908086831
    }]


def test_interpreter(monkeypatch):
    monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                        mock_get_documents)
    monkeypatch.setattr('processor.comparison.comparisonantlr.rule_interpreter', mock_get_documents)
    from processor.comparison.interpreter import Comparator
    comparator = Comparator('0.1', 'validator', {}, {
                    "testId": "1",
                    "snapshotId": "1",
                    "attribute": "location",
                    "comparison":"exist"
                })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "3",
        "snapshotId": "1",
        "attribute": "location.name",
        "comparison": "not exist"
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": "gt 10"
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "1",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": '"eastus2"'
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "1",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": 'len(eastus2)'
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "1",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": "'eastus2'"
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": "gt a"
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": "gt len(7)"
    })
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId": "1",
        "attribute": "location",
        "comparison": "eq '{2}.location'"
    })
    comparator = Comparator('0.2', 'validator', {}, {
        "testId": "3",
        "snapshotId": "1",
        "attribute": "location.name",
        "comparison": "not exist"
    })
    comparator.validate()
    comparator = Comparator('0.3', 'validator', {}, {
        "testId": "3",
        "snapshotId": "1",
        "attribute": "location.name",
        "comparison": "not exist"
    })
    comparator.validate()
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "1",
        "rule": "exist({1}.location)"
    })
    comparator.validate()
    comparator = Comparator('0.1', 'validator', {}, {})
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId": "1",
        "attribute": "id",
        "comparison": "gt 10"
    })
    val = comparator.validate()
    assert 'passed' == val['result']
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId1": "1",
        "attribute": "id",
        "comparison": "gt 10"
    })
    val = comparator.validate()
    # print(type(comparator))


def test_interpreter_1(monkeypatch):
    monkeypatch.setattr('processor.comparison.interpreter.get_documents',
                        mock_zero_get_documents)
    from processor.comparison.interpreter import Comparator
    comparator = Comparator('0.1', 'validator', {}, {
        "testId": "4",
        "snapshotId": "1",
        "attribute": "id",
        "comparison": "gt 10"
    })
    val = comparator.validate()
    comparator = Comparator('0.1', 'validator', {}, {})
    val = comparator.validate()

def atest_comparator():
    from processor.comparison.interpreter import Comparator
    comparator = Comparator('0.1', 'validator', {}, 'a', 'exist')
    print(type(comparator))
    comparator = Comparator('0.2', {'a': 'b'}, 'a', 'exist')
    print(comparator.validate())
    print(type(comparator))
    comparator = Comparator('0.3', {'a': 'b'}, 'a', 'exist')
    print(type(comparator))
    print(type(comparator.comparator))
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b'}, 'b', 'exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b'}, 'b', 'not exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 1}}, 'c.e', 'not exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 1}}, 'c.d', 'not exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 1}}, 'c.d', 'exist')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'gt 10')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'eq 10')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'neq 5')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'eq "eastus"')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'eq len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'neq len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'gt len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'gte len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'lt len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', 'lte len(7)')
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 'eastus2'}}, 'c.d', "eq '{2}.location'")
    print(comparator.validate())
    comparator = Comparator('0.1', {'a': 'b', 'c': {'d': 10}}, 'c.d', 'gtw 10')
    print(comparator.validate())