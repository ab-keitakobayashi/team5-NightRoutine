# 開発

npm run dev

npm install

npm install axios

npm install v-calendar@next @popperjs/core

npm run dev

# saaya 用 git hub のうれしいコマンド

git branch 　：
　今どこのブランチにいるかわかる

git checkout -b 任意のブランチ名 origin/main：
　ブランチ切れる

git push -u origin 任意のブランチ名：
　プッシュできる

＊main でいじらないこと
＊ちゃんとコメントアウトもコメントもしようね

# Vue 3 + TypeScript + Vite

This template should help get you started developing with Vue 3 and TypeScript in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about the recommended Project Setup and IDE Support in the [Vue Docs TypeScript Guide](https://vuejs.org/guide/typescript/overview.html#project-setup).

# AWS setting

エンドポイント：aws-handson-db-group-5.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com
name: admin
password:fy26admin
(as same as the handson's docs)

for test
table name: testusers
colunm:
user_id INT PRIMARY KEY AUTO_INCREMENT,
user_name varchar(250),
user_mailAddress varchar(250),
class_id int,oython
period date,
avatar_id int,
enemy_id int,
enemy_HP int,
EF_item_id_1 int,
EF_item_id_2 int,
EF_item_id_3 int,
EF_item_id_4 int,
EF_item_id_5 int

ここから情報
import pymysql
import os

def main_handler(event, context): # RDS 接続情報
host = "aws-handson-db-group-5.c7c4ksi06r6a.ap-southeast-2.rds.amazonaws.com" # RDS のエンドポイント
user = "admin" # RDS 作成時に設定したユーザー名
password = "fy26admin" # そのユーザーのパスワード
db = "NightRoutine" # 作成したデータベース名

    # RDSに接続
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        connect_timeout=5
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT NOW();")
            result = cursor.fetchone()
        return {
            'statusCode': 200,
            'body': f'現在時刻: {result[0]}'
        }
    finally:
        connection.close()
