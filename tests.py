from command import CMD
from pathlib import Path

def test_CMD():
    valid_command = CMD("--raport ./tests/src_file.cpp ./tests/test_file.cpp")
    assert valid_command.args == {
        "source_file": Path("./tests/src_file.cpp"),
        "test_file": Path("./tests/test_file.cpp"),
    }
    assert valid_command.flags == {
        "errors": False,
        "raport": True
    }
    print("Test passed!")


    valid_command2 = CMD("./tests/src_file.cpp ./tests/test_file.cpp")
    assert valid_command2.flags == {
        "errors": False,
        "raport": False
    }
    print("Test passed!")


    valid_command3 = CMD("-r ./tests/src_file.cpp ./tests/test_file.cpp")
    assert valid_command3.flags == {
        "errors": False,
        "raport": True
    }
    print("Test passed!")


    try:
        CMD("-raport ./tests/src_file.cpp ./tests/test_file.cpp")
    except ValueError as err:
        assert str(err) == "The `-raport` flag does not exist"
        print("Test passed!")
    else:
        print("Test failed!")


    try:
        CMD("./tests/src_file.c ./tests/test_file.cpp")
    except ValueError as err:
        assert str(err) == "`./tests/src_file.c` is not a valid path"
        print("Test passed!")
    else:
        print("Test failed!")


    try:
        CMD("./tests/src_file.cpp ./tests/test_file.cpp ./tests/test_file.cpp")
    except ValueError as err:
        assert str(err) == "Too many arguments, the source file is `tests/src_file.cpp` and the test file is `tests/test_file.cpp`"
        print("Test passed!")
    else:
        print("Test failed!")


if __name__ == "__main__":
    test_CMD()