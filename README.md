<h1>gemini-python-flask-sqlite</h1>
<h5>本示例使用sqlite存储不同用户的聊天记录，使gemini能够理解以前的聊天记录，实现上下文的语义分析。是用flask Socket实现的</h5>
==================================<br>
python 10及以上(ubuntu 22.04及以上都内置好了，有可能pip3会提示需要安装，那就安装），在终端里运行：<br>
<code>
sudo apt update<br>
sudo apt install sqlite3 -y<br>
pip3 install -U flask flask_socketio google.generativeai markdown<br>
</code>
==================================<br>
<li> 一、将申请来的gemini api key填入config.py里<br></li>
<li> 二、python3 app.py如访问http://192.168.65.23:5001</li>
<h3>2024-1-22更新</h3>
添加了聊天返回API，<br>
如：<br>
http://192.168.65.23:5001/chat?<微信ID>=cbf_41513522%content=<消息内容><br>
http://192.168.65.23:5001/chat?wxid=cbf_41513522%content=hello<br>
它会返回回答的JSON：<br>
{'reply': 'hello,Can I help you?'}
