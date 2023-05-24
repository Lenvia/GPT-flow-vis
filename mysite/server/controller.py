"""
@file: controller.py
@author: Runpu
@time: 2023/5/24 12:30
"""
# Import the os package
import os

# Import the openai package
import openai

# From the IPython.display package, import display and Markdown
# from IPython.display import display, Markdown

openai.api_key = os.getenv("OPENAI_API_KEY")


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