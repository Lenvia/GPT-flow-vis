import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    HumanMessage,
    FunctionMessage,
    AIMessage,
    SystemMessage,
)
from langchain.tools import format_tool_to_openai_function

from functions import *
from tools import *

llm = ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo-0613')

messages = [SystemMessage(content="You are a rigorous assistant and ask you to be thoughtful in your answers.")]


def function_calling(text):
    messages.append(HumanMessage(content=text))
    tools = [GetSeedConfigTool(), GetDatasetInfoTool()]
    functions = [format_tool_to_openai_function(t) for t in tools]
    # print(functions)

    response_message = llm.predict_messages(
        messages, functions=functions
    )

    if response_message.additional_kwargs.get("function_call"):
        available_functions = {
            "seed_for_streamline": printParams,
            "get_dataset_info": printDatasetInfo,
        }
        # 获取将调用的方法和参数
        function_name = response_message.additional_kwargs["function_call"]["name"]
        function_to_call = available_functions[function_name]
        arguments = json.loads(response_message.additional_kwargs["function_call"]["arguments"])
        print(arguments)

        if function_name == "seed_for_streamline":
            args = SeedConfig(**arguments)

            arg_dict = vars(args)

            missing_params = [arg_name for arg_name, arg_value in arg_dict.items() if arg_value is None]

            if missing_params:
                # TODO 应该在这里加上进一步的推理，例如根据上下文
                descriptions = [param_descriptions.get(param_name) for param_name in missing_params]
                descriptions = [description for description in descriptions if description is not None]
                message = AIMessage(content=f"缺失参数：{', '.join(descriptions)}，请提供：")
                # message = AIMessage(content=f"{', '.join(missing_params)} 参数缺失，请提供：")
                print(message)
                supply = input("请提供缺失的参数：")
                messages.append(message)
                return function_calling(supply)

            # 执行完毕，不用继续请求chain
            return function_to_call(args)

        elif function_name == "get_dataset_info":
            function_response = function_to_call()
        else:
            function_response = empty()
            pass

        function_message = FunctionMessage(name=function_name, content=function_response)
        print(function_message)
        messages.append(function_message)
        response_message = llm.predict_messages(
            messages=messages, functions=functions
        )

    else:
        print("无需调用函数")
        pass

    return "AIの回答: " + response_message.content


if __name__ == '__main__':
    # output = function_calling("撒点的x范围为0到123，最大步数3000")
    output = function_calling(input("请输入指令："))

    print(output)
    # output = function_calling("在x范围为0到123，最大步数3000")
    # output = function_calling("数据集的信息是什么？")
    # print(output)
