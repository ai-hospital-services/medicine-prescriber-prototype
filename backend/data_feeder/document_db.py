""" Module for document db. """

import json
from dataclasses import dataclass

from bson import json_util, objectid
from pymongo import MongoClient
from structlog import get_logger

from . import config, reader


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


def delete_subjective_symptoms() -> None:
    """Function to delete subjective symptoms."""
    logger = get_logger()
    logger.info("Starting delete subjective symptoms")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.subjective_symptoms.delete_many({})
    logger.info("Completed delete subjective symptoms")


def delete_associated_symptoms() -> None:
    """Function to delete associated symptoms."""
    logger = get_logger()
    logger.info("Starting delete associated symptoms")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.associated_symptoms.delete_many({})
    logger.info("Completed delete associated symptoms")


def delete_gender() -> None:
    """Function to delete gender."""
    logger = get_logger()
    logger.info("Starting delete gender")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.gender.delete_many({})
    logger.info("Completed delete gender")


def delete_age_groups() -> None:
    """Function to delete age groups."""
    logger = get_logger()
    logger.info("Starting delete age groups")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.age_groups.delete_many({})
    logger.info("Completed delete age groups")


def delete_investigations() -> None:
    """Function to delete investigations."""
    logger = get_logger()
    logger.info("Starting delete investigations")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.investigations.delete_many({})
    logger.info("Completed delete investigations")


def delete_provisional_diagnosis_advises() -> None:
    """Function to delete provisional diagnosis advises."""
    logger = get_logger()
    logger.info("Starting delete provisional diagnosis advises")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    database.provisional_diagnosis_advises.delete_many({})
    logger.info("Completed delete provisional diagnosis advises")


# def delete_advised_investigations() -> None:
#     """Function to delete advised investigations."""
#     logger = get_logger()
#     logger.info("Starting delete advised investigations")
#     database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
#     database.advised_investigations.delete_many({})
#     logger.info("Completed delete advised investigations")


# def delete_management() -> None:
#     """Function to delete management."""
#     logger = get_logger()
#     logger.info("Starting delete management")
#     database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
#     database.management.delete_many({})
#     logger.info("Completed delete management")


# def delete_surgical_management() -> None:
#     """Function to delete surgical management."""
#     logger = get_logger()
#     logger.info("Starting delete surgical management")
#     database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
#     database.surgical_management.delete_many({})
#     logger.info("Completed delete surgical management")


def upsert_subjective_symptoms(
    subjective_symptoms: list[str],
) -> None:
    """Function to upsert subjective symptoms."""
    logger = get_logger()
    logger.info("Starting upsert subjective symptoms")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    for subjective_symptom in subjective_symptoms:
        database.subjective_symptoms.find_one_and_replace(
            {
                "symptom": subjective_symptom,
            },
            {
                "symptom": subjective_symptom,
            },
            upsert=True,
        )

        logger.info(
            "Completed upsert subjective symptoms",
            subjective_symptom=subjective_symptom,
        )


def upsert_associated_symptoms(
    associated_symptoms: list[reader.AssociativeSymptom],
) -> None:
    """Function to upsert associated symptoms."""
    logger = get_logger()

    logger.info("Starting upsert associated symptoms")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    subjective_symptoms = []
    for document in database.subjective_symptoms.find({}):
        document = json_util.dumps(document)
        document = json.loads(document)
        subjective_symptoms.append((document["symptom"], document["_id"]["$oid"]))
    for associated_symptom in associated_symptoms:
        find = [
            x
            for x in subjective_symptoms
            if x[0] == associated_symptom.subjective_symptom
        ]
        database.associated_symptoms.find_one_and_replace(
            {
                "symptom": associated_symptom.symptom,
                "subjective_symptom_id": objectid.ObjectId(oid=find[0][1]),
            },
            {
                "symptom": associated_symptom.symptom,
                "subjective_symptom_id": objectid.ObjectId(oid=find[0][1]),
            },
            upsert=True,
        )
        logger.info(
            "Completed upsert associated symptoms",
            associated_symptom=associated_symptom,
        )


def upsert_gender(
    gender: list[str],
) -> None:
    """Function to upsert gender."""
    logger = get_logger()
    logger.info("Starting upsert gender")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    for g in gender:
        database.gender.find_one_and_replace(
            {
                "gender": g,
            },
            {
                "gender": g,
            },
            upsert=True,
        )
        logger.info(
            "Completed upsert gender",
            gender=g,
        )


def upsert_age_groups(
    age_groups: list[str],
) -> None:
    """Function to upsert age groups."""
    logger = get_logger()
    logger.info("Starting upsert age groups")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    for age in age_groups:
        database.age_groups.find_one_and_replace(
            {
                "age": age,
            },
            {
                "age": age,
            },
            upsert=True,
        )
        logger.info(
            "Completed upsert age groups",
            age=age,
        )


def upsert_investigations(
    investigations: list[str],
) -> None:
    """Function to upsert investigations."""
    logger = get_logger()
    logger.info("Starting upsert investigations")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    for i in investigations:
        database.investigations.find_one_and_replace(
            {
                "investigation": i,
            },
            {
                "investigation": i,
            },
            upsert=True,
        )
        logger.info(
            "Completed upsert investigations",
            investigations=i,
        )


def upsert_provisional_diagnosis_advises(
    provisional_diagnosis_advises: list[reader.ProvisionalDiagnosisAdvise],
) -> None:
    """Function to upsert provisional diagnosis advises."""
    logger = get_logger()
    logger.info("Starting upsert provisional diagnosis advises")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
    for a in provisional_diagnosis_advises:
        for b in a.advises:
            database.provisional_diagnosis_advises.find_one_and_replace(
                {
                    "provisional_diagnosis": a.provisional_diagnosis,
                    "advised_investigations": b.advised_investigations,
                    "management": b.management,
                    "surgical_management": b.surgical_management,
                },
                {
                    "provisional_diagnosis": a.provisional_diagnosis,
                    "advised_investigations": b.advised_investigations,
                    "management": b.management,
                    "surgical_management": b.surgical_management,
                },
                upsert=True,
            )
        logger.info(
            "Completed upsert provisional diagnosis advises",
            provisional_diagnosis=a.provisional_diagnosis,
        )


# def upsert_advised_investigations(
#     advised_investigations: list[str],
# ) -> None:
#     """Function to upsert advised investigations."""
#     logger = get_logger()
#     logger.info("Starting upsert advised investigations")
#     database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
#     for i in advised_investigations:
#         database.advised_investigations.find_one_and_replace(
#             {
#                 "advised_investigations": i,
#             },
#             {
#                 "advised_investigations": i,
#             },
#             upsert=True,
#         )
#         logger.info(
#             "Completed upsert advised investigations",
#             advised_investigations=i,
#         )


# def upsert_management(
#     management: list[str],
# ) -> None:
#     """Function to upsert management."""
#     logger = get_logger()
#     logger.info("Starting upsert management")
#     database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
#     for m in management:
#         database.management.find_one_and_replace(
#             {
#                 "management": m,
#             },
#             {
#                 "management": m,
#             },
#             upsert=True,
#         )
#         logger.info(
#             "Completed upsert management done",
#             management=m,
#         )


# def upsert_surgical_management(
#     surgical_management: list[str],
# ) -> None:
#     """Function to upsert surgical management."""
#     logger = get_logger()
#     logger.info("Starting upsert surgical management")
#     database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]
#     for m in surgical_management:
#         database.surgical_management.find_one_and_replace(
#             {
#                 "surgical_management": m,
#             },
#             {
#                 "surgical_management": m,
#             },
#             upsert=True,
#         )
#         logger.info(
#             "Completed upsert surgical management done",
#             surgical_management=m,
#         )
