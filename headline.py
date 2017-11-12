import boto3
import os
from botocore.vendored import requests

PHONE_NUMBER = os.environ['PHONE_NUMBER']
SUBREDDIT = os.environ['SUBREDDIT']

# Force connection to us-west-2, since not all regions support SMS
sns_client = boto3.client('sns', region_name='us-west-2')


def lambda_handler(event, context):

    top_posts = requests.get("https://www.reddit.com/r/%s/top/.json" % SUBREDDIT).json()
    top_post = top_posts["data"]["children"][0]["data"]

    tinyurl = requests.get("https://tinyurl.com/api-create.php?url=%s" % top_post['url']).text

    headline = "%s - %s" % (top_post["title"], tinyurl)
    response = sns_client.publish(PhoneNumber=PHONE_NUMBER, Message=headline)

