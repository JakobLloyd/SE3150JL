import json

from squirrel_server import SquirrelServerHandler


def _handler(mocker):
    request = SquirrelServerHandler.__new__(SquirrelServerHandler)
    request.send_response = mocker.Mock()
    request.send_header = mocker.Mock()
    request.end_headers = mocker.Mock()
    request.wfile = mocker.Mock()
    return request


def describe_SquirrelServerHandler():
    def describe_handleSquirrelsIndex():
        def it_returns_the_squirrel_collection(mocker):
            request = _handler(mocker)
            squirrels = [
                {"id": 1, "name": "kyanne", "size": "small"},
                {"id": 2, "name": "bingus", "size": "large"},
            ]
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrels.return_value = squirrels

            request.handleSquirrelsIndex()

            db.return_value.getSquirrels.assert_called_once_with()
            request.send_response.assert_called_once_with(200)
            request.send_header.assert_called_once_with(
                "Content-Type", "application/json"
            )
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                json.dumps(squirrels).encode("utf-8")
            )

        def it_returns_an_empty_collection_when_no_squirrels_exist(mocker):
            request = _handler(mocker)
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrels.return_value = []

            request.handleSquirrelsIndex()

            request.send_response.assert_called_once_with(200)
            request.wfile.write.assert_called_once_with(b"[]")

    def describe_handleSquirrelsRetrieve():
        def it_returns_a_squirrel_when_it_exists(mocker):
            request = _handler(mocker)
            squirrel = {"id": 1, "name": "kyanne", "size": "small"}
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = squirrel

            request.handleSquirrelsRetrieve("1")

            db.return_value.getSquirrel.assert_called_once_with("1")
            request.send_response.assert_called_once_with(200)
            request.send_header.assert_called_once_with(
                "Content-Type", "application/json"
            )
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                json.dumps(squirrel).encode("utf-8")
            )

        def it_returns_not_found_when_the_squirrel_is_missing(mocker):
            request = _handler(mocker)
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = None
            request.handle404 = mocker.Mock()

            request.handleSquirrelsRetrieve("999")

            db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()

    def describe_handleSquirrelsCreate():
        def it_creates_a_squirrel_from_form_data(mocker):
            request = _handler(mocker)
            request.getRequestData = mocker.Mock(
                return_value={"name": "jeff", "size": "small"}
            )
            db = mocker.patch("squirrel_server.SquirrelDB")

            request.handleSquirrelsCreate()

            db.return_value.createSquirrel.assert_called_once_with("jeff", "small")
            request.send_response.assert_called_once_with(201)
            request.end_headers.assert_called_once_with()

    def describe_handleSquirrelsUpdate():
        def it_updates_an_existing_squirrel(mocker):
            request = _handler(mocker)
            request.getRequestData = mocker.Mock(
                return_value={"name": "jerry", "size": "large"}
            )
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = {
                "id": 4,
                "name": "jeff",
                "size": "small",
            }

            request.handleSquirrelsUpdate("4")

            db.return_value.getSquirrel.assert_called_once_with("4")
            db.return_value.updateSquirrel.assert_called_once_with(
                "4", "jerry", "large"
            )
            request.send_response.assert_called_once_with(204)
            request.end_headers.assert_called_once_with()

        def it_returns_not_found_when_updating_a_missing_squirrel(mocker):
            request = _handler(mocker)
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
            request = _handler(mocker)
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = {
                "id": 2,
                "name": "bingus",
                "size": "large",
            }

            request.handleSquirrelsDelete("2")

            db.return_value.getSquirrel.assert_called_once_with("2")
            db.return_value.deleteSquirrel.assert_called_once_with("2")
            request.send_response.assert_called_once_with(204)
            request.end_headers.assert_called_once_with()

        def it_returns_not_found_when_deleting_a_missing_squirrel(mocker):
            request = _handler(mocker)
            request.handle404 = mocker.Mock()
            db = mocker.patch("squirrel_server.SquirrelDB")
            db.return_value.getSquirrel.return_value = None

            request.handleSquirrelsDelete("999")

            db.return_value.getSquirrel.assert_called_once_with("999")
            request.handle404.assert_called_once_with()
            db.return_value.deleteSquirrel.assert_not_called()

    def describe_handle404():
        def it_writes_a_not_found_response(mocker):
            request = _handler(mocker)

            request.handle404()

            request.send_response.assert_called_once_with(404)
            request.send_header.assert_called_once_with("Content-Type", "text/plain")
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(b"404 Not Found")
