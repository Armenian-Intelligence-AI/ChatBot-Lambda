import os
import logging as logger
import boto3

logger.getLogger().setLevel(logger.INFO)

dynamodb_client = boto3.client('dynamodb')

DATABASE_HOST: str = os.environ['DATABASE_HOST']
DATABASE_NAME: str = os.environ['DATABASE_NAME']
DATABASE_USERNAME: str = os.environ['DATABASE_USERNAME']
DATABASE_PASSWORD: str = os.environ['DATABASE_PASSWORD']
PRIORITY_LABELS: list = [7]
NOT_PRIORITY_LABELS: list = [5]
