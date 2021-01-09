var templates = {
    customer: `<li>
    <div class="conversation-list">
        <div class="chat-avatar">
            <img src="static/images/users/avatar-4.jpg" alt="">
        </div>

        <div class="user-chat-content">
            <div class="ctext-wrap">
                <div class="ctext-wrap-content">
                    <p class="mb-0">
                        {{CHAT_TEXT}}
                    </p>
                </div>
                <div class="dropdown align-self-start">
                    <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        <i class="ri-more-2-fill"></i>
                    </a>
                    <div class="dropdown-menu">
                        <a class="dropdown-item" href="javascript:analyse('{{CHAT_TEXT}}')">Analyse Sentiment <i class="ri-bubble-chart-fill float-end text-muted"></i></a>
                        <a class="dropdown-item" href="#">Copy <i class="ri-file-copy-line float-end text-muted"></i></a>
                        <a class="dropdown-item" href="#">Save <i class="ri-save-line float-end text-muted"></i></a>
                        <a class="dropdown-item" href="#">Forward <i class="ri-chat-forward-line float-end text-muted"></i></a>
                        <a class="dropdown-item" href="#">Delete <i class="ri-delete-bin-line float-end text-muted"></i></a>
                    </div>
                </div>
            </div>
            <div class="conversation-name">Doris Brown</div>
        </div>
    </div>
</li>`,
    user: `<li class="right">
    <div class="conversation-list">
        <div class="chat-avatar">
            <img src="static/images/users/avatar-1.jpg" alt="">
        </div>

        <div class="user-chat-content">
            <div class="ctext-wrap">
                <div class="ctext-wrap-content">
                    <p class="mb-0">
                        {{CHAT_TEXT}}
                    </p>
                </div>
            </div>
            <div class="conversation-name">Ashi Patel</div>
        </div>
    </div>
</li>`
};

var chatMessage = $("#chatMessage");
var chatButton = $("#chatButton");
var chatWindow = $("#chatWindow");
var channel = "/chat";
var socket = io.connect('http://' + document.domain + ':' + location.port + channel);
socket.on('connect', function() {
    socket.emit('my_connection', {data: 'I\'m connected!'});
});
socket.on("message", function (message) {
    refreshMessages(message.data);
});

function refreshMessages(message) {
    agent = message.sender;
    var html;
    if(agent == "customer")
    {
        html = templates.customer;
    } else {
        html = templates.user;
    }

    html = html.replace("{{CHAT_TEXT}}", message.message);
    html = html.replace("{{CHAT_TEXT}}", message.message);
    chatWindow.append(html);
}

function sendMessage()
{
    chatWindow.scrollTop = chatWindow.scrollHeight;
    var message = chatMessage.val();
    var author = "Ashi Patel";
    socket.emit('message', {data: {message: message, author: author, sender: "user"}});
    chatMessage.val("");
    chatWindow.animate({ scrollTop: chatWindow.scrollHeight }, "slow");
}

function analyse(msg)
{
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/ajax/do_sentiment_text_only",
        data: {
            chat_message: msg
        },
        success: function (response) {
            alert(response);
        }
    });
}
$(function(){
    chatButton.on("click", function() {
        sendMessage();
    });
    chatMessage.keyup(function(e){
        if(e.keyCode == 13)
        {
            sendMessage();
        }
    });
});