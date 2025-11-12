import telebot
import json
import init

from managers.dialog_manager import NegotiationManager
from managers.stat_manager import StatManager
from managers.parser_manager import ParserManager
from managers.getManager import ManagerGet
from managers.parsesob_manager import FootballParserManager
from managers.model_long import IncludeModel

bot = init
def mainReal():
    #main
    print("hello world")
    from managers.Near_Event import Near_Event

    init.chatBot = init.Init2().i()
    bot = init.chatBot
    d = Near_Event(bot)

    dialog = NegotiationManager()
    dialog.negotiationManager()

    parserob = FootballParserManager()
    parserob.init()

    stat = StatManager()

    parser = ParserManager()
    parser.parserInit()
    menagerGet = ManagerGet()
    
    usingModel = IncludeModel(bot)
    
    init.chatBot.polling(none_stop=True)

    #main

if __name__ == "__main__":
    mainReal()