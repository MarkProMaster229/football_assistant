import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

class Stat:
    def __init__(self):
        self.bot = init.chatBot
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("tea_"))(self.statSelected)
        self.tours_dict = {}
        self.touch = {}

    def statGame(self, msg):
        self.tours_dict.clear()
        keyboard = InlineKeyboardMarkup(row_width=2)
        with open("matches.json", "r", encoding="utf-8") as f:
            data2 = json.load(f)

        for obj in data2:
            tour_name = obj["tour"]
            keyboard.add(InlineKeyboardButton(tour_name, callback_data=f"tea_{tour_name}"))

            match_info = {
                "date": obj["date"],
                "time": obj["time"],
                "home": obj["home"],
                "away": obj["away"],
                "score": obj["score"]
            }
            if tour_name not in self.tours_dict:
                self.tours_dict[tour_name] = []
            self.tours_dict[tour_name].append(match_info)

        self.bot.send_message(msg.chat.id, "Выберите тур:", reply_markup=keyboard)

    def statSelected(self, call):
        selected_name = call.data.split("_")[1]
        self.touch[call.from_user.id] = selected_name
        tour_matches = self.tours_dict[selected_name]

        text = ""
        for match in tour_matches:
            text += f"{match['date']} {match['time']} {match['home']} - {match['away']} : {match['score']}\n"

        self.bot.send_message(call.message.chat.id, text)






    #def match(self, msg):
        #keyboard = InlineKeyboardMarkup(row_width=2)
        #for team in self.teams:
            #keyboard.add(InlineKeyboardButton(team, callback_data=f"tea_{team}"))
        #self.bot.send_message(msg.chat.id, "Выберите команду:", reply_markup=keyboard)

    #def team_selected(self, call):
        #team_name = call.data.split("_")[1]
        #self.user_teams[call.from_user.id] = team_name
        #self.bot.send_message(call.message.chat.id, f"Вы выбрали команду: {team_name}")
