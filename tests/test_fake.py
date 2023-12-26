import pytest


@pytest.fixture
def query():
    return 2


@pytest.mark.parametrize("num,ans", ([(1, 2), (2, 4)]))
def test(query, num, ans):
    assert query * num == ans
