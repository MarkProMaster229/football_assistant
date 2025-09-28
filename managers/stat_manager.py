from business_logic.stat import Stat
import init

class StatManager:
    def __init__(self):
        self.stat = Stat()
        self.register_handlers()

    def register_handlers(self):
        @self.stat.bot.message_handler(commands=['stat'])
        def handle_stat_command(msg):
            self.stat.statGame(msg)
