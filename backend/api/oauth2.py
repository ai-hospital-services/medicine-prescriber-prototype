""" Module for OAuth2. """

from dataclasses import dataclass
import json

import requests
from cache3 import SafeCache
from jwcrypto import jwk, jwt
from oauthlib import oauth2
from structlog import get_logger

from . import config


@dataclass(init=True)
class State:
    """Class for storing state."""

    CACHE = None
    TOKEN_URL = None
    JWKS = None


def init_cache_state() -> None:
    """Initialise cache and state."""
    logger = get_logger()

    logger.info("Starting init cache and state")

    if State.CACHE is not None:
        State.CACHE.clear()

    State.CACHE = SafeCache()
    State.CACHE.timeout = config.CACHE_TIMEOUT

    response = requests.get(
        f"https://{config.TENANT_DOMAIN}/.well-known/openid-configuration",
        timeout=config.WEB_REQUEST_TIMEOUT,
    )
    State.CACHE.set(
        key=config.TENANT_OPENID_CONFIGURATION_CACHE_KEY, value=response.json()
    )
    State.TOKEN_URL = State.CACHE.get(config.TENANT_OPENID_CONFIGURATION_CACHE_KEY)[
        "token_endpoint"
    ]
    response = requests.get(
        State.CACHE.get(config.TENANT_OPENID_CONFIGURATION_CACHE_KEY)["jwks_uri"],
        timeout=config.WEB_REQUEST_TIMEOUT,
    )
    State.JWKS = jwk.JWKSet.from_json(keyset=response.content)

    logger.debug(
        "Initialised cache and state with tenant configuration",
        TENANT_OPENID_CONFIGURATION=State.CACHE.get(
            config.TENANT_OPENID_CONFIGURATION_CACHE_KEY
        ),
        TOKEN_URL=State.TOKEN_URL,
        JWKS=State.JWKS,
    )

    logger.info("Completed init cache and state")


def check_cache() -> None:
    """Check cache for expiration and initialise if yes."""
    logger = get_logger()

    logger.info("Starting check cache")
    if not State.CACHE.has_key(config.TENANT_OPENID_CONFIGURATION_CACHE_KEY):
        init_cache_state()
    logger.info("Completed check cache")


def get_access_token(authorisation_code) -> str:
    """Get access token using authorisation code."""
    logger = get_logger()
    logger.info("Starting get access token")

    if authorisation_code is None or authorisation_code.strip() == "":
        logger.error("Empty authorisation_code", authorisation_code=authorisation_code)
        return None

    check_cache()

    client = oauth2.WebApplicationClient(
        client_id=config.CLIENT_ID, code=authorisation_code
    )
    request = client.prepare_token_request(
        token_url=State.TOKEN_URL,
        redirect_url=config.REDIRECT_URL,
        client_secret=config.CLIENT_SECRET,
    )
    response = requests.post(
        url=request[0],
        headers=request[1],
        data=request[2],
        timeout=config.WEB_REQUEST_TIMEOUT,
    )
    logger.info("Completed get access token")

    return response.text


def validate_access_token(token, asserted_claims) -> bool:
    """Validate access token and verify claims."""
    logger = get_logger()
    logger.info("Starting validate access token")

    if (
        token is None
        or asserted_claims is None
        or token.strip() == ""
        or asserted_claims.strip() == ""
    ):
        logger.error(
            "Empty token or asserted claims",
            token=token,
            asserted_claims=asserted_claims,
        )
        return False

    check_cache()

    jwtoken = jwt.JWT()
    try:
        jwtoken.deserialize(jwt=token)
    except Exception as exception:  # pylint: disable=broad-except
        logger.error("Error deserialising access token", exception=str(exception))
        return False

    try:
        jwtoken.validate(key=State.JWKS)
    except Exception as exception:  # pylint: disable=broad-except
        logger.error("Error validating access token", exception=str(exception))
        return False

    try:
        claims = json.loads(jwtoken.claims)
        scope = claims["scope"]
    except Exception as exception:  # pylint: disable=broad-except
        logger.error(
            "Error validating claims from access token",
            exception=str(exception),
            claims=jwtoken.claims,
            asserted_claims=asserted_claims,
        )
        return False

    logger.info("Completed validate access token")

    return asserted_claims in scope
