# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.
"""Module that handles Pollen charm's state."""

from pathlib import Path

from pydantic import BaseModel, Extra

HTTP_PORT = "443"


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
        self.rng_tools_file = None

    @property
    def website(self) -> WebsiteModel:
        """The state for this application of the website.

        Returns: a WebsiteDict object to be used by the website relation.
        """
        website_data = {"hostname": format(self._hostname), "port": HTTP_PORT}
        website_model = WebsiteModel(**website_data)
        return website_model

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

    def check_rng_file(self):
        """Check if the rng-tools-debian file needs modification."""
        file = Path("/etc/default/rng-tools-debian")
        # The file already has this line commented by default,
        # so we should check if it appears in the file twice (commented and actually written).
        # The file needs the commented code header so the rngd service does not fail.
        self.rng_tools_file = (
            None
            if not file.exists()
            or 2
            > file.read_text(encoding="utf-8").count(
                'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
            )
            else 'RNGDOPTIONS="--fill-watermark=90% --feed-interval=1"'
        )
        if not self.rng_tools_file:
            file.write_text(f"\n{self.rng_tools_file}", encoding="utf-8")
