# from vtkmodules.all import *  # 当你不知道引入哪个包时，就打开本行注释，全部引入
import os.path
import random
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkIOLegacy import *
import datetime


def generate_streamline(filename, vtk_base_dir, streamline_base_dir, xrange=None, yrange=None, zrange=None,
                        number_of_points=1000):
    reader = vtkRectilinearGridReader()
    reader.SetFileName(os.path.join(vtk_base_dir, filename))
    reader.Update()

    # 获取速度向量
    # vectors = reader.GetOutput().GetPointData().GetVectors()

    # 设置撒点区域
    xmin, xmax = xrange
    ymin, ymax = yrange
    zmin, zmax = zrange
    nseeds = number_of_points

    # 随机生成种子点
    seeds = vtkPoints()
    for i in range(nseeds):
        seed_x = random.uniform(xmin, xmax)
        seed_y = random.uniform(ymin, ymax)
        seed_z = random.uniform(zmin, zmax)
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

    writer.SetFileName(os.path.join(streamline_base_dir, out_put))
    writer.SetInputConnection(streamer.GetOutputPort())
    writer.Write()

    print('done!')


# generate_streamline(filename="/mysite/server/experiment/flow/temp/grid.vtk",
#                     xrange=[190, 590],
#                     yrange=[40, 440],
#                     zrange=[0, 32],
#                     number_of_points=500)
