"""
This module defines the EncryptionStack, which sets up encryption resources for SOC 2 compliance.
It creates two KMS keys: one for general use and another specifically for S3 encryption.
These keys enable data encryption at rest, which is a crucial aspect of data protection
and confidentiality in SOC 2 compliance.
"""

from aws_cdk import Stack, aws_kms as kms
from constructs import Construct

class EncryptionStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a KMS key for general use
        self.general_key = kms.Key(self, "GeneralEncryptionKey",
            enable_key_rotation=True,
            description="General purpose encryption key for SOC 2 compliance"
        )

        # Create a KMS key for S3 encryption
        self.s3_key = kms.Key(self, "S3EncryptionKey",
            enable_key_rotation=True,
            description="S3 bucket encryption key for SOC 2 compliance"
        )
