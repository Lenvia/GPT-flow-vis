# from vtkmodules.all import *  # 当你不知道引入哪个包时，就打开本行注释，全部引入
import ctypes
import os.path
import random
import io
import datetime

import xarray as xr
import numpy as np

from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkPlane
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersCore import vtkCutter, vtkAppendPolyData
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkIOLegacy import *
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.util.vtkConstants import VTK_FLOAT, VTK_INT
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkIOLegacy import vtkRectilinearGridWriter

from glo_var import gInfo


def quicklook(input_path):
    # 加载.nc文件
    ds = xr.open_dataset(input_path)

    with io.StringIO() as buf:
        ds.info(buf=buf)
        gInfo.dataset_info = buf.getvalue()


def nc2vtk(file_name, nc_base_dir, vtk_base_dir, level=0):
    input_path = os.path.join(nc_base_dir, file_name)
    # 加载.nc文件
    ds = xr.open_dataset(input_path)

    # print(ds.variables)
    # print(ds.dims)
    # print(ds.coords)
    # print(ds.info())

    # 提取u和v变量
    if len(ds.u.shape) == 4:
        u = ds.u.sel(time=ds.time[0]).values
        v = ds.v.sel(time=ds.time[0]).values
    else:
        u = ds.u.values
        v = ds.v.values

    # 对nan值进行处理
    u = np.where(np.isnan(u), 0, u)
    v = np.where(np.isnan(v), 0, v)

    # 获取坐标值并转换为 NumPy 数组
    depth = ds.depth.values
    lat = ds.lat.values
    lon = ds.lon.values

    if level == -1:
        level = len(depth) - 1

    u = u[level]
    v = v[level]

    # 创建网格信息
    xdim, ydim, _ = len(lon), len(lat), len(depth)

    gInfo.xdim = xdim
    gInfo.ydim = ydim

    x = np.arange(0, xdim, 1, dtype='float64')  # np.arrange(起点，终点，步长）
    y = np.arange(0, ydim, 1, dtype='float64')
    z = np.arange(level, level + 1, 1, dtype='float64')

    x_coo = numpy_to_vtk(num_array=x, deep=True, array_type=VTK_FLOAT)
    y_coo = numpy_to_vtk(num_array=y, deep=True, array_type=VTK_FLOAT)
    z_coo = numpy_to_vtk(num_array=z, deep=True, array_type=VTK_FLOAT)

    grid = vtkRectilinearGrid()
    grid.SetDimensions(xdim, ydim, 1)
    grid.SetXCoordinates(x_coo)
    grid.SetYCoordinates(y_coo)
    grid.SetZCoordinates(z_coo)

    # 添加向量数据
    u = np.ravel(u)
    v = np.ravel(v)
    w = np.zeros_like(u)

    vectors = numpy_to_vtk(np.column_stack((u, v, w)), deep=True)
    vectors.SetName("Vectors")
    grid.GetPointData().SetVectors(vectors)

    # 写入vtk文件
    writer = vtkRectilinearGridWriter()

    gInfo.vtk_file_name = str(level) + '_' + file_name.split('.')[0] + '.vtk'  # 把层数放前面，方便时序

    output_path = os.path.join(vtk_base_dir, gInfo.vtk_file_name)
    writer.SetFileName(output_path)
    writer.SetInputData(grid)
    writer.Write()

    print("done!")


def generate_streamline(filename, vtk_base_dir, streamline_base_dir, xrange=None, yrange=None, level=0,
                        number_of_points=1000, max_steps=2000, init_len=0.1):
    reader = vtkRectilinearGridReader()

    print("--------check--------", vtk_base_dir, filename)
    reader.SetFileName(os.path.join(vtk_base_dir, filename))
    reader.Update()

    # 设置撒点区域
    xmin, xmax = xrange
    ymin, ymax = yrange
    nseeds = number_of_points

    # 随机生成种子点
    seeds = vtkPoints()
    for i in range(nseeds):
        seed_x = random.uniform(xmin, xmax)
        seed_y = random.uniform(ymin, ymax)
        # seed_z = random.uniform(zmin, zmax)
        seed_z = level
        seeds.InsertNextPoint((seed_x, seed_y, seed_z))
    source = vtkPolyData()
    source.SetPoints(seeds)

    # 生成流线
    streamer = vtkStreamTracer()
    streamer.SetInputConnection(reader.GetOutputPort())
    streamer.SetSourceData(source)
    streamer.SetInitialIntegrationStep(init_len)
    streamer.SetIntegratorTypeToRungeKutta45()
    streamer.SetIntegrationDirectionToBoth()
    # streamer.SetComputeVorticity(True)
    streamer.SetMaximumNumberOfSteps(max_steps)
    streamer.Update()  # 必须更新！！！！
    streamer_output = streamer.GetOutput()

    # 由于流线不具有边界，所以需要再插入4个孤立点
    isolated_point = vtkPoints()
    isolated_point.InsertNextPoint((0, 0, 0))
    isolated_point.InsertNextPoint((gInfo.xdim - 1, 0, 0))
    isolated_point.InsertNextPoint((0, gInfo.ydim - 1, 0))
    isolated_point.InsertNextPoint((gInfo.xdim - 1, gInfo.ydim - 1, 0))
    isolated_polydata = vtkPolyData()
    isolated_polydata.SetPoints(isolated_point)

    # 创建一个新的 vtkAppendPolyData 对象，用来组合流线和孤立点
    appendFilter = vtkAppendPolyData()
    appendFilter.AddInputData(streamer_output)  # 添加流线数据
    appendFilter.AddInputData(isolated_polydata)  # 添加孤立点数据
    appendFilter.Update()  # 更新 appendFilter
    combined_data = appendFilter.GetOutput()  # 获取合并后的数据

    # 保存流线为vtk文件
    writer = vtkPolyDataWriter()
    # 根据时间戳生成文件名
    now = datetime.datetime.now()
    out_put = filename.split('.')[0] + "_{}{}_{}{}.vtk".format(now.month, now.day, now.hour, now.minute)

    gInfo.streamline_file_name = out_put
    gInfo.pics_name = out_put.split('.')[0] + ".png"

    print("--------check--------", streamline_base_dir, out_put)
    writer.SetFileName(os.path.join(streamline_base_dir, out_put))

    writer.SetInputData(combined_data)
    # writer.SetInputConnection(streamer.GetOutputPort())

    writer.Write()

    print('done!')


def generate_pathline():
    pass


def make_snapshot(file_name, width, height, output):  # output 必须是绝对路径
    lib = ctypes.cdll.LoadLibrary('server/experiment/CProj/build/libstreamline.dylib')
    # 调用函数
    gen = lib.gen
    gen.restype = None
    gen.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
    gen(file_name.encode('utf-8'), width, height, output.encode('utf-8'))

    print("snapshot saved.")


if __name__ == "__main__":
    pass
    # for i in range(26, 32):
    #     nc2vtk('IWP_DAILY_201412'+str(i)+'.nc', "../data/nc_flow_field", "../data/vtk_flow_field")
    # quicklook('../data/nc_flow_field/IWP_DAILY_20141123.nc')

    # generate_streamline(filename="IWP_DAILY_20141123.vtk",
    #                     vtk_base_dir="../data/vtk_flow_field",
    #                     streamline_base_dir="../data/streamlines",
    #                     xrange=[0, 780],
    #                     yrange=[0, 480],
    #                     level=0,
    #                     number_of_points=1000)

    # make_snapshot(
    #     "../data/streamlines/IWP_DAILY_20141123_531_1621.vtk",
    #     780, 480, "/Users/yy/GithubProjects/GPT-flow-vis/mysite/server/experiment/111.png")
