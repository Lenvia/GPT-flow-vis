def printParams(xmin: int, xmax: int, ymin: int, ymax: int, level: int, nseeds: int, max_steps: int,
                init_len: float):
    paramStr = "已抽取到参数 xmin:{} xmax:{} ymin:{} ymax:{} level:{} nseeds:{} max_steps:{} init_len{}" \
        .format(xmin, xmax, ymin, ymax, level, nseeds, max_steps, init_len)
    print(paramStr)
    return paramStr


def empty():
    print("------empty------")
    return "------empty------"
