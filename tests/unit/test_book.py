from http import HTTPStatus

from flask.testing import FlaskClient

from tests.tests_utils import decode_response, is_redirection_page


def test_book_competition_over(client: FlaskClient) -> None:
    response = client.get(
        "/book/over/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert (
        "Sorry, this competition is over, places are not available anymore."
        in decoded_response
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_book_competition_going(client: FlaskClient) -> None:
    response = client.get(
        "/book/going/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "This competition is open until" in decoded_response
    assert response.status_code == HTTPStatus.OK


def test_book_non_existing_competition(client: FlaskClient) -> None:
    response = client.get(
        "/book/DoesntExist/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_book_non_existing_club(client: FlaskClient) -> None:
    response = client.get(
        "/book/empty/DoesntExist",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST
