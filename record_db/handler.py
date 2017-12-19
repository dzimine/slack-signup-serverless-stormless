import json
import logging
import os

import boto3
dynamodb = boto3.resource('dynamodb')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def endpoint(event, context):
    logger.info("Event received: {}".format(json.dumps(event)))
    try:
        event = event['body']
        event['email']
    except KeyError:
        raise Exception("Couldn't create the record: `email` not found.")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {k: event[k] for k in ['email', 'first_name', 'last_name']}

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "item": item
    }
