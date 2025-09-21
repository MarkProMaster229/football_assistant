import telebot
import json
import init

from business_logic.negotiation import Negotiation
bot = init
def mainReal():
    #main
    print("hello world")

    init.chatBot = init.Init2().i()

    dialog = Negotiation()
    dialog.connekted()

    init.chatBot.polling(none_stop=True)

    #main

if __name__ == "__main__":
    mainReal()