import boto3
import os
from botocore.vendored import requests

SNS_TOPIC = os.environ['SNS_TOPIC']
SUBREDDIT = os.environ['SUBREDDIT']

sns_topic = boto3.resource('sns').Topic(SNS_TOPIC)


def lambda_handler(event, context):

    top_posts = requests.get("https://www.reddit.com/r/%s/top/.json" % SUBREDDIT).json()
    top_post = top_posts["data"]["children"][0]["data"]

    tinyurl = requests.get("https://tinyurl.com/api-create.php?url=%s" % top_post['url']).text

    headline = "%s - %s" % (top_post["title"], tinyurl)
    sns_topic.publish(Message=headline)

