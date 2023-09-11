from flask.testing import FlaskClient

import html_checks
from tests.tests_utils import decode_response


def test_index_html(client: FlaskClient) -> None:
    response = client.get("/")
    decoded_response = decode_response(response.data)
    assert html_checks.is_log_in_form_in_html(decoded_response)
