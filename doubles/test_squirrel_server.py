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
            mock_wfile = mocker.Mock()
            request = FakeRequest(mock_wfile, "GET", "/squirrels")
            mocker.patch.object(SquirrelServerHandler, "wbufsize", 1)
            mock_send_response = mocker.patch.object(
                SquirrelServerHandler, "send_response"
            )
            mock_send_header = mocker.patch.object(
                SquirrelServerHandler, "send_header"
            )
            mock_end_headers = mocker.patch.object(
                SquirrelServerHandler, "end_headers"
            )
            mock_db = mocker.patch.object(
                SquirrelDB, "getSquirrels", return_value=[
                    {"id": 1, "name": "kyanne", "size": "small"},
                    {"id": 2, "name": "bingus", "size": "large"},
                ]
            )
            squirrels = [
                {"id": 1, "name": "kyanne", "size": "small"},
                {"id": 2, "name": "bingus", "size": "large"},
            ]

            response = SquirrelServerHandler(request, ("127.0.0.1", 80), None)

            mock_db.assert_called_once_with()
            mock_send_response.assert_called_once_with(200)
            mock_send_header.assert_called_once_with(
                "Content-Type", "application/json"
            )
            mock_end_headers.assert_called_once_with()
            response.wfile.write.assert_called_once_with(
                bytes(json.dumps(squirrels), "utf-8")
            )

        def it_returns_an_empty_collection_when_no_squirrels_exist(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            mock_db.return_value.getSquirrels.return_value = []

            request.handleSquirrelsIndex()

            mock_db.return_value.getSquirrels.assert_called_once_with()
            request.send_response.assert_called_once_with(200)
            request.wfile.write.assert_called_once_with(bytes("[]", "utf-8"))

    def describe_handleSquirrelsRetrieve():
        def it_returns_a_squirrel_when_it_exists(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            squirrel = {"id": 1, "name": "kyanne", "size": "small"}
            mock_db.return_value.getSquirrel.return_value = squirrel

            request.handleSquirrelsRetrieve("1")

            mock_db.return_value.getSquirrel.assert_called_once_with("1")
            request.send_response.assert_called_once_with(200)
            request.send_header.assert_called_once_with(
                "Content-Type", "application/json"
            )
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                bytes(json.dumps(squirrel), "utf-8")
            )

        def it_returns_not_found_when_the_squirrel_is_missing(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            mock_db.return_value.getSquirrel.return_value = None
            request.handle404 = mocker.Mock()

            request.handleSquirrelsRetrieve("999")

            mock_db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()

    def describe_handleSquirrelsCreate():
        def it_creates_a_squirrel_from_form_data(mocker):
            mock_wfile = mocker.Mock()
            request = FakeRequest(
                mock_wfile,
                "POST",
                "/squirrels",
                body="name=jeff&size=small",
            )
            mocker.patch.object(SquirrelServerHandler, "wbufsize", 1)
            mock_send_response = mocker.patch.object(
                SquirrelServerHandler, "send_response"
            )
            mock_end_headers = mocker.patch.object(
                SquirrelServerHandler, "end_headers"
            )
            mock_db = mocker.patch.object(SquirrelDB, "createSquirrel")

            SquirrelServerHandler(request, ("127.0.0.1", 80), None)

            mock_db.assert_called_once_with("jeff", "small")
            mock_send_response.assert_called_once_with(201)
            mock_end_headers.assert_called_once_with()

        def it_passes_unusual_form_values_to_the_database(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.getRequestData = mocker.Mock(
                return_value={"name": "Zigzag McGee", "size": "colossal"}
            )
            request.send_response = mocker.Mock()
            request.end_headers = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")

            request.handleSquirrelsCreate()

            request.getRequestData.assert_called_once_with()
            mock_db.return_value.createSquirrel.assert_called_once_with(
                "Zigzag McGee", "colossal"
            )
            request.send_response.assert_called_once_with(201)
            request.end_headers.assert_called_once_with()

    def describe_handleSquirrelsUpdate():
        def it_updates_an_existing_squirrel_from_form_data(mocker):
            mock_wfile = mocker.Mock()
            request = FakeRequest(
                mock_wfile,
                "PUT",
                "/squirrels/4",
                body="name=jerry&size=large",
            )
            mocker.patch.object(SquirrelServerHandler, "wbufsize", 1)
            mock_send_response = mocker.patch.object(
                SquirrelServerHandler, "send_response"
            )
            mock_end_headers = mocker.patch.object(
                SquirrelServerHandler, "end_headers"
            )
            mock_get_squirrel = mocker.patch.object(
                SquirrelDB,
                "getSquirrel",
                return_value={
                    "id": 4,
                    "name": "jeff",
                    "size": "small",
                },
            )
            mock_update_squirrel = mocker.patch.object(SquirrelDB, "updateSquirrel")

            SquirrelServerHandler(request, ("127.0.0.1", 80), None)

            mock_get_squirrel.assert_called_once_with("4")
            mock_update_squirrel.assert_called_once_with(
                "4", "jerry", "large"
            )
            mock_send_response.assert_called_once_with(204)
            mock_end_headers.assert_called_once_with()

        def it_returns_not_found_when_updating_a_missing_squirrel(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.getRequestData = mocker.Mock()
            request.handle404 = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            mock_db.return_value.getSquirrel.return_value = None

            request.handleSquirrelsUpdate("999")

            mock_db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()
            request.getRequestData.assert_not_called()
            mock_db.return_value.updateSquirrel.assert_not_called()

    def describe_handleSquirrelsDelete():
        def it_deletes_an_existing_squirrel(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.end_headers = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            mock_db.return_value.getSquirrel.return_value = {
                "id": 2,
                "name": "bingus",
                "size": "large",
            }

            request.handleSquirrelsDelete("2")

            mock_db.return_value.getSquirrel.assert_called_once_with("2")
            mock_db.return_value.deleteSquirrel.assert_called_once_with("2")
            request.send_response.assert_called_once_with(204)
            request.end_headers.assert_called_once_with()

        def it_returns_not_found_when_deleting_a_missing_squirrel(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.handle404 = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            mock_db.return_value.getSquirrel.return_value = None

            request.handleSquirrelsDelete("999")

            mock_db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()
            mock_db.return_value.deleteSquirrel.assert_not_called()

    def describe_handle404():
        def it_writes_a_not_found_response(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()

            request.handle404()

            request.send_response.assert_called_once_with(404)
            request.send_header.assert_called_once_with(
                "Content-Type", "text/plain"
            )
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                bytes("404 Not Found", "utf-8")
            )