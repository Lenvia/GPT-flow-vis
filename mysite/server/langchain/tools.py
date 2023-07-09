from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

# 参数描述字典
param_descriptions = {
    "xmin": "x 最小值",
    "xmax": "x 最大值",
    "ymin": "y 最小值",
    "ymax": "y 最大值",
    "level": "层数（深度）",
    "nseeds": "种子点的个数",
    "max_steps": "最大步数",
    "init_len": "初始步长"
}


# SeedConfig 撒点配置项
class SeedConfig(object):
    def __init__(self, xmin, xmax, ymin=None, ymax=None, level=0, nseeds=None, max_steps=3000, init_len=None):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.level = level
        self.nseeds = nseeds
        self.max_steps = max_steps
        self.init_len = init_len


class GetSeedConfigCheckInput(BaseModel):
    xmin: int = Field(..., description="x的最小值，默认为-1")
    xmax: int = Field(..., description="x的最大值，默认为-1")
    ymin: int = Field(..., description="y的最小值，默认为-1")
    ymax: int = Field(..., description="y的最大值，默认为-1")
    level: int = Field(..., description="层数，即z坐标。最上层为0，最下层为-1，默认值为0")
    nseeds: int = Field(..., description="播撒的种子点的个数，默认为1000")
    max_steps: int = Field(..., description="最大步长，默认为2000")
    init_len: float = Field(..., description="初始步长，默认为0.1")


# GetSeedConfigTool 获取撒点配置项，并后续调用撒点函数生成流线、轨迹线
class GetSeedConfigTool(BaseTool):
    name = "seed_for_streamline"
    description = """提取有关流线撒点相关的配置项，例如区域（x、y、z的范围）、步长、种子点数量等"""

    def _run(self, xmin: int, xmax: int, ymin: int, ymax: int, level: int, nseeds: int, max_steps: int,
             init_len: float):
        return ""

    def _arun(self, fly_from: str, fly_to: str, date_from: str, date_to: str, sort: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetSeedConfigCheckInput
    verbose = True


# GetDatasetInfoTool 查看数据集信息
class GetDatasetInfoTool(BaseTool):
    name = "get_dataset_info"
    description = """查看数据集的信息，例如属性、维度、取值范围等"""

    def _run(self):
        return ""

    def _arun(self, fly_from: str, fly_to: str, date_from: str, date_to: str, sort: str):
        raise NotImplementedError("This tool does not support async")

    verbose = True
