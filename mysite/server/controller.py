"""
@file: controller.py
@author: Runpu
@time: 2023/5/24 12:30
"""
import json
import os.path
import re

from .experiment.flow.streamline_vtk import generate_streamline, make_snapshot
from .gpt.prompts import prompts, index2key
from .gpt.access import chat
from .experiment.flow.glo_var import gInfo, streamline_base_dir, vtk_base_dir, nc_base_dir, pics_base_dir
from .experiment.flow.nc2vtk import nc2vtk


def dispatch(text):
    system_prompt = prompts["controller"]
    resp = chat(system_prompt, [text])
    match = re.search(r"[-+]?\d*\.\d+|\d+", resp)
    if match:
        process_id = match.group()
        process_id = int(process_id)
    else:
        process_id = -1
        print("无效的指令")

    return process_id


def handle_message(text):
    try:
        process_id = dispatch(text)
        print("即将跳转：", process_id)

        if process_id == 1:  # 撒点
            pic_path = process_seed(process_id, text)
            # 制作消息
            data = {
                "id": 1,
                "data": pic_path
            }
        if process_id == 3:  # 询问数据集
            status, info = process_dataset(process_id, text)
            data = {
                "id": 3,
                "data": info,
                "status": status
            }

        return data
    except Exception as e:
        print(e)
        return None


# seed 播撒种子点生成流线返回图像
def process_seed(process_id, text):
    system_prompt = prompts[index2key[process_id]]
    resp = chat(system_prompt, [text])  # 配置文件回答

    pattern = r'<content>(.*?)</content>'  # 定义正则表达式，匹配包含在<content>标签中的内容
    matches = re.findall(pattern, resp, re.DOTALL)  # 考虑存在换行符
    matches = [match.replace('\n', '') for match in matches]

    pic_path = ""
    if len(matches) > 0:
        match = matches[0]
        json_config = json.loads(match)  # 解析为JSON格式
        seedItem = json_config['seedItem']

        print(seedItem)
        gInfo.print_attributes()

        # TODO 根据 json_config 调用 播撒函数，得到图片的路径

        if seedItem is None or gInfo.file_name is None:
            print("Error")
            return pic_path

        try:
            level = int(seedItem['level'])

            # 生成流场vtk
            clip_name = gInfo.file_name.split('.')[0] + '_' + str(level) + '.vtk'
            clip_path = os.path.join(vtk_base_dir, clip_name)
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

            print("--------check--------")
            generate_streamline(filename=gInfo.vtk_file_name,
                                vtk_base_dir=vtk_base_dir,
                                streamline_base_dir=streamline_base_dir,
                                xrange=[xmin, xmax],
                                yrange=[ymin, ymax],
                                level=level,
                                number_of_points=nseeds)
            print("--------check--------", pics_base_dir, gInfo.pics_name)
            # 生成图片
            pic_path = os.path.abspath(os.path.join(pics_base_dir, gInfo.pics_name))

            make_snapshot(file_name=os.path.join(streamline_base_dir, gInfo.streamline_file_name), width=gInfo.xdim,
                          height=gInfo.ydim, output=pic_path)
            return gInfo.pics_name

        except Exception as e:
            print(e)

        return pic_path

    return pic_path


def process_dataset(process_id, text):
    if gInfo.dataset_info is None:
        return -1, "Error"

    system_prompt = prompts[index2key[process_id]]
    query = gInfo.dataset_info + "\n\n" + text
    resp = chat(system_prompt, [query])  # 配置文件回答
    return 1, resp