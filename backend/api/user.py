""" Module for user. """

from dataclasses import dataclass
from datetime import datetime


@dataclass(init=True)
class UserInfo:
    """Class for storing user info from social media login."""

    email_address: str
    name: str
    login_sub: str
    picture_url: str
