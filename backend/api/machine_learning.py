""" Module for prediction. """

from dataclasses import dataclass

import numpy as np
import tensorflow as tf
from structlog import get_logger

from . import config


@dataclass(init=True)
class State:
    """Class for storing state."""

    SYMPTOMS_TOKENISER = None
    CAUSES_TOKENISER = None
    MODEL = None


def configure() -> None:
    """Configure machine learning tokenisers and model."""
    with open(file=config.SYMPTOMS_TOKENISER_FILE, mode="r", encoding="utf-8") as file:
        State.SYMPTOMS_TOKENISER = tf.keras.preprocessing.text.tokenizer_from_json(
            file.read()
        )
    with open(file=config.CAUSES_TOKENISER_FILE, mode="r", encoding="utf-8") as file:
        State.CAUSES_TOKENISER = tf.keras.preprocessing.text.tokenizer_from_json(
            file.read()
        )
    State.MODEL = tf.keras.models.load_model(config.MODEL_FILE)


def predict_provisional_diagnosis(
    subjective_symptoms, associated_symptoms, investigations_done, gender, age
) -> list[(str, float)]:
    """Predict provisional diagnosis from symptoms."""
    logger = get_logger()
    logger.info(
        "Starting predict provisional diagnosis",
        subjective_symptoms=subjective_symptoms,
    )
    logger.debug(
        "",
        associated_symptoms=associated_symptoms,
        investigations_done=investigations_done,
        gender=gender,
        age=age,
    )

    # prepare symptoms corpus
    symptoms_corpus = (
        subjective_symptoms
        + config.SYMPTOMS_SEPARATOR
        + associated_symptoms
        + config.SYMPTOMS_SEPARATOR
        + investigations_done
        + config.SYMPTOMS_SEPARATOR
        + gender
        + config.SYMPTOMS_SEPARATOR
        + age
    )
    symptoms_corpus = symptoms_corpus.split(config.SYMPTOMS_SEPARATOR)
    symptoms_corpus = [str(item).strip().lower() for item in symptoms_corpus]
    symptoms_corpus = f"{config.SYMPTOMS_SEPARATOR}".join(symptoms_corpus)

    # validate arguments
    for item in symptoms_corpus.split(config.SYMPTOMS_SEPARATOR):
        if not item in list(State.SYMPTOMS_TOKENISER.word_index.keys()):
            message = f"Error: invalid or unknown symptom - {item}"
            logger.error("Completed predict provisional diagnosis", message=message)
            raise Exception(message)

    symptoms_sequences = State.SYMPTOMS_TOKENISER.texts_to_sequences([symptoms_corpus])
    symptoms_padded = tf.keras.preprocessing.sequence.pad_sequences(
        symptoms_sequences,
        padding=config.SYMPTOMS_SEQUENCE_PADDING_TYPE,
        maxlen=config.SYMPTOMS_SEQUENCE_MAXLEN,
    )
    symptoms_padded = np.array(symptoms_padded)

    causes_probabilities = State.MODEL.predict(symptoms_padded)[0]
    causes_rankings = np.argsort(causes_probabilities).tolist()
    response = [
        # first most probable
        (
            round(causes_probabilities[causes_rankings[-1]] * 100, 2),
            State.CAUSES_TOKENISER.index_word[causes_rankings[-1] + 1],
        ),
        # second most probable
        (
            round(causes_probabilities[causes_rankings[-2]] * 100, 2),
            State.CAUSES_TOKENISER.index_word[causes_rankings[-2] + 1],
        ),
        # third most probable
        (
            round(causes_probabilities[causes_rankings[-3]] * 100, 2),
            State.CAUSES_TOKENISER.index_word[causes_rankings[-3] + 1],
        ),
    ]
    logger.info(
        "Completed predict provisional diagnosis",
        subjective_symptom=subjective_symptoms,
    )

    return response
