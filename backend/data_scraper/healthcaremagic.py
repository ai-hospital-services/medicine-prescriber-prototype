""" Module for data scraper. """

import urllib.parse
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

import requests
from bs4 import BeautifulSoup
from retry import retry
from structlog import get_logger

from . import config


class QuestionType(Enum):
    """Class for question type enum."""

    PREMIUM = 1
    PUBLIC_FORUM = 2


@dataclass(init=True)
class QuestionBank:
    """Class for question bank."""

    doctor_profile_link: str = None
    question_bank_link: str = None
    question_type: QuestionType = None


def fetch_question_bank_list(doctor_profile_link) -> list[QuestionBank]:
    """Function to fetch question bank list."""
    logger = get_logger()

    # make a web request for question bank list
    logger.info(
        "Starting fetch question bank list",
        domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
        doctor_profile_link=doctor_profile_link,
    )
    response = _web_request_get(doctor_profile_link)
    if response.status_code != 200:
        logger.error(
            "Completed fetch question bank list",
            domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
            doctor_profile_link=doctor_profile_link,
            response_status_code=response.status_code,
        )
        raise Exception(
            f"Error: request failed with response status code: {response.status_code}"
        )
    logger.info(
        "Completed fetch question bank list",
        domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
        doctor_profile_link=doctor_profile_link,
        response_status_code=response.status_code,
    )

    # parse the web response
    premium_question_link = None
    public_question_link = None
    soup = BeautifulSoup(response.content, "html.parser")
    h2s = soup.find_all("h2", class_="OrangeH2")
    for h2 in h2s:
        if "Premium questions answered by" in h2.string and not premium_question_link:
            view_all_anchor = h2.find_next("a", class_="moreAnchor")
            if view_all_anchor:
                premium_question_link = urllib.parse.urljoin(
                    config.HEALTHCAREMAGIC_DOMAIN_URL,
                    urllib.parse.quote(
                        str.strip(str.strip(view_all_anchor.attrs["href"])).encode(
                            "latin1"
                        )
                    ),
                )
        if (
            "Public forum questions answered by" in h2.string
            and not public_question_link
        ):
            view_all_anchor = h2.find_next("a", class_="moreAnchor")
            if view_all_anchor:
                public_question_link = urllib.parse.urljoin(
                    config.HEALTHCAREMAGIC_DOMAIN_URL,
                    urllib.parse.quote(
                        str.strip(str.strip(view_all_anchor.attrs["href"])).encode(
                            "latin1"
                        )
                    ),
                )

    return [
        QuestionBank(
            doctor_profile_link=doctor_profile_link,
            question_bank_link=premium_question_link,
            question_type=QuestionType.PREMIUM,
        ),
        QuestionBank(
            doctor_profile_link=doctor_profile_link,
            question_bank_link=public_question_link,
            question_type=QuestionType.PUBLIC_FORUM,
        ),
    ]


@retry(tries=10, delay=10, backoff=2)
def _web_request_get(url) -> requests.Response:
    return requests.get(url=url, timeout=config.HEALTHCAREMAGIC_REQUEST_TIMEOUT_SECONDS)


@dataclass(init=True)
class Question:
    """Class for question."""

    doctor_profile_link: str = None
    question_type: QuestionType = None
    question_detail_link: str = None
    question_title: str = None


def fetch_premium_question_list(
    question_bank: QuestionBank, start_page_number=-1, end_page_number=-1
) -> list[Question]:
    """Function to fetch premium question list."""
    logger = get_logger()

    if question_bank.question_type != QuestionType.PREMIUM:
        return []

    # make a web request for premium question list
    page_number = 1
    question_list = []
    question_listing_link = question_bank.question_bank_link
    while question_listing_link:
        logger.info(
            f"Starting fetch premium questions on listing page {page_number} for doctor profile {question_bank.doctor_profile_link}",
            domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
            doctor_profile_link=question_bank.doctor_profile_link,
            question_type=question_bank.question_type,
            page_number=page_number,
        )
        response = _web_request_get(question_listing_link)
        if response.status_code != 200:
            logger.error(
                f"Completed fetch premium questions on listing page {page_number} for doctor profile {question_bank.doctor_profile_link}",
                domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
                doctor_profile_link=question_bank.doctor_profile_link,
                question_type=question_bank.question_type,
                page_number=page_number,
                response_status_code=response.status_code,
            )
            raise Exception(
                f"Error: request failed with response status code: {response.status_code}"
            )
        logger.info(
            f"Completed fetch premium questions on listing page {page_number} for doctor profile {question_bank.doctor_profile_link}",
            domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
            doctor_profile_link=question_bank.doctor_profile_link,
            question_type=question_bank.question_type,
            page_number=page_number,
            response_status_code=response.status_code,
        )

        # parse the web response
        soup = BeautifulSoup(response.content, "html.parser")

        # get all the premium questions
        if start_page_number > 0 and page_number >= start_page_number:
            wrapper_div = soup.find("div", class_="hpInWrap")
            question_anchors = wrapper_div.find_all("a", class_="smallTitle")
            for question_anchor in question_anchors:
                question = Question(
                    doctor_profile_link=question_bank.doctor_profile_link,
                    question_type=question_bank.question_type,
                    question_detail_link=urllib.parse.urljoin(
                        config.HEALTHCAREMAGIC_DOMAIN_URL,
                        urllib.parse.quote(
                            str.strip(question_anchor.attrs["href"]).encode("latin1")
                        ),
                    ),
                    question_title=question_anchor.string,
                )
                question_list.append(question)
        else:
            logger.info(
                f"Skipping parse premium questions on listing page {page_number} for doctor profile {question_bank.doctor_profile_link}",
                domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
                question_type=question_bank.question_type,
                page_number=page_number,
                response_status_code=response.status_code,
            )

        # check the next question listing pagination link
        question_listing_link = None
        pagination_div = soup.find("div", id="paginationDiv")
        pagination_anchors = pagination_div.find_all("a", class_="box")
        for pagination_anchor in pagination_anchors:
            if "Next" in pagination_anchor.string:
                question_listing_link = urllib.parse.urljoin(
                    config.HEALTHCAREMAGIC_DOMAIN_URL,
                    str.strip(pagination_anchor.attrs["href"]),
                )
                break

        if end_page_number > 0 and page_number >= end_page_number:
            break

        page_number += 1

    return question_list


@dataclass(init=True)
class QuestionAnswer:
    """Class for question and answer."""

    doctor_profile_link: str = None
    question_type: QuestionType = None
    question_detail_link: str = None
    question_title: str = None
    question_posted_on: str = None
    question_text: str = None
    answer_text: str = None
    followup_list: list[(str, str)] = field(default_factory=list)
    last_updated: datetime = None


def fetch_premium_question_answer_list(
    question_list: list[Question],
) -> list[QuestionAnswer]:
    """Function to fetch premium question answer list."""
    logger = get_logger()

    # make a web request for premium question answer list
    question_answer_list = []
    for question in [
        q for q in question_list if q.question_type == QuestionType.PREMIUM
    ]:
        logger.info(
            f"Starting fetch premium question answers from detail link {question.question_detail_link} for doctor profile {question.doctor_profile_link}",
            domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
            question_detail_link=question.question_detail_link,
        )
        response = _web_request_get(question.question_detail_link)
        if response.status_code != 200:
            logger.error(
                f"Completed fetch premium question answers from detail link {question.question_detail_link} for doctor profile {question.doctor_profile_link}",
                domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
                question_detail_link=question.question_detail_link,
                response_status_code=response.status_code,
            )
            raise Exception(
                f"Error: request failed with response status code: {response.status_code}"
            )
        logger.info(
            f"Completed fetch premium question answers from detail link {question.question_detail_link} for doctor profile {question.doctor_profile_link}",
            domain_url=config.HEALTHCAREMAGIC_DOMAIN_URL,
            question_detail_link=question.question_detail_link,
            response_status_code=response.status_code,
        )

        # parse the web response
        question_answer = QuestionAnswer(
            doctor_profile_link=question.doctor_profile_link,
            question_type=QuestionType.PREMIUM,
            question_detail_link=question.question_detail_link,
            last_updated=datetime.now(),
        )
        soup = BeautifulSoup(response.content, "html.parser")

        # get the title
        h1 = soup.find("h1", class_="subheading text-primary fw500 my-0")
        question_answer.question_title = h1.string

        # get the main question
        wrapper_div = soup.find("div", class_="doctor-quesans")
        main_question_div = wrapper_div.find("div", class_="leftarrow-box")
        question_posted_on = str.strip(
            main_question_div.find("span").string
        ).removeprefix("Posted on ")
        if "days ago" in question_posted_on:
            question_posted_on = str.strip(question_posted_on.removesuffix("days ago"))
            question_answer.question_posted_on = datetime.today() - timedelta(
                days=float(question_posted_on)
            )
        else:
            question_answer.question_posted_on = datetime.strptime(
                question_posted_on,
                "%a, %d %b %Y",
            )
        question_answer.question_text = str.strip(
            main_question_div.find("div", class_="card").text
        )

        # get the main answer
        main_answer_div = wrapper_div.find("div", class_="rightarrow-box")
        if main_answer_div is None:
            main_answer_div = main_question_div
        question_answer.answer_text = str.strip(
            main_answer_div.find("div", class_="card").text
        )

        # get the follow-up question and answer
        followup_div = main_answer_div.find_next_sibling("div")
        while followup_div:
            if followup_div.attrs["class"] == [
                "rightarrow-box"
            ]:  # if a direct answer w/o question
                followup_question_text = ""
                followup_answer_text = str.strip(
                    followup_div.find("div", class_="card").text
                )
                followup_div = followup_div.find_next_sibling("div")

                question_answer.followup_list.append(
                    (followup_question_text, followup_answer_text)
                )
            elif followup_div.attrs["class"] == [
                "leftarrow-box"
            ]:  # if a question followed by an answer
                followup_question_text = str.strip(
                    followup_div.find("div", class_="card").text
                )
                followup_answer_div = followup_div.find_next_sibling(
                    "div", class_="rightarrow-box"
                )
                if followup_answer_div:
                    followup_answer_text = str.strip(
                        followup_answer_div.find("div", class_="card").text
                    )
                    followup_div = followup_answer_div.find_next_sibling("div")
                else:
                    followup_answer_text = ""
                    followup_div = followup_div.find_next_sibling("div")

                question_answer.followup_list.append(
                    (followup_question_text, followup_answer_text)
                )
            else:  # if neither a question nor an answer
                followup_div = None

        question_answer_list.append(question_answer)

        # # TODO: remove
        # break

    return question_answer_list
