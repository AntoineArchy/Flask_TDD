from http import HTTPStatus

from flask.testing import FlaskClient

from tests.tests_utils import decode_response
from tests.unit.html import html_checks


def test_from_welcome_to_logout(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert html_checks.is_logout_option_available_in_welcome_html(decoded_response)

    logout = client.get("/logout")
    assert logout.status_code == HTTPStatus.FOUND


def test_from_welcome_to_booking(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert html_checks.is_book_option_available_for_going_competition_in_welcome_html(
        decoded_response
    )

    booking = client.get(
        "/book/going/book",
        follow_redirects=True,
    )
    decoded_response = decode_response(booking.data)
    assert html_checks.is_competition_name_displayed_in_booking_html(decoded_response)
    assert html_checks.is_booking_form_displayed_in_booking_html(decoded_response)


def test_from_welcome_to_display_board(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)

    assert html_checks.is_display_board_link_available_in_welcome_html(decoded_response)
    display = client.get("/displayBoard", follow_redirects=True)
    decoded_response = decode_response(display.data)

    assert html_checks.are_clubs_points_displayed_in_display_board_html(
        decoded_response
    )
    assert html_checks.is_club_list_displayed_in_display_board_html(decoded_response)
