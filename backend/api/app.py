""" Module for backend api endpoints. """

import flask
from flask import request
from flask_cors import CORS

from . import config
from . import main as core

app = flask.Flask(__name__)
CORS(app)


@app.route("/")
def welcome() -> str:
    """Function on '/' printing welcome message."""
    return "Welcome to backend api!"


@app.route("/read-all-subjective-symptoms", methods=["GET"])
def read_all_subjective_symptoms() -> flask.Response:
    """Function on '/read-all-subjective-symptoms' getting all subjective symptoms."""
    return _make_response(core.read_all_subjective_symptoms())


@app.route("/read-all-objective-symptoms", methods=["GET"])
def read_all_objective_symptoms() -> flask.Response:
    """Function on '/read-all-objective-symptoms' getting all objective symptoms."""
    return _make_response(core.read_all_objective_symptoms())


@app.route("/predict-cause", methods=["POST"])
def predict_cause() -> flask.Response:
    """Function on '/predict-cause' getting prediction result for cause."""
    return _make_response(
        core.predict_cause(
            request.form["subjective_symptoms"],
            request.form["objective_symptoms"],
            request.form["gender"],
        )
    )


@app.route("/read-all-etiologies", methods=["GET"])
def read_all_etiologies() -> flask.Response:
    """Function on '/read-all-etiologies' getting all etiologies."""
    return _make_response(core.read_all_etiologies())


@app.route("/read-etiology/<subjective_symptom_id>/<cause>", methods=["GET"])
def read_etiology(subjective_symptom_id, cause) -> flask.Response:
    """Function on '/read-etiology' getting etiology by subjective symptom and cause."""
    return _make_response(core.read_etiology(subjective_symptom_id, cause))


@app.route("/read-drugs/<etiology_id>", methods=["GET"])
def read_drugs(etiology_id) -> flask.Response:
    """Function on '/read-drugs' getting drugs by etiology."""
    return _make_response(core.read_drugs(etiology_id))


def _make_response(result) -> flask.Response:
    if result is None:
        response = flask.make_response("", 404)
    else:
        response = flask.make_response(result, 200)
    return response


def main() -> None:
    """Entry point if called as executable."""
    core.init()
    app.run(
        host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE, use_reloader=False
    )


if __name__ == "__main__":
    main()
