import logging
import os
import boto3
import uuid
import configparser

class Database:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("./config/config.ini")
        self.accessKeyId = config['AWS']['accessKeyId']        
        self.accessKey = config['AWS']['accessKey']
    
    def save_data(self, messageId, fromObj, chatObj, cmd, date):
        dynamo = boto3.client('dynamodb', region_name='us-west-2', aws_access_key_id = self.accessKeyId, aws_secret_access_key = self.accessKey)
        if chatObj.type == 'private':
            chat = { 
                'id': {'S': str(chatObj.id)},
                'type': {'S': chatObj.type},
                'username': {'S': chatObj.username},
                'first_name': {'S': chatObj.first_name}
            }
        else:
            chat = { 
                'id': {'S': str(chatObj.id)},
                'type': {'S': chatObj.type},
                'title': {'S': chatObj.title}
            }
        item = {
            'uuid': {'S': str(uuid.uuid4())},
            'message_id': {'S': str(messageId)},
            'from': {'M': { 
                'id': {'S': str(fromObj.id)},
                'first_name': {'S': fromObj.first_name},
                'username': {'S': fromObj.username},
                'language_code': {'S': fromObj.language_code}
            }},
            'chat': {'M': chat},
            'date': {'S': str(date)},
            'text': {'S': cmd}
        }
        dynamo.put_item(Item=item, TableName='ChatHistory')