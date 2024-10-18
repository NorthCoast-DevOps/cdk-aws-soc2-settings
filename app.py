#!/usr/bin/env python3
"""
This is the entry point for the AWS SOC 2 Compliance CDK application.
It creates an instance of the MainStack with the name "SOC2Settings",
which will be visible in the AWS CloudFormation console.
The app.synth() call generates the CloudFormation template from the defined constructs.
"""

from aws_cdk import App
from aws_soc2_settings.main_stack import MainStack

app = App()

# Create the main stack with the name "SOC2Settings"
MainStack(app, "SOC2Settings",
    # If you want to add a description to the stack, you can do so like this:
    description="SOC 2 Compliance Settings and Resources"
)

app.synth()
