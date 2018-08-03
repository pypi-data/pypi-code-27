from awslabs.challenge import Challenge
import boto3

class MyChallenge(Challenge):

    title = "A Static Website"
    description = "Now turn the created bucket into a website with an index.html containing Hello World"

    def start(self):
        self.instructions()

    def validate(self):

        client = boto3.client('s3')

        bucket_is_website = False
        response = client.get_bucket_website(
                Bucket=self.get('bucket')
            )
        print(response['IndexDocument']['Suffix'])
        try:
            response = client.get_bucket_website(
                Bucket=self.get('bucket')
            )
            if 'IndexDocument' in response and response['IndexDocument']['Suffix'] == 'index.html':
                bucket_is_website = True
        except:
            pass

        if bucket_is_website:
            return self.success("The bucket is indeed a website. Good job!")
        else:
            return self.fail("The bucket {} is NOT a website and NOT serving an index.html containing hello world. Try again.".format(self.get('bucket')))
