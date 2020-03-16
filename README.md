# TodoCan
## lambdaで動作するAPIのプログラムです
 - 実行コマンド-> python-lambda-local -f lambda_handler lambda_function.py event.json
 - event.jsonは適宜変更して実行してください。
 - dynamodbを使ってます。  

## API
### ユーザー作成
`/todocan/create-user?user_name=[user_name]`  
info  
ユーザーを作成します。  
既存ユーザーと同じ名前の場合は作成できません。  

return
- 成功時
  - `{"success_message":f"{user_name}Added!"}`
- すでにあるユーザー名の場合
  - `{"error_message":"AlredyExist"}`


### TODO追加
`/todocan/add?user_name=[user_name]&task=[task_name]&assumed_time=[assumed_time(int)]`  
info  
TODOにタスクを追加します。  
`assumed_time`は予想される作業時間を整数で入力してください。    

return  
- 成功時
  - すべてのTODOデータが返ってきます。(json)
- すでにあるタスクの場合
  - `{"error_message":"TaskAlreadyExist"}`


### DO
`/todocan/do?user_name=[user_name]&task=[task_name]`  
info  
TODOにあるタスクをDOINGに移動させます。  
`task`は、タスク名と同一のもの、またはTODO一覧のindexの番号を入れてください。  
  
return  
- 成功時
  - すべてのDOINGデータが返ってきます。(json)
- 存在しないタスクの場合
  - `{"error_message":"TaskNotFound"}`


### DONE
`/todocan/done?user_name=[user_name]&task=[task_name]`  
info  
DOINGにあるタスクをDONEに移動させます。  
`task`は、タスク名と同一のもの、またはDOING一覧のindexの番号を入れてください。  
  
return
- 成功時
  - すべてのDONEデータが返ってきます。(json)
- 存在しないタスクの場合
  - `{"error_message":"TaskNotFound"}`
  - 

### 一覧取得
`/todocan/ls?user_name=[user_name]&action=[action]`  
info  
特定の、またはすべてのデータを取得します。  
取得したい項目(TODO,DOING,DONE)を`action`に入力してください。  
また、全体のデータがほしい場合は`action`は指定しなくて大丈夫です。  
  
return
- 成功時
  - 特定のデータが返ってきます。


## DBについて
DBの保存形式については`default-db.json`を参照してください。  