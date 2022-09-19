# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsSecretsManager(BaseProvider):
    "AWS SecretsManager plugin"

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct SecretsManager service
        """
        self.resource = resource
        super().__init__(**kwargs, client_type="secretsmanager")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        secrets = []

        def list_secrets(secrets, next_token=None):
            if next_token:
                response = self.conn.list_secrets(NextToken=next_token)
            else:
                response = self.conn.list_secrets()
            secrets += [{**item, "type": "secretsmanager"} for item in response.get("SecretList", [])]
            if "NextToken" in response:
                list_secrets(secrets, response["NextToken"])

        list_secrets(secrets)
        return secrets

    def get_resources(self) -> Any:
        """
        Fetches SecretsManager details
        """
        resource = {**self.resource}

        return resource

def register() -> Any:
    """register class method
    Returns:
        Any: register class
    """
    factory.register("secretsmanager", AwsSecretsManager)
