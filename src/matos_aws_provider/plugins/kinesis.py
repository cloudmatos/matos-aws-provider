# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsKinesis(BaseProvider):
    """Aws Kinesis plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct Kinesis service
        """

        super().__init__(**kwargs, client_type="kinesis")
        self.resource = resource
        self.kms = self.client("kms")

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        return [{"type": "kinesis"}]

    def get_resources(self) -> Any:
        """Get resource"""
        resource = {**self.resource}
        resource["DataStreams"] = self.get_streams()

        details_arr = []
        for stream in resource["DataStreams"]:
            details_arr.append(self.get_stream_details(stream))

        resource["DataStreams"] = details_arr
        return resource

    def get_streams(self):
        """Get all streams"""
        response = self.conn.list_streams()
        return response.get("StreamNames", [])

    def get_stream_details(self, stream_name):
        """Get key details"""
        # response = self.conn.describe_stream()
        return self.conn.describe_stream(StreamName=stream_name)

def register() -> Any:
    """Register plugin"""
    factory.register("kinesis", AwsKinesis)
