import json
from src.pyls.pyls import (build_size, apply_filter, print_top_level, print_path_info,
                           print_top_level_vertically_with_info)

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

def test_print_top_level(capsys):  # or use "capfd" for fd-level
    print_top_level(json_data, False, None)
    captured = capsys.readouterr()
    assert captured.out == "LICENSE README.md ast go.mod lexer main.go parser token\n"
    print_top_level(json_data, True, None)
    captured = capsys.readouterr()
    assert captured.out == ".gitignore LICENSE README.md ast go.mod lexer main.go parser token\n"

def test_print_path_info(capsys):
    print_path_info(json_data, False, False, False, None, "parser")
    captured = capsys.readouterr()
    assert (captured.out == "drwxr-xr-x 1.3K Nov 17 8:21 ./parser/parser_test.go\n" +
            "-rw-r--r-- 1.6K Nov 17 7:35 ./parser/parser.go\n" +
            "drwxr-xr-x 533 Nov 14 11:33 ./parser/go.mod\n")

    print_path_info(json_data, False, False, False, None,
                    "token/test_deep/test_deeper")
    captured = capsys.readouterr()
    assert (captured.out == "-rw-r--r-- 910 Nov 14 10:27 ./token/test_deep/test_deeper/deep_deep\n" +
            "drwxr-xr-x 66 Nov 14 7:52 ./token/test_deep/test_deeper/deep_deep_again\n")

    print_path_info(json_data, False, False, False, None,
                    "this_is_a/wrong/path")
    captured = capsys.readouterr()
    assert (captured.out == "error: cannot access 'this_is_a/wrong/path': No such file or directory\n")

def test_print_vertically_with_info(capsys):
    print_top_level_vertically_with_info(json_data, False, False, False, None)
    captured = capsys.readouterr()
    assert (captured.out == "drwxr-xr-x 1.0K Nov 14 6:57 LICENSE\n" +
            "drwxr-xr-x 83 Nov 14 6:57 README.md\n-rw-r--r-- 4.0K Nov 14 11:28 ast\n" +
            "drwxr-xr-x 60 Nov 14 9:21 go.mod\ndrwxr-xr-x 4.0K Nov 14 10:51 lexer\n" +
            "-rw-r--r-- 74 Nov 14 9:27 main.go\ndrwxr-xr-x 4.0K Nov 17 8:21 parser\n" +
            "-rw-r--r-- 4.0K Nov 14 10:27 token\n")

    print_top_level_vertically_with_info(json_data, True, False, False, None)
    captured = capsys.readouterr()
    assert (captured.out == "drwxr-xr-x 8.7K Nov 14 6:57 .gitignore\ndrwxr-xr-x 1.0K Nov 14 6:57 LICENSE\n" +
            "drwxr-xr-x 83 Nov 14 6:57 README.md\n-rw-r--r-- 4.0K Nov 14 11:28 ast\n" +
            "drwxr-xr-x 60 Nov 14 9:21 go.mod\ndrwxr-xr-x 4.0K Nov 14 10:51 lexer\n" +
            "-rw-r--r-- 74 Nov 14 9:27 main.go\ndrwxr-xr-x 4.0K Nov 17 8:21 parser\n" +
            "-rw-r--r-- 4.0K Nov 14 10:27 token\n")

    print_top_level_vertically_with_info(json_data, True, False, False, None)
    captured = capsys.readouterr()
    assert (captured.out == "drwxr-xr-x 8.7K Nov 14 6:57 .gitignore\ndrwxr-xr-x 1.0K Nov 14 6:57 LICENSE\n" +
            "drwxr-xr-x 83 Nov 14 6:57 README.md\n-rw-r--r-- 4.0K Nov 14 11:28 ast\n" +
            "drwxr-xr-x 60 Nov 14 9:21 go.mod\ndrwxr-xr-x 4.0K Nov 14 10:51 lexer\n" +
            "-rw-r--r-- 74 Nov 14 9:27 main.go\ndrwxr-xr-x 4.0K Nov 17 8:21 parser\n" +
            "-rw-r--r-- 4.0K Nov 14 10:27 token\n")

    print_top_level_vertically_with_info(json_data, False, True, False, None)
    captured = capsys.readouterr()
    assert (captured.out == "-rw-r--r-- 4.0K Nov 14 10:27 token\ndrwxr-xr-x 4.0K Nov 17 8:21 parser\n" +
            "-rw-r--r-- 74 Nov 14 9:27 main.go\ndrwxr-xr-x 4.0K Nov 14 10:51 lexer\n" +
            "drwxr-xr-x 60 Nov 14 9:21 go.mod\n-rw-r--r-- 4.0K Nov 14 11:28 ast\n" +
            "drwxr-xr-x 83 Nov 14 6:57 README.md\ndrwxr-xr-x 1.0K Nov 14 6:57 LICENSE\n")

    print_top_level_vertically_with_info(json_data, False, True, True, None)
    captured = capsys.readouterr()
    assert (captured.out == "drwxr-xr-x 4.0K Nov 17 8:21 parser\n-rw-r--r-- 4.0K Nov 14 11:28 ast\n" +
            "drwxr-xr-x 4.0K Nov 14 10:51 lexer\n-rw-r--r-- 4.0K Nov 14 10:27 token\n" +
            "-rw-r--r-- 74 Nov 14 9:27 main.go\ndrwxr-xr-x 60 Nov 14 9:21 go.mod\n" +
            "drwxr-xr-x 83 Nov 14 6:57 README.md\ndrwxr-xr-x 1.0K Nov 14 6:57 LICENSE\n")

    print_top_level_vertically_with_info(json_data, False, True, True, "file")
    captured = capsys.readouterr()
    assert (captured.out == "-rw-r--r-- 74 Nov 14 9:27 main.go\ndrwxr-xr-x 60 Nov 14 9:21 go.mod\n" +
            "drwxr-xr-x 83 Nov 14 6:57 README.md\ndrwxr-xr-x 1.0K Nov 14 6:57 LICENSE\n")

    print_top_level_vertically_with_info(json_data, False, True, True, "dir")
    captured = capsys.readouterr()
    assert (captured.out == "drwxr-xr-x 4.0K Nov 17 8:21 parser\n-rw-r--r-- 4.0K Nov 14 11:28 ast\n" +
            "drwxr-xr-x 4.0K Nov 14 10:51 lexer\n-rw-r--r-- 4.0K Nov 14 10:27 token\n")