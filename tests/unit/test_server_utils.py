import server_utils

PAST = "2020-03-27 10:00:00"

FUTURE = "6000-03-27 10:00:00"

TEST_COMPETITIONS = [
    {"name": "going", "date": "2026-03-27 10:00:00", "numberOfPlaces": "5"}
]
TEST_COMPETITION = TEST_COMPETITIONS[0]

TEST_CLUBS = [{"name": "Existing", "email": "email@test.srv", "points": "10"}]

TEST_CLUB = TEST_CLUBS[0]

TEST_FORM = {
    "club": TEST_CLUB.get("name"),
    "places": int(TEST_COMPETITION.get("numberOfPlaces")) - 1,
    "competition": TEST_COMPETITION.get("name"),
}


def test_is_comp_over_true() -> None:
    assert server_utils.is_competition_over({"date": PAST}) is True


def test_is_comp_over_false() -> None:
    assert server_utils.is_competition_over({"date": FUTURE}) is False


def test_find_club_by_name_found() -> None:
    assert (
        server_utils.find_club_by_name(TEST_CLUBS[0].get("name"), TEST_CLUBS)
        == TEST_CLUBS[0]
    )


def test_find_club_by_name_not_found() -> None:
    doesnt_exist = server_utils.find_club_by_name(
        TEST_CLUBS[0].get("name") + " ", TEST_CLUBS
    )
    assert doesnt_exist is None
    assert doesnt_exist not in TEST_CLUBS


def test_find_club_by_email_found() -> None:
    assert (
        server_utils.find_club_by_email(TEST_CLUBS[0].get("email"), TEST_CLUBS)
        == TEST_CLUBS[0]
    )


def test_find_club_by_email_not_found() -> None:
    doesnt_exist = server_utils.find_club_by_email(
        TEST_CLUBS[0].get("email") + " ", TEST_CLUBS
    )
    assert doesnt_exist is None
    assert doesnt_exist not in TEST_CLUBS


def test_find_competition_by_name_found() -> None:
    assert (
        server_utils.find_competition_by_name(
            TEST_COMPETITIONS[0].get("name"), TEST_COMPETITIONS
        )
        is TEST_COMPETITIONS[0]
    )


def test_find_competition_by_name_not_found() -> None:
    doesnt_exist = server_utils.find_competition_by_name(
        TEST_COMPETITIONS[0].get("name") + " ", TEST_COMPETITIONS
    )
    assert doesnt_exist is None
    assert doesnt_exist not in TEST_COMPETITIONS


def test_get_form_data_complete_data() -> None:
    assert server_utils.get_form_data(TEST_FORM) == tuple(TEST_FORM.values())


def test_get_form_data_no_data() -> None:
    assert server_utils.get_form_data({}) == tuple([None] * len(TEST_FORM))


def test_parse_places_required_valid_data() -> None:
    assert server_utils.parse_places_required("4") is 4


def test_parse_places_required_float() -> None:
    assert server_utils.parse_places_required("1.5") is None


def test_parse_places_required_non_numerical() -> None:
    assert server_utils.parse_places_required(None) is None
    assert server_utils.parse_places_required("This is not a number") is None


def test_is_valid_booking_full_comp() -> None:
    TEST_COMPETITION["numberOfPlaces"] = "-5"
    status, message = server_utils.is_valid_booking(TEST_CLUB, TEST_COMPETITION, 0)
    assert status is False
    assert message == "Sorry this competition is already full."

    TEST_COMPETITION["numberOfPlaces"] = "5"


def test_is_valid_booking_purchase_more_than_valid():
    status, message = server_utils.is_valid_booking(TEST_CLUB, TEST_COMPETITION, 15)
    assert status is False
    assert message == "Sorry you can't book more than 12 places."


def test_is_valid_booking_purchase_with_no_points() -> None:
    TEST_CLUB["points"] = "0"
    status, message = server_utils.is_valid_booking(TEST_CLUB, TEST_COMPETITION, 1)
    assert status is False
    assert message == "Sorry you dont have anymore points."
    TEST_CLUB["points"] = "10"


def test_is_valid_booking_purchase_more_than_available_points() -> None:
    status, message = server_utils.is_valid_booking(
        TEST_CLUB, TEST_COMPETITION, int(TEST_CLUB["points"]) + 1
    )
    assert status is False
    assert (
        message == f"Sorry you can't book more than {int(TEST_CLUB['points'])} places."
    )


def test_is_valid_booking_purchase_more_than_available_places() -> None:
    status, message = server_utils.is_valid_booking(
        TEST_CLUB, TEST_COMPETITION, int(TEST_COMPETITION["numberOfPlaces"]) + 1
    )
    assert status is False
    assert (
        message
        == f"Sorry you can't book more than {int(TEST_COMPETITION['numberOfPlaces'])} places."
    )


def test_is_valid_booking_valid_data() -> None:
    status, message = server_utils.is_valid_booking(TEST_CLUB, TEST_COMPETITION, 2)
    assert status is True
    assert message is None


def test_update_booking_data() -> None:
    target_club_points = int(TEST_CLUB["points"]) - 1
    target_competition_places = int(TEST_COMPETITION["numberOfPlaces"]) - 1

    server_utils.update_booking_data(TEST_CLUB, TEST_COMPETITION, 1)

    assert TEST_CLUB["points"] == target_club_points
    assert TEST_COMPETITION["numberOfPlaces"] == target_competition_places
