import os
from .experiment.flow.glo_var import gInfo, nc_base_dir, vtk_base_dir, streamline_base_dir, pics_base_dir, pathline_base_dir


def get_nc_dir(file_name):
    return os.path.join(nc_base_dir, file_name)


def get_vtk_dir(file_name):
    return os.path.join(vtk_base_dir, file_name)


def get_pics_dir(file_name):
    return os.path.join(pics_base_dir, file_name)


def get_streamline_dir(file_name):
    return os.path.join(streamline_base_dir, file_name)


def get_pathline_dir(file_name):
    return os.path.join(pathline_base_dir, file_name)


def get_abs_nc_dir(file_name):
    return os.path.abspath(get_nc_dir(file_name))


def get_abs_vtk_dir(file_name):
    return os.path.abspath(get_vtk_dir(file_name))


def get_abs_pics_dir(file_name):
    return os.path.abspath(get_pics_dir(file_name))


def get_abs_streamline_dir(file_name):
    return os.path.abspath(get_streamline_dir(file_name))


def get_abs_pathline_dir(file_name):
    return os.path.abspath(get_pathline_dir(file_name))