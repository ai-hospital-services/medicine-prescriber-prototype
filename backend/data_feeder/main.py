""" Module for command line interface (cli). """

import os

from . import config, document_db, lib, reader


def fetch_subjective_symptoms() -> list[str]:
    """Function to fetch subjective symptoms."""
    return reader.fetch_subjective_symptoms()


def fetch_associated_symptoms() -> list[reader.AssociativeSymptom]:
    """Function to fetch associated symptoms."""
    return reader.fetch_associated_symptoms()


def fetch_gender() -> list[str]:
    """Function to fetch gender."""
    return reader.fetch_gender()


def fetch_age_groups() -> list[str]:
    """Function to fetch age groups."""
    return reader.fetch_age_groups()


def fetch_investigations() -> list[str]:
    """Function to fetch investigations."""
    return reader.fetch_investigations()


def fetch_provisional_diagnosis_advises() -> list[reader.ProvisionalDiagnosisAdvise]:
    """Function to fetch provisional diagnosis advises."""
    return reader.fetch_provisional_diagnosis_advises()


# def fetch_advised_investigations() -> list[str]:
#     """Function to fetch advised investigations."""
#     return reader.fetch_advised_investigations()


# def fetch_management() -> list[str]:
#     """Function to fetch management."""
#     return reader.fetch_management()


# def fetch_surgical_management() -> list[str]:
#     """Function to fetch surgical management."""
#     return reader.fetch_surgical_management()


def delete_subjective_symptoms() -> None:
    """Function to delete subjective symptoms."""
    document_db.delete_subjective_symptoms()


def delete_associated_symptoms() -> None:
    """Function to delete associated symptoms."""
    document_db.delete_associated_symptoms()


def delete_gender() -> None:
    """Function to delete gender."""
    document_db.delete_gender()


def delete_age_groups() -> None:
    """Function to delete age groups."""
    document_db.delete_age_groups()


def delete_investigations() -> None:
    """Function to delete investigations."""
    document_db.delete_investigations()


def delete_provisional_diagnosis_advises() -> None:
    """Function to delete provisional diagnosis advises."""
    document_db.delete_provisional_diagnosis_advises()


# def delete_advised_investigations() -> None:
#     """Function to delete advised investigations."""
#     document_db.delete_advised_investigations()


# def delete_management() -> None:
#     """Function to delete management."""
#     document_db.delete_management()


# def delete_surgical_management() -> None:
#     """Function to delete surgical management."""
#     document_db.delete_surgical_management()


def upsert_subjective_symptoms(
    subjective_symptoms: list[str],
) -> None:
    """Function to upsert subjective symptoms."""
    document_db.upsert_subjective_symptoms(
        subjective_symptoms=subjective_symptoms,
    )


def upsert_associated_symptoms(
    associated_symptoms: list[reader.AssociativeSymptom],
) -> None:
    """Function to upsert associated symptoms."""
    document_db.upsert_associated_symptoms(
        associated_symptoms=associated_symptoms,
    )


def upsert_gender(
    gender: list[str],
) -> None:
    """Function to upsert gender."""
    document_db.upsert_gender(
        gender=gender,
    )


def upsert_age_groups(
    age_groups: list[str],
) -> None:
    """Function to upsert age groups."""
    document_db.upsert_age_groups(
        age_groups=age_groups,
    )


def upsert_investigations(
    investigations: list[str],
) -> None:
    """Function to upsert investigations."""
    document_db.upsert_investigations(
        investigations=investigations,
    )


def upsert_provisional_diagnosis_advises(
    provisional_diagnosis_advises: list[reader.ProvisionalDiagnosisAdvise],
) -> None:
    """Function to upsert provisional diagnosis advises."""
    document_db.upsert_provisional_diagnosis_advises(
        provisional_diagnosis_advises=provisional_diagnosis_advises,
    )


# def upsert_advised_investigations(
#     advised_investigations: list[str],
# ) -> None:
#     """Function to upsert advised investigations."""
#     document_db.upsert_advised_investigations(
#         advised_investigations=advised_investigations,
#     )


# def upsert_management(
#     management: list[str],
# ) -> None:
#     """Function to upsert management."""
#     document_db.upsert_management(
#         management=management,
#     )


# def upsert_surgical_management(
#     surgical_management: list[str],
# ) -> None:
#     """Function to upsert surgical management."""
#     document_db.upsert_surgical_management(
#         surgical_management=surgical_management,
#     )


def init() -> None:
    """Entry point if called as an executable."""
    lib.CLIArgs = lib.parse_cli_args()
    config.DEBUG_MODE = lib.CLIArgs.debug_mode
    config.MONGODB_URL = os.environ.get("MONGODB_URL", default=config.MONGODB_URL)
    config.MONGODB_DATABASE = os.environ.get(
        "MONGODB_DATABASE", default=config.MONGODB_DATABASE
    )

    lib.configure_global_logging_level()
    lib.log_config_settings()

    document_db.configure_mongodb_client()
    # mongodb.log_mongodb_status()


if __name__ == "__main__":
    init()

    delete_subjective_symptoms()
    subjective_symptoms = fetch_subjective_symptoms()
    upsert_subjective_symptoms(subjective_symptoms)

    delete_associated_symptoms()
    associated_symptoms = fetch_associated_symptoms()
    upsert_associated_symptoms(associated_symptoms)

    delete_gender()
    gender = fetch_gender()
    upsert_gender(gender)

    delete_age_groups()
    age_groups = fetch_age_groups()
    upsert_age_groups(age_groups)

    delete_investigations()
    investigations = fetch_investigations()
    upsert_investigations(investigations)

    delete_provisional_diagnosis_advises()
    advises = fetch_provisional_diagnosis_advises()
    upsert_provisional_diagnosis_advises(advises)

    # delete_advised_investigations()
    # advised_investigations = fetch_advised_investigations()
    # upsert_advised_investigations(advised_investigations)

    # delete_management()
    # management = fetch_management()
    # upsert_management(management)

    # delete_surgical_management()
    # surgical_management = fetch_surgical_management()
    # upsert_surgical_management(surgical_management)
