from config import *
import sqlite3
from datetime import datetime
import google.generativeai as genai
import json
import re
import os


#从配置文件中获取GEMINI_API_KEY
api_key = gemini_api_key
#格式化当前日期时间
update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#创建新用户
def write_content_by_wxid(wxid,content=''):
    try:
        user_data_dic = {'wxid': wxid, 'content': content, 'update_time': update_time}
        conn = sqlite3.connect('gemini.db')
        os.chmod('gemini.db', 0o777)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                wxid TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                update_time TEXT DEFAULT '2023-12-25 12:00:00'
            )
        ''')
        insert_query = "INSERT INTO users (wxid, content, update_time) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (user_data_dic['wxid'], user_data_dic['content'], user_data_dic['update_time']))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"插入{wxid}记录发生异常：{e}")

#读取符合用户聊天记录
def read_content_by_wxid(wxid):
    conn = sqlite3.connect('gemini.db')
    cursor = conn.cursor()
    # 执行查询
    cursor.execute("SELECT content FROM users where wxid='%s'" %wxid)
    # 获取所有数据
    data = cursor.fetchall()
    # 关闭数据库连接
    conn.close()
    # 检查是否找到记录
    msg = data[0][0]
    #将字符转为json列表
    msg = json.loads(msg)
    return msg


#更新聊天记录
def update_content_by_wxid(wxid, content):
    try:
        conn = sqlite3.connect('gemini.db')
        cursor = conn.cursor()
        # 执行更新
        cursor.execute("UPDATE users SET content=?,update_time=? WHERE wxid=?", (content,update_time,wxid))
        # 提交更改
        conn.commit()
        # 关闭数据库连接
        conn.close()
    except Exception as e:
        print(f"更新{wxid}记录发生异常：{e}")

# GEMINI聊天
def chat(content,messages=[]):
    try:
        genai.configure(api_key = gemini_api_key)
        model = genai.GenerativeModel('gemini-pro')
        #parts = input("请输入问题:")
        parts = content
        # 将用户问话加到数组里
        messages.append({'role':'user','parts': [parts]})
        # 执行对话
        response = model.generate_content(messages)
        # 将AI回答的话添加到数组里
        messages.append({'role':'model','parts':[response.text]})
        return (messages,response.text)
    except Exception as e:
        return ([],str(e)+'\r\n出现错误，请联系QQ：415135222')

# 判断输出是否包含html源代码
def contains_backticks_content(s):
    return bool(re.search(r'```html.*?```', s, re.DOTALL))

# 定义一个替换函数
def replace_html_tags(match):
    content = match.group()
    # 将 < 替换为 &lt;，将 > 替换为 &gt;
    content = content.replace('<', '&lt;').replace('>', '&gt;')
    return content

# 使用正则表达式替换html中瑕疵
def replace_match_html(html_code):
    result = re.sub(r'```html.*?```', replace_html_tags, html_code, flags=re.DOTALL)
    result = result.replace("<p>```html&lt;/p&gt;","<p>```html</p>")
    result = result.replace("&lt;p&gt;```</p>","<br>```</p>")
    result = "<pre><code>"+result+"</code></pre>"
    return result

