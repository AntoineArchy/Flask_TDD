from http import HTTPStatus

from flask.testing import FlaskClient


def test_display_board(client: FlaskClient) -> None:
    response = client.get("/displayBoard")
    assert response.status_code == HTTPStatus.OK
