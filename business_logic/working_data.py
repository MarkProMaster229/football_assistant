from managers.parser_manager import ParserManager

class Work:

    def __init__(self):
        self.parser = ParserManager()
        self.players_array = []

    def work(self):


        data = self.parser.parserInit()
        for player in data:
            self.players_array.append([player["number"], player["name"], player["position"]])
            print(player["number"], player["name"], player["position"])