import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Stat:
    def __init__(self):
        self.bot = init.chatBot
        self.user_teams = {}
        self.teams = ["Барса", "Реал", "Бавария", "ПСЖ"]  # можно потом получать динамически

        self.bot.callback_query_handler(func=lambda call: call.data.startswith("team_"))(self.team_selected)

        self.bot.message_handler(commands=['match'])(self.match)

    def match(self, msg):
        keyboard = InlineKeyboardMarkup(row_width=2)
        for team in self.teams:
            keyboard.add(InlineKeyboardButton(team, callback_data=f"team_{team}"))
        self.bot.send_message(msg.chat.id, "Выберите команду:", reply_markup=keyboard)

    def team_selected(self, call):
        team_name = call.data.split("_")[1]
        self.user_teams[call.from_user.id] = team_name
        self.bot.send_message(call.message.chat.id, f"Вы выбрали команду: {team_name}")
