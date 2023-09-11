from __future__ import annotations

import datetime
import json
from http import HTTPStatus
from typing import Dict, Tuple

from flask import Flask, render_template, request, redirect, flash, url_for, Response

import server_utils


def load_data(file_name: str) -> Dict:
    with open(file_name) as data_file:
        data = json.load(data_file)
        return data


def display_html_template(template: str, status: HTTPStatus, **kwargs) -> Tuple[str, HTTPStatus]:
    """ Helper fonction qui s'occupe de l'affichage de templates """
    return (
        render_template(
            template_name_or_list=f"{template}.html",
            now=datetime.datetime.now(),
            **kwargs,
        ),
        status,
    )


app = Flask(__name__)
app.secret_key = "something_special"

clubs = load_data("clubs.json")["clubs"]
competitions = load_data("competitions.json")["competitions"]

# clubs = load_data(("tests/clubs.json")
# competitions = load_data("tests/competitions.json")


@app.route("/")
def index() -> Tuple[str, HTTPStatus]:
    """ Permet à un utilisateur de se connecter au site  """
    return display_html_template("index", HTTPStatus.OK)


@app.route("/showSummary", methods=["POST"])
def show_summary() -> Tuple[str, HTTPStatus]:
    """ Contrôle le mail transmis par l'utilisateur et le redirige sur la page adequate. """
    email = request.form.get("email", None)
    club = server_utils.find_club_by_email(email, clubs)

    if not club:
        flash("Sorry, that email wasn't found.")
        return display_html_template("index", HTTPStatus.BAD_REQUEST)

    return display_html_template(
        "welcome",
        HTTPStatus.OK,
        club=club,
        competitions=competitions,
    )


@app.route("/book/<competition>/<club>")
def book(competition: str, club: str) -> Tuple[str, HTTPStatus] | Response:
    """ Permet à un utilisateur de reserve des places pour une competition """
    found_club = server_utils.find_club_by_name(club, clubs)
    found_competition = server_utils.find_competition_by_name(competition, competitions)

    if not found_competition or not found_club:
        flash("Something went wrong-please try again")
        return redirect(url_for("index"), HTTPStatus.BAD_REQUEST)
    if server_utils.is_competition_over(found_competition):
        flash("Sorry, this competition is over, places are not available anymore.")
        return display_html_template(
            "welcome", HTTPStatus.BAD_REQUEST, club=club, competitions=competitions
        )

    return display_html_template(
        "booking", HTTPStatus.OK, club=found_club, competition=found_competition
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places() -> Tuple[str, HTTPStatus] | Response:
    """ Contrôle l'intégrité des informations transmises par l'utilisateur avant réservation ou redirection. """
    club_name, places_required_str, competition_name = server_utils.get_form_data(
        request.form
    )

    club = server_utils.find_club_by_name(club_name, clubs)
    competition = server_utils.find_competition_by_name(competition_name, competitions)

    if not club or not competition or server_utils.is_competition_over(competition):
        flash("Something went wrong-please try again")
        return redirect(url_for("index"), HTTPStatus.BAD_REQUEST)

    places_required = server_utils.parse_places_required(places_required_str)
    if places_required is None:
        flash("Please provide a valid rounded number")
        return display_html_template(
            "welcome", HTTPStatus.BAD_REQUEST, club=club, competitions=competitions
        )

    valid_booking, error_msg = server_utils.is_valid_booking(
        club, competition, places_required
    )
    if valid_booking:
        server_utils.update_booking_data(club, competition, places_required)
        flash("Great-booking complete!")
        return display_html_template(
            "welcome", HTTPStatus.OK, club=club, competitions=competitions
        )

    flash(error_msg)
    return display_html_template(
        "welcome", HTTPStatus.BAD_REQUEST, club=club, competitions=competitions
    )


@app.route("/displayBoard")
def display_board() -> Tuple[str, HTTPStatus]:
    """ Permet à l'utilisateur de consulté les points des clubs inscrits sur le site. """
    return display_html_template("display_board", HTTPStatus.OK, clubs=clubs)


@app.route("/logout")
def logout() -> Response:
    """ Permet à l'utilisateur de retourner sur la page d'identification. """
    return redirect(url_for("index"), HTTPStatus.FOUND)
