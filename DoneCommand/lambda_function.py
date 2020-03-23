import json
import os
from os.path import join, dirname
from datetime import datetime
from datetime import datetime as dt
from decimal import Decimal

import boto3
from dotenv import load_dotenv

def lambda_handler(event, context):
    """doneコマンドが入力された時のlambda関数
    
    Arguments:
        event {dict} -- lambda実行時に渡すデータ
        context {dict} -- 正直わかってない。たぶん周りのファイルとかかな
    
    Returns:
        json -- 取得したデータをjsonで返す
    """
    dynamodb = connect_db()
    user_name = event["user_name"]
    task = event["task"]
    table = dynamodb.Table('TodoCan')
    user_data = table.get_item(Key={"user_name":user_name})["Item"]

    pop_todo = []
    if type(task) == str:
        for index, data in enumerate(user_data["DOING"]):
            if task in data["task_name"]:
                pop_todo = user_data["DOING"].pop(index)
    else:
        pop_todo = user_data["DOING"].pop(task)
    
    if pop_todo:           
        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        measurement_time = (dt.strptime(now, '%Y-%m-%d %H:%M') - dt.strptime(pop_todo["start"], '%Y-%m-%d %H:%M'))
        pop_todo["finish"] = now
        pop_todo["measurement_time"] = Decimal(f'{measurement_time.total_seconds() / 3600}')
        user_data["DONE"].append(pop_todo)
        table.put_item(Item=user_data)
        return user_data["DONE"]
    else:
        return {"error_message":"TaskNotFound"}
    
    


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