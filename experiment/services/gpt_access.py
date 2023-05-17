"""
@file: gpt_access.py
@author: Runpu
@time: 2023/5/17 16:37
"""

import requests
from ..configs.config import ENDPOINT, proxies, headers  # 配置
# from ..configs.no_proxy_config import ENDPOINT, headers  # 配置


def generate_response(prompt):
    data = {
        "messages": prompt,
        "model": "gpt-3.5-turbo",
        "max_tokens": 200,
        "temperature": 0.3,
        "n": 1
    }
    response = requests.post(ENDPOINT, headers=headers, json=data, proxies=proxies)
    # response = requests.post(ENDPOINT, headers=headers, json=data)
    print(response.json())
    try:
        response_text = response.json()['choices'][0]['message']['content']
    except:
        response_text = "服务器内部错误，请稍后重试"
    return response_text
