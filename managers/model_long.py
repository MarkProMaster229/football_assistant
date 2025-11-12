from business_logic.working_data import Work
import init
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from managers.parser_manager import ParserManager
import threading

class IncludeModel:
    def __init__(self, bot):
        from business_logic.model import Model
        from business_logic.stat import Stat

        self.bot = bot
        self.model = Model()
        self.stat = Stat()
        self.lock = threading.Lock()
        self.busy = False
        self.waiting_users = set()
        self.register_handlers()

    def register_handlers(self):
        @self.bot.message_handler(commands=['model'])
        def handle_model_command(msg):
            if self.busy:
                self.bot.send_message(msg.chat.id, "Сейчас бот занят другим пользователем. Попробуйте чуть позже.")
                return

            self.busy = True
            self.bot.send_message(msg.chat.id, "Напиши свой вопрос, помощник ответит на него.")
            self.waiting_users.add(msg.chat.id)
            
        @self.bot.message_handler(func=lambda m: True)
        def handle_text(msg):
            if msg.chat.id not in self.waiting_users:
                return
            self.bot.send_chat_action(msg.chat.id, 'typing')
            user_query = msg.text
            try:
                result = self.model.modelGeneration(user_query)
                self.bot.send_message(msg.chat.id, result)
            except Exception as e:
                self.bot.send_message(msg.chat.id, f"Ошибка при генерации: {e}")
            finally:
                self.waiting_users.remove(msg.chat.id)
                self.busy = False

