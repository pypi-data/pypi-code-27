from awslabs.challenge import Challenge
import boto3

class MyChallenge(Challenge):

    title = "Launch an instance"
    description = "Create an instance with type t2.small, based on the latest Amazon Linux 2 AMI."

    def start(self):
        self.instructions()

    def validate(self):
        return self.success("You should fix this and that and bla")
