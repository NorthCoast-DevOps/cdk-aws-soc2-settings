"""
This module defines the NetworkSecurityStack, which sets up advanced network security
resources for SOC 2 compliance. It enables AWS WAF for web application protection,
AWS Shield for DDoS protection, and AWS Network Firewall for network traffic filtering.
It also sets up an event-driven system to automatically apply WAF to new ALBs and API Gateways.
"""

from aws_cdk import (
    Stack, aws_wafv2 as wafv2, aws_shield as shield,
    aws_networkfirewall as networkfirewall, aws_ec2 as ec2,
    aws_lambda as lambda_, aws_iam as iam, aws_events as events,
    aws_events_targets as targets, CfnOutput
)
from constructs import Construct

class NetworkSecurityStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create WAF Web ACL
        web_acl = wafv2.CfnWebACL(self, "WAFWebACL",
            default_action={"allow": {}},
            scope="REGIONAL",
            visibility_config={
                "cloudWatchMetricsEnabled": True,
                "metricName": "WAFWebACL",
                "sampledRequestsEnabled": True
            },
            rules=[
                {
                    "name": "AWSManagedRulesCommonRuleSet",
                    "priority": 1,
                    "statement": {
                        "managedRuleGroupStatement": {
                            "vendorName": "AWS",
                            "name": "AWSManagedRulesCommonRuleSet"
                        }
                    },
                    "overrideAction": {"none": {}},
                    "visibilityConfig": {
                        "sampledRequestsEnabled": True,
                        "cloudWatchMetricsEnabled": True,
                        "metricName": "AWSManagedRulesCommonRuleSet"
                    }
                }
            ]
        )

        # Enable AWS Shield Advanced
        shield.CfnProtection(self, "ShieldProtection",
            name="ShieldProtection",
            resource_arn=f"arn:aws:elasticloadbalancing:{self.region}:{self.account}:loadbalancer/*"
        )

        # Create Network Firewall
        firewall = networkfirewall.CfnFirewall(self, "NetworkFirewall",
            firewall_name="SOC2NetworkFirewall",
            firewall_policy_arn=self.create_firewall_policy().attr_firewall_policy_arn,
            vpc_id=vpc.vpc_id,
            subnet_mappings=[{"subnetId": subnet.subnet_id} for subnet in vpc.public_subnets]
        )

        # Create Lambda function to associate WAF with new resources
        auto_associate_waf_lambda = lambda_.Function(self, "AutoAssociateWAFLambda",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="auto_associate_waf_lambda.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "WEB_ACL_ARN": web_acl.attr_arn
            }
        )

        # Grant necessary permissions to the Lambda function
        auto_associate_waf_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=[
                "elasticloadbalancing:DescribeLoadBalancers",
                "apigateway:GET",
                "wafv2:AssociateWebACL",
                "wafv2:DisassociateWebACL"
            ],
            resources=["*"]
        ))

        # Create EventBridge rule for ALB creation
        events.Rule(self, "ALBCreationRule",
            event_pattern=events.EventPattern(
                source=["aws.elasticloadbalancing"],
                detail_type=["AWS API Call via CloudTrail"],
                detail={
                    "eventSource": ["elasticloadbalancing.amazonaws.com"],
                    "eventName": ["CreateLoadBalancer"]
                }
            ),
            targets=[targets.LambdaFunction(auto_associate_waf_lambda)]
        )

        # Create EventBridge rule for API Gateway creation
        events.Rule(self, "APIGatewayCreationRule",
            event_pattern=events.EventPattern(
                source=["aws.apigateway"],
                detail_type=["AWS API Call via CloudTrail"],
                detail={
                    "eventSource": ["apigateway.amazonaws.com"],
                    "eventName": ["CreateRestApi", "CreateStage"]
                }
            ),
            targets=[targets.LambdaFunction(auto_associate_waf_lambda)]
        )

        CfnOutput(self, "WebACLArn", value=web_acl.attr_arn, description="WAF Web ACL ARN")
        CfnOutput(self, "FirewallArn", value=firewall.attr_firewall_arn, description="Network Firewall ARN")

    def create_firewall_policy(self):
        return networkfirewall.CfnFirewallPolicy(
            self, 
            "FirewallPolicy",
            firewall_policy_name="FirewallPolicy",
            firewall_policy={
                "statelessDefaultActions": ["aws:forward_to_sfe"],
                "statelessFragmentDefaultActions": ["aws:forward_to_sfe"],
                "statefulRuleGroupReferences": [
                    {
                        "resourceArn": self.create_stateful_rule_group().attr_rule_group_arn
                    }
                ]
            }
        )

    def create_stateful_rule_group(self):
        return networkfirewall.CfnRuleGroup(
            self, 
            "StatefulRuleGroup",
            capacity=100,
            rule_group_name="StatefulRuleGroup",
            type="STATEFUL",
            rule_group={
                "rulesSource": {
                    "statefulRules": [
                        {
                            "action": "PASS",
                            "header": {
                                "destination": "ANY",
                                "destinationPort": "ANY",
                                "direction": "ANY",
                                "protocol": "TCP",
                                "source": "ANY",
                                "sourcePort": "ANY"
                            },
                            "ruleOptions": [
                                {
                                    "keyword": "sid:1"
                                }
                            ]
                        }
                    ]
                }
            }
        )
