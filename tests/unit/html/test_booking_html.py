from flask.testing import FlaskClient

import html_checks
from tests.tests_utils import decode_response


def test_displayed_booking_html(client: FlaskClient) -> None:
    response = client.get(
        "/book/going/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert html_checks.is_competition_name_displayed_in_booking_html(decoded_response)
    assert html_checks.are_competition_places_displayed_in_booking_html(
        decoded_response
    )
    assert html_checks.is_competition_date_displayed_in_booking_html(decoded_response)
    assert html_checks.is_booking_form_displayed_in_booking_html(decoded_response)
