import xarray as xr
import pyvista as pv
import numpy as np
from vtkmodules.util.numpy_support import numpy_to_vtk
from vtkmodules.util.vtkConstants import VTK_FLOAT
from vtkmodules.vtkCommonDataModel import vtkRectilinearGrid
from vtkmodules.vtkIOLegacy import vtkRectilinearGridWriter


def nc2vtk(input_path, output_path):
    # 加载.nc文件
    ds = xr.open_dataset(input_path)

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

    x = np.arange(0, xdim, 1, dtype='float64')  # np.arange(起点，终点，步长）
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

    writer.SetFileName(output_path)
    writer.SetInputData(grid)
    writer.Write()

    print("done!")


if __name__ == '__main__':
    nc2vtk('/Users/yy/Desktop/IWP_DAILY_20141123.nc', 'output.vtk')
