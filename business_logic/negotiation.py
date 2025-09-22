import init

class Negotiation:
    def __init__(self):
        self.bot = init.chatBot
        self.users = []

    def connekted(self):
        bot = self.bot
        users = self.users

        # стартовый хэндлер для команды /start
        @bot.message_handler(commands=['start'])
        def start_handler(message):
            user_id = message.from_user.id
            if user_id not in users and len(users) < 2:
                users.append(user_id)
                bot.send_message(user_id, "Вы подключены к анонимному чату.")
                bot.send_message(user_id, "debug status: True")

            if len(users) == 2:
                for uid in users:
                    bot.send_message(uid, "Анонимный чат начат!")

        print("test: Анонимный чат запущен")
