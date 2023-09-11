from flask.testing import FlaskClient

import html_checks
from tests.tests_utils import decode_response


def test_display_display_board(client: FlaskClient) -> None:
    response = client.get("/displayBoard", follow_redirects=True)
    decoded_response = decode_response(response.data)

    assert html_checks.are_clubs_points_displayed_in_display_board_html(
        decoded_response
    )
    assert html_checks.is_club_list_displayed_in_display_board_html(decoded_response)
