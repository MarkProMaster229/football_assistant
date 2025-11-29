import os
from gradio_client import Client

class Model:
    def generate_response(self, messages):
        client = Client("MarkProMaster229/host")
        result = client.predict(
            prompt= messages,
            api_name="/generate_text"
            )
        print(result)
        gen_text = result
        return gen_text
    