from mysite.server.langchain.tools import SeedConfig


def printParams(params: SeedConfig):
    paramStr = "已抽取到参数 xmin:{} xmax:{} ymin:{} ymax:{} level:{} nseeds:{} max_steps:{} init_len: {}" \
        .format(params.xmin, params.xmax, params.ymin, params.ymax, params.level, params.nseeds, params.max_steps,
                params.init_len)
    # print(paramStr)
    return paramStr


def empty():
    # print("------empty------")
    return "------empty------"


def printDatasetInfo():
    info = "数据集包含经度、纬度、温度、时间等信息"
    # print(info)
    return info
