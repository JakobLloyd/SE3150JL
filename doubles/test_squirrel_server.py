import json

from squirrel_server import SquirrelServerHandler


def describe_SquirrelServerHandler():
    def describe_handleSquirrelsIndex():
        def it_returns_the_squirrel_collection(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.send_response = mocker.Mock()
            request.send_header = mocker.Mock()
            request.end_headers = mocker.Mock()
            request.wfile = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            squirrels = [
                {"id": 1, "name": "kyanne", "size": "small"},
                {"id": 2, "name": "bingus", "size": "large"},
            ]
            mock_db.return_value.getSquirrels.return_value = squirrels

            request.handleSquirrelsIndex()

            mock_db.return_value.getSquirrels.assert_called_once_with()
            request.send_response.assert_called_once_with(200)
            request.send_header.assert_called_once_with(
                "Content-Type", "application/json"
            )
            request.end_headers.assert_called_once_with()
            request.wfile.write.assert_called_once_with(
                bytes(json.dumps(squirrels), "utf-8")
            )

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
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.getRequestData = mocker.Mock(
                return_value={"name": "jeff", "size": "small"}
            )
            request.send_response = mocker.Mock()
            request.end_headers = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")

            request.handleSquirrelsCreate()

            request.getRequestData.assert_called_once_with()
            mock_db.return_value.createSquirrel.assert_called_once_with(
                "jeff", "small"
            )
            request.send_response.assert_called_once_with(201)
            request.end_headers.assert_called_once_with()

    def describe_handleSquirrelsUpdate():
        def it_updates_an_existing_squirrel_from_form_data(mocker):
            request = SquirrelServerHandler.__new__(SquirrelServerHandler)
            request.getRequestData = mocker.Mock(
                return_value={"name": "jerry", "size": "large"}
            )
            request.send_response = mocker.Mock()
            request.end_headers = mocker.Mock()
            mock_db = mocker.patch("squirrel_server.SquirrelDB")
            mock_db.return_value.getSquirrel.return_value = {
                "id": 4,
                "name": "jeff",
                "size": "small",
            }

            request.handleSquirrelsUpdate("4")

            mock_db.return_value.getSquirrel.assert_called_once_with("4")
            request.getRequestData.assert_called_once_with()
            mock_db.return_value.updateSquirrel.assert_called_once_with(
                "4", "jerry", "large"
            )
            request.send_response.assert_called_once_with(204)
            request.end_headers.assert_called_once_with()