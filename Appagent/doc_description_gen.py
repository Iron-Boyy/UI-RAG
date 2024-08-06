import os
from call_gpt import call_openai_completion_api
path = '/home/SENSETIME/luozhihao/code/AppAgent/Label.txt'
 
with open(path, "r") as w:
    doc_content = w.read()

INTRODUCTION_PROMPT = '''
I will provide the APP's name and it's ui elements' function description. You need to generate a detailed description for the APP. Guidelines: 1. Write a general overview of the API's purpose and functionality. 2. Use clear, concise language and avoid jargon, keeping the description under 300 tokens in length. Output with the following format:<APP name>:<APP's description>
'''
name = "Markor"

messages=[{
        "role": "system",
        "content": INTRODUCTION_PROMPT
    },
    {
    "role": "user",
    "content": "{\"name\":"+name+", \"ui elements description\":"+doc_content+"}"
    }]
model = "gpt-4o"
kwargs = {
    #"top_k":0.7,
    "temperature": 0.1,
    #"stream": False,
    # "max_new_tokens": 10
}
documention = call_openai_completion_api(messages, model, **kwargs)
documention = documention[0]['content'].content
print(documention)
# f = open("Markor_induction.txt",'a')
# f.write(doc_item)