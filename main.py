import telebot
import json
def mainReal():
    with open('token.json', 'r') as f:
        config = json.load(f)

    token = config['token']
    chatBot = telebot.TeleBot(token)

    @chatBot.message_handler(commands=['start'])
    def commanndStart(message):
        chat = message.chat
        info = (
            f"Chat ID: {chat.id}\n"
            f"Type: {chat.type}\n"  # 'private', 'group', 'supergroup', 'channel'
            f"Title: {chat.title}"
        )
        chatBot.send_message(message.chat.id, info)

    chatBot.polling(none_stop= True)

if __name__ == "__main__":
    mainReal()