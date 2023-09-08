import datetime
import json
from http import HTTPStatus

from flask import Flask, render_template, request, redirect, flash, url_for

import server_utils


def load_data(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
        return data


app = Flask(__name__)
app.secret_key = "something_special"

clubs = load_data("clubs.json")["clubs"]
competitions = load_data("competitions.json")["competitions"]

# clubs = load_data(("tests/clubs.json")
# competitions = load_data("tests/competitions.json")


@app.route("/")
def index():
    return display_html_template("index", HTTPStatus.OK)


@app.route("/showSummary", methods=["POST"])
def show_summary():
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
def book(competition, club):
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
def purchase_places():
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


def display_html_template(template, status, **kwargs):
    return (
        render_template(template_name_or_list=f"{template}.html", now=datetime.datetime.now(), **kwargs),
        status,
    )


@app.route("/displayBoard")
def display_board():
    return display_html_template("display_board", HTTPStatus.OK, clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"), HTTPStatus.FOUND)
