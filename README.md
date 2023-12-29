<h1> gemini-python-flask-sqlite</h1>
<h5>本示例使用sqlite存储不同用户的聊天记录，使gemini能够理解以前的聊天记录，实现上下文的语义分析。是用flask Socket实现的</h5>
==================================<br>
python 10及以上(ubuntu 22.04及以上都内置好了），在终端里运行：<br>
<code>
sudo apt update<br>
sudo apt install sqlite3 -y<br>
pip3 install -U flask flask_socketio google.generativeai markdown<br>
</code>
==================================<br>
<li> 一、将申请来的gemini api key填入config.py里<br></li>
<li> 二、python3 app.py如访问http://192.168.65.23:5001</li>
