from transformers import AutoTokenizer, AutoModelForCausalLM

class Model:
    def modelGeneration(self, user_query: str):
        
        model_name = "katanemo/Arch-Router-1.5B"

        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
            lm = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
        except OSError:
            print("Модель не найдена локально, качаю")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            lm = AutoModelForCausalLM.from_pretrained(model_name)

        messages = [
            {"role": "user", "content": user_query},
        ]

        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        ).to(lm.device)

        outputs = lm.generate(
            **inputs,
            max_new_tokens=40,
            do_sample=True,
            temperature=0.3,
            top_p=0.3,
        )

        gen_text = tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True)
        print(gen_text, "   выход")
        return gen_text
