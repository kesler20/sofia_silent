# Pytest Features
the --cov flag enables test coverage reports to be generated
it is also possible to generate reports in html so that you can see
which lines have not being covered
```python
import pytest

# can be used to inject many parameters to functions
@pytest.mark.parametrize("param,expected",[
    ("input1","expected_value1"),
    ("input2","expected_value2"),
    ("input3","expected_value3"),
])

def test_foo(param,expected):
    assert slap_many(param) is expected

# you can skip tests if you have not implemented a feature yet
# this will encourage test driven development
@pytest.mark.skip(reason="feature not implemented yet")
def test_feature():
    # do something
```

fixtures allow you to share a resource such as a database connection across the multiple tests
therefore, instead of writing setup code for multiple tests you can use the following

``conftest.py``
```python
import pytest

# if a resource needs to be accessed multiple times across different tests and the access is expensive 
# you should use yield because is a resource which needs to be closed
# the connection will be torn down after all tests run
# by specifying the scope you allow the connection to be created only once
# as the result of the function is called so that the function i called only once
@pytest.fixture(scope="session")
def db_conn():
    db = ...
    url = ...
    with db.connect(url) as conn:
        yield conn
    
test_slapping
import pytest 
def test_slapping(db_conn):
    db_conn.read_slaps()
    assert...
```
