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

        def it_returns_an_empty_response_body(http_client, request_body, request_headers):
            http_client.request('POST', '/squirrels', request_body, request_headers)
            response = http_client.getresponse()

            assert response.read() == b''

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

        def it_round_trips_url_encoded_special_characters(http_client):
            name = 'Chip & Dale + 50%'
            size = 'extra small'
            body = urllib.parse.urlencode({'name': name, 'size': size})
            http_client.request('POST', '/squirrels', body, {'Content-Type': 'application/x-www-form-urlencoded'})
            response = http_client.getresponse()
            response.read()
            http_client.request('GET', '/squirrels/1')
            response = http_client.getresponse()

            assert json.loads(response.read()) == {'id': 1, 'name': name, 'size': size}

        def it_lists_multiple_squirrels_in_id_order(http_client):
            for name in ('Second', 'Third'):
                body = urllib.parse.urlencode({'name': name, 'size': 'small'})
                http_client.request('POST', '/squirrels', body, {'Content-Type': 'application/x-www-form-urlencoded'})
                response = http_client.getresponse()
                response.read()
            http_client.request('GET', '/squirrels')
            response = http_client.getresponse()

            assert [squirrel['id'] for squirrel in json.loads(response.read())] == [1, 2]

        @pytest.mark.parametrize('body', ['', 'name=Chippy', 'size=small'])
        def it_closes_the_connection_when_a_required_field_is_missing(http_client, body):
            http_client.request('POST', '/squirrels', body, {'Content-Type': 'application/x-www-form-urlencoded'})

            with pytest.raises(http.client.RemoteDisconnected):
                http_client.getresponse()

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

        def it_returns_json_content_type_for_a_known_squirrel(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/1')
            response = http_client.getresponse()

            assert response.getheader('Content-Type') == 'application/json'

        def it_accepts_a_leading_zero_in_the_identifier(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/01')
            response = http_client.getresponse()

            assert json.loads(response.read()) == {'id': 1, 'name': 'Chippy', 'size': 'small'}

        def it_retrieves_a_squirrel_even_with_extra_path_segments(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/1/extra')
            response = http_client.getresponse()

            assert response.status == 200

        def it_accepts_a_plus_sign_in_the_identifier(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/+1')
            response = http_client.getresponse()

            assert response.status == 200

        def it_retrieves_a_squirrel_with_a_trailing_slash(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/1/')
            response = http_client.getresponse()

            assert response.status == 200

        def it_treats_a_trailing_collection_slash_as_the_collection(http_client):
            http_client.request('GET', '/squirrels/')
            response = http_client.getresponse()

            assert json.loads(response.read()) == []

        def it_treats_an_empty_identifier_segment_as_the_collection(http_client):
            http_client.request('GET', '/squirrels//1')
            response = http_client.getresponse()

            assert json.loads(response.read()) == []

        def it_does_not_ignore_a_query_string_after_the_identifier(http_client, make_a_squirrel):
            http_client.request('GET', '/squirrels/1?view=full')
            response = http_client.getresponse()

            assert response.status == 404

        @pytest.mark.parametrize('squirrel_id', [
            '0',
            '-1',
            'abc',
            '1.5',
            '999999999999999999999999999999999999',
            '-999999999999999999999999999999999999',
            'null',
            'true',
            '%31',
            '1%2Fextra',
        ])
        def it_returns_404_for_unusual_identifiers(http_client, squirrel_id):
            http_client.request('GET', f'/squirrels/{squirrel_id}')
            response = http_client.getresponse()

            assert response.status == 404

    def describe_update_squirrel():

        def it_returns_204_status_code_for_a_valid_update(http_client, make_a_squirrel):
            body = urllib.parse.urlencode({'name': 'Acorn', 'size': 'large'})
            http_client.request('PUT', '/squirrels/1', body, {'Content-Type': 'application/x-www-form-urlencoded'})
            response = http_client.getresponse()

            assert response.status == 204

        def it_returns_an_empty_response_body_for_a_valid_update(http_client, make_a_squirrel):
            body = urllib.parse.urlencode({'name': 'Acorn', 'size': 'large'})
            http_client.request('PUT', '/squirrels/1', body, {'Content-Type': 'application/x-www-form-urlencoded'})
            response = http_client.getresponse()

            assert response.read() == b''

        def it_updates_the_persisted_squirrel(http_client, make_a_squirrel, tmp_path):
            body = urllib.parse.urlencode({'name': 'Acorn', 'size': 'large'})
            http_client.request('PUT', '/squirrels/1', body, {'Content-Type': 'application/x-www-form-urlencoded'})
            response = http_client.getresponse()
            response.read()
            conn = sqlite3.connect(tmp_path / 'squirrel_db.db')
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM squirrels WHERE id = 1')
                squirrel = cursor.fetchone()
            finally:
                conn.close()

            assert squirrel == (1, 'Acorn', 'large')

        def it_round_trips_url_encoded_values_on_update(http_client, make_a_squirrel):
            name = 'Acorn & Oak + 25%'
            size = 'very small'
            body = urllib.parse.urlencode({'name': name, 'size': size})
            http_client.request('PUT', '/squirrels/1', body, {'Content-Type': 'application/x-www-form-urlencoded'})
            response = http_client.getresponse()
            response.read()
            http_client.request('GET', '/squirrels/1')
            response = http_client.getresponse()

            assert json.loads(response.read()) == {'id': 1, 'name': name, 'size': size}

    def describe_delete_squirrel():

        def it_returns_204_status_code_for_a_valid_delete(http_client, make_a_squirrel):
            http_client.request('DELETE', '/squirrels/1')
            response = http_client.getresponse()

            assert response.status == 204

        def it_removes_the_persisted_squirrel(http_client, make_a_squirrel, tmp_path):
            http_client.request('DELETE', '/squirrels/1')
            response = http_client.getresponse()
            response.read()
            conn = sqlite3.connect(tmp_path / 'squirrel_db.db')
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM squirrels WHERE id = 1')
                squirrel = cursor.fetchone()
            finally:
                conn.close()

            assert squirrel is None

        def it_returns_404_when_deleting_the_same_squirrel_twice(http_client, make_a_squirrel):
            http_client.request('DELETE', '/squirrels/1')
            response = http_client.getresponse()
            response.read()
            http_client.request('DELETE', '/squirrels/1')
            response = http_client.getresponse()

            assert response.status == 404

    def describe_not_found_responses():

        @pytest.mark.parametrize('method, path, body', [
            ('GET', '/unknown', None),
            ('GET', '/squirrels/999', None),
            ('GET', '/squirrels/1/extra', None),
            ('POST', '/unknown', 'name=Hedgehog&size=small'),
            ('POST', '/squirrels/1', 'name=Hedgehog&size=small'),
            ('POST', '/squirrels/1/extra', 'name=Hedgehog&size=small'),
            ('PUT', '/unknown/1', 'name=Hedgehog&size=small'),
            ('PUT', '/squirrels', 'name=Hedgehog&size=small'),
            ('PUT', '/squirrels/999', 'name=Hedgehog&size=small'),
            ('PUT', '/squirrels/1/extra', 'name=Hedgehog&size=small'),
            ('DELETE', '/unknown/1', None),
            ('DELETE', '/squirrels', None),
            ('DELETE', '/squirrels/999', None),
            ('DELETE', '/squirrels/1/extra', None),
        ])
        def it_returns_404_for_invalid_paths(http_client, method, path, body):
            headers = {'Content-Type': 'application/x-www-form-urlencoded'} if body is not None else {}
            http_client.request(method, path, body, headers)
            response = http_client.getresponse()

            assert response.status == 404

        def it_returns_plain_text_for_not_found(http_client):
            http_client.request('GET', '/unknown')
            response = http_client.getresponse()

            assert response.getheader('Content-Type') == 'text/plain'

        def it_returns_the_not_found_message(http_client):
            http_client.request('GET', '/unknown')
            response = http_client.getresponse()

            assert response.read() == b'404 Not Found'