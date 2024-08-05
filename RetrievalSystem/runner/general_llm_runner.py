# -*- coding: utf-8 -*-

import requests
import json
from .utils import clear_spe_tokens

template= '''
<|im_start|>system
请你扮演一个19岁的女孩，职业是个人助理，中国人，由商汤科技算法工程师创造。你总是客观、中立，不会评价和对比人物，不拉踩，不涉及政治，确保提供的信息是真实和准确的。在保护隐私和数据安全的前提下，你总是尊重每个人，并确保不会做任何可能伤害人类的事。 当用户需要你完成特定的写作或文案任务时，你应从一个普通、中立的角度来进行写作，不要带入“人工智能助手”、“AI语言模型”的身份。 注意，所有任务生成都需要遵循markdown格式，标题字号当放大、加粗；副标题/⼩标题字号适当放⼤、加粗；每个段落有间隔。<|im_end|>
<|im_start|>user
{query}<|im_end|>
<|im_start|>assistant
'''
def call_intern_general(query):
    url = 'http://101.230.144.204:8083/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        'inputs': template.replace("{query}", query),
        'parameters': {
            'do_sample': True,
            'ignore_eos': False,
            "max_new_tokens": 1024,
            "temperature": 0.001,
            "top_k": 5,
            "top_p": 0.85,
            "repetition_penalty": 1.05,
        }
    }

    response = requests.post(url, headers=headers, json=data)
    
    return clear_spe_tokens(response.json()["generated_text"][0])


if __name__ == '__main__':

    result = call_intern_general("x写个小诗歌，主题是恋爱日记。")
    print(result)

