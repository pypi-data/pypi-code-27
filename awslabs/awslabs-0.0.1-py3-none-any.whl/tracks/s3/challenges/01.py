from awslabs.challenge import Challenge
import boto3

class MyChallenge(Challenge):

    title = "Create an S3 bucket"
    description = "Create an S3 bucket and upload a readme.txt file with the content 'awslabs'."

    def start(self):

        self.instructions()

    def validate(self):

        client = boto3.client('s3')
        buckets = client.list_buckets()
        object_found = False
        usedbucket = ""

        for bucket in buckets['Buckets']:
            try:
                obj = client.get_object(Bucket=bucket['Name'], Key='readme.txt')
                if "awslabs" in obj['Body'].read().decode('utf-8'):
                    object_found = True
                    usedbucket = bucket["Name"]
                    break
            except:
                pass

        if object_found:
            self.save('bucket', usedbucket)
            return self.success("You created a bucket {}, uploaded a file with the correct content.".format(usedbucket))
        else:
            return self.fail("Cannot find a bucket containing a readme.txt with 'awslabs' in it. It should not contain any spaces, new lines etc.")
        
