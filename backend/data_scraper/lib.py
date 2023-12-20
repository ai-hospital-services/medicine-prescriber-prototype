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
    doctor_profile_link: str = None


def parse_cli_args() -> CLIArgs:
    """Parse cli arguments."""
    logger = get_logger()

    logger.info("Starting parse cli arguments")
    parser = argparse.ArgumentParser(description="CLI arguments")
    parser.add_argument("--debug-mode", help="Enable debug mode logging")
    parser.add_argument("--doctor-profile-link", help="Doctor profile link")
    args = parser.parse_args()
    debug_mode = json.loads(args.debug_mode) if args.debug_mode else config.DEBUG_MODE
    doctor_profile_link = args.doctor_profile_link
    result = CLIArgs(debug_mode=debug_mode, doctor_profile_link=doctor_profile_link)
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
    for configuration in [attr for attr in dir(config) if not attr.startswith("__")]:
        logger.debug(configuration, value=config.__dict__[configuration])
    logger.info("Completed log config settings in DEBUG mode")
