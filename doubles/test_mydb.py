import pytest
import os

from mydb import MyDB


def describe_MyDB():
    def describe_init():
        def it_assigns_fname_attribute_value(mocker):
            mocker.patch("mydb.os.path.isfile", return_value=True)
            db = MyDB("test.db")
            assert db.fname == "test.db"

    def describe_loadStrings():
        def it_loads_strings_from_the_database(mocker):
            mocker.patch("mydb.os.path.isfile", return_value=True)
            mock_open = mocker.patch("mydb.open", mocker.mock_open())
            mock_load = mocker.patch("mydb.pickle.load", return_value=["one", "two"])
            db = MyDB("test.db")

            result = db.loadStrings()

            assert result == ["one", "two"]
            mock_open.assert_called_once_with("test.db", "rb")
            mock_load.assert_called_once_with(mock_open.return_value.__enter__.return_value)

    def describe_saveStrings():
        def it_saves_strings_to_the_database(mocker):
            mocker.patch("mydb.os.path.isfile", return_value=True)
            mock_open = mocker.patch("mydb.open", mocker.mock_open())
            mock_dump = mocker.patch("mydb.pickle.dump")
            db = MyDB("test.db")

            db.saveStrings(["one", "two"])

            mock_open.assert_called_once_with("test.db", "wb")
            mock_dump.assert_called_once_with(
                ["one", "two"], mock_open.return_value.__enter__.return_value
            )

def it_creates_empty_database_if_it_does_not_exist(mocker):
    mock_isfile = mocker.patch("mydb.os.path.isfile", return_value=False)
    mock_save_strings = mocker.patch.object(MyDB, "saveStrings")

    MyDB("test.db")

    mock_isfile.assert_called_once_with("test.db")
    mock_save_strings.assert_called_once_with([])