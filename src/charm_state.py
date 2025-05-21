# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.
"""Module that handles Pollen charm's state."""

from pydantic import BaseModel, Extra

HTTP_PORT = 8080


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

    def __init__(self, hostname: str) -> None:
        """Construct.

        Args:
            hostname: hostname to build the website property
        """
        self._hostname = hostname

    @property
    def website(self) -> WebsiteModel:
        """The state for this application of the website.

        Returns: a WebsiteDict object to be used by the website relation.
        """
        website_data = {"hostname": format(self._hostname), "port": str(HTTP_PORT)}
        website_model = WebsiteModel(**website_data)
        return website_model.model_dump()

    @classmethod
    def from_charm(cls, charm) -> "CharmState":
        """Initialize a new instance of the CharmState class from the associated charm.

        Args:
            charm: PollenOperator charm.

        Return:
            The CharmState instance created by the provided charm.
        """
        hostname = charm.model.get_binding("website").network.bind_address
        return cls(hostname)
