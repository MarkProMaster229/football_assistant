from business_logic.working_data import Work
import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from managers.parser_manager import ParserManager
class ManagerGet:
    def __init__(self):
        self.work = Work()

        self.manaderPars = ParserManager()
        self.bot = init.chatBot

        @self.bot.message_handler(commands=['players'])
        def handle_players(message):
            self.getTables(message.chat.id)

    def getTables(self, chat_id):
        data = self.manaderPars.parserInit()
        for player in data:
            Keyboard = InlineKeyboardMarkup(row_width=2)
            button = InlineKeyboardButton(
                text=player["name"],
                callback_data=f'player_{player["number"]}'
            )
            Keyboard.add(button)
            self.bot.send_message(
                chat_id,
                f'{player["number"]} - {player["position"]}',
                reply_markup=Keyboard
            )
