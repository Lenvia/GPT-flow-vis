# from vtkmodules.all import *  # 当你不知道引入哪个包时，就打开本行注释，全部引入
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


def generate_streamline(filename, vtk_base_dir, streamline_base_dir, xrange=None, yrange=None, level=0,
                        number_of_points=1000):
    reader = vtkRectilinearGridReader()
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

    writer.SetFileName(os.path.join(streamline_base_dir, out_put))
    writer.SetInputConnection(streamer.GetOutputPort())
    writer.Write()

    print('done!')


def make_snapshot():
    # 读取 VTK 文件
    # 创建一个vtk reader
    reader = vtkPolyDataReader()
    reader.SetFileName('../data/streamlines/IWP_DAILY_20141123_526_2121.vtk')
    reader.Update()

    # 获取点的坐标
    polydata = reader.GetOutput()
    points = polydata.GetPoints()
    coords = vtk_to_numpy(points.GetData())

    scale = 3

    # 创建二维数组
    x_dim = 780 * scale
    y_dim = 480 * scale
    grid = np.zeros((x_dim, y_dim))

    # 遍历所有点，保存z坐标在0~1范围内的点到二维数组中
    for coord in coords:
        x, y, z = coord

        if np.nan in coord:
            continue
        if 0 <= z <= 1:
            grid[int(np.round(x * scale))][int(np.round(y * scale))] += 1

    # 打印二维数组
    # print(grid)

    # 使用matplotlib绘制二维数组

    # plt.colorbar(label='num')

    # plt.xlabel('X')
    # plt.ylabel('Y')
    # 去除白框
    plt.imshow(grid)
    plt.clim(0, max(1, int(5 / scale)))
    plt.axis('off')
    # plt.margins(0, 0)

    # 调整图像的边距
    plt.subplots_adjust(top=1, bottom=0, left=0, right=1, hspace=0, wspace=0)

    # plt.title('num')
    plt.savefig("temp.jpg", dpi=500, bbox_inches='tight', pad_inches=0)
    plt.show()


if __name__ == "__main__":
    generate_streamline(filename="IWP_DAILY_20141123.vtk",
                        vtk_base_dir="../data/vtk_flow_field",
                        streamline_base_dir="../data/streamlines",
                        xrange=[0, 780],
                        yrange=[0, 480],
                        level=0,
                        number_of_points=1000)

    # make_snapshot()
