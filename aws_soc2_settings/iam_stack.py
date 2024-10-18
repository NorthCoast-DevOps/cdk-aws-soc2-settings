"""
This module defines the IAMStack, which sets up Identity and Access Management (IAM) resources
for SOC 2 compliance. It creates an admin group with full access, an EC2 instance role with
SSM access, and establishes a strong password policy. These resources help enforce the principle
of least privilege and ensure secure access management within the AWS environment.
"""

from aws_cdk import Stack, aws_iam as iam, CfnResource
from constructs import Construct

class IAMStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an IAM group for administrators and attach AdministratorAccess policy
        admin_group = iam.Group(self, "AdminGroup")
        admin_group.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        )

        # Create a role for EC2 instances with SSM access
        iam.Role(self, "EC2Role",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")]
        )

        # Set the account password policy using CfnResource
        CfnResource(self, "AccountPasswordPolicy",
            type="AWS::IAM::AccountPasswordPolicy",
            properties={
                "PasswordPolicy": {
                    "MinimumPasswordLength": 14,
                    "RequireLowercaseCharacters": True,
                    "RequireNumbers": True,
                    "RequireUppercaseCharacters": True,
                    "RequireSymbols": True,
                    "AllowUsersToChangePassword": True,
                    "MaxPasswordAge": 90,
                    "PasswordReusePrevention": 24,
                }
            }
        )
