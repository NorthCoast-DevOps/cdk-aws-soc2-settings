"""
This module defines the MainStack, which is the primary stack for the SOC 2 compliance setup.
It's named "SOC2Settings" and orchestrates the creation of all other stacks by instantiating 
them as nested stacks. This approach allows for a modular and organized infrastructure 
definition while deploying everything as a single unit.
"""

from aws_cdk import Stack
from constructs import Construct
from .iam_stack import IAMStack
from .logging_stack import LoggingStack
from .encryption_stack import EncryptionStack
from .network_stack import NetworkStack
from .backup_stack import BackupStack
from .security_stack import SecurityStack
from .vulnerability_asset_stack import VulnerabilityAssetStack
from .network_security_stack import NetworkSecurityStack

class MainStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        iam_stack = IAMStack(self, "SOC2IAMStack")
        logging_stack = LoggingStack(self, "SOC2LoggingStack")
        encryption_stack = EncryptionStack(self, "SOC2EncryptionStack")
        network_stack = NetworkStack(self, "SOC2NetworkStack")
        backup_stack = BackupStack(self, "SOC2BackupStack")
        security_stack = SecurityStack(self, "SOC2SecurityStack")
        vulnerability_asset_stack = VulnerabilityAssetStack(self, "SOC2VulnerabilityAssetStack")
        
        # Pass the VPC from NetworkStack to NetworkSecurityStack
        network_security_stack = NetworkSecurityStack(self, "SOC2NetworkSecurityStack", vpc=network_stack.vpc)
