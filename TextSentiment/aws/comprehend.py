import boto3
import json
import os

comprehend = boto3.client(service_name='comprehend',
region_name='ap-south-1',
aws_access_key_id = os.getenv("aws_access_key_id"),
aws_secret_access_key = os.getenv("aws_secret_access_key"))

def analyse_sentiment(text):
    data = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return data

if __name__ == "__main__":
    text = "I Don't want to talk to you."
    print('Calling DetectSentiment')
    # print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
    print(analyse_sentiment(text))
    print('End of DetectSentiment\n')