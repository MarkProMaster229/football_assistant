# negotiation.py
import init

class Negotiation:
    def connekted(self):
        print("Хендлер зарегистрирован")
        bot = init.chatBot

        # хендлер на любые сообщения
        @bot.message_handler(func=lambda m: True)
        def any_message_handler(message):
            bot.send_message(message.chat.id, f"Принял сообщение: {message.text}")

        # хендлер на callback (кнопки)
        @bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            user_id = call.from_user.id
            chat_id = call.message.chat.id
            bot.send_message(chat_id, f"user_id={user_id}, chat_id={chat_id}")
