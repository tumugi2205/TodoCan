import json
import os
from os.path import join, dirname

import boto3
from dotenv import load_dotenv

def lambda_handler(event, context):
    """lsコマンドが入力された時のlambda関数
    
    Arguments:
        event {dict} -- lambda実行時に渡すデータ
        context {dict} -- 正直わかってない。たぶん周りのファイルとかかな
    
    Returns:
        json -- 取得したデータをjsonで返す
    """
    dynamodb = connect_db()
    user_name = event["user_name"]
    action = event["action"]
    table = dynamodb.Table('TodoCan')
    user_data = table.get_item(Key={"user_name":user_name})["Item"]

    if "todo" == action:
        return user_data["TODO"]
    elif "doing" == action:
        return user_data["DOING"]
    elif "done" == action:
        return user_data["DONE"]
    elif not action:
        return user_data


def connect_db():
    return boto3.resource('dynamodb',
        region_name='us-east-2',
        aws_access_key_id=get_key("aws_access_key_id"),
        aws_secret_access_key=get_key("aws_secret_access_key") 
        )
        
def get_key(key_name):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key_name)