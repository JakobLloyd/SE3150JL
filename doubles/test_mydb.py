import pytest
import os

from doubles.mydb import MyDB




def it_assigns_fname_attrribute_value(mocker):
    mocker.patch("os.path.isfile", return_value=True)
    db = MyDB("test.db")
    assert db.fname == "somefilename"

def it_creates_empty_database_if_it_does_not_exist(mocker):
    mock_isfile = mocker.patch("os.path.isfile", return_value=False)
    mock_open = mocker.patch("builtins.open", mocker.mock_open())
    mock_dump = mocker.patch("pickle.dump")
    db = MyDB("test.db")

    mock_isfile.assert_called_once_with("somefilename")
    mock_open.assert_called_once_with("somefilename", 'wb')
    mock_dump.assert_called_once_with([], mock_open())
    assert os.path.isfile("somefilename") == False