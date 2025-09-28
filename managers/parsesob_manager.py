import json
from business_logic.parsesob import FootballParser

class FootballParserManager:
    def __init__(self,output_file="matches.json"):
        self.output_file = output_file

    def edit_json(self):
        with open(self.output_file, "r", encoding="utf-8") as f:
            matches = json.load(f)
        for i in range(len(matches)):
            if "score" in matches[i] and "vs" in matches[i]["score"]:
                matches[i]["score"] = "матчу еще только предстоит быть"
                matches[i]["score_home"] = 0
                matches[i]["score_away"] = 0
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(matches, f, ensure_ascii=False, indent=4)

    def init(self):

        FootballParser.start()
        self.edit_json()
        print("успех")