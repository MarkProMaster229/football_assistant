import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Stat:
    def __init__(self):
        self.bot = init.chatBot
        self.users = []

    def match(self):#не математика, а матч
        bot = self.bot
        users = self.users

        @bot.message_handler(commands=['match'])
        def start(msg):
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton("Расписание матчей", callback_data="schedule"))
            keyboard.add(InlineKeyboardButton("Состав команды", callback_data="squad"))
            bot.send_message(msg.chat.id, "Выберите действие:", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            if call.data == "schedule":
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, "Здесь будет расписание матчей")
            elif call.data == "squad":
                bot.answer_callback_query(call.id)
                bot.send_message(call.message.chat.id, "Здесь будет состав команды")

