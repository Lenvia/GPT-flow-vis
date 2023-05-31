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
import experiment.flow.glo_var as glo_var
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
        print(json_config)
        # TODO 根据 json_config 调用 播撒函数，得到图片的路径

        if glo_var.file_name is None:
            return pic_path

        level = int(json_config["level"])

        try:
            # 生成流场vtk
            if not os.path.exists(
                    os.path.join(glo_var.vtk_base_dir, glo_var.file_name.split('.')[0] + '_' + str(level) + '.vtk')):
                nc2vtk(glo_var.file_name, glo_var.nc_base_dir, glo_var.vtk_base_dir, level)
            # 生成流线
            xmin = int(json_config["xmin"])
            xmax = int(json_config["xmax"])
            ymin = int(json_config["ymin"])
            ymax = int(json_config["ymax"])
            nseeds = int(json_config["nseeds"])

            generate_streamline(filename=glo_var.vtk_file_name,
                                vtk_base_dir=glo_var.vtk_base_dir,
                                streamline_base_dir=glo_var.streamline_base_dir,
                                xrange=[xmin, xmax],
                                yrange=[ymin, ymax],
                                level=level,
                                number_of_points=nseeds)

            # 生成图片
            pic_path = os.path.abspath(os.path.join(glo_var.pics_base_dir, glo_var.pics_name))
            make_snapshot(os.path.join(glo_var.streamline_base_dir, glo_var.streamline_file_name), glo_var.xdim,
                          glo_var.ydim)
            return pic_path

        except Exception as e:
            print(e)

        return pic_path

    return pic_path


def process_dataset(process_id, text):
    if glo_var.dataset_info is None:
        return -1, "Error"

    system_prompt = prompts[index2key[process_id]]
    query = glo_var.dataset_info + "\n\n" + text
    resp = chat(system_prompt, [query])  # 配置文件回答
    return 1, resp
