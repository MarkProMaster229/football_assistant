from business_logic.model import Model
import threading
import time

class IncludeModel:
    def __init__(self, bot):
        self.bot = bot
        self.lock = threading.Lock()
        self.busy = False
        self.current_user = None
        self.waiting_queue = []
        self.register_handlers()
        self.model = Model()

    def register_handlers(self):
        @self.bot.message_handler(commands=['model'])
        def handle_model_command(msg):
            with self.lock:
                user_id = msg.chat.id
                
                if user_id == self.current_user or user_id in self.waiting_queue:
                    self.bot.send_message(user_id, "Вы уже в очереди. Дождитесь ответа.")
                    return
                

                if self.busy:
                    self.waiting_queue.append(user_id)
                    position = len(self.waiting_queue)
                    self.bot.send_message(
                        user_id, 
                        f"Бот занят. Вы в очереди, позиция: {position}. Ожидайте..."
                    )
                    return
                
                self.busy = True
                self.current_user = user_id
                
            self.bot.send_message(user_id, "Напиши свой вопрос, помощник ответит на него.")
        
        @self.bot.message_handler(func=lambda m: True)
        def handle_text(msg):
            user_id = msg.chat.id
            
            with self.lock:
                if user_id != self.current_user:
                    return
            
            user_query = msg.text
            
            self.bot.send_message(user_id, "🔄 Ваш ответ создается, подождите...")

            self.bot.send_chat_action(user_id, 'typing')
            
            try:
                result = self.model.load(user_query)
                
                self.bot.send_message(user_id, result)
                
            except Exception as e:
                self.bot.send_message(user_id, f"Ошибка при генерации: {e}")
                
            finally:
                with self.lock:
                    self.busy = False
                    self.current_user = None
                    
                    if self.waiting_queue:
                        next_user = self.waiting_queue.pop(0)
                        self.busy = True
                        self.current_user = next_user
                        threading.Thread(
                            target=self.notify_next_user,
                            args=(next_user,)
                        ).start()
    
    def notify_next_user(self, user_id):
        time.sleep(0.1)
        self.bot.send_message(
            user_id, 
            "Теперь ваша очередь! Напишите свой вопрос."
        )