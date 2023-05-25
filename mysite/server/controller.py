"""
@file: controller.py
@author: Runpu
@time: 2023/5/24 12:30
"""
import json
import os
import openai


# From the IPython.display package, import display and Markdown
# from IPython.display import display, Markdown

openai.api_key = os.getenv("OPENAI_API_KEY")


def handle_message(text_data):
    try:
        data = json.loads(text_data)
        code = data.get('code')
        message = data.get('message')

        if code is None or message is None:
            return "无效的消息格式:" + text_data

        # 根据状态码分类处理消息
        res = None
        if code == 100:
            res = process_status_100(message)
        elif code == 200:
            res = process_status_200(message)
        else:
            res = process_unknown_status(message)
        return res

    except json.JSONDecodeError:
        return "无效的 JSON 格式:"+text_data


# 示例处理函数，你可以根据实际需求进行替换
def process_status_100(message):
    return message


def process_status_200(message):
    return message


def process_unknown_status(message):
    return message


def chat(system, user_assistant):
    assert isinstance(system, str), "`system` should be a string"
    assert isinstance(user_assistant, list), "`user_assistant` should be a list"
    system_msg = [{"role": "system", "content": system}]
    user_assistant_msgs = [
        {"role": "assistant", "content": user_assistant[i]} if i % 2 else {"role": "user", "content": user_assistant[i]}
        for i in range(len(user_assistant))]

    msgs = system_msg + user_assistant_msgs
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=msgs)
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."
    return response["choices"][0]["message"]["content"]


response_fn_test = chat("You are a machine learning expert.", ["Explain what a neural network is."])
# display(Markdown(response_fn_test))
