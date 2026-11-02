import os
import pickle

import pytest

from mydb import MyDB


@pytest.fixture
def db_file(tmp_path):
    return tmp_path / "goofball.db"


@pytest.fixture
def nonempty_db(db_file):
    with open(db_file, "wb") as f:
        pickle.dump(["wackadoo", "test-o-matic"], f)
    return MyDB(db_file)


@pytest.fixture
def empty_db(db_file):
    with open(db_file, "wb") as f:
        pickle.dump([], f)
    return MyDB(db_file)


def describe_MyDB():

    def describe_initializer():

        def it_assigns_fname_attribute_value(db_file):
            db = MyDB(db_file)
            assert db.fname == db_file

        def it_creates_an_empty_database_if_it_does_not_exist(db_file):
            MyDB(db_file)
            with open(db_file, "rb") as f:
                assert pickle.load(f) == []

        def it_preserves_an_existing_database(nonempty_db, db_file):
            assert os.path.isfile(db_file)
            with open(db_file, "rb") as f:
                assert pickle.load(f) == ["wackadoo", "test-o-matic"]

    def describe_loadStrings():

        def it_returns_the_strings_from_the_file(nonempty_db):
            assert nonempty_db.loadStrings() == ["wackadoo", "test-o-matic"]

        def it_returns_an_empty_list_from_an_empty_database(empty_db):
            assert empty_db.loadStrings() == []

    def describe_saveStrings():

        def it_replaces_the_persisted_list(nonempty_db, db_file):
            nonempty_db.saveStrings(["one", "two"])
            with open(db_file, "rb") as f:
                assert pickle.load(f) == ["one", "two"]

    def describe_saveString():

        def it_appends_a_string_to_an_empty_list(empty_db, db_file):
            empty_db.saveString("first entry")
            with open(db_file, "rb") as f:
                assert pickle.load(f) == ["first entry"]

        def it_appends_a_string_to_the_existing_list(nonempty_db, db_file):
            nonempty_db.saveString("new entry")
            with open(db_file, "rb") as f:
                assert pickle.load(f) == ["wackadoo", "test-o-matic", "new entry"]
