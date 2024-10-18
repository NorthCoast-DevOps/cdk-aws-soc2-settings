from aws_cdk import (
    Stack,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

class AwsSoc2SettingsStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(self, 
            "Soc2SettingsBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY
        )
