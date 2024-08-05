import requests
import numpy as np


def get_embedding(text):
	
    API_URL = "https://api-inference.huggingface.co/models/BAAI/bge-small-zh-v1.5"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    output = query({
        "inputs": f"{text}",
    })[0][0]

    output = np.array(output,dtype=np.float32)

    output = output / np.linalg.norm(output)

    return output[np.newaxis,...]


if __name__ == '__main__':

    response = get_embedding("你好")
    print(response)
    print(response.shape)


