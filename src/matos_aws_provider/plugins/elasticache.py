# -*- coding: utf-8 -*-
from typing import Any, Dict
import logging
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class AwsElastiCache(BaseProvider):
    "AWS elasticache plugin"

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct elasticache service
        """
        self.functions = resource
        super().__init__(**kwargs, client_type="elasticache")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """

        nodes = []

        def describe_reserved_cache_nodes(nodes, marker=None):
            if marker:
                response = self.conn.describe_reserved_cache_nodes(Marker=marker)
            else:
                response = self.conn.describe_reserved_cache_nodes()
            nodes += [{**item, "type": "elasticache"} for item in response.get("ReservedCacheNodes", [])]
            if "Marker" in response:
                describe_reserved_cache_nodes(nodes, response["Marker"])

        describe_reserved_cache_nodes(nodes)
        return nodes

    def get_resources(self) -> Any:
        """
        Fetches elasticache details

        """
        resource = {**self.resource}

        return resource

def register() -> Any:
    """register class method

    Returns:
        Any: register class
    """
    factory.register("elasticache", AwsElastiCache)
