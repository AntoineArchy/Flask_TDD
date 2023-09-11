from flask.testing import FlaskClient

from tests.tests_utils import decode_response
from tests.unit.html import html_checks


def test_from_index_to_welcome(client: FlaskClient) -> None:
    response = client.get("/")
    decoded_response = decode_response(response.data)

    assert html_checks.is_log_in_form_in_html(decoded_response)

    logged_in = client.post(
        "/showSummary", data={"email": "index@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(logged_in.data)

    assert html_checks.is_club_name_displayed_in_welcome_html(decoded_response, "index")
