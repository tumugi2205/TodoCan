import json
import os
from os.path import join, dirname
from datetime import datetime
from datetime import datetime as dt
from decimal import Decimal

import boto3
from dotenv import load_dotenv

def lambda_handler(event, context):
    """addコマンドが入力された時のlambda関数
    
    Arguments:
        event {dict} -- lambda実行時に渡すデータ
        context {dict} -- 正直わかってない。たぶん周りのファイルとかかな
    
    Returns:
        json -- 取得したデータをjsonで返す
    """
    dynamodb = connect_db()
    result_data = {}
    user_name = event["user_name"]
    task = event["task"]
    assumed_time = event["assumed_time"]
    table = dynamodb.Table('TodoCan')
    user_data = table.get_item(Key={"user_name":user_name})["Item"]

    for todo, doing in zip(user_data["TODO"], user_data["DOING"]):
        if task in todo["task_name"] or task in doing["task_name"]:
            return {"error_message":"TaskAlreadyExist"}
    add_data = {
        "task_name":task,
        "assumed_time":assumed_time
    }
    user_data["TODO"].append(add_data)
    table.put_item(Item=user_data)
    return user_data["TODO"]
    
    


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