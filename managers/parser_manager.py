import os
import time
from datetime import datetime, timedelta
import json

from business_logic.parse import Parse

class ParserManager:
    def __init__(self):
        self.parser = Parse()
        self.file_path = 'players.json'
        self.update_interval = timedelta(hours=24)
    def parserInit(self):
        if os.path.exists(self.file_path):
            last_modified = datetime.fromtimestamp(os.path.getmtime(self.file_path))
            now = datetime.now()

            if now - last_modified < self.update_interval:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print("Используем кэшированный файл JSON")
                return data

        print("Обновляем JSON через парсер")
        self.parser.parser()

        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data