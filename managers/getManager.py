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

        self.bot.callback_query_handler(
            func=lambda call: call.data.startswith("player_")
        )(self.handle_player_info)

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
                f'\nНомер: {player["number"]} - {player["position"]}\nИмя: {player["name"]}',
                reply_markup=Keyboard
            )

    def handle_player_info(self, call):
        player_number = call.data.split("_")[1]
        data = self.manaderPars.parserInit()
        player = next((p for p in data if p["number"] == player_number), None)

        if player:
            text = (
                f'Имя: {player["name"]}\n'
                f'Позиция: {player["position"]}\n'
                f'Матчи: {player["matches"]}\n'
                f'Голы: {player["goals"]}\n'
                f'Ассисты: {player["assists"]}\n'
                f'ЖК: {player["yellow_cards"]}\n'
                f'КК: {player["red_cards"]}'
            )
            if player["image"]:
                self.bot.send_photo(call.message.chat.id, player["image"], caption=text)
            else:
                self.bot.send_message(call.message.chat.id, text)
        else:
            self.bot.send_message(call.message.chat.id, "Игрок не найден.")
