from flask.testing import FlaskClient

from tests.tests_utils import decode_response
from tests.unit.html import html_checks


def test_from_booking_to_welcome(client: FlaskClient) -> None:
    response = client.get(
        f"/book/going/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert html_checks.is_booking_form_displayed_in_booking_html(decoded_response)
    booking = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )
    decoded_response = decode_response(booking.data)

    assert html_checks.is_club_name_displayed_in_welcome_html(
        decoded_response, "purchase_places"
    )
