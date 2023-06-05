# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

from typing import TypedDict

from pydantic import BaseModel, Extra, Field, IPvAnyAddress


class WebsiteDict(TypedDict):
    """
    Attrs:
        hostname: Website hostname.
        port: Website port.
    """
    hostname: str
    port: int


class WebsiteModel(BaseModel, extra=Extra.forbid):
    """
    Attrs:
        hostname: Website hostname.
        port: Website port.
    """

    hostname: IPvAnyAddress
    port: int = Field(int)


class CharmState:
    """
    Attrs:
        website: Website to pass over the website relation
    """

    @property
    def website(self, hostname) -> WebsiteDict:
        """The state for this application of the website.

        Returns: a WebsiteDict object to be used by the website relation.
        """
        website_data = {"hostname": hostname, "port": 443}
        website_model = WebsiteModel(**website_data)
        return website_model
