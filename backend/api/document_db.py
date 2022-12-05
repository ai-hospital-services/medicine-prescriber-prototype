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
    """Log mongodb status."""
    logger = get_logger()

    logger.info("Starting log mongodb status")
    server_status_result = State.MONGODB_CLIENT.user.command("serverStatus")
    logger.info(server_status_result)
    logger.info("Completed log mongodb status")


def read_all_subjective_symptoms() -> list[str]:
    """Read all subjective symptoms."""
    logger = get_logger()

    logger.info("Starting read all subjective symptoms")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.subjective_symptoms.find({}):
        document = json_util.dumps(document)
        document = _replace_oid(document)
        result.append(json.loads(document))
    logger.info("Completed read all subjective symptoms")

    return result


def read_all_objective_symptoms() -> list[str]:
    """Read all objective symptoms."""
    logger = get_logger()

    logger.info("Starting read all objective symptoms")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.objective_symptoms.find({}):
        document = json_util.dumps(document)
        document = _replace_oid(document)
        result.append(json.loads(document))

    logger.info("Completed read all objective symptoms")

    return result


def read_all_etiologies() -> list[str]:
    """Read all etiologies data."""
    logger = get_logger()

    logger.info("Starting read all etiologies")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.etiologies.find({}):
        document = json_util.dumps(document)
        document = _replace_oid(document)
        result.append(json.loads(document))

    logger.info("Completed read all etiologies")

    return result


def read_etiology(subjective_symptom_id, cause) -> str:
    """Read etiology data by subjective symptom and cause."""
    logger = get_logger()

    logger.info(
        "Starting read etiology by symptom and cause",
        subjective_symptom_id=subjective_symptom_id,
        cause=cause,
    )
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    document = database.etiologies.find_one(
        {
            "subjective_symptom_id": ObjectId(subjective_symptom_id),
            "cause": str(cause).lower(),
        }
    )
    document = json_util.dumps(document) if document is not None else None
    document = _replace_oid(document) if document is not None else None
    document = json.loads(document) if document is not None else None
    logger.info(
        "Completed read etiology by symptom and cause",
        subjective_symptom=subjective_symptom_id,
        cause=cause,
    )

    return str(document) if document is not None else None


def read_drugs(etiology_id) -> list[str]:
    """Read drugs data by etiology."""
    logger = get_logger()

    logger.info("Starting read drugs by etiology", etiology_id=etiology_id)
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    result = []
    for document in database.drugs.find({"etiology_id": ObjectId(etiology_id)}):
        document = json_util.dumps(document)
        document = _replace_oid(document)
        result.append(json.loads(document))
    logger.info("Completed read drugs by etiology", etiology_id=etiology_id)

    return result


def _replace_oid(string):
    while True:
        pattern = re.compile(r'{\s*"\$oid":\s*("[a-z0-9]{1,}")\s*}')
        match = re.search(pattern, string)
        if match:
            string = string.replace(match.group(0), match.group(1))
        else:
            return string
