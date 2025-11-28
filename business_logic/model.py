import os
import gdown
import zipfile
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_URL = "https://drive.google.com/uc?export=download&id=1AhmxgWeZfPg7jXECf0GtF--tttEYaTdE"
LOCAL_DIR = "./local_model_dir/3"

def download_model_if_needed(url, local_dir):
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    model_file_path = os.path.join(local_dir, "model.zip")

    # Проверяем, есть ли распакованная модель
    # Так как после распаковки архив создаёт вложенную папку "3", сразу проверяем в ней
    inner_dir = os.path.join(local_dir, "3")
    config_path = os.path.join(inner_dir, "config.json")
    
    if not os.path.exists(config_path):
        # Скачиваем архив, если его нет
        if not os.path.exists(model_file_path):
            print(f"Скачивание модели по ссылке {url} в {local_dir}...")
            gdown.download(url, model_file_path, quiet=False)
            print("Скачивание завершено.")

        print("Распаковка архива...")
        with zipfile.ZipFile(model_file_path, 'r') as zip_ref:
            zip_ref.extractall(local_dir)  # архив создаст вложенную папку "3"
        print("Распаковка завершена.")
    else:
        print(f"Модель уже распакована в {inner_dir}. Пропускаем скачивание и распаковку.")

class Model:
    def __init__(self, local_path):
        # После распаковки модель лежит в ./local_model_dir/3/3
        absolute_path = os.path.abspath(os.path.join(local_path, "3"))
        print(f"Загрузка модели и токенизатора из абсолютного пути: {absolute_path}")    
        self.tokenizer = AutoTokenizer.from_pretrained(absolute_path)
        self.model = AutoModelForCausalLM.from_pretrained(absolute_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print("Модель готова к использованию.")
    
    def modelGeneration(self, user_query):
        inputs = self.tokenizer(user_query, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs['input_ids'],
            max_new_tokens=100,
            do_sample=True,
            temperature=0.3,
            top_p=0.3,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def generate_response(self, messages):
        inputs = self.tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=False,
            return_tensors="pt",
        ).to(self.device)

        outputs = self.model.generate(
            inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.3,
            top_p=0.3,
        )
        gen_text = self.tokenizer.decode(outputs[inputs.shape[-1]:], skip_special_tokens=True)
        print(f"Сгенерированный текст: {gen_text}")
        return gen_text

# Скачиваем и распаковываем модель, если нужно
download_model_if_needed(MODEL_URL, LOCAL_DIR)