# from vtkmodules.all import *  # 当你不知道引入哪个包时，就打开本行注释，全部引入
import ctypes
import os.path
import random

from vtkmodules.util import colors
from vtkmodules.util.numpy_support import vtk_to_numpy
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkPlane
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkIOLegacy import *
import datetime
import numpy as np
import matplotlib.pyplot as plt

from vtkmodules.vtkImagingCore import vtkImageReslice
from vtkmodules.vtkRenderingCore import vtkWindowToImageFilter, vtkDataSetMapper, vtkActor, vtkRenderer, \
    vtkRenderWindow, vtkRenderWindowInteractor, vtkPolyDataMapper

from .glo_var import gInfo


def generate_streamline(filename, vtk_base_dir, streamline_base_dir, xrange=None, yrange=None, level=0,
                        number_of_points=1000):
    reader = vtkRectilinearGridReader()

    print("--------check--------", vtk_base_dir, filename)
    reader.SetFileName(os.path.join(vtk_base_dir, filename))
    reader.Update()

    # 获取速度向量
    # vectors = reader.GetOutput().GetPointData().GetVectors()

    # 设置撒点区域
    xmin, xmax = xrange
    ymin, ymax = yrange
    # zmin, zmax = zrange
    nseeds = number_of_points

    # 随机生成种子点
    seeds = vtkPoints()
    for i in range(nseeds):
        seed_x = random.uniform(xmin, xmax)
        seed_y = random.uniform(ymin, ymax)
        # seed_z = random.uniform(zmin, zmax)
        seed_z = level
        seeds.InsertNextPoint(seed_x, seed_y, seed_z)
    source = vtkPolyData()
    source.SetPoints(seeds)

    # 生成流线
    streamer = vtkStreamTracer()
    streamer.SetInputConnection(reader.GetOutputPort())
    streamer.SetSourceData(source)
    streamer.SetMaximumPropagation(200.0)
    streamer.SetInitialIntegrationStep(0.1)
    streamer.SetIntegratorTypeToRungeKutta45()
    streamer.SetIntegrationDirectionToBoth()
    streamer.SetComputeVorticity(True)
    streamer.SetMaximumNumberOfSteps(2000)

    # streamer.SetComputeStreamFunction(True)
    # streamer.SetIntegrationStepUnitToCellLengthUnit()
    # streamer.SetInterpolatorTypeToCellLocator()
    # streamer.SetInterpolatorTypeToDataSetPointLocator()
    # streamer.SetInterpolatorTypeToKochanekSpline()

    # 保存流线为vtk文件
    writer = vtkPolyDataWriter()

    # 根据时间戳生成文件名
    now = datetime.datetime.now()
    out_put = filename.split('.')[0] + "_{}{}_{}{}.vtk".format(now.month, now.day, now.hour, now.minute)

    gInfo.streamline_file_name = out_put
    gInfo.pics_name = out_put.split('.')[0] + ".png"

    print("--------check--------", streamline_base_dir, out_put)
    writer.SetFileName(os.path.join(streamline_base_dir, out_put))
    writer.SetInputConnection(streamer.GetOutputPort())
    writer.Write()

    print('done!')


def make_snapshot(file_name, width, height, output):  # output 必须是绝对路径
    print(file_name, width, height, output)
    lib = ctypes.cdll.LoadLibrary('server/experiment/CProj/build/libstreamline.dylib')
    # 调用函数
    gen = lib.gen
    gen.restype = None
    gen.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    gen(file_name.encode('utf-8'), width, height, output.encode('utf-8'))


if __name__ == "__main__":
    # generate_streamline(filename="IWP_DAILY_20141123.vtk",
    #                     vtk_base_dir="../data/vtk_flow_field",
    #                     streamline_base_dir="../data/streamlines",
    #                     xrange=[0, 780],
    #                     yrange=[0, 480],
    #                     level=0,
    #                     number_of_points=1000)

    make_snapshot(
        "../data/streamlines/IWP_DAILY_20141123_531_1621.vtk",
        780, 480, "/Users/yy/GithubProjects/GPT-flow-vis/mysite/server/experiment/111.png")
