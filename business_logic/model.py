from gradio_client import Client
import time

class Model:
    def __init__(self, model_type="amd"):
        self.model_type = model_type
        self.client_amd = None
        self.client_markpro = None
        self.available_models = []
        self.last_health_check = 0
        
        self.system_prompt_amd = "Ты — бот-помощник для группы фанатов футбольного клуба 'Пари Нижний Новгород'. Ты очень любишь футбол и этот клуб. Твоя задача — помогать фанатам клуба с актуальной информацией: новостями, матчами, статистикой и обсуждениями. Общайся дружелюбно, с энтузиазмом и в духе спортивной атмосферы."
        self.temperature_amd = 0.4
        
        self._init_models_safe()
    
    def _init_models_safe(self):
        """Инициализация моделей без падений"""
        print("🔄 Инициализация моделей...")
        
        try:
            self.client_amd = Client("amd/gpt-oss-120b-chatbot", timeout=20)
            _ = self.client_amd.predict(
                message="test",
                system_prompt="test",
                temperature=0.1,
                api_name="/chat"
            )
            self.available_models.append("amd")
            print("✅ AMD модель доступна")
        except Exception as e:
            print(f"⚠️ AMD модель недоступна: {e}")
            self.client_amd = None
        
        try:
            self.client_markpro = Client("MarkProMaster229/host", timeout=20)
            _ = self.client_markpro.predict(
                prompt="test",
                api_name="/generate_text"
            )
            self.available_models.append("markpro")
            print("✅ Markpro модель доступна")
        except Exception as e:
            print(f"⚠️ Markpro модель недоступна: {e}")
            self.client_markpro = None
        
        print(f"📊 Доступные модели: {self.available_models}")
    
    def _check_and_reconnect(self):
        """Проверяем и переподключаем модели если нужно"""
        current_time = time.time()
        if current_time - self.last_health_check > 300:
            self.last_health_check = current_time
            self._init_models_safe()
    
    def generate_response(self, messages):
        self._check_and_reconnect()

        if not self.available_models:
            return "🤖 К сожалению, AI-модели временно недоступны. Мы уже работаем над восстановлением! Пока можете задавать вопросы о статистике и матчах."
        

        if "amd" in self.available_models and self.client_amd:
            try:
                result = self.client_amd.predict(
                    message=messages,
                    system_prompt=self.system_prompt_amd,
                    temperature=self.temperature_amd,
                    api_name="/chat",
                    timeout=30
                )
                print("Ответ от модели (amd):", result[:100] + "...")
                

                response_marker = "💬 Response:"
                if response_marker in result:
                    response_start_index = result.find(response_marker) + len(response_marker)
                    response_text = result[response_start_index:].strip()
                    return response_text
                elif result.strip():
                    return result.strip()
                
            except Exception as e:
                print(f"❌ Ошибка AMD модели: {e}")

                if "amd" in self.available_models:
                    self.available_models.remove("amd")
                self.client_amd = None
        

        if "markpro" in self.available_models and self.client_markpro:
            try:
                print("🔄 Используем Markpro модель...")
                result_markpro = self.client_markpro.predict(
                    prompt=messages,
                    api_name="/generate_text",
                    timeout=30
                )
                print("Ответ от модели (markpro):", result_markpro[:100] + "...")
                return result_markpro.strip()
                
            except Exception as e:
                print(f"❌ Ошибка Markpro модели: {e}")
                if "markpro" in self.available_models:
                    self.available_models.remove("markpro")
                self.client_markpro = None
        

        return "🤖 AI-модель временно недоступна. Пожалуйста, повторите запрос позже."
    
    def get_status(self):
        """Возвращает статус моделей для мониторинга"""
        return {
            "available_models": self.available_models,
            "total_models": 2,
            "amd_available": "amd" in self.available_models,
            "markpro_available": "markpro" in self.available_models
        }