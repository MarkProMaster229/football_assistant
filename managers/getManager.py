from business_logic.working_data import Work
import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from managers.parser_manager import ParserManager
class ManagerGet:
    def __init__(self):
        self.work = Work()
        self.manaderPars = ParserManager()
        self.bot = init.chatBot

        self.bot.message_handler(commands=['players'])(self.handle_players)

        self.bot.callback_query_handler(
            func=lambda call: call.data.startswith("player_")
        )(self.handle_player_info)

    def handle_players(self, message):
        self.getTables(message.chat.id)

    def getTables(self, chat_id):
        data = self.manaderPars.parserInit()
        Keyboard = InlineKeyboardMarkup(row_width=2)

        for player in data:
            button = InlineKeyboardButton(
                text=player["name"],
                callback_data=f'player_{player["number"]}'
            )
            Keyboard.add(button)

        self.bot.send_message(
            chat_id,
            "Вот список игроков команды. Выберите интересующего игрока для подробной информации:",
            reply_markup=Keyboard
        )

    def handle_player_info(self, call):
        player_number = call.data.split("_")[1]
        data = self.manaderPars.parserInit()  # Используем правильное имя атрибута
        player = next((p for p in data if str(p["number"]) == player_number), None)

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
                self.bot.send_message(call.message.chat.id, text + "\n(Изображение не найдено)")
        else:
            self.bot.send_message(call.message.chat.id, "Игрок не найден.")
