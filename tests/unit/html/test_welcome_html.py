from flask.testing import FlaskClient

import html_checks
from tests.tests_utils import decode_response


def test_display_welcome_html(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert html_checks.is_club_name_displayed_in_welcome_html(decoded_response, "show_summary")
    assert html_checks.are_points_displayed_in_welcome_html(decoded_response)
    assert html_checks.is_competition_list_displayed_in_welcome_html(decoded_response)
    assert html_checks.are_competition_details_displayed_in_welcome_html(decoded_response)


def test_urls_welcome_html(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert html_checks.is_logout_option_available_in_welcome_html(decoded_response)
    assert html_checks.is_display_board_link_available_in_welcome_html(decoded_response)


def test_booking_option_welcome_html(client: FlaskClient) -> None:
    response = client.post(
        "/showSummary", data={"email": "show_summary@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert html_checks.is_book_option_available_for_going_competition_in_welcome_html(
        decoded_response
    )
    assert html_checks.is_book_option_unavailable_for_over_competition_in_welcome_html(
        decoded_response
    )
    assert html_checks.is_book_option_unavailable_for_full_competition_in_welcome_html(
        decoded_response
    )
