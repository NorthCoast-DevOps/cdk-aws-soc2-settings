import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_soc2_settings.aws_soc2_settings_stack import AwsSoc2SettingsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_soc2_settings/aws_soc2_settings_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsSoc2SettingsStack(app, "aws-soc2-settings")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
