# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsGlacier(BaseProvider):
    """AWS Glacier plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct Glacier service
        """

        super().__init__(**kwargs, client_type="glacier")
        self.resource = resource

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        vaults = []

        def describe_vaults(vaults, next_token=None):
            if next_token:
                response = self.conn.list_vaults(NextToken=next_token)
            else:
                response = self.conn.list_vaults()
            vaults += [{**item, "type": "glacier"} for item in response.get("VaultList", [])]
            if "NextToken" in response:
                describe_vaults(vaults, response["NextToken"])

        describe_vaults(vaults)
        return vaults

    def get_resources(self) -> Any:
        """
        Fetches vaults details.
        """
        resource = {**self.resource}
        resource["VaultsAccessPolicy"] = self.conn.get_vault_access_policy(vaultName= self.resource["VaultName"])
        return resource

def register() -> Any:
    """Register plugin"""
    factory.register("glacier", AwsGlacier)