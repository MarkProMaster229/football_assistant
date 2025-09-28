import init
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
class Negotiation:
    def __init__(self):
        self.bot = init.chatBot
        self.users = []


    def connekted(self):
        bot = self.bot
        users = self.users


        # стартовый хэндлер для команды /start
        #@bot.message_handler(commands=['start'])
        #def start_handler(message):
            #user_id = message.from_user.id
            #if user_id not in users and len(users) < 2:
                #users.append(user_id)
                #bot.send_message(user_id, "Вы подключены к анонимному чату.")
                #bot.send_message(user_id, "debug status: True")

            #if len(users) == 2:
                #for uid in users:
                    #bot.send_message(uid, "Анонимный чат начат!")

        #print("test: Анонимный чат запущен")
        user_teams = {}
        @bot.message_handler(commands=['dialogue'])
        def dialogue(message):
            dialogue = ["PariNN(офиц.канал Telegram)", "PariNN(офиц.канал VK)"]

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            for d in dialogue:
                keyboard.add(types.InlineKeyboardButton(d, callback_data=f"team_{d}"))
            bot.send_message(message.chat.id, "Выберите команду:", reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: call.data.startswith("team_"))
        def dialoge_selected(call):
            team_name = call.data.split("_", 1)[1]
            team_links = {
                "PariNN(офиц.канал Telegram)": "https://t.me/fcparinn",
                "PariNN(офиц.канал VK)": "http://vk.com/fcparinn",
                }

            link = team_links.get(team_name, "https://example.com")
            user_teams[call.from_user.id] = team_name
            bot.send_message(call.message.chat.id, f"Вы выбрали команду: {team_name}")
            bot.send_message(
                chat_id=call.message.chat.id,
                text=f"Вы выбрали команду: [{team_name}]({link})",
                parse_mode="Markdown"
                )


