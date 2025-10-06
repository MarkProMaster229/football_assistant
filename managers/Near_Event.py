import init
import json

class Near_Event:
    def __init__(self, bot):
        self.bot = bot
        self.bot.register_message_handler(self.near_event_handler, commands=['nearEvent'])


    def nearEvent(self):
        with open("matches.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            dataNearEvent = []
            allEvent = []
            for i in range(len(data)):
                if data[i]["score"] == "матчу еще только предстоит быть":
                    dataNearEvent = data[i]
                    allEvent.append(dataNearEvent)

    def get_near_events(self):
        with open("matches.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        allEvent = [e for e in data if e.get("score") == "матчу еще только предстоит быть"]
        return allEvent

    def near_event_handler(self, message):
        user_id = message.from_user.id
        events = self.get_near_events()
        if not events:
            self.bot.send_message(user_id, "Скоро игр нет")
            return

        text_lines = [f"{e.get('home','?')} — {e.get('away','?')}  {e.get('date','?')} {e.get('time','?')}" for e in events]
        text = "Игры которые скоро будут:\n" + "\n".join(text_lines)
        self.bot.send_message(user_id, text)