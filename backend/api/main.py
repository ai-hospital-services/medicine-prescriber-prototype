""" Module for command line interface (cli). """

import os

from . import config, document_db, lib, machine_learning, oauth2


def read_all_subjective_symptoms() -> list[str]:
    """Read all subjective symptoms."""
    return document_db.read_all_subjective_symptoms()


def read_all_objective_symptoms() -> list[str]:
    """Read all objective symptoms."""
    return document_db.read_all_objective_symptoms()


def predict_cause(
    subjective_symptoms, objective_symptoms, gender
) -> list[(str, float)]:
    """Predict cause from symptoms."""
    return machine_learning.predict_cause(
        subjective_symptoms, objective_symptoms, gender
    )


def read_all_etiologies() -> list[str]:
    """Read all etiologies data."""
    return document_db.read_all_etiologies()


def read_etiology(subjective_symptom_id, cause) -> str:
    """Read etiology data by subjective symptom and cause."""
    return document_db.read_etiology(subjective_symptom_id, cause)


def read_drugs(etiology_id) -> list[str]:
    """Read drugs by etiology."""
    return document_db.read_drugs(etiology_id)


def get_access_token(authorisation_code) -> str:
    """Get access token using authorisation code."""
    return oauth2.get_access_token(authorisation_code)


def validate_access_token(token, claims) -> bool:
    """Validate access token and verify claims."""
    return oauth2.validate_access_token(token, claims)


def init() -> None:
    """Entry point if called as an executable."""
    cli_args = lib.parse_cli_args()
    config.DEBUG_MODE = cli_args.debug_mode
    config.PORT = cli_args.port
    config.MODEL_FILE = os.environ.get("MODEL_FILE", default=config.MODEL_FILE)
    config.SYMPTOMS_TOKENISER_FILE = os.environ.get(
        "SYMPTOMS_TOKENISER_FILE", default=config.SYMPTOMS_TOKENISER_FILE
    )
    config.CAUSES_TOKENISER_FILE = os.environ.get(
        "CAUSES_TOKENISER_FILE", default=config.CAUSES_TOKENISER_FILE
    )
    config.SYMPTOMS_SEPARATOR = os.environ.get(
        "SYMPTOMS_SEPARATOR", default=config.SYMPTOMS_SEPARATOR
    )
    config.SYMPTOMS_SEQUENCE_PADDING_TYPE = os.environ.get(
        "SYMPTOMS_SEQUENCE_PADDING_TYPE", default=config.SYMPTOMS_SEQUENCE_PADDING_TYPE
    )
    config.SYMPTOMS_SEQUENCE_MAXLEN = os.environ.get(
        "SYMPTOMS_SEQUENCE_MAXLEN", default=config.SYMPTOMS_SEQUENCE_MAXLEN
    )
    config.MONGODB_URL = os.environ.get("MONGODB_URL", default=config.MONGODB_URL)
    config.MONGODB_DATABASE = os.environ.get(
        "MONGODB_DATABASE", default=config.MONGODB_DATABASE
    )
    config.WEB_REQUEST_TIMEOUT = os.environ.get(
        "WEB_REQUEST_TIMEOUT", default=config.WEB_REQUEST_TIMEOUT
    )
    config.CACHE_TIMEOUT = os.environ.get("CACHE_TIMEOUT", default=config.CACHE_TIMEOUT)
    config.TENANT_DOMAIN = os.environ.get("TENANT_DOMAIN", default=config.TENANT_DOMAIN)
    config.TENANT_OPENID_CONFIGURATION_CACHE_KEY = os.environ.get(
        "TENANT_OPENID_CONFIGURATION_CACHE_KEY",
        default=config.TENANT_OPENID_CONFIGURATION_CACHE_KEY,
    )
    config.AUTHORISATION_HEADER_KEY = os.environ.get(
        "AUTHORISATION_HEADER_KEY", default=config.AUTHORISATION_HEADER_KEY
    )
    config.REDIRECT_URL = os.environ.get("REDIRECT_URL", default=config.REDIRECT_URL)
    config.CLIENT_ID = os.environ.get("CLIENT_ID", default=config.CLIENT_ID)
    config.CLIENT_SECRET = os.environ.get("CLIENT_SECRET", default=config.CLIENT_SECRET)

    lib.configure_global_logging_level()
    lib.log_config_settings()

    machine_learning.configure()
    document_db.configure_mongodb_client()
    # mongodb.log_mongodb_status()
    oauth2.init_cache_state()


if __name__ == "__main__":
    init()
