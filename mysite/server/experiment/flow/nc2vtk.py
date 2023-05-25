import os.path

import xarray as xr
import numpy as np
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.util.vtkConstants import VTK_FLOAT
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkIOLegacy import vtkRectilinearGridWriter


def nc2vtk(file_name, nc_base_dir, vtk_base_dir):
    input_path = os.path.join(nc_base_dir, file_name)
    # 加载.nc文件
    ds = xr.open_dataset(input_path)

    # print(ds.variables)
    # print(ds.dims)
    # print(ds.coords)
    print(ds.info())

    # 提取u和v变量
    if len(ds.u.shape) == 4:
        u = ds.u.sel(time=ds.time[0]).values
        v = ds.v.sel(time=ds.time[0]).values
    else:
        u = ds.u.values
        v = ds.v.values

    # 获取坐标值并转换为 NumPy 数组
    depth = ds.depth.values
    lat = ds.lat.values
    lon = ds.lon.values

    # 创建网格信息
    xdim, ydim, zdim = len(lon), len(lat), len(depth)

    x = np.arange(0, xdim, 1, dtype='float64')  # np.arrange(起点，终点，步长）
    y = np.arange(0, ydim, 1, dtype='float64')
    z = np.arange(0, zdim, 1, dtype='float64')

    x_coo = numpy_to_vtk(num_array=x, deep=True, array_type=VTK_FLOAT)
    y_coo = numpy_to_vtk(num_array=y, deep=True, array_type=VTK_FLOAT)
    z_coo = numpy_to_vtk(num_array=z, deep=True, array_type=VTK_FLOAT)

    grid = vtkRectilinearGrid()
    grid.SetDimensions(xdim, ydim, zdim)
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

    output_path = os.path.join(vtk_base_dir, file_name)
    writer.SetFileName(output_path)
    writer.SetInputData(grid)
    writer.Write()

    print("done!")


if __name__ == '__main__':
    nc2vtk('IWP_DAILY_20141123.nc', "../data/nc_flow_field", "../data/vtk_flow_field")