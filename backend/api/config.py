""" Module for configuration settings. """

DEBUG_MODE = False

# flask
PORT = 80

# machine learning
MODEL_FILE = "api/data/model.h5"
SYMPTOMS_TOKENISER_FILE = "api/data/symptoms_tokeniser.json"
CAUSES_TOKENISER_FILE = "api/data/causes_tokeniser.json"
SYMPTOMS_SEPARATOR = ";"
SYMPTOMS_SEQUENCE_PADDING_TYPE = "pre"
SYMPTOMS_SEQUENCE_MAXLEN = 9

# mongodb
MONGODB_URL = "mongodb://localhost:27017/"
