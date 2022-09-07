# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsCloudWorkspaces(BaseProvider):
    """AWS workspaces plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct workspaces service
        """

        super().__init__(**kwargs, client_type="workspaces")
        self.resource = resource

    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        workspaces = []

        def describe_workspaces(workspaces, next_token=None):
            if next_token:
                response = self.conn.describe_workspaces(NextToken=next_token)
            else:
                response = self.conn.describe_workspaces()
            workspaces += [{**item, "type": "workspaces"} for item in response.get("Workspaces", [])]
            if "NextToken" in response:
                describe_workspaces(workspaces, response["NextToken"])

        describe_workspaces(workspaces)
        return workspaces

    def get_resources(self) -> Any:
        """
        Fetches workspaces details.
        """
        resource = {**self.resource}
        resource["WorkspacesConnectionStatus"] = self.describe_workspaces_connection_status(
            self.resource["WorkspaceId"]
        )
        return resource

    def describe_workspaces_connection_status(self, workspace_id):
        """Get topic attributes"""
        response = self.conn.describe_workspaces_connection_status(WorkspaceIds=[workspace_id])
        connection_state = None
        for workspaces_connection in response.get("WorkspacesConnectionStatus"):
            if "ConnectionState" in workspaces_connection:
                connection_state = workspaces_connection.get("ConnectionState")
        return connection_state

def register() -> Any:
    """Register plugin"""
    factory.register("workspaces", AwsCloudWorkspaces)
