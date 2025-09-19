import telebot
import json
class Init2:
    def i(self):
        with open('token.json', 'r') as f:
            config = json.load(f)

        token = config['token']
        chatBot = telebot.TeleBot(token)
        return chatBot