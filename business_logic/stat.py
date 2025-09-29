import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

class Stat:
    def __init__(self):
        self.bot = init.chatBot
        self.tours_dict = {}
        self.touch = {}
        self.load_json()
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("tea_"))(self.statSelected)

    def load_json(self):
        with open("matches.json", "r", encoding="utf-8") as f:
            data2 = json.load(f)
        for obj in data2:
            tour_name = obj["tour"]
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


    def statGame(self, msg):
        self.tours_dict.clear()  # очищаем предыдущие туры
        keyboard = InlineKeyboardMarkup(row_width=2)


        json_path = "matches.json"
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data2 = json.load(f)
            print(f"[LOG] JSON загружен, найдено {len(data2)} объектов")
        except FileNotFoundError:
            print(f"[ERROR] Файл {json_path} не найден")
            self.bot.send_message(msg.chat.id, f"Ошибка: файл {json_path} не найден")
            return
        except json.JSONDecodeError as e:
            print(f"[ERROR] Ошибка чтения JSON: {e}")
            self.bot.send_message(msg.chat.id, f"Ошибка чтения JSON: {e}")
            return

        for obj in data2:
            tour_name = obj["tour"].strip()
            print(f"[LOG] Обрабатываем тур: '{tour_name}'")
            keyboard.add(InlineKeyboardButton(tour_name, callback_data=f"tea_{tour_name}"))

            match_info = {
                "date": obj["date"],
                "time": obj["time"],
                "home": obj["home"],
                "away": obj["away"],
                "score": obj["score"]
            }
            self.tours_dict.setdefault(tour_name, []).append(match_info)

        print(f"[LOG] Всего туров в словаре: {list(self.tours_dict.keys())}")
        self.bot.send_message(msg.chat.id, "Выберите тур:", reply_markup=keyboard)

    def statSelected(self, call):
        selected_name = call.data.split("_", 1)[1].strip()
        self.touch[call.from_user.id] = selected_name

        print(f"[LOG] Пользователь {call.from_user.id} выбрал тур: '{selected_name}'")
        if selected_name not in self.tours_dict:
            print(f"[ERROR] Тур '{selected_name}' не найден в словаре")
            self.bot.send_message(call.message.chat.id, "Тур не найден 😢")
            return

        tour_matches = self.tours_dict[selected_name]
        text = "\n".join(
            f"{m['date']} {m['time']} {m['home']} - {m['away']} : {m['score']}" for m in tour_matches
        )
        self.bot.send_message(call.message.chat.id, text)
