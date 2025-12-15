import os
import init
import asyncio
import json

from telethon import TelegramClient
from telebot import types
from telebot import TeleBot, types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
class Negotiation:
    def __init__(self):
        self.bot = init.chatBot
        self.users = []
        self.tele_client = None
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")
        config_path = os.path.abspath(config_path)

        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
            self.api_id = config.get("api_id")
            self.api_hash = config.get("api_hash")
        else:
            self.api_id = None
            self.api_hash = None

    def connekted(self):
        bot = self.bot
        users = self.users
        def get_last_post_sync(channel_username):
            if not (self.api_id and self.api_hash):
                return "Нет API для Telegram, пост не может быть получен."
            from telethon import TelegramClient
            import asyncio

            async def fetch():
                async with TelegramClient('tele_session', self.api_id, self.api_hash) as client:
                    msgs = await client.get_messages(channel_username, limit=1)
                    if not msgs:
                        return "Нет сообщений в канале."
                    msg = msgs[0]
                    if msg.message:
                        return msg.message
                    elif hasattr(msg, 'text') and msg.text:
                        return msg.text
                    else:
                        return "Сообщение пустое или содержит только медиа."

            try:
                return asyncio.run(fetch())
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(fetch())
                loop.close()
                return result




        @bot.message_handler(commands=['start'])
        def start_handler(message):
            user_id = message.from_user.id
            bot.send_message(user_id, 
                             "⚽ **Фанатский бот ФК ПАРИ НН** ⚽\n\n"
                             "Привет! 👋 Вот список команд и возможностей нашего бота:\n\n"
                             "/start - 🏠 Главное меню\n"
                             "/stat - 📊 Статистика последних игр команды\n"
                             "/players - 👥 Информация о составе команды\n"
                             "/dialogue - 💬 Официальные группы команды\n"
                             "/nearEvent - 📅 Ближайшие игры\n"
                             "Поддержи свою команду! 🔥"
                             )



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
            if "Telegram" in team_name:
                last_post = get_last_post_sync("fcparinn")
                bot.send_message(call.message.chat.id, f"Последний пост канала:\n\n{last_post}")
