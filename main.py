import telebot
import json
import init

from managers.dialog_manager import NegotiationManager
from managers.stat_manager import Stat
from managers.parser_manager import ParserManager
from business_logic.working_data import Work
bot = init
def mainReal():
    #main
    print("hello world")

    init.chatBot = init.Init2().i()

    dialog = NegotiationManager()
    dialog.negotiationManager()

    stat = Stat()

    parser = ParserManager()
    parser.parserInit()



    init.chatBot.polling(none_stop=True)

    #main

if __name__ == "__main__":
    mainReal()