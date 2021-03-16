import boto3
import configparser
import logging
from botocore.exceptions import ClientError
import random

class S3():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        self.accessKeyId = config['AWS']['accessKeyId']        
        self.accessKey = config['AWS']['accessKey']
        self.session = boto3.Session(
            aws_access_key_id=self.accessKeyId,
            aws_secret_access_key=self.accessKey,
        )
        self.bucket = 'veryusefulbot-memes'
        self.PATH = 'https://veryusefulbot-memes.s3-us-west-2.amazonaws.com/{}'

    def uploadFile(self, fileName, object_name=None):
        if object_name is None:
            object_name = fileName
        # Upload the file
        s3_client = boto3.client('s3', aws_access_key_id = self.accessKeyId, aws_secret_access_key = self.accessKey)
        try:
            response = s3_client.upload_file(fileName, self.bucket, object_name, ExtraArgs={'ACL':'public-read'})
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def getFile(self):
        s3_client = boto3.client('s3', aws_access_key_id = self.accessKeyId, aws_secret_access_key = self.accessKey)
        files = []
        try:
            for key in s3_client.list_objects(Bucket=self.bucket)['Contents']:
                files.append(self.PATH.format(key['Key']))
            return random.choice(files)
        except ClientError as e:
            logging.error(e)