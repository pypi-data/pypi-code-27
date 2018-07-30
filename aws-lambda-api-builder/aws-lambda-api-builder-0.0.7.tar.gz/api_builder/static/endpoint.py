import json

def main(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({"greeting": "Hello, " + event["pathParameters"]["name"]})
    }