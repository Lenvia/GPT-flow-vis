"""
@file: prompts.py
@author: Runpu
@time: 2023/5/25 21:47
"""

index2key = {

}

prompts = {
    "controller": "",  # 输入：用户指令 ｜ 输出：用户指令类型，跳转唯一标识符 ｜ 后续：根据标识符选择调用函数或转发给其他gpt
    "seed": "",  # 输入：用户撒点描述 ｜输出： json 格式的配置项（例如 xyz范围、撒点数等）｜后续：调用 streamline_vtk 生成流线

    "dataset_info": "",  # 输入：xr.open的到的数据集的 .info() 文本 ｜ 输出：json格式的数据集信息｜后续：返回给前端
    "render": "",  # 输入：用户指定的渲染样式 ｜ 输出：json格式的配置项 ｜ 后续：调用渲染函数
    "3": "",
    "4": "",
    "5": "",

}
