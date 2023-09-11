LOG_IN_FORM = (
    '<form action="showSummary" method="post">',
    '<label for="email">Email:</label>',
    '<input type="email" name="email" id=""/>',
    '<button type="submit">Enter</button>',
    "</form>",
)


BOOK_COMPETITION_FORM = (
    '<form action="/purchasePlaces" method="post">',
    '<input type="hidden" name="club" value=',
    '<input type="hidden" name="competition" value="',
    '<label for="places">How many places?</label>',
    '<input type="number" name="places" max=',
    '<button type="submit">Book</button>',
    "</form>",
)
LOG_OUT_LINK = '<a href="/logout">Logout</a>'

DISPLAY_BOARD_LINK = '<a href="/displayBoard">See other clubs available points</a>'

COMPETITIONS_LIST_TEMPLATE = (
    "<h3>Competitions:</h3>",
    "<ul>",
    "<li>",
    "</li>",
    "<hr />",
    "</ul>",
)

CLUB_LIST_TEMPLATE = (
    "<h3>Clubs:</h3>",
    "<ul>",
    "<li>",
    "</li>",
    "<hr />",
    "</ul>",
)

COMPETITION_DETAILS_TEMPLATE = (
    "Date:",
    "Number of Places:",
    '<a href="/book/',
    ">Book Places</a>",
)


def is_log_in_form_in_html(parsed_html: str) -> bool:
    for html_snippets in LOG_IN_FORM:
        assert html_snippets in parsed_html
    return True


def is_club_name_displayed_in_welcome_html(parsed_html: str, club_name: str) -> bool:
    return f"Welcome, {club_name}" in parsed_html


def is_logout_option_available_in_welcome_html(parsed_html: str) -> bool:
    return LOG_OUT_LINK in parsed_html


def are_points_displayed_in_welcome_html(parsed_html: str) -> bool:
    return "Points available: " in parsed_html


def is_display_board_link_available_in_welcome_html(parsed_html: str) -> bool:
    return DISPLAY_BOARD_LINK in parsed_html


def is_competition_list_displayed_in_welcome_html(parsed_html: str) -> bool:
    for html_snippets in COMPETITIONS_LIST_TEMPLATE:
        assert html_snippets in parsed_html
    return True


def are_competition_details_displayed_in_welcome_html(parsed_html: str) -> bool:
    for html_snippets in COMPETITION_DETAILS_TEMPLATE:
        assert html_snippets in parsed_html
    return True


def is_book_option_available_for_going_competition_in_welcome_html(parsed_html: str) -> bool:
    return '<a href="/book/going/show_summary">Book Places</a>' in parsed_html


def is_book_option_unavailable_for_over_competition_in_welcome_html(parsed_html: str) -> bool:
    return '<a href="/book/over/show_summary">Book Places</a>' not in parsed_html


def is_book_option_unavailable_for_full_competition_in_welcome_html(parsed_html: str) -> bool:
    return '<a href="/book/full/show_summary">Book Places</a>' not in parsed_html


def is_competition_name_displayed_in_booking_html(parsed_html: str) -> bool:
    return "<title>Booking for" and "|| GUDLFT</title>" in parsed_html


def are_competition_places_displayed_in_booking_html(parsed_html: str) -> bool:
    return "Places available:" in parsed_html


def is_competition_date_displayed_in_booking_html(parsed_html: str) -> bool:
    return "This competition is open until" in parsed_html


def is_booking_form_displayed_in_booking_html(parsed_html: str) -> bool:
    for html_snippets in BOOK_COMPETITION_FORM:
        assert html_snippets in parsed_html
    return True


def are_clubs_points_displayed_in_display_board_html(parsed_html: str) -> bool:
    return "remaining points:" in parsed_html


def is_club_list_displayed_in_display_board_html(parsed_html: str) -> bool:
    for html_snippets in CLUB_LIST_TEMPLATE:
        assert html_snippets in parsed_html
    return True
