# gemini-python-flask-sqlite
本示例使用sqlite存储不同用户的聊天记录，使gemini能够理解以前的聊天记录，实现上下文的语义分析。是用flask Socket实现的
==================================
python 10及以上<br>
sudo apt update<br>
sudo apt install sqlite3 -y<br>
pip3 install -U flask flask_socketio google.generativeai markdown
==================================
## 一、将申请来的gemini api key填入config.py里
## 二、python3 app.py如访问http://192.168.65.23:5001
