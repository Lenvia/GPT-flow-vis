"""
@file: global.py
@author: Runpu
@time: 2023/5/25 18:58
"""


nc_base_dir = 'server/experiment/data/nc_flow_field'
vtk_base_dir = 'server/experiment/data/vtk_flow_field'
streamline_base_dir = 'server/experiment/data/streamlines'
pics_base_dir = 'server/experiment/data/pics'

file_name = None  # xxx.nc
vtk_file_name = None  # 当前第几层的流场vtk
streamline_file_name = None
pics_name = None

dataset_info = None

xdim = None
ydim = None
