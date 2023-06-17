"""
@file: controller.py
@author: Runpu
@time: 2023/5/24 12:30
"""
import base64
import json
import os.path
import re

from .errors import Errors, err_msg
from .experiment.flow.vtk_helper import generate_streamline, make_snapshot, nc2vtk
from .gpt.prompts import prompts, Instruct
from .gpt.access import chat
from .experiment.flow.glo_var import gInfo, streamline_base_dir, vtk_base_dir, nc_base_dir, pics_base_dir
from server import connection
from .utils import *


def dispatch(text):
    system_prompt = prompts[Instruct.CONTROLLER]

    process_id = -1

    try:
        resp = chat(system_prompt, [text])
    except Exception as e:
        print(e)
        return Errors.GPT_ACCESS, process_id

    match = re.search(r"[-+]?\d*\.\d+|\d+", resp)

    if match:
        process_id = match.group()
        process_id = int(process_id)
    else:
        return Errors.UNKNOWN_INSTRUCT, process_id

    return Errors.SUCCESS, process_id


def handle_message(text):
    try:
        status, process_id = dispatch(text)
        # just for dev
        # process_id = 1
        # print("即将跳转：", process_id)

        if status != Errors.SUCCESS:  # 指令解析失败
            data = {
                'code': status,
                "id": process_id,
                "content": err_msg[status],
            }
            return data

        # 指令解析成功
        if process_id == Instruct.SEED:  # 撒点
            status, base64ImageData = process_seed(process_id, text)

            content = "流线已生成"
            if status != Errors.SUCCESS:
                content = err_msg[status],

            # 制作消息
            data = {
                'code': status,
                "id": process_id,
                "data": base64ImageData,
                "content": content
            }
        elif process_id == Instruct.DATASET_INFO:  # 询问数据集
            status, info = process_dataset(process_id, text)

            content = info
            if status != Errors.SUCCESS:
                content = err_msg[status],

            data = {
                'code': status,
                "id": process_id,
                "content": content,
            }

        else:  # 其他情况
            data = {
                'code': Errors.SUCCESS,
                "id": process_id,
                "content": err_msg[Errors.SUCCESS],
            }
        return data
    except Exception as e:  # 无法解析指令/GPT错误
        print(e)
        data = {
            'code': Errors.GPT_ACCESS,
            "id": -1,
            "content": err_msg[Errors.GPT_ACCESS],
        }
        return data


# seed 播撒种子点生成流线返回图像
def process_seed(process_id, text):
    system_prompt = prompts[process_id]
    resp = chat(system_prompt, [text])  # 配置文件回答

    pattern = r'<content>(.*?)</content>'  # 定义正则表达式，匹配包含在<content>标签中的内容
    matches = re.findall(pattern, resp, re.DOTALL)  # 考虑存在换行符
    matches = [match.replace('\n', '') for match in matches]

    base64ImageData = ""

    if len(matches) <= 0:  # 指令解析失败
        return Errors.UNKNOWN_INSTRUCT, base64ImageData

    match = matches[0]
    json_config = json.loads(match)  # 解析为JSON格式
    seedItem = json_config['seedItem']

    print(seedItem)
    # gInfo.print_attributes()

    # 根据 json_config 调用 播撒函数，得到图片的路径
    if seedItem is None or gInfo.file_name is None:
        return Errors.DEFAULT, base64ImageData

    try:
        level = int(seedItem['level'])

        # 生成流场vtk
        clip_name = gInfo.file_name.split('.')[0] + '_' + str(level) + '.vtk'
        clip_path = get_vtk_dir(clip_name)
        if not os.path.exists(clip_path):
            nc2vtk(gInfo.file_name, nc_base_dir, vtk_base_dir, level)
        else:  # 已经生成过切片了，那么 xdim, ydim这些信息是有的
            # dev 用
            gInfo.xdim = 780
            gInfo.ydim = 480
            gInfo.vtk_file_name = clip_name
            # print("Error")
            # return pic_path

        # 生成流线
        xmin = int(seedItem["xmin"])
        xmax = int(seedItem["xmax"])
        ymin = int(seedItem["ymin"])
        ymax = int(seedItem["ymax"])
        nseeds = int(seedItem["nseeds"])

        generate_streamline(filename=gInfo.vtk_file_name,
                            vtk_base_dir=vtk_base_dir,
                            streamline_base_dir=streamline_base_dir,
                            xrange=[xmin, xmax],
                            yrange=[ymin, ymax],
                            level=level,
                            number_of_points=nseeds)
        print("--------check--------", pics_base_dir, gInfo.pics_name)
        # 生成图片
        pic_path = get_abs_pics_dir(gInfo.pics_name)

        make_snapshot(file_name=get_streamline_dir(gInfo.streamline_file_name), width=2 * gInfo.xdim,
                      height=2 * gInfo.ydim, output=pic_path)

        with open(pic_path, 'rb') as f:
            image_data = f.read()
            base64ImageData = base64.b64encode(image_data).decode('utf-8')

    except Exception as e:
        print(e)
        return Errors.DEFAULT, base64ImageData

    return Errors.SUCCESS, base64ImageData


def process_dataset(process_id, text):
    if gInfo.dataset_info is None:
        return Errors.FILE_FORMAT, ""

    system_prompt = prompts[process_id]
    query = gInfo.dataset_info + "\n\n" + text
    resp = chat(system_prompt, [query])  # 配置文件回答
    return Errors.SUCCESS, resp
