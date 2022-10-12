# -*- coding: utf-8 -*-
from typing import Any, Dict
from matos_aws_provider.lib import factory
from matos_aws_provider.lib.base_provider import BaseProvider


class AwsCloudWAF(BaseProvider):
    """AWS waf plugin"""

    def __init__(self, resource: Dict, **kwargs) -> None:
        """
        Construct waf service
        """

        super().__init__(**kwargs, client_type=None)
        self.resource = resource
        self.waf = self.client('waf')
        self.wafv2 = self.client('wafv2')
        self.waf_regional = self.client('waf-regional')


    def get_inventory(self) -> Any:
        """
        Service discovery
        """
        return [{"type": "waf"}]

    def get_resources(self) -> Any:
        """
        Fetches waf details.
        """
        resource = {**self.resource}
        resource["WAF"] = self.waf_list_rules()
        for rule in resource["WAF"]:
            if "RuleId" in rule:
                rule["Rules"] = self.waf.get_rule(
                    RuleId=rule["RuleId"]
                )
        resource["WAFV2WEBACLs"] = self.wafv2_list_web_acls()
        for webacl in resource["WAFV2WEBACLs"]:
            if "Id" in webacl:
                webacl[
                    "WebACLs"
                ] = self.wafv2.get_web_acl(Name=webacl["Name"], Scope='REGIONAL', Id=webacl["Id"])

        resource["WAFV2RuleGroups"] = self.wafv2_list_rule_groups()
        for rulegroup in resource["WAFV2RuleGroups"]:
            if "Id" in rulegroup:
                rulegroup[
                    "RuleGroups"
                ] = self.wafv2.get_rule_group(Name=rulegroup["Name"], Scope='REGIONAL', Id=rulegroup["Id"])

        resource["WAFREGIONALWebACLs"] = self.waf_regional_list_web_acls()
        for webacl in resource["WAFREGIONALWebACLs"]:
            if "WebACLId" in webacl:
                webacl[
                    "WebACLs"
                ] = self.waf_regional.get_web_acl(WebACLId=webacl["WebACLId"])

        resource["WAFRegionalRules"] = self.wafregional_list_rule()
        for rule in resource["WAFRegionalRules"]:
            if "RuleId" in rule:
                rule[
                    "Rules"
                ] = self.waf_regional.get_rule(RuleId=rule["RuleId"])
        return resource

    def waf_list_rules(self):
        """List waf rule"""
        waf_rule = []

        def list_rules(next_marker, waf_rule):
            resp = self.waf.list_rules(NextMarker=next_marker)
            waf_rule += resp.get("Rules", [])
            if resp.get("NextMarker"):
                list_rules(resp.get("NextMarker"), waf_rule)

        resp = self.waf.list_rules()
        waf_rule += resp.get("Rules", [])
        if resp.get("NextMarker"):
            list_rules(resp.get("NextMarker"), waf_rule)
        return waf_rule

    def wafv2_list_web_acls(self):
        """List wafv2 web acl"""
        wafv2_acl = []

        def list_web_acls(next_marker, wafv2_acl):
            resp = self.wafv2.list_web_acls(Scope='REGIONAL', NextMarker=next_marker)
            wafv2_acl += resp.get("WebACLs", [])
            if resp.get("NextMarker"):
                list_web_acls(resp.get("NextMarker"), wafv2_acl)

        resp = self.wafv2.list_web_acls(Scope='REGIONAL')
        wafv2_acl += resp.get("WebACLs", [])
        if resp.get("NextMarker"):
            list_web_acls(resp.get("NextMarker"), wafv2_acl)
        return wafv2_acl

    def wafv2_list_rule_groups(self):
        """List wafv2 rule groups"""
        wafv2_rulegroup = []

        def list_rule_groups(next_marker, wafv2_rulegroup):
            resp = self.wafv2.list_rule_groups(Scope='REGIONAL', NextMarker=next_marker)
            wafv2_rulegroup += resp.get("RuleGroups", [])
            if resp.get("NextMarker"):
                list_rule_groups(resp.get("NextMarker"), wafv2_rulegroup)

        resp = self.wafv2.list_rule_groups(Scope='REGIONAL')
        wafv2_rulegroup += resp.get("RuleGroups", [])
        if resp.get("NextMarker"):
            list_rule_groups(resp.get("NextMarker"), wafv2_rulegroup)
        return wafv2_rulegroup

    def waf_regional_list_web_acls(self):
        """List waf reginal web acl"""
        wafregional_acl = []

        def list_web_acls(next_marker, wafregional_acl):
            resp = self.waf_regional.list_web_acls(NextMarker=next_marker)
            wafregional_acl += resp.get("WebACLs", [])
            if resp.get("NextMarker"):
                list_web_acls(resp.get("NextMarker"), wafregional_acl)

        resp = self.waf_regional.list_web_acls()
        wafregional_acl += resp.get("WebACLs", [])
        if resp.get("NextMarker"):
            list_web_acls(resp.get("NextMarker"), wafregional_acl)
        return wafregional_acl

    def wafregional_list_rule(self):
        """List waf regional rule"""
        wafregional_rules = []

        def list_rules(next_marker, wafregional_rules):
            resp = self.waf_regional.list_rules(NextMarker=next_marker)
            wafregional_rules += resp.get("Rules", [])
            if resp.get("NextMarker"):
                list_rules(resp.get("NextMarker"), wafregional_rules)

        resp = self.waf_regional.list_rules()
        wafregional_rules += resp.get("Rules", [])
        if resp.get("NextMarker"):
            list_rules(resp.get("NextMarker"), wafregional_rules)
        return wafregional_rules

def register() -> Any:
    """Register plugin"""
    factory.register("waf", AwsCloudWAF)
