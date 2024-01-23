
# -*- coding: utf-8 -*-
################################################
# python 10及以上
# sudo apt update
# sudo apt install sqlite3 -y
# pip3 install -U flask flask_socketio google.generativeai markdown
################################################

from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
from dal import *
from dal_redis import *
from datetime import datetime
import json


app = Flask(__name__)
CORS(app) #允许跨域

@app.route('/', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
def index():
    data = {
        'errcode': 0
    }
    return jsonify(data)

@app.route('/chat', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'])
def chat_with_gemini():
    # 获取用户微信号和问题
    keyword = request.args.get('keyword')
    wxid = request.args.get('wxid')

    # 从SQLSERVER中查找该用户聊天记录并转化为JSON
    messages = read_content_by_wxid(wxid)['chat_history']

    


    print("=============old messages=================")
    print(messages)
    # 执行聊天并存储为历史记录列表
    chat_data = chat(keyword, messages)
    messages = chat_data[0]
    response = chat_data[1]
    print("=============new response=================")
    print(response)
    # # 防止聊天记录过大，gemini上限是32K上下文
    # messages_byte_count = str(messages).encode('utf-8')
    # if len(messages_byte_count) > 32000:
    #     messages = messages[2:]
    # 将新的总记录写入redis
    #RedisHandler().set_redis_data(wxid, messages)
     
    # if get_historynum_by_wxid(wxid, keyword, response) == 0:
    #     write_content_by_wxid(wxid, keyword, response)
    #     print(f'已写入新记录')

    # 构建JSON
    msg = {}
    msg['reply'] = response
    # 返回json
    return jsonify(msg)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
