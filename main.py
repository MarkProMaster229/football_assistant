import telebot
import json
from init import Init2
def mainReal():
    #main
    init1 = Init2()
    chatBot = init1.i()
#TODO тестирование
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
#main
if __name__ == "__main__":
    mainReal()