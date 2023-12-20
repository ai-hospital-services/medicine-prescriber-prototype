""" Module for document db. """

from dataclasses import dataclass

from pymongo import MongoClient
from structlog import get_logger

from . import config
from . import healthcaremagic as hcm


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


def upsert_question_answer_list(
    question_answer_list: list[hcm.QuestionAnswer],
) -> None:
    """Function to upsert question answer list."""
    logger = get_logger()

    logger.info("Starting upsert question answer list")
    database = State.MONGODB_CLIENT[config.MONGODB_DATABASE]

    for question_answer in question_answer_list:
        database.doctor_raw_data.find_one_and_replace(
            {
                "doctor_profile_link": question_answer.doctor_profile_link,
                "question_detail_link": question_answer.question_detail_link,
            },
            {
                "doctor_profile_link": question_answer.doctor_profile_link,
                "question_detail_link": question_answer.question_detail_link,
                "question_type": question_answer.question_type.name,
                "question_title": question_answer.question_title,
                "question_posted_on": question_answer.question_posted_on,
                "question_text": question_answer.question_text,
                "answer_text": question_answer.answer_text,
                "followup_list": question_answer.followup_list,
                "last_updated": question_answer.last_updated,
            },
            upsert=True,
        )

        logger.info(
            "Completed upsert question answer list",
            doctor_profile_link=question_answer.doctor_profile_link,
            question_detail_link=question_answer.question_detail_link,
        )
