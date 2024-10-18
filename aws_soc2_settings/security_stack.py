"""
This module defines the SecurityStack, which sets up security monitoring resources for SOC 2 compliance.
It enables AWS GuardDuty for threat detection and AWS Security Hub for security posture management.
These services help maintain ongoing security monitoring and alerting, which are crucial for
meeting the security criteria of SOC 2 compliance.
"""

from aws_cdk import Stack, aws_guardduty as guardduty, aws_securityhub as securityhub, aws_config as config
from constructs import Construct

class SecurityStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Enable AWS Config
        config.CfnConfigurationRecorder(self, "ConfigRecorder",
            role_arn=f"arn:aws:iam::{self.account}:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig",
            recording_group=config.CfnConfigurationRecorder.RecordingGroupProperty(
                all_supported=True,
                include_global_resource_types=True
            )
        )

        # Enable GuardDuty
        guardduty.CfnDetector(self, "GuardDutyDetector",
            enable=True
        )

        # Enable Security Hub
        securityhub.CfnHub(self, "SecurityHub")
