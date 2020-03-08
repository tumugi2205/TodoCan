# TODO: ベロシティグラフを開く場合は第一引数に見たいファイル名を入れる
# TODO: ファイル名は自動作成にする
# TODO: TODOlistを追加
# TODO: 各項目の確認ができるようにする
# TODO: 割り込みタスクを表現する
# TODO: タスク追加などのAPIを作成する
# TODO:　djangoでweb番を作成しておく。基本ローカル操作で問題ないが、チーム開発をオンラインでする場合は確認手段がほしい。
# TODO: グラフをjsで作成する
# TODO: 日付や週ごとなどにグラフを分けて、遷移して全部見れると面白そう
# TODO: gitgraphみたいなのがあると面白そう
# TODO: できるだけ簡単にタスクの追加、確認などができるようにしたい。案を出す。
# TODO: jsonファイルではなくNOSQLとか使ってみる。どうせならLambdaでサーバレスページ作って、

# TODO: task_id で全部操作できるようにしたい
# TODO: 削除機能の追加
# TODO: 利用時間の丸め込みと単位

from datetime import datetime
from datetime import datetime as dt
from dateutil import relativedelta
import os
import json
import sys

import unicodedata


def left(digit, msg):
    for c in msg:
        if unicodedata.east_asian_width(c) in ('F', 'W', 'A'):
            digit -= 2
        else:
            digit -= 1
    return msg + ' ' * digit


now = datetime.now()
now_week_head = now - relativedelta.relativedelta(
    days=now.weekday(), hour=0, minute=0, second=0, microsecond=0)
day = now.strftime('%Y/%m/%d')
time = now.strftime('%Y/%m/%d-%H:%M')
now_week_head = now_week_head.strftime('%Y/%m/%d')

if not os.path.exists("TodoManage.json"):
    Initial = {}
    with open("TodoManage.json", "w") as f:
        json.dump(Initial, f, indent=4)

with open("TodoManage.json") as f:
    todo_data = json.load(f)

args = sys.argv
if len(args) > 4:
    user_name = args[1]
    action_command = args[2]
    action_type = args[3]
    task = args[4]
    assumed_time = int(args[5])
elif len(args) == 4:
    user_name = args[1]
    action_command = args[2]
    task = args[3]

if user_name not in todo_data:
    todo_data[user_name] = {"TODO": [], "DOING": [], "DONE": {}}
if now_week_head not in todo_data[user_name]["DONE"]:
    todo_data[user_name]["DONE"][now_week_head] = []
print()
if "add" in action_command:
    if "todo" == action_type:
        if task in todo_data[user_name]["TODO"]:
            print(f"already add {task} in TODO. ")
            exit()
        else:
            todo_data[user_name]["TODO"].append({task: [assumed_time]})
            print(f'{task} add TODO.(Assumed_time: {assumed_time})')
    with open("TodoManage.json", "w") as f:
        json.dump(todo_data, f, indent=4)
elif "do" == action_command:
    if task.isdecimal():
        task = int(task)
        if task > len(todo_data[user_name]["TODO"]) or task < 0:
            print("There is no such task!")
            exit()
        task_data = todo_data[user_name]["TODO"].pop(task)
        task_key = list(task_data.keys())[0]
        if task_key not in todo_data[user_name]["DOING"]:
            task_data[task_key].append(time)
            todo_data[user_name]["DOING"].append(task_data)
            print(f'You start "{task_key}" now. ({time})')
        with open("TodoManage.json", "w") as f:
            json.dump(todo_data, f, indent=4)
    else:
        print(
            'You must input task_id. If you want check task_id, you can use "ls" command.'
        )
        exit()
elif "done" == action_command:
    if task.isdecimal():
        task = int(task)
        if task > len(todo_data[user_name]["DOING"]) or task < 0:
            print("There is no such task!")
            exit()
        task_data = todo_data[user_name]["DOING"].pop(task)
        task_key = list(task_data.keys())[0]
        if task_key not in todo_data[user_name]["DONE"][now_week_head]:
            task_data[task_key].append(time)
            time_data = (dt.strptime(time, '%Y/%m/%d-%H:%M') -
                         dt.strptime(task_data[task_key][1], '%Y/%m/%d-%H:%M'))
            task_data[task_key].append(time_data.total_seconds() / 3600)
            todo_data[user_name]["DONE"][now_week_head].append(task_data)
            print(f'You done "{task_key}" now. ({time})')
        with open("TodoManage.json", "w") as f:
            json.dump(todo_data, f, indent=4)
    else:
        print(
            'You must input task_id. If you want check task_id, you can use "ls" command.'
        )
        exit()

elif "ls" in action_command:
    if "todo" in task:
        maxlen = 0
        for data in todo_data[user_name]["TODO"]:
            if len(list(data.keys())[0]) >= maxlen:
                maxlen = len(list(data.keys())[0])
        for i, t in enumerate(todo_data[user_name]["TODO"]):
            print(
                f"task_id[{i}]: {left(maxlen+25, list(t.keys())[0])} (Assumed_time: {list(t.values())[0][0]})"
            )
        print()
    elif "doing" in task:
        maxlen = 0
        for data in todo_data[user_name]["DOING"]:
            if len(list(data.keys())[0]) >= maxlen:
                maxlen = len(list(data.keys())[0])
        for i, v in enumerate(todo_data[user_name]["DOING"]):
            print(
                f"task_id[{i}]: {left(maxlen+25, list(v.keys())[0])} (start: {list(v.values())[0][1]}, Assumed_time: {list(v.values())[0][0]})"
            )
        print()
    elif "done" in task:
        for ti, val in todo_data[user_name]["DONE"].items():
            print(f"week head: {ti}")
            data_len = len(val)
            count = 0
            maxlen = 0
            for data in val:
                if len(list(data.keys())[0]) >= maxlen:
                    maxlen = len(list(data.keys())[0])
            for data in val:
                count += 1
                task = list(data.keys())[0]
                ass = list(data.values())[0][0]
                start_time = list(data.values())[0][1]
                done_time = list(data.values())[0][2]
                result_time = list(data.values())[0][3]
                if count != data_len:
                    print(
                        f" ├ {left(maxlen+25, task)} {start_time} ~ {done_time} [ass: {ass:.1f} / res: {result_time:.2f} (h)]"
                    )
                if count == data_len:
                    print(
                        f" └ {left(maxlen+25, task)} {start_time} ~ {done_time} [ass: {ass:.1f} / res: {result_time:.2f} (h)]"
                    )
            print()