import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from business_logic.stat import Stat
import init

class Startbot:
    def __init__(self):
        self.bot = init.chatBot
        self.stat = Stat()
        print("startBot")
        self.user_data = {}
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(msg):
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("статистика игр", callback_data="btn_stat"),
                InlineKeyboardButton("Кнопка 2", callback_data="btn_2")
            )
            self.bot.send_message(msg.chat.id, "Выберите действие:", reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith("btn_"))
        def handle_button(call):
            user_id = call.from_user.id
            self.user_data[user_id] = call.data

            if call.data == "btn_stat":

                self.stat.statGame(call.message)

            elif call.data == "btn_2":
                self.bot.send_message(call.message.chat.id, "Вы нажали кнопку 2!")
            else:
                self.bot.send_message(call.message.chat.id, f"Вы нажали {call.data}")
