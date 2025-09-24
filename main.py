import telebot
import json
import init

from business_logic.negotiation import Negotiation
from business_logic.stat import Stat
from business_logic.parse import Parse
bot = init
def mainReal():
    #main
    print("hello world")

    init.chatBot = init.Init2().i()

    dialog = Negotiation()
    dialog.connekted()

    stat = Stat()

    pars = Parse()
    pars.parser()

    init.chatBot.polling(none_stop=True)

    #main

if __name__ == "__main__":
    mainReal()