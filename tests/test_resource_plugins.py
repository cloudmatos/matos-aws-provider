# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from matos_aws_provider.lib import loader, factory
from matos_aws_provider.plugins import get_package
from matos_aws_provider.plugins.cluster import AwsCluster
from matos_aws_provider.plugins.instance import AwsInstance
from matos_aws_provider.plugins.storage import AwsStorage
from matos_aws_provider.plugins.network import AwsNetwork
from matos_aws_provider.plugins.sql import AwsSQL
from matos_aws_provider.plugins.iam import AwsIAM
from matos_aws_provider.plugins.cloudtrail import AwsCloudtrail
from matos_aws_provider.plugins.kms import AwsKms
from matos_aws_provider.plugins.policy import AwsPolicy
from matos_aws_provider.plugins.no_sql import AwsDynamoDB
from matos_aws_provider.plugins.disk import AwsDisk
from matos_aws_provider.plugins.snap_shot import AwsSnapshot
from matos_aws_provider.plugins.eip import AwsEip
from matos_aws_provider.plugins.apphosting import AwsAppHosting
from matos_aws_provider.plugins.lb import AwsLb
from matos_aws_provider.plugins.analyzer import AwsAnalyzer
from matos_aws_provider.plugins.filesystem import AwsFilesystem
from matos_aws_provider.plugins.user_groups import AwsUserGroup
from matos_aws_provider.plugins.sagemaker import AwsSagemaker
from matos_aws_provider.plugins.config_service import AwsConfigBase
from matos_aws_provider.plugins.elasticsearch import AwsElasticsearch
from matos_aws_provider.plugins.guardduty import AwsGuardduty
from matos_aws_provider.plugins.redshift import AwsRedshift
from matos_aws_provider.plugins.functions import AwsLambda
from matos_aws_provider.plugins.s3control import AwsS3Control
from matos_aws_provider.plugins.dax import AwsDax
from matos_aws_provider.plugins.opensearch import AwsOpenSearch
from matos_aws_provider.plugins.cloudfront import AwsCloudFront
from matos_aws_provider.plugins.api_gateway import AwsApiGateway
from matos_aws_provider.plugins.rest_api import AwsRestApi
from matos_aws_provider.plugins.sqs import AwsSQS
from matos_aws_provider.plugins.ssm import AwsSSM
from matos_aws_provider.plugins.sns import AwsSNS
from matos_aws_provider.plugins.docdb import AwsDocdb
from matos_aws_provider.plugins.log_metrics import AwsLogMetric
from matos_aws_provider.plugins.codebuild import AwsCodebuild
from matos_aws_provider.plugins.glue import AwsGlue
from matos_aws_provider.plugins.acm import AwsACM
from matos_aws_provider.plugins.securityhub import AwsSecurityHub
from matos_aws_provider.provider import Provider
from matos_aws_provider.plugins.route53 import AwsRoute53
from matos_aws_provider.plugins.route53domain import AwsRoute53Domain
from matos_aws_provider.plugins.autoscaling import AwsAutoscaling
from matos_aws_provider.plugins.cloudformation import AwsCloudFormation
from matos_aws_provider.plugins.ecs import AwsECS
from matos_aws_provider.plugins.emr import AwsEMR

DUMMY_CRED = {
    "ACCESS_KEY_ID": "",
    "SECRET_ACCESS_KEY": "",
    "DEFAULT_REGION": "us-west-1",
}


class TestResourcePlugin(unittest.TestCase):
    def setUp(self):
        """Set up data test"""
        self.resource_types = {
            "cluster": AwsCluster,
            "instance": AwsInstance,
            "storage": AwsStorage,
            "network": AwsNetwork,
            "sql": AwsSQL,
            "serviceAccount": AwsIAM,
            "trail": AwsCloudtrail,
            "kms": AwsKms,
            "policy": AwsPolicy,
            "no_sql": AwsDynamoDB,
            "disk": AwsDisk,
            "snapshot": AwsSnapshot,
            "eip": AwsEip,
            "apphosting": AwsAppHosting,
            "lb": AwsLb,
            "analyzer": AwsAnalyzer,
            "filesystem": AwsFilesystem,
            "user_groups": AwsUserGroup,
            "sagemaker": AwsSagemaker,
            "config_service": AwsConfigBase,
            "elasticsearch": AwsElasticsearch,
            "guardduty": AwsGuardduty,
            "redshift": AwsRedshift,
            "functions": AwsLambda,
            "s3control": AwsS3Control,
            "dax": AwsDax,
            "opensearch": AwsOpenSearch,
            "cloudfront": AwsCloudFront,
            "apigateway": AwsApiGateway,
            "rest_api": AwsRestApi,
            "sqs": AwsSQS,
            "ssm": AwsSSM,
            "sns": AwsSNS,
            "docdb": AwsDocdb,
            "logs_metrics": AwsLogMetric,
            "codebuild": AwsCodebuild,
            "glue": AwsGlue,
            "acm": AwsACM,
            "securityhub": AwsSecurityHub,
            "route53": AwsRoute53,
            "route53domains": AwsRoute53Domain,
            "autoscaling": AwsAutoscaling,
            "cloudformation": AwsCloudFormation,
            "ecs": AwsECS,
            "emr": AwsEMR,
        }

    def test_get_plugins_pass(self):
        """Test fetch plugin return ok"""
        provider = Provider(credentials=DUMMY_CRED)
        plugin_map = provider.service_factory.fetch_plugins()
        for key, obj_register in self.resource_types.items():
            self.assertEqual(obj_register, plugin_map.get(key))

    def test_fetch_plugins_with_exception(self):
        """Fetch plugins with expect exception"""
        loader.load_plugins(get_package())
        with self.assertRaises(ValueError):
            factory.create({"type": "1234"})


if __name__ == "__main__":
    unittest.main()
