import json
from src.pyls.pyls import build_size, apply_filter

with open("../data/sample.json") as f:
    json_data = json.load(f)


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

def test_apply_filter():
    for item in json_data["contents"]:
        if "contents" not in item:
            assert apply_filter(item, "dir") is True
            assert apply_filter(item, "file") is False
        else:
            assert apply_filter(item, "dir") is False
            assert apply_filter(item, "file") is True



