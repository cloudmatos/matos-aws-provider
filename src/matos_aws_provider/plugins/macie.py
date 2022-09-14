# -*- coding: utf-8 -*-
from typing import Any
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsMacie(BaseProvider):
    """Aws macie class

    Args:
        BaseProvider (Class): Base provider class
    """
    def __init__(self, resource, **kwargs) -> None:
        """
        Construct macie service
        """

        self.resource = resource
        super().__init__(**kwargs, client_type="macie2")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        return [{"type": "macie"}]

    def get_resources(self):
        """
        Fetches macie details.
        """
        resource = {**self.resource}
        resource['Macie'] = self.conn.get_macie_session()
        return resource


def register() -> Any:
    """Register plugin"""
    factory.register("macie", AwsMacie)