import json

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

function_descriptions = [
    {
        'name': 'seed_for_streamline', 'description': '提取有关流线撒点相关的配置项，例如区域、步长、种子点数量等',
        'parameters': {
            'title': 'GetSeedConfigCheckInput',
            'type': 'object',
            'properties': {
                'xmin': {'title': 'Xmin', 'description': 'x的最小值，默认为-1', 'type': 'integer'},
                'xmax': {'title': 'Xmax', 'description': 'x的最大值，默认为-1', 'type': 'integer'},
                'ymin': {'title': 'Ymin', 'description': 'y的最小值，默认为-1', 'default': -1,
                         'type': 'integer'},
                'ymax': {'title': 'Ymax', 'description': 'y的最大值，默认为-1', 'default': -1,
                         'type': 'integer'},
                'level': {'title': 'Level', 'description': '层数，即z坐标。默认值为0（表示表面，即最上层），最后一层为-1',
                          'default': 0, 'type': 'integer'},
                'nseeds': {'title': 'Nseeds', 'description': '播撒的种子点的个数，默认值为-1', 'type': 'integer'},
                'max_steps': {'title': 'Max Steps', 'description': '最大步长，默认为2000', 'default': 2000,
                              'type': 'integer'},
                'init_len': {'title': 'Init Len', 'description': '初始步长，默认为0.1', 'type': 'number'}},
            'required': ['xmin', 'xmax', 'nseeds', 'ymin', 'ymax', 'init_len']
        }
    }
]

# user_request = "在x范围为0到123，y从0到50，种子点设置550个，最大步数3000"
user_request = "最大步数3000"

first_response = llm.predict_messages([HumanMessage(content=user_request)],
                                      functions=function_descriptions)

function_name = first_response.additional_kwargs["function_call"]["name"]

arguments = first_response.additional_kwargs["function_call"]["arguments"]

print(json.loads(arguments))
