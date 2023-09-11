from http import HTTPStatus

from flask.testing import FlaskClient

from tests.tests_utils import decode_response, is_redirection_page


def test_purchase_no_club(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_non_existing_club(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "DoesntExist", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_no_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "purchase_places", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_non_existing_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "DoesntExist", "club": "purchase_places", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_competition_over(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "over", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert is_redirection_page(decoded_response)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_no_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Please provide a valid rounded number" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_non_numerical_number_of_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "€"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Please provide a valid rounded number" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_non_int_number_of_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "1.1"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Please provide a valid rounded number" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_competition_is_full(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "full", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert "Sorry this competition is already full." in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_not_enough_places_for_purchase(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "going", "club": "purchase_places", "places": "6"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert "Sorry you can't book more than 5 places." in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_purchase_more_than_allowed_places(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "going", "club": "purchase_places", "places": "15"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Sorry you can't book more than 12 places" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_not_enough_points_for_purchase(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert "Sorry you can't book more than 10 places" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_points_are_deducted_after_booking(client: FlaskClient) -> None:
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert "Points available: 9" in decoded_response
    assert response.status_code == HTTPStatus.OK
