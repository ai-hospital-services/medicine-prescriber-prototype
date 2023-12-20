""" Module for command line interface (cli). """

import os

from . import config, document_db
from . import healthcaremagic as hcm
from . import lib


def fetch_question_bank_list(doctor_profile_link) -> list[hcm.QuestionBank]:
    """Function to fetch question bank list."""
    return hcm.fetch_question_bank_list(doctor_profile_link=doctor_profile_link)


def fetch_premium_question_list(
    question_bank: hcm.QuestionBank, start_page_number=-1, end_page_number=-1
) -> list[hcm.Question]:
    """Function to fetch premium question list."""
    return hcm.fetch_premium_question_list(
        question_bank=question_bank,
        start_page_number=start_page_number,
        end_page_number=end_page_number,
    )


def fetch_premium_question_answer_list(
    question_list: list[hcm.Question],
) -> list[hcm.QuestionAnswer]:
    """Function to fetch premium question answer list."""
    return hcm.fetch_premium_question_answer_list(
        question_list=question_list,
    )


def upsert_question_answer_list(
    question_answer_list: list[hcm.QuestionAnswer],
) -> None:
    """Function to upsert question answer list."""
    document_db.upsert_question_answer_list(
        question_answer_list=question_answer_list,
    )


def init() -> None:
    """Entry point if called as an executable."""
    lib.CLIArgs = lib.parse_cli_args()
    config.DEBUG_MODE = lib.CLIArgs.debug_mode
    config.MONGODB_URL = os.environ.get("MONGODB_URL", default=config.MONGODB_URL)
    config.MONGODB_DATABASE = os.environ.get(
        "MONGODB_DATABASE", default=config.MONGODB_DATABASE
    )
    config.HEALTHCAREMAGIC_DOMAIN_URL = os.environ.get(
        "HEALTHCAREMAGIC_DOMAIN_URL", default=config.HEALTHCAREMAGIC_DOMAIN_URL
    )
    config.HEALTHCAREMAGIC_DOMAIN_URL = os.environ.get(
        "HEALTHCAREMAGIC_DOMAIN_URL", default=config.HEALTHCAREMAGIC_DOMAIN_URL
    )

    lib.configure_global_logging_level()
    lib.log_config_settings()

    document_db.configure_mongodb_client()
    # mongodb.log_mongodb_status()


if __name__ == "__main__":
    init()
    question_bank_list = fetch_question_bank_list(lib.CLIArgs.doctor_profile_link)
    for question_bank in [
        qb for qb in question_bank_list if qb.question_type == hcm.QuestionType.PREMIUM
    ]:
        premium_question_list = fetch_premium_question_list(
            question_bank=question_bank, start_page_number=201, end_page_number=244
        )
        question_answer_list = fetch_premium_question_answer_list(
            question_list=premium_question_list
        )
        upsert_question_answer_list(question_answer_list)
