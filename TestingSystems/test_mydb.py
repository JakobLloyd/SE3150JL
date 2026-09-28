import os.path
import pickle
import pytest
import subprocess

from mydb import MyDB

todo = pytest.mark.skip(reason='todo: pending spec')

DB_FILE = "goofball.db"

@pytest.fixture
def nonempty_db():
    with open(DB_FILE, 'wb') as f:
        pickle.dump(['wackadoo', 'test-o-matic'], f)
    return MyDB(DB_FILE)

@pytest.fixture
def empty_db():
   with open(DB_FILE, 'wb') as f:
       pickle.dump([], f)
   return MyDB(DB_FILE)

@pytest.fixture(autouse=True)
def cleanup():
    # this code runs BEFORE each test case
    # --nothing yet--
    yield
    # this code runs AFTER each test case
    os.remove(DB_FILE)

def describe_MyDB():

    def describe_initializer():

        def it_assigns_fname_attribute_value():
            db = MyDB(DB_FILE)
            assert db.fname == DB_FILE

        # instead of checking to see that the create file got called (behavior) 
        # now we'll use an OS function to see if the file actually got created (state)
        def it_creates_empty_database_if_it_does_not_exist(empty_db):
            db = MyDB(DB_FILE)
            assert os.path.isfile(DB_FILE)

        def it_does_not_create_database_if_it_already_exists(nonempty_db):
            assert os.path.isfile(DB_FILE)
            with open(DB_FILE, 'rb') as f:
                assert pickle.load(f) == ['wackadoo', 'test-o-matic']

    @todo
    def describe_loadStrings():
        pass

    @todo
    def describe_saveStrings():
        pass

    @todo
    def describe_saveString():
        pass
