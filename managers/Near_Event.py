import init
import json

class Near_Event:

    def nearEvent(self):
        with open("matches.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            dataNearEvent = []
            allEvent = []
            for i in range(len(data)):
                if data[i]["score"] == "матчу еще только предстоит быть":
                    dataNearEvent = data[i]
                    allEvent.append(dataNearEvent)

        with open("dataNearEvent","w",encoding="utf-8") as f:
            json.dump(allEvent,f,ensure_ascii=False,indent=4)
            print (allEvent)


