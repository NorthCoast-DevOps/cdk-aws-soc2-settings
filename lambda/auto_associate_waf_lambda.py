"""
This Lambda function automatically associates a WAF Web ACL with newly created
Application Load Balancers (ALBs) and API Gateways. It is triggered by EventBridge
rules when these resources are created.
"""

import boto3
import os
import time

wafv2 = boto3.client('wafv2')
elbv2 = boto3.client('elbv2')
apigw = boto3.client('apigateway')

WEB_ACL_ARN = os.environ['WEB_ACL_ARN']

def handler(event, context):
    print(f"Received event: {event}")
    
    if 'elasticloadbalancing' in event['detail']['eventSource']:
        handle_alb_creation(event)
    elif 'apigateway' in event['detail']['eventSource']:
        handle_api_gateway_creation(event)

def handle_alb_creation(event):
    # Wait for ALB to be active
    time.sleep(30)
    
    load_balancer_arn = event['detail']['responseElements']['loadBalancers'][0]['loadBalancerArn']
    
    try:
        wafv2.associate_web_acl(
            WebACLArn=WEB_ACL_ARN,
            ResourceArn=load_balancer_arn
        )
        print(f"Associated WAF Web ACL with ALB: {load_balancer_arn}")
    except Exception as e:
        print(f"Error associating WAF Web ACL with ALB: {str(e)}")

def handle_api_gateway_creation(event):
    if event['detail']['eventName'] == 'CreateRestApi':
        api_id = event['detail']['responseElements']['id']
    elif event['detail']['eventName'] == 'CreateStage':
        api_id = event['detail']['requestParameters']['restApiId']
    
    # Wait for API Gateway to be ready
    time.sleep(10)
    
    try:
        stages = apigw.get_stages(restApiId=api_id)['item']
        for stage in stages:
            stage_arn = f"arn:aws:apigateway:{event['region']}::/restapis/{api_id}/stages/{stage['stageName']}"
            wafv2.associate_web_acl(
                WebACLArn=WEB_ACL_ARN,
                ResourceArn=stage_arn
            )
            print(f"Associated WAF Web ACL with API Gateway stage: {stage_arn}")
    except Exception as e:
        print(f"Error associating WAF Web ACL with API Gateway: {str(e)}")
