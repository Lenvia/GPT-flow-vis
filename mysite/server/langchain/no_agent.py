import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    FunctionMessage,
    AIMessage,
)
from langchain.tools import format_tool_to_openai_function

from functions import *
from tools import *

llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-0613')

messages = []


def function_calling(text):
    messages.append(HumanMessage(content=text))
    tools = [GetSeedConfigTool()]
    functions = [format_tool_to_openai_function(t) for t in tools]

    response_message = llm.predict_messages(
        messages, functions=functions
    )

    if response_message.additional_kwargs.get("function_call"):
        available_functions = {
            "seed_config_extract": printParams,
        }
        # 获取将调用的方法和参数
        function_name = response_message.additional_kwargs["function_call"]["name"]
        function_to_call = available_functions[function_name]
        arguments = json.loads(response_message.additional_kwargs["function_call"]["arguments"])

        if function_name == "seed_config_extract":
            if arguments.get("init_len") is None:
                messages.append(AIMessage(content="init_len 参数缺失，请提供："))
                supply = input("请提供 init_len：")
                return function_calling(supply)

            function_response = function_to_call(
                xmin=arguments.get("xmin"),
                xmax=arguments.get("xmax"),
                ymax=arguments.get("ymax"),
                ymin=arguments.get("ymin"),
                level=arguments.get("level"),
                nseeds=arguments.get("nseeds"),
                max_steps=arguments.get("max_steps"),
                init_len=arguments.get("init_len"),
            )
        else:
            function_response = empty()

        function_message = FunctionMessage(name=function_name, content=function_response)
        messages.append(function_message)
        response_message = llm.predict_messages(
            messages=messages, functions=functions
        )

    else:
        print("无需调用函数")
        pass

    return "AIの回答: " + response_message.content


if __name__ == '__main__':
    output = function_calling("在x范围为0到123，最大步数3000")
    print(output)
