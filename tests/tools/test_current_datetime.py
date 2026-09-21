from tools.current_datetime import current_datetime

def test_current_datetime():
    result = current_datetime()
    assert isinstance(result, str)