# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from matos_aws_provider.provider import Provider

DUMMY_CRED = {
    "ACCESS_KEY_ID": "",
    "SECRET_ACCESS_KEY": "",
    "DEFAULT_REGION": "us-west-1",
}


class TestDiscoveryPlugin(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.service_type_map = {
            "cluster": "eks",
            "instance": "ec2",
            "trail": "cloudtrail",
            "storage": "s3",
            "snapshot": "iam",
            "network": "ec2",
            "kms": "kms",
            "eip": "ec2",
            "serviceAccount": "iam",
            "sql": "rds",
            "no_sql": "dynamodb",
            "lb": "elb",
            "filesystem": "efs",
            "apphosting": "elasticbeanstalk",
            "analyzer": "accessanalyzer",
            "policy": "iam",
            "user_groups": "iam",
            "sagemaker": "sagemaker",
            "config_service": "config",
            "elasticsearch": "es",
            "guardduty": "guardduty",
            "redshift": "redshift",
            "functions": "lambda",
            "s3control": "sts",
            "dax": "dax",
            "opensearch": "opensearch",
            "cloudfront": "cloudfront",
            "apigateway": "apigatewayv2",
            "rest_api": "apigateway",
            "sqs": "sqs",
            "ssm": "ssm",
            "sns": "sns",
            "docdb": "docdb",
            "logs_metrics": "logs",
            "codebuild": "codebuild",
            "glue": None,
            "acm": "acm",
            "securityhub": "securityhub",
        }

    def test_check_plugins_type_pass(self):
        """Test check plugins type return ok"""
        provider = Provider(credentials=DUMMY_CRED)
        for key_type, client_type in self.service_type_map.items():
            discovery_service = provider.service_factory.create(
                {"type": key_type, "credentials": DUMMY_CRED}
            )
            self.assertEqual(discovery_service.client_type, client_type)


if __name__ == "__main__":
    unittest.main()
