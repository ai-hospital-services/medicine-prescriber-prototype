""" Module for document db. """

import json
import re
from dataclasses import dataclass

from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
from structlog import get_logger

from . import config


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
        document = json_util.dumps(document)
        document = _replace_oid(document)
        result.append(json.loads(document))
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
        document = json_util.dumps(document)
        document = _replace_oid(document)
        document = _replace_date(document)
        result.append(json.loads(document))
    logger.info(
        "Completed read doctor raw data links by question detail link",
        question_detail_link=question_detail_link,
    )

    return result


def read_all_symptoms() -> list[str]:
    """Read all symptoms."""
    logger = get_logger()

    logger.info(
        "Starting read all symptoms",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.symptoms.find({}):
        document = json_util.dumps(document)
        document = _replace_oid(document)
        document = _replace_date(document)
        result.append(json.loads(document))
    logger.info(
        "Completed read all symptoms",
    )

    return result


def read_all_causes() -> list[str]:
    """Read all causes."""
    logger = get_logger()

    logger.info(
        "Starting read all causes",
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.causes.find({}):
        document = json_util.dumps(document)
        document = _replace_oid(document)
        document = _replace_date(document)
        result.append(json.loads(document))
    logger.info(
        "Completed read all causesÍ",
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
        document = json_util.dumps(document)
        document = _replace_oid(document)
        document = _replace_date(document)
        result.append(json.loads(document))
    logger.info(
        "Completed read doctor processed data links by question detail link",
        question_detail_link=question_detail_link,
    )

    return result


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
