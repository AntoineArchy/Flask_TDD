from datetime import datetime


def is_competition_over(competition):
    return datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now()


def find_club_by_name(club_name, clubs):
    return next((club for club in clubs if club["name"] == club_name), None)


def find_club_by_email(club_email, clubs):
    return next((club for club in clubs if club["email"] == club_email), None)


def find_competition_by_name(competition_name, competitions):
    return next(
        (
            competition
            for competition in competitions
            if competition["name"] == competition_name
        ),
        None,
    )


def get_form_data(form):
    club_name = form.get("club", None)
    places_required = form.get("places", None)
    competition_name = form.get("competition", None)
    return club_name, places_required, competition_name


def parse_places_required(places_required):
    if places_required is None or not places_required.isdigit():
        return None
    return int(places_required)


def is_valid_booking(club, competition, places_required):
    if int(competition["numberOfPlaces"]) <= 0:
        return False, "Sorry this competition is already full."
    elif places_required > 12:
        return False, "Sorry you can't book more than 12 places."
    elif places_required > int(club["points"]):
        return False, f"Sorry you can't book more than {int(club['points'])} places."
    elif int(competition["numberOfPlaces"]) < places_required:
        return (
            False,
            f"Sorry you can't book more than {competition['numberOfPlaces']} places.",
        )
    return True, None


def update_booking_data(club, competition, places_required):
    club["points"] = int(club["points"]) - places_required
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
