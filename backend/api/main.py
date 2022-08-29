""" Module for command line interface (cli). """

import os

from . import config, document_db, lib, machine_learning


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


def init() -> None:
    """Entry point if called as an executable."""
    cli_args = lib.parse_cli_args()
    config.DEBUG_MODE = cli_args.debug_mode
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

    lib.configure_global_logging_level()
    lib.log_config_settings()

    machine_learning.configure()
    document_db.configure_mongodb_client()
    # mongodb.log_mongodb_status()


if __name__ == "__main__":
    init()
