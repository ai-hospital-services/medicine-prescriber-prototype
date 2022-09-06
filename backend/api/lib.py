"""  Module for library functions. """

import argparse
import json
import logging
from dataclasses import dataclass

import structlog
from structlog import get_logger

from . import config


@dataclass(init=True)
class CLIArgs:
    """Class for command line interface (cli) arguments."""

    debug_mode: bool = None
    port: int = None


def parse_cli_args() -> CLIArgs:
    """Parse cli arguments."""
    logger = get_logger()

    logger.info("Starting parse cli arguments")
    parser = argparse.ArgumentParser(description="CLI arguments")
    parser.add_argument("--debug-mode", help="Enable debug mode logging")
    parser.add_argument("--port", help="Port number to run on")
    args = parser.parse_args()
    debug_mode = json.loads(args.debug_mode) if args.debug_mode else config.DEBUG_MODE
    port = args.port if args.port else config.PORT
    result = CLIArgs(debug_mode=debug_mode, port=port)
    logger.info("Completed parse cli arguments")

    return result


def configure_global_logging_level() -> None:
    """Configure global logging level."""
    logger = get_logger()

    logger.info("Starting configure global logging level")
    structlog.configure_once(
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if config.DEBUG_MODE else logging.INFO
        )
    )
    if config.DEBUG_MODE:
        logger.debug("Global logging level is set as DEBUG")
    else:
        logger.info("Global logging level is set as INFO")
    logger.info("Completed configure global logging level")


def log_config_settings() -> None:
    """Log configuration settings in debug mode."""
    logger = get_logger()

    logger.info("Starting log config settings in DEBUG mode")
    logger.debug("", DEBUG_MODE=config.DEBUG_MODE)
    logger.debug("", PORT=config.PORT)
    logger.debug(
        "",
        SYMPTOMS_TOKENISER_FILE=config.SYMPTOMS_TOKENISER_FILE,
    )
    logger.debug("", CAUSES_TOKENISER_FILE=config.CAUSES_TOKENISER_FILE)
    logger.debug("", MODEL_FILE=config.MODEL_FILE)
    logger.debug("", WEB_REQUEST_TIMEOUT=config.WEB_REQUEST_TIMEOUT)
    logger.debug("", CACHE_TIMEOUT=config.CACHE_TIMEOUT)
    logger.debug("", TENANT_DOMAIN=config.TENANT_DOMAIN)
    logger.debug(
        "",
        TENANT_OPENID_CONFIGURATION_CACHE_KEY=config.TENANT_OPENID_CONFIGURATION_CACHE_KEY,
    )
    logger.debug("", AUTHORISATION_HEADER_KEY=config.AUTHORISATION_HEADER_KEY)
    logger.debug("", REDIRECT_URL=config.REDIRECT_URL)
    logger.debug("", CLIENT_ID=config.CLIENT_ID)
    logger.debug("", CLIENT_SECRET=config.CLIENT_SECRET)
    logger.info("Completed log config settings in DEBUG mode")
