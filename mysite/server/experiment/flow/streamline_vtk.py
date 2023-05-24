# from vtkmodules.all import *  # 当你不知道引入哪个包时，就打开本行注释，全部引入
import random
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkIOLegacy import *


def generate_streamline(filename, output, xrange=None, yrange=None, zrange=None, number_of_points=1000):
    reader = vtkRectilinearGridReader()
    reader.SetFileName(filename)
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
    writer.SetFileName(output)
    writer.SetInputConnection(streamer.GetOutputPort())
    writer.Write()

    print('done!')


generate_streamline(filename="/mysite/server/experiment/flow/temp/grid.vtk",
                    output='/Users/yy/GithubProjects/GPT-flow-vis/experiment/flow/temp/streamline2.vtk',
                    xrange=[190, 590],
                    yrange=[40, 440],
                    zrange=[0, 32],
                    number_of_points=500)
