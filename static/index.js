//添加 Socket.IO 客户端脚本 -->

// 显示手机号输入模态框
function showPhoneNumberModal() {
    var phoneNumberModal = new bootstrap.Modal(document.getElementById('phoneNumberModal'), {
        backdrop: 'static', // 防止点击背景关闭模态框
        keyboard: false // 防止按下键盘 ESC 键关闭模态框
    });
    phoneNumberModal.show();
}

// 保存手机号
function savePhoneNumber() {
    var phoneNumberInput = document.getElementById('phoneNumberInput').value;
    if (phoneNumberInput.trim() !== '') {
        // 保存手机号到 localStorage
        localStorage.setItem('phoneNumber', phoneNumberInput);
        // 关闭模态框
        var phoneNumberModal = bootstrap.Modal.getInstance(document.getElementById('phoneNumberModal'));
        phoneNumberModal.hide();
    }
}

// 页面加载完成后设置文本域焦点
// 获取文本域元素
// var userInput = document.getElementById('userInput');
document.addEventListener('DOMContentLoaded', function () {
    //userInput.focus();
    if (localStorage.getItem('phoneNumber') == (''||null)){
        showPhoneNumberModal(); // 页面加载时弹出手机号输入模态框
    }else{
        document.getElementById('phoneNumber').value = localStorage.getItem('phoneNumber')
    }
    //随机加载背景图片
    // 随机背景图片数组
    var backgroundImages = [
        'url(../static/bg.jpg)',
        'url(../static/bg1.jpg)',
        'url(../static/bg2.jpg)',
        'url(../static/bg3.jpg)',
        'url(../static/bg4.jpg)',
        'url(../static/bg5.jpg)'
    ];

    // 随机选择一张背景图片
    var randomIndex = Math.floor(Math.random() * backgroundImages.length);
    var randomImage = backgroundImages[randomIndex];

    // 设置背景图片
    document.body.style.backgroundImage = randomImage;
});

// 连接到 Socket.IO 服务器
var socket = io.connect('http://' + document.domain + ':' + location.port);

// 处理从服务器接收到的消息
socket.on('message_from_server', function (data) {
    //var messageText = marked.parse(data['message']);
    var messageText = data['message'];
    console.log('Received message from server:', messageText);
    // 在页面上显示收到的消息
    var messageContainer = document.getElementById('messageContainer');
    var messageElement = document.createElement('p');
    messageElement.className = 'from-them';
    messageElement.innerHTML = messageText;
    //messageElement.textContent = messageText;
    messageContainer.appendChild(messageElement);
});

// 处理客户端发送的消息
function localUserMessage(userInput) {
    // 在页面上显示客户端发送的消息，并保持原有样式
    var messageContainer = document.getElementById('messageContainer');
    var userMessageElement = document.createElement('p');
    userMessageElement.className = 'from-me';
    //userMessageElement.innerHTML = userInput;
    userMessageElement.textContent = userInput;
    messageContainer.appendChild(userMessageElement);
}

// 发送消息给服务器
function sendMessageToServer() {
    var userInput = document.getElementById('userInput').value;
    var phoneNumber = document.getElementById('phoneNumber').value;
    if (userInput.trim() !== '') {
        //socket.emit('message_from_client', userInput);
        socket.emit('message_from_client', { userInput: userInput, phoneNumber: phoneNumber });
        document.getElementById('userInput').value = ''; // 清空输入框
        //serverMesssage();
        localUserMessage(userInput);
        //文本域获得焦点
        //userInput.focus();
        //滚动条拉到底部
        window.scrollTo(0, document.body.scrollHeight);
    }

    // 监听键盘事件
    userInput.addEventListener('keydown', function (event) {
        // 检查是否按下 Enter 键，同时没有按下 Shift 键
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault(); // 阻止默认的 Enter 换行行为
            sendMessageToServer();
        }
    });
}
