import html

from flask import Response


def decode_response(response_bytes: Response.data) -> str:
    decoded_text = response_bytes.decode("utf-8")
    decoded_text = html.unescape(decoded_text)
    return decoded_text


def is_redirection_page(decoded_response: str) -> bool:
    return "<title>Redirecting...</title>\n<h1>Redirecting...</h1>" in decoded_response
