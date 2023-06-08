# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
"""Module that handles Pollen charm's state."""

from typing import TypedDict

from pydantic import BaseModel, Extra


class WebsiteDict(TypedDict):
    """Custom dict for the website property.

    Attrs:
        hostname: Website hostname.
        port: Website port.
    """

    hostname: str
    port: str


class WebsiteModel(BaseModel, extra=Extra.forbid):
    """Pydantic validation model for the website property.

    Attrs:
        hostname: Website hostname.
        port: Website port.
    """

    hostname: str
    port: str


class CharmState:
    """Class that represents the state of the Pollen charm.

    Attrs:
        website: Website to pass over the website relation
    """

    def __init__(self, hostname: str | None) -> None:
        """Construct.

        Args:
            hostname: hostname to build the website property
        """
        self._hostname = hostname

    @property
    def website(self) -> WebsiteDict:
        """The state for this application of the website.

        Returns: a WebsiteDict object to be used by the website relation.
        """
        website_data = {"hostname": format(self._hostname), "port": "443"}
        website_model = WebsiteModel(**website_data)
        return website_model

    @classmethod
    def from_charm(cls, hostname) -> "CharmState":
        """Initialize a new instance of the CharmState class from the associated charm.

        Args:
            hostname: the hostname to be used by the website property.

        Return:
            The CharmState instance created by the provided charm.
        """
        return cls(hostname=hostname)
