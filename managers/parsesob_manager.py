from business_logic.parsesob import FootballParser

class FootballParserManager:
    def __init__(self):
        self.s = 2

    def init(self):
        FootballParser.start()
        print("успех")