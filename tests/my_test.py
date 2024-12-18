from src.pyls.pyls import build_size


def test_build_size():
    size = 1023
    assert build_size(size) == '1023'
    size = 1024
    assert build_size(size) == '1.0K'
    size = 1048576
    assert build_size(size) == '1.0M'
    size = 1073741824
    assert build_size(size) == '1.0G'
    size = 1099511627776
    assert build_size(size) == '1.0T'




