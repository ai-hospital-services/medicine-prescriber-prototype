""" Module for backend api endpoints. """

from flask import Flask, Response, make_response, request
from flask_cors import CORS

from . import config
from . import main as core

app = Flask(__name__)
CORS(app)


@app.route("/")
def welcome() -> str:
    """Function on '/' printing welcome message."""
    return "Welcome to backend api!"


@app.route("/get-access-token/<authorisation_code>")
def get_access_token(authorisation_code) -> str:
    """Function on '/get-access-token' to get access token using authorisation code."""
    return _make_response(core.get_access_token(authorisation_code))


@app.route("/validate-access-token/<asserted_claims>")
def validate_access_token(asserted_claims) -> str:
    """Function on '/validate-access-token' to validate access token and verify claims."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, asserted_claims):
        return make_response("", 401)
    return make_response("", 200)


@app.route("/read-all-subjective-symptoms", methods=["GET"])
def read_all_subjective_symptoms() -> Response:
    """Function on '/read-all-subjective-symptoms' getting all subjective symptoms."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:subjective_symptoms"):
        return make_response("", 401)
    return _make_response(core.read_all_subjective_symptoms())


@app.route("/read-all-objective-symptoms", methods=["GET"])
def read_all_objective_symptoms() -> Response:
    """Function on '/read-all-objective-symptoms' getting all objective symptoms."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:objective_symptoms"):
        return make_response("", 401)
    return _make_response(core.read_all_objective_symptoms())


@app.route("/predict-cause", methods=["POST"])
def predict_cause() -> Response:
    """Function on '/predict-cause' getting prediction result for cause."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "predict:cause"):
        return make_response("", 401)
    return _make_response(
        core.predict_cause(
            request.form["subjective_symptoms"],
            request.form["objective_symptoms"],
            request.form["gender"],
        )
    )


@app.route("/read-all-etiologies", methods=["GET"])
def read_all_etiologies() -> Response:
    """Function on '/read-all-etiologies' getting all etiologies."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:etiologies"):
        return make_response("", 401)
    return _make_response(core.read_all_etiologies())


@app.route("/read-etiology/<subjective_symptom_id>/<cause>", methods=["GET"])
def read_etiology(subjective_symptom_id, cause) -> Response:
    """Function on '/read-etiology' getting etiology by subjective symptom and cause."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:etiologies"):
        return make_response("", 401)
    return _make_response(core.read_etiology(subjective_symptom_id, cause))


@app.route("/read-drugs/<etiology_id>", methods=["GET"])
def read_drugs(etiology_id) -> Response:
    """Function on '/read-drugs' getting drugs by etiology."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:drugs"):
        return make_response("", 401)
    return _make_response(core.read_drugs(etiology_id))


def _get_bearer_token() -> str:
    header = request.headers.get(config.AUTHORISATION_HEADER_KEY)
    return header.removeprefix("Bearer").strip() if header is not None else ""


def _make_response(result) -> Response:
    response = make_response("", 404) if result is None else make_response(result, 200)
    return response


def main() -> None:
    """Entry point if called as executable."""
    core.init()
    app.run(
        host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE, use_reloader=False
    )


if __name__ == "__main__":
    main()
