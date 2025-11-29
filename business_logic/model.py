from gradio_client import Client

class Model:
    def __init__(self, model_type="amd"):

        if model_type == "amd":
            self.client_amd = Client("amd/gpt-oss-120b-chatbot")
            self.api_name_amd = "/chat"
            self.system_prompt_amd = "Ты — бот-помощник для группы фанатов футбольного клуба 'Пари Нижний Новгород'. Ты очень любишь футбол и этот клуб. Твоя задача — помогать фанатам клуба с актуальной информацией: новостями, матчами, статистикой и обсуждениями. Общайся дружелюбно, с энтузиазмом и в духе спортивной атмосферы."
            self.temperature_amd = 0.4
        elif model_type == "markpro":
            self.client_markpro = Client("MarkProMaster229/host")
            self.api_name_markpro = "/generate_text"
        else:
            raise ValueError("Неверный тип модели. Используйте 'amd' или 'markpro'.")

    def generate_response(self, messages):
        try:
            result = self.client_amd.predict(
                message=messages,
                system_prompt=self.system_prompt_amd,
                temperature=self.temperature_amd,
                api_name=self.api_name_amd
            )
            print("Ответ от модели (amd):", result)
            response_marker = "💬 Response:"
            if response_marker in result:
                response_start_index = result.find(response_marker) + len(response_marker)
                response_text = result[response_start_index:].strip()
                return response_text
            elif result.strip():
                return result.strip()
            else:
                raise Exception("Ответ от модели 'amd' пустой или некорректный.")
        except Exception as e:
            print(f"Ошибка при запросе к модели 'amd': {e}")
            print("Попытка использовать модель 'markpro'...")
            try:
                result_markpro = self.client_markpro.predict(
                    prompt=messages,
                    api_name=self.api_name_markpro
                )
                print("Ответ от модели (markpro):", result_markpro)
                return result_markpro.strip()
            except Exception as e:
                print(f"Ошибка при запросе к модели 'markpro': {e}")
                return "Не удалось получить ответ от обеих моделей."
