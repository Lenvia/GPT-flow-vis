"""
@file: testclib.py
@author: Runpu
@time: 2023/5/30 15:19
"""
import ctypes


# 加载库
import os
import datetime

from mysite.server.experiment.flow.vtk_helper import extract_date


def test_render():
    lib = ctypes.cdll.LoadLibrary('CProj/build/librender.dylib')
    file_name = "/Users/yy/GithubProjects/GPT-flow-vis/mysite/server/experiment/data/streamlines/IWP_DAILY_20141123_531_1621.vtk"
    width = 780
    height = 480
    output = "/Users/yy/GithubProjects/GPT-flow-vis/mysite/server/experiment/test_render.png"

    # 调用函数
    gen = lib.gen
    gen.restype = None
    gen.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    gen(file_name.encode('utf-8'), width, height, output.encode('utf-8'))


def generate_pathline(filename_list, vtk_base_dir, pathline_base_dir, xrange=None, yrange=None, level=0,
                      number_of_points=1000, num_step=2000, step_size=0.5, inter_num=2):
    xmin, xmax = xrange
    ymin, ymax = yrange
    nseeds = number_of_points

    # 使用 sorted 函数进行排序，key 函数是上面定义的 extract_date 函数
    sorted_file_list = sorted(filename_list, key=extract_date)
    # 绝对路径
    sorted_file_list = [os.path.abspath(os.path.join(vtk_base_dir, f)) for f in sorted_file_list]

    # 根据时间戳生成文件名
    now = datetime.datetime.now()
    out_put = filename_list[0].split('.')[0] + "_{}{}_{}{}.vtk".format(now.month, now.day, now.hour, now.minute)
    out_put = os.path.join(pathline_base_dir, out_put)

    # 调用C++库
    lib = ctypes.cdll.LoadLibrary('CProj/build/libpathline.dylib')
    gen_pathline = lib.gen_pathline

    gen_pathline.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.c_long, ctypes.POINTER(ctypes.c_float),
                             ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_long, ctypes.c_float,
                             ctypes.c_int, ctypes.c_char_p]
    gen_pathline.restype = None

    num_file = len(sorted_file_list)
    array_type = ctypes.c_char_p * num_file

    file_list = array_type(*[str.encode(i) for i in sorted_file_list])

    xrange = (ctypes.c_float * 2)(xmin, xmax)
    yrange = (ctypes.c_float * 2)(ymin, ymax)

    gen_pathline(file_list, num_file, xrange, yrange, nseeds, num_step, step_size, inter_num, out_put.encode('utf-8'))


def test_pathline():
    generate_pathline(
        filename_list=[
            "0_IWP_DAILY_20141226.vtk",
            "0_IWP_DAILY_20141227.vtk",
            "0_IWP_DAILY_20141228.vtk",
            "0_IWP_DAILY_20141229.vtk",
            "0_IWP_DAILY_20141230.vtk",
        ],
        vtk_base_dir="data/vtk_flow_field",
        pathline_base_dir="data/pathlines",
        xrange=[0, 780],
        yrange=[0, 480],
        number_of_points=1000,
    )


if __name__ == '__main__':
    test_pathline()
