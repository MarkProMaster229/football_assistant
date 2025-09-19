# init.py
import telebot
import json

chatBot = None

class Init2:
    def i(self):
        global chatBot
        with open('token.json', 'r') as f:
            config = json.load(f)

        token = config['token']
        chatBot = telebot.TeleBot(token)
        return chatBot
