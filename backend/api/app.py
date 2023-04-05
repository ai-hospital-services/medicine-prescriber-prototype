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


@app.route("/get-access-token/<authorisation_code>", methods=["GET"])
def get_access_token(authorisation_code) -> str:
    """Function on '/get-access-token' to get access token using authorisation code."""
    return _make_response_from_result(core.get_access_token(authorisation_code))


@app.route("/validate-access-token/<asserted_claims>", methods=["GET"])
def validate_access_token(asserted_claims) -> str:
    """Function on '/validate-access-token' to validate access token and verify claims."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, asserted_claims):
        return make_response("", 401)
    return make_response("", 200)


@app.route("/get-user-profile/<email_address>", methods=["GET"])
def get_user_profile(email_address) -> str:
    """Function on '/get-user-profile' to get user profile."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:user_profile"):
        return make_response("", 401)
    return _make_response_from_result(core.get_user_profile())


# region symptoms to causes


@app.route("/read-all-subjective-symptoms", methods=["GET"])
def read_all_subjective_symptoms() -> Response:
    """Function on '/read-all-subjective-symptoms' to read all subjective symptoms."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:subjective_symptoms"):
        return make_response("", 401)
    return _make_response_from_result(core.read_all_subjective_symptoms())


@app.route("/read-all-associated-symptoms", methods=["GET"])
def read_all_associated_symptoms() -> Response:
    """Function on '/read-all-associated-symptoms' to read all associated symptoms."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:associated_symptoms"):
        return make_response("", 401)
    return _make_response_from_result(core.read_all_associated_symptoms())


@app.route("/read-all-gender", methods=["GET"])
def read_all_gender() -> Response:
    """Function on '/read-all-gender' to read all gender values."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:gender"):
        return make_response("", 401)
    return _make_response_from_result(core.read_all_gender())


@app.route("/read-all-age-groups", methods=["GET"])
def read_all_age_groups() -> Response:
    """Function on '/read-all-age-groups' to read all age groups."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:age_groups"):
        return make_response("", 401)
    return _make_response_from_result(core.read_all_age_groups())


@app.route("/read-all-investigations", methods=["GET"])
def read_all_investigations() -> Response:
    """Function on '/read-all-investigations' to read all investigations."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:investigations"):
        return make_response("", 401)
    return _make_response_from_result(core.read_all_investigations())


@app.route("/predict-provisional-diagnosis", methods=["POST"])
def predict_provisional_diagnosis() -> Response:
    """Function on '/predict-provisional-diagnosis' getting prediction result for provisional diagnosis."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "predict:provisional_diagnosis"):
        return make_response("", 401)
    return _make_response_from_result(
        core.predict_provisional_diagnosis(
            request.form["subjective_symptoms"],
            request.form["associated_symptoms"],
            request.form["investigations_done"],
            request.form["gender"],
            request.form["age"],
        )
    )


@app.route("/read-advises", methods=["GET"])
def read_advises() -> Response:
    """Function on '/read-advises' to read advised investigations, management and surgical management."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:advises"):
        return make_response("", 401)
    return _make_response_from_result(
        core.read_advises(request.args.get("provisional_diagnosis"))
    )


# endregion

# region data scrapper


@app.route("/read-doctor-raw-data-links", methods=["GET"])
def read_doctor_raw_data_links() -> str:
    """Function on '/read-doctor-raw-data-links' to read doctor raw data links."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:doctor-raw-data-links"):
        return make_response("", 401)
    profile_link = request.args.get("profile_link")
    return _make_response_from_result(core.read_doctor_raw_data_links(profile_link))


@app.route("/read-doctor-raw-data", methods=["GET"])
def read_doctor_raw_data() -> str:
    """Function on '/read-doctor-raw-data' to read doctor raw data."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:doctor-raw-data"):
        return make_response("", 401)
    question_detail_link = request.args.get("question_detail_link")
    return _make_response_from_result(core.read_doctor_raw_data(question_detail_link))


@app.route("/read-doctor-processed-data", methods=["GET"])
def read_doctor_processed_data() -> str:
    """Function on '/read-doctor-processed-data' to read doctor processed data."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "read:doctor-processed-data"):
        return make_response("", 401)
    question_detail_link = request.args.get("question_detail_link")
    return _make_response_from_result(
        core.read_doctor_processed_data(question_detail_link)
    )


@app.route("/upsert-doctor-processed-data", methods=["POST"])
def upsert_doctor_processed_data() -> None:
    """Function on '/upsert-doctor-processed-data' to read doctor processed data."""
    token = _get_bearer_token()
    if not core.validate_access_token(token, "upsert:doctor-processed-data"):
        return make_response("", 401)
    question_detail_link = request.form.get("question_detail_link")
    return _make_response_from_result(
        core.read_doctor_processed_data(question_detail_link)
    )


# endregion


def _get_bearer_token() -> str:
    header = request.headers.get(config.AUTHORISATION_HEADER_KEY)
    return header.removeprefix("Bearer").strip() if header is not None else ""


def _make_response_from_result(result) -> Response:
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
