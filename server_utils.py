from __future__ import annotations

from datetime import datetime
from typing import Dict, Tuple, List


def is_competition_over(competition: Dict) -> bool:
    return datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now()


def find_club_by_name(club_name: str, clubs: List[Dict[str, str]]) -> Dict | None:
    return next((club for club in clubs if club["name"] == club_name), None)


def find_club_by_email(club_email: str, clubs: List[Dict[str, str]]) -> Dict | None:
    return next((club for club in clubs if club["email"] == club_email), None)


def find_competition_by_name(competition_name: str, competitions: List[Dict[str, str]]) -> Dict | None:
    return next(
        (
            competition
            for competition in competitions
            if competition["name"] == competition_name
        ),
        None,
    )


def get_form_data(form: Dict) -> Tuple[str | None, str | None, str | None]:
    club_name = form.get("club", None)
    places_required = form.get("places", None)
    competition_name = form.get("competition", None)
    return club_name, places_required, competition_name


def parse_places_required(places_required: str | None) -> int | None:
    if places_required is None or not places_required.isdigit():
        return None
    return int(places_required)


def is_valid_booking(club: Dict, competition: Dict, places_required: int) -> Tuple[bool, str | None]:
    # match / case ne sont pas utilisables ici, car pas d'expressions authorise dans les tokens, à creuser.
    if int(competition["numberOfPlaces"]) <= 0:
        return False, "Sorry this competition is already full."
    elif places_required > 12:
        return False, "Sorry you can't book more than 12 places."
    elif int(club["points"]) < 1:
        return False, "Sorry you dont have anymore points."
    elif places_required > int(club["points"]):
        return False, f"Sorry you can't book more than {int(club['points'])} places."
    elif int(competition["numberOfPlaces"]) < places_required:
        return (
            False,
            f"Sorry you can't book more than {competition['numberOfPlaces']} places.",
        )

    return True, None


# def is_valid_booking(club, competition, places_required):
#     # Use match/case to simplify the code
#     match places_required:
#         case int(competition["numberOfPlaces"]) <= 0:
#             return False, "Sorry this competition is already full."
#         case places_required > 12:
#             return False, "Sorry you can't book more than 12 places."
#         case places_required > int(club["points"]):
#             return False, f"Sorry you can't book more than {int(club['points'])} places."
#         case int(competition["numberOfPlaces"]) < places_required:
#             return False, f"Sorry you can't book more than {competition['numberOfPlaces']} places."
#         case _:
#             return True, None


def update_booking_data(club: Dict, competition: Dict, places_required: int) -> None:
    club["points"] = int(club["points"]) - int(places_required)
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - int(
        places_required
    )
