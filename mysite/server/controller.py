"""
@file: controller.py
@author: Runpu
@time: 2023/5/24 12:30
"""
import json
import re
from .gpt.prompts import prompts, index2key
from .gpt.access import chat


def dispatch(text):
    system_prompt = prompts["controller"]
    resp = chat(system_prompt, [text])
    match = re.search(r"[-+]?\d*\.\d+|\d+", resp)
    if match:
        process_id = match.group()
        process_id = int(process_id)
    else:
        process_id = -1
        print("无效的指令")

    return process_id


def handle_message(text):
    try:
        process_id = dispatch(text)
        print("即将跳转：", process_id)

        if process_id == 1:
            process_1(process_id, text)

        # data = json.loads(text_data)
        # code = data.get('code')
        # message = data.get('message')
        #
        # if code is None or message is None:
        #     return "无效的消息格式:" + text_data
        #
        # # 根据状态码分类处理消息
        # res = None
        # if code == 100:
        #     res = process_status_100(message)
        # elif code == 200:
        #     res = process_status_200(message)
        # else:
        #     res = process_unknown_status(message)
        # return res

    except json.JSONDecodeError:
        return "无效的 JSON 格式"


# 示例处理函数，你可以根据实际需求进行替换
def process_1(process_id, text):
    system_prompt = prompts[index2key[process_id]]
    resp = chat(system_prompt, [text])

    print(resp)


def process_status_200(message):
    return message


def process_unknown_status(message):
    return message
