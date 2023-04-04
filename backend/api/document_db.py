""" Module for document db. """

import json
import re
from dataclasses import dataclass

from bson import json_util
from pymongo import MongoClient
from structlog import get_logger

from . import config, user


@dataclass(init=True)
class State:
    """Class for storing state."""

    MONGODB_CLIENT = None


def configure_mongodb_client() -> None:
    """Configure mongodb client."""
    logger = get_logger()

    logger.info("Starting configure mongo client")
    url = config.MONGODB_URL
    State.MONGODB_CLIENT = MongoClient(url)
    logger.debug(f"Configured mongodb client with {url}")
    logger.info("Completed configure mongodb client")


def log_mongodb_status() -> None:
    """Log mongodb status in debug mode."""
    logger = get_logger()

    logger.info("Starting log mongodb status in DEBUG mode")
    server_status_result = State.MONGODB_CLIENT.user.command("serverStatus")
    logger.debug(server_status_result)
    logger.info("Completed log mongodb status in DEBUG mode")


# region symptoms to causes


def get_user(email_address) -> str:
    """Get user."""
    logger = get_logger()

    logger.info(
        "Starting get user",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    for document in database.users.find({"email_address": email_address}):
        result = _clean_document(document)
    logger.info(
        "Completed get user",
    )

    return result


def upsert_user(user: dict) -> None:
    """Upsert user."""
    logger = get_logger()

    logger.info(
        "Starting upsert user",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.users.find_one_and_replace(
        {
            "email_address": user["email_address"],
        },
        {
            "email_address": user["email_address"],
            "login_sub": user["login_sub"],
            "name": user["name"],
            "picture_url": user["picture_url"],
            "profile_url": user["profile_url"],
            "last_logged_in": user["last_logged_in"],
        },
    )
    logger.info(
        "Completed upsert user",
    )


def read_all_subjective_symptoms() -> list[str]:
    """Read all subjective symptoms."""
    logger = get_logger()

    logger.info(
        "Starting read all subjective symptoms",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.subjective_symptoms.find({}):
        result.append(_clean_document(document))
    logger.info(
        "Completed read all subjective symptoms",
    )

    return result


def read_all_associated_symptoms() -> list[str]:
    """Read all associated symptoms."""
    logger = get_logger()

    logger.info(
        "Starting read all associated symptoms",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.associated_symptoms.find({}):
        result.append(_clean_document(document))
    logger.info(
        "Completed read all associated symptoms",
    )

    return result


def read_all_gender() -> list[str]:
    """Read all gender values."""
    logger = get_logger()

    logger.info(
        "Starting read all gender values",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.gender.find({}):
        result.append(_clean_document(document))
    logger.info(
        "Completed read all gender values",
    )

    return result


def read_all_age_groups() -> list[str]:
    """Read all age groups."""
    logger = get_logger()

    logger.info(
        "Starting read all age groups",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.age_groups.find({}):
        result.append(_clean_document(document))
    logger.info(
        "Completed read all age groups",
    )

    return result


def read_all_investigations() -> list[str]:
    """Read all investigations."""
    logger = get_logger()

    logger.info(
        "Starting read all investigations",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.investigations.find({}):
        result.append(_clean_document(document))
    logger.info(
        "Completed read all investigations",
    )

    return result


def read_advises(provisional_diagnosis) -> list[str]:
    """Read advised investigations, management and surgical management."""
    logger = get_logger()

    logger.info(
        "Starting read advised investigations, management and surgical management",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.provisional_diagnosis_advises.find(
        {"provisional_diagnosis": provisional_diagnosis}
    ):
        result.append(_clean_document(document))
    logger.info(
        "Completed read advised investigations, management and surgical management",
    )

    return result


# endregion

# region data scrapper


def read_doctor_raw_data_links(profile_link) -> list[str]:
    """Read doctor raw data links."""
    logger = get_logger()

    logger.info(
        "Starting read doctor raw data links by profile link",
        profile_link=profile_link,
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.doctor_raw_data.find(
        {"doctor_profile_link": profile_link},
        {"_id": True, "question_detail_link": True},
    ):
        result.append(_clean_document(document))
    logger.info(
        "Completed read doctor raw data links by profile link",
        profile_link=profile_link,
    )

    return result


def read_doctor_raw_data(question_detail_link) -> list[str]:
    """Read doctor raw data."""
    logger = get_logger()

    logger.info(
        "Starting read doctor raw data by question detail link",
        question_detail_link=question_detail_link,
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.doctor_raw_data.find(
        {"question_detail_link": question_detail_link},
    ):
        result.append(_clean_document(document))
    logger.info(
        "Completed read doctor raw data links by question detail link",
        question_detail_link=question_detail_link,
    )

    return result


def read_doctor_processed_data(question_detail_link) -> list[str]:
    """Read doctor processed data."""
    logger = get_logger()

    logger.info(
        "Starting read doctor processed data by question detail link",
        question_detail_link=question_detail_link,
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.doctor_processed_data.find(
        {"question_detail_link": question_detail_link},
    ):
        result.append(_clean_document(document))
    logger.info(
        "Completed read doctor processed data links by question detail link",
        question_detail_link=question_detail_link,
    )

    return result


# endregion


def _clean_document(document):
    document = json_util.dumps(document)
    document = _replace_oid(document)
    document = _replace_date(document)
    return json.loads(document)


def _replace_oid(string):
    while True:
        pattern = re.compile(r'{\s*"\$oid":\s*("[a-z0-9]{1,}")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string


def _replace_date(string):
    while True:
        pattern = re.compile(r'{\s*"\$date":\s*("[TZ0-9-:.]{1,}")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string
