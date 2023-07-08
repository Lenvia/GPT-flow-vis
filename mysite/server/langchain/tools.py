from typing import Optional, Type

from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class GetSeedConfigCheckInput(BaseModel):
    xmin: int = Field(..., description="x的最小值，默认为-1")
    xmax: int = Field(..., description="x的最大值，默认为-1")
    ymin: int = Field(..., description="y的最小值，默认为-1")
    ymax: int = Field(..., description="y的最大值，默认为-1")
    level: int = Field(..., description="层数，即z坐标。最上层为0，最下层为-1，默认值为0")
    nseeds: int = Field(..., description="播撒的种子点的个数，默认值为-1")
    max_steps: int = Field(..., description="最大步长，默认为2000")
    init_len: float = Field(..., description="初始步长，默认为0.1")


class GetSeedConfigTool(BaseTool):
    name = "seed_config_extract"
    description = """提取有关流线撒点相关的配置项，例如区域（x、y、z的范围）、步长、种子点数量等"""

    def _run(self, xmin: int, xmax: int, ymin: int, ymax: int, level: int, nseeds: int, max_steps: int,
             init_len: float):
        # get_seed_config_response = printParams(xmin, xmax, ymin, ymax, level, nseeds, max_steps, init_len)
        #
        # return get_seed_config_response
        return ""

    def _arun(self, fly_from: str, fly_to: str, date_from: str, date_to: str, sort: str):
        raise NotImplementedError("This tool does not support async")

    args_schema: Optional[Type[BaseModel]] = GetSeedConfigCheckInput
    verbose = True
