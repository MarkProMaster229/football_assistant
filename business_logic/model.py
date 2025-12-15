import requests

class Model:
    def __init__(self):
        pass

    def load(self, user_query):
        url = "http://localhost:11434/api/chat"
        
        system_prompt = (
    "Ты футбольный помощник клуба «Пари ФК НН». "
    "Отвечай максимально кратко, только по делу, минимум слов."
)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]

        payload = {
            "model": "deepseek-r1:14b",
            "messages": messages,
            "stream": False
        }

        r = requests.post(url, json=payload, timeout=300)
        r.raise_for_status()

        data = r.json()
        return data["message"]["content"]
