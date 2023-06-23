import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage
from langchain.tools import format_tool_to_openai_function

llm = ChatOpenAI(model="gpt-3.5-turbo-0613")

function_descriptions = [
    {
        "name": "seed_config_extract",
        "description": "提取有关流线撒点相关的配置项，例如区域、步长、种子点数量等",
        "parameters": {
            "type": "object",
            "properties": {
                "xmin": {
                    "type": "integer",
                    "description": "x轴边界的最小值，默认为-1",
                },
                "xmax": {
                    "type": "integer",
                    "description": "x轴边界的最大值，默认为-1",
                },
                "ymin": {
                    "type": "integer",
                    "description": "y轴边界的最小值，默认为-1",
                },
                "ymax": {
                    "type": "integer",
                    "description": "y轴边界的最大值，默认为-1",
                },
                "level": {
                    "type": "integer",
                    "description": "层数，即z坐标。默认值为0（表示表面，即最上层），最后一层为-1",
                },
                "nseeds": {
                    "type": "integer",
                    "description": "播撒的种子点的个数，默认值为-1",
                },
                "max_steps": {
                    "type": "integer",
                    "description": "最大步长，默认为2000",
                },
                "init_len": {
                    "type": "integer",
                    "description": "初始步长，默认为0.1",
                },
            },
        }
    }
]

user_request = "在x范围为0到123，y从0到50，种子点设置550个，最大步数3000"

first_response = llm.predict_messages([HumanMessage(content=user_request)],
                                      functions=function_descriptions
                                      )

function_name = first_response.additional_kwargs["function_call"]["name"]

arguments = first_response.additional_kwargs["function_call"]["arguments"]

# print(first_response.additional_kwargs)
print(json.loads(arguments))
