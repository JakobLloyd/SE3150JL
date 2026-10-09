import http.client
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import urllib.parse

import pytest

from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def describe_squirrel_server():

    @pytest.fixture(autouse=True)
    def run_http_server(tmp_path):
        db_path = tmp_path / 'squirrel_db.db'
        shutil.copyfile(PROJECT_DIR / 'empty_squirrel_db.db', db_path)
        env = os.environ.copy()
        env['SQUIRREL_SERVER_PORT'] = '0'
        proc = subprocess.Popen(
            [sys.executable, str(PROJECT_DIR / 'squirrel_server.py')],
            cwd=str(tmp_path),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        try:
            startup_line = proc.stdout.readline().strip()
            if not startup_line.startswith('squirrel_server running at 127.0.0.1:'):
                raise RuntimeError(f'Server failed to start: {startup_line}')
            port = int(startup_line.rsplit(':', 1)[1])
            yield port
        finally:
            if proc.poll() is None:
                proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()
            proc.stdout.close()

    @pytest.fixture
    def http_client(run_http_server):
        conn = http.client.HTTPConnection('127.0.0.1', run_http_server)
        yield conn
        conn.close()

    @pytest.fixture
    def request_body():
        return urllib.parse.urlencode({'name': 'Chippy', 'size': 'small'})

    @pytest.fixture
    def request_headers():
        return {'Content-Type': 'application/x-www-form-urlencoded'}

    @pytest.fixture
    def make_a_squirrel(http_client, request_body, request_headers):
        http_client.request('POST', '/squirrels', request_body, request_headers)
        response = http_client.getresponse()
        response.read()

    def describe_get_squirrels():

        def it_returns_200_status_code(http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()

            assert response.status == 200

        def it_returns_json_content_type_header(http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()

            assert response.getheader('Content-Type') == 'application/json'

        def it_returns_an_empty_json_array(http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()
            body = json.loads(response.read())

            assert body == []

        def it_returns_the_existing_squirrel(make_a_squirrel, http_client):
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()
            body = json.loads(response.read())

            assert body == [{'id': 1, 'name': 'Chippy', 'size': 'small'}]

    def describe_create_squirrel():

        def it_returns_201_status_code(http_client, request_body, request_headers):
            http_client.request('POST', '/squirrels', request_body, request_headers)
            response = http_client.getresponse()

            assert response.status == 201

        def it_persists_the_squirrel(http_client, request_body, request_headers, tmp_path):
            http_client.request('POST', '/squirrels', request_body, request_headers)
            response = http_client.getresponse()
            response.read()
            conn = sqlite3.connect(tmp_path / 'squirrel_db.db')
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM squirrels WHERE id = 1')
                squirrel = cursor.fetchone()
            finally:
                conn.close()

            assert squirrel == (1, 'Chippy', 'small')

    def describe_retrieve_squirrel():

        def it_returns_200_status_code_for_a_known_squirrel(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/1')
            response = http_client.getresponse()

            assert response.status == 200

        def it_returns_json_for_a_known_squirrel(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/1')
            response = http_client.getresponse()
            body = json.loads(response.read())

            assert body == {'id': 1, 'name': 'Chippy', 'size': 'small'}