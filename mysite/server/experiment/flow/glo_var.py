"""
@file: global.py
@author: Runpu
@time: 2023/5/25 18:58
"""


nc_base_dir = 'server/experiment/data/nc_flow_field'
vtk_base_dir = 'server/experiment/data/vtk_flow_field'
streamline_base_dir = 'server/experiment/data/streamlines'
pics_base_dir = 'server/experiment/data/pics'
pathline_base_dir = 'server/experiment/data/pathlines'


class Info:
    def __init__(self):
        self.file_type = 0  # 默认流线
        self.file_name = None  # xxx.nc
        self.vtk_file_name = None  # 当前第几层的流场vtk
        self.streamline_file_name = None
        self.pics_name = None
        self.dataset_info = None
        self.xdim = None
        self.ydim = None

        self.file_name_list = []

    def empty(self):
        self.file_type = 0  # 默认流线
        self.file_name = None  # xxx.nc
        self.vtk_file_name = None  # 当前第几层的流场vtk
        self.streamline_file_name = None
        self.pics_name = None
        self.dataset_info = None
        self.xdim = None
        self.ydim = None

        self.file_name_list = []

    def print_attributes(self):
        for attr in dir(self):
            if not callable(getattr(self, attr)) and not attr.startswith("__"):
                print(f'{attr} : {getattr(self, attr)}')


gInfo = Info()
