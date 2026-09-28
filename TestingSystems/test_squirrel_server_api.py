import http.client
import json
import os
import pytest
import shutil
import sqlite3
import subprocess
import sys
import time
import urllib.parse

todo = pytest.mark.skip(reason='todo: pending spec')

def describe_squirrel_server():

    @pytest.fixture(autouse=True)
    def reset_db():
        shutil.copyfile('empty_squirrel_db.db', 'squirrel_db.db')
        yield
        os.remove('squirrel_db.db')

    @pytest.fixture
    def db():
        conn = sqlite3.connect('squirrel_db.db')
        return conn.cursor()

    @pytest.fixture(autouse=True, scope='session')
    def run_http_server():
        proc = subprocess.Popen([sys.executable, 'squirrel_server.py'])
        time.sleep(0.5)
        yield
        proc.kill()

    @pytest.fixture
    def http_client():
        conn = http.client.HTTPConnection('localhost:8080')
        return conn

    @pytest.fixture
    def request_body():
        return urllib.parse.urlencode({ 'name': 'Chippy', 'size': 'small' })

    @pytest.fixture
    def request_headers():
        return { 'Content-Type': 'application/x-www-form-urlencoded' }

    @pytest.fixture
    def make_a_squirrel(http_client, request_body, request_headers):
        http_client.request('POST', '/squirrels', request_body, request_headers)
        http_client.close()

    def describe_get_squirrels():

        def it_returns_200_status_code(http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()
            status_code = response.status
            http_client.close()

            assert status_code == 200

        # this is an important example. We're not just testing outcomes that
        # the user can see. We want to be sure we follow the API spec as well.
        def it_returns_json_content_type_header(http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()
            content_type_header = response.getheader('Content-Type')
            http_client.close()

            assert content_type_header == "application/json"

        def it_returns_json_array_with_one_squirrel(make_a_squirrel, http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()
            body = response.read()
            parsed_body = json.loads(body)
            http_client.close()

            assert parsed_body == [{ 'id': 1, 'name': 'Chippy', 'size': 'small' }]

    def describe_create_squirrel():

        def it_returns_201_status_code(http_client, request_body, request_headers):
            http_client.request('POST', '/squirrels', request_body, request_headers)
            response = http_client.getresponse()
            status_code = response.status
            http_client.close()

            assert status_code == 201

        def it_creates_the_squirrel_in_the_dataset(http_client, request_body, request_headers, db):
            http_client.request('POST', '/squirrels', request_body, request_headers)
            response = http_client.getresponse()
            status_code = response.status
            http_client.close()

            # it's ok to use knowledge of the integration (the DB structure) 
            # to ensure that something was completed correctly
            db.execute('SELECT * FROM squirrels WHERE id = 1')

            assert db.fetchone() == (1, 'Chippy', 'small')

