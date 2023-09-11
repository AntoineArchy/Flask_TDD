from http import HTTPStatus

from flask.testing import FlaskClient

from tests.tests_utils import decode_response


def test_invalid_email(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "invalid@example.com"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Sorry, that email wasn't found." in decoded_response


def test_no_email(client: FlaskClient) -> None:
    response = client.post("/showSummary", data={}, follow_redirects=True)

    decoded_response = decode_response(response.data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Sorry, that email wasn't found." in decoded_response


def test_email_valid(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert response.status_code == HTTPStatus.OK
    assert "Welcome, show_summary@test.srv" in decoded_response


def test_logout(client: FlaskClient) -> None:
    response = client.get("/logout")
    assert response.status_code == HTTPStatus.FOUND
