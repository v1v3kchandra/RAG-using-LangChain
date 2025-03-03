css = '''
<style>
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.chat-message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
    max-width: 80%;
}

.chat-message.user {
    background-color: #2b313e;
    border-radius: 15px 15px 0 15px;
    padding: 1rem;
    align-self: flex-end;
}

.chat-message.bot {
    background-color: #475063;
    border-radius: 15px 15px 15px 0;
    padding: 1rem;
    align-self: flex-start;
}

.chat-message .avatar {
    width: 50px;
    height: 50px;
    flex-shrink: 0;
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    max-width: 70%;
    padding: 0.75rem 1.25rem;
    font-size: 1rem;
    color: #fff;
    word-wrap: break-word;
}
</style>

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://png.pngtree.com/png-vector/20200610/ourmid/pngtree-computer-vector-illustration-in-cartoon-style-png-image_2222574.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://png.pngtree.com/element_our/png/20181206/users-vector-icon-png_260862.jpg">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
