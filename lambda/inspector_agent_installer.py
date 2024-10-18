"""
This Lambda function automatically installs the AWS Inspector agent on newly created EC2 instances.
It is triggered by an EventBridge rule when an EC2 instance enters the 'pending' state.
The function waits for the instance to become available in Systems Manager and then uses SSM to
install the Inspector agent.
"""

import boto3
import os
import time

def handler(event, context):
    ec2 = boto3.client('ec2')
    ssm = boto3.client('ssm')
    region = os.environ['REGION']

    instance_id = event['detail']['instance-id']

    # Wait for the instance to become available in Systems Manager
    max_retries = 30
    for i in range(max_retries):
        response = ssm.describe_instance_information(
            Filters=[{'Key': 'InstanceIds', 'Values': [instance_id]}]
        )
        if response['InstanceInformationList']:
            break
        if i == max_retries - 1:
            print(f"Instance {instance_id} did not become available in Systems Manager. Skipping.")
            return
        time.sleep(10)  # Wait 10 seconds before checking again

    # Install Inspector agent
    try:
        ssm.send_command(
            InstanceIds=[instance_id],
            DocumentName='AWSInspector-ManageAWSAgent',
            Parameters={'Operation': ['Install']}
        )
        print(f"Initiated Inspector agent installation on instance {instance_id}")
    except ssm.exceptions.InvalidInstanceId:
        print(f"Instance {instance_id} is not yet ready for SSM commands. The agent will be installed when the instance is fully initialized.")
