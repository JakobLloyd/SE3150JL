import io
import json

from squirrel_db import SquirrelDB
from squirrel_server import SquirrelServerHandler


class FakeRequest:
    def __init__(self, mock_wfile, method, path, body=None):
        self._mock_wfile = mock_wfile
        self._method = method
        self._path = path
        self._body = body

    def sendall(self, data):
        return

    def makefile(self, mode, *args, **kwargs):
        if mode == "rb":
            if self._body:
                headers = "Content-Length: {}\r\n".format(len(self._body))
                body = self._body
            else:
                headers = ""
                body = ""
            request = bytes(
                "{} {} HTTP/1.0\r\n{}\r\n{}".format(
                    self._method, self._path, headers, body
                ),
                "utf-8",
            )
            return io.BytesIO(request)
        if mode == "wb":
            return self._mock_wfile


def describe_SquirrelServerHandler():
    def describe_handleSquirrelsIndex():
        def it_returns_the_squirrel_collection(mocker):
            request = FakeRequest(mocker.Mock(), "GET", "/squirrels")
            mocker.patch.object(SquirrelServerHandler, "wbufsize", 1)
            send_response = mocker.patch.object(SquirrelServerHandler, "send_response")
            send_header = mocker.patch.object(SquirrelServerHandler, "send_header")
            end_headers = mocker.patch.object(SquirrelServerHandler, "end_headers")
            squirrels = [
                {"id": 1, "name": "kyanne", "size": "small"},
                {"id": 2, "name": "bingus", "size": "large"},
            ]
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrels.return_value = squirrels

            response = SquirrelServerHandler(request, ("127.0.0.1", 80), None)

            db.return_value.getSquirrels.assert_called_once_with()
            send_response.assert_called_once_with(200)
            send_header.assert_called_once_with("Content-Type", "application/json")
            end_headers.assert_called_once_with()
            response.wfile.write.assert_called_once_with(
                bytes(json.dumps(squirrels), "utf-8")
            )

        def it_returns_an_empty_collection_when_no_squirrels_exist(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrels.return_value = []

            request.handleSquirrelsIndex()

            db.return_value.getSquirrels.assert_called_once_with()
            request.send_response.assert_called_once_with(200)
            request.wfile.write.assert_called_once_with(bytes("[]", "utf-8"))

    def describe_handleSquirrelsRetrieve():
        def it_returns_a_squirrel_when_it_exists(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")
            squirrel = {"id": 1, "name": "kyanne", "size": "small"}
            db.return_value.getSquirrel.return_value = squirrel

            request.handleSquirrelsRetrieve("1")

            db.return_value.getSquirrel.assert_called_once_with("1")
            request.send_response.assert_called_once_with(200)
            request.send_header.assert_called_once_with("Content-Type", "application/json")
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                bytes(json.dumps(squirrel), "utf-8")
            )

        def it_returns_not_found_when_the_squirrel_is_missing(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = None
            request.handle404 = mocker.Mock()

            request.handleSquirrelsRetrieve("999")

            db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()

    def describe_handleSquirrelsCreate():
        def it_creates_a_squirrel_from_form_data(mocker):
            request = FakeRequest(
                mocker.Mock(), "POST", "/squirrels", body="name=jeff&size=small"
            )
            mocker.patch.object(SquirrelServerHandler, "wbufsize", 1)
            send_response = mocker.patch.object(SquirrelServerHandler, "send_response")
            end_headers = mocker.patch.object(SquirrelServerHandler, "end_headers")
            db = mocker.patch("squirrel_server.SquirrelDB")

            SquirrelServerHandler(request, ("127.0.0.1", 80), None)

            db.return_value.createSquirrel.assert_called_once_with("jeff", "small")
            send_response.assert_called_once_with(201)
            end_headers.assert_called_once_with()

        def it_passes_unusual_form_values_to_the_database(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.getRequestData = mocker.Mock(
                return_value={"name": "Zigzag McGee", "size": "colossal"}
            )
            request.send_response = mocker.Mock()
            request.end_headers = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")

            request.handleSquirrelsCreate()

            request.getRequestData.assert_called_once_with()
            db.return_value.createSquirrel.assert_called_once_with(
                "Zigzag McGee", "colossal"
            )
            request.send_response.assert_called_once_with(201)
            request.end_headers.assert_called_once_with()

    def describe_handleSquirrelsUpdate():
        def it_updates_an_existing_squirrel_from_form_data(mocker):
            request = FakeRequest(
                mocker.Mock(), "PUT", "/squirrels/4", body="name=jerry&size=large"
            )
            mocker.patch.object(SquirrelServerHandler, "wbufsize", 1)
            send_response = mocker.patch.object(SquirrelServerHandler, "send_response")
            end_headers = mocker.patch.object(SquirrelServerHandler, "end_headers")
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = {
                "id": 4, "name": "jeff", "size": "small"
            }

            SquirrelServerHandler(request, ("127.0.0.1", 80), None)

            db.return_value.getSquirrel.assert_called_once_with("4")
            db.return_value.updateSquirrel.assert_called_once_with(
                "4", "jerry", "large"
            )
            send_response.assert_called_once_with(204)
            end_headers.assert_called_once_with()

        def it_returns_not_found_when_updating_a_missing_squirrel(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.getRequestData = mocker.Mock()
            request.handle404 = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = None

            request.handleSquirrelsUpdate("999")

            db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()
            request.getRequestData.assert_not_called()
            db.return_value.updateSquirrel.assert_not_called()

    def describe_handleSquirrelsDelete():
        def it_deletes_an_existing_squirrel(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.end_headers = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = {
                "id": 2, "name": "bingus", "size": "large"
            }

            request.handleSquirrelsDelete("2")

            db.return_value.getSquirrel.assert_called_once_with("2")
            db.return_value.deleteSquirrel.assert_called_once_with("2")
            request.send_response.assert_called_once_with(204)
            request.end_headers.assert_called_once_with()

        def it_returns_not_found_when_deleting_a_missing_squirrel(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.handle404 = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = None

            request.handleSquirrelsDelete("999")

            db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()
            db.return_value.deleteSquirrel.assert_not_called()

    def describe_handle404():
        def it_writes_a_not_found_response(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()

            request.handle404()

            request.send_response.assert_called_once_with(404)
            request.send_header.assert_called_once_with("Content-Type", "text/plain")
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                bytes("404 Not Found", "utf-8")
            )
