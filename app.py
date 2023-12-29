
################################################
# python 10及以上
# sudo apt update
# sudo apt install sqlite3 -y
# pip3 install -U flask flask_socketio google.generativeai markdown
################################################

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dal import *
from datetime import datetime
import json
import re
import markdown

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message_from_client')
def handle_message(data):
    #print('Received message from client:', data)

    # Extract user input and phone number from the received data
    user_input = data.get('userInput', '')
    phone_number = data.get('phoneNumber', '')

    #print(f'User input: {user_input}, Phone number: {phone_number}')

    wxid = phone_number
    content = user_input

    #查找数据库
    try:
        messages = read_content_by_wxid(wxid)
    except:
        messages = []
        write_content_by_wxid(wxid,content='')

    # print("old message:")
    # print(messages)
    # print('The old messages type is'+str(type(messages)))

    # 执行聊天并存储为历史记录列表
    
    chat_data = chat(content,messages)
    messages = chat_data[0]
    response = chat_data[1]
    # print('===========response:===============')
    # print(response)
    # 使用markdown渲染
    response = markdown.markdown(response)
    # print('===========re replace code :===============')
    # 防止html源代码被解析
    response = replace_match_html(response)

    # 代码高亮
    # response = add_code_language_targe(response)
    # response = response.replace("```","")
    # print(response)

    #防止聊天记录过大，gemini上限是32K上下文
    messages_byte_count = str(messages).encode('utf-8')
    if len(messages_byte_count) > 32000:
        messages = messages[2:]

    # print("new message:")
    # print(messages)
    # print('The new messages type is:'+str(type(messages))+'and length is:'+str(len(messages)))

    # 更新到数据库
    #messages_todb = str(messages).replace("'",'"')
    #将list转换成单引号的JSON
    if len(messages) > 0 :
        content = json.dumps(messages, ensure_ascii=False)
        update_content_by_wxid(wxid, content)

    #response_data = {'message': str(response)}
    response_data = {'message': response}
    emit('message_from_server', response_data)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5001, debug=True,allow_unsafe_werkzeug=True)
