"""
This module defines the NetworkStack, which sets up network resources for SOC 2 compliance.
It creates a VPC with public and private subnets, and a security group for web servers.
These resources help establish network segmentation and access controls, which are
important aspects of the security and availability criteria in SOC 2 compliance.
"""

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC with public and private subnets
        self.vpc = ec2.Vpc(self, "VPC",
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24),
                ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24)
            ]
        )

        # Create a security group for web servers
        self.web_sg = ec2.SecurityGroup(self, "WebServerSG",
            vpc=self.vpc,
            description="Security group for web servers",
            allow_all_outbound=True
        )
        self.web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP traffic")
        self.web_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "Allow HTTPS traffic")
