import aws_cdk as core
import aws_cdk.assertions as assertions

from scalable_django_chat.scalable_django_chat_stack import ScalableDjangoChatStack

# example tests. To run these tests, uncomment this file along with the example
# resource in scalable_django_chat/scalable_django_chat_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ScalableDjangoChatStack(app, "scalable-django-chat")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
