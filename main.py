import telebot
import json
import init

from managers.dialog_manager import NegotiationManager
from managers.stat_manager import StatManager
from managers.parser_manager import ParserManager
from managers.getManager import ManagerGet
from managers.parsesob_manager import FootballParserManager

bot = init
def mainReal():
    #main
    print("hello world")

    init.chatBot = init.Init2().i()

    dialog = NegotiationManager()
    dialog.negotiationManager()

    stat = StatManager()

    parser = ParserManager()
    parser.parserInit()
    menagerGet = ManagerGet()

    parserob = FootballParserManager()
    parserob.init()

    init.chatBot.polling(none_stop=True)

    #main

if __name__ == "__main__":
    mainReal()