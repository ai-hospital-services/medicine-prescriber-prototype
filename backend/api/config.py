""" Module for configuration settings. """

DEBUG_MODE = False

# flask
PORT = 8080

# machine learning
MODEL_FILE = "api/data/model.h5"
SYMPTOMS_TOKENISER_FILE = "api/data/symptoms_tokeniser.json"
CAUSES_TOKENISER_FILE = "api/data/causes_tokeniser.json"
SYMPTOMS_SEPARATOR = "|"
SYMPTOMS_SEQUENCE_PADDING_TYPE = "pre"
SYMPTOMS_SEQUENCE_MAXLEN = 25

# mongodb
MONGODB_URL = "mongodb://localhost:27017/"
MONGODB_DATABASE = "ai_hospital_services"

# oauth2
WEB_REQUEST_TIMEOUT_SECONDS = 15
CACHE_TIMEOUT_SECONDS = 600
TENANT_DOMAIN = "<TENANT DOMAIN>"
TENANT_OPENID_CONFIGURATION_CACHE_KEY = "TENANT_OPENID_CONFIGURATION"
AUTHORISATION_HEADER_KEY = "Authorization"
REDIRECT_URL = "http://localhost:9090/auth.html"
CLIENT_ID = "<CLIENT ID>"
CLIENT_SECRET = "<CLIENT SECRET>"
