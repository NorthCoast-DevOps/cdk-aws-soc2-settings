"""
This module defines the LoggingStack, which sets up logging and monitoring resources
for SOC 2 compliance. It creates a CloudTrail trail for API activity logging and
a CloudWatch log group for application logs. These resources help maintain an audit
trail of actions taken within the AWS environment and provide a centralized location
for log storage and analysis.
"""

from aws_cdk import Stack, aws_logs as logs, aws_cloudtrail as cloudtrail, aws_s3 as s3
from constructs import Construct

class LoggingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a secure S3 bucket for CloudTrail logs
        trail_bucket = s3.Bucket(self, "CloudTrailBucket",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True
        )

        # Create a CloudTrail trail
        cloudtrail.Trail(self, "CloudTrail",
            bucket=trail_bucket,
            is_multi_region_trail=True,
            include_global_service_events=True
        )

        # Create a CloudWatch log group for application logs
        logs.LogGroup(self, "ApplicationLogGroup",
            retention=logs.RetentionDays.ONE_YEAR
        )
