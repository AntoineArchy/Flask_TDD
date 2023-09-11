from http import HTTPStatus

from flask.testing import FlaskClient


def test_index(client: FlaskClient) -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
