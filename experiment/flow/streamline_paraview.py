"""
@file: streamline_paraview.py
@author: Runpu
@time: 2023/5/18 18:19
"""
from paraview.simple import *

paraview.simple._DisableFirstRenderCameraReset()


def generate_streamline(filename, output, center=[], number_of_points=1000, radius=200):
    # 加载 RectilinearGrid 类型的 vtk 文件
    grid = LegacyVTKReader(FileNames=[filename])

    point_source = PointSource()
    point_source.Center = center
    point_source.NumberOfPoints = number_of_points
    point_source.Radius = radius

    stream_tracer_with_custom_source = StreamTracerWithCustomSource(Input=grid,
                                                                    SeedSource=point_source)
    stream_tracer_with_custom_source.Vectors = ['POINTS', 'Vectors']
    stream_tracer_with_custom_source.MaximumStreamlineLength = 200.0
    stream_tracer_with_custom_source.IntegrationDirection = "BOTH"
    # stream_tracer.TerminalSpeed = 0.01
    #
    # # 执行 StreamTracer 过程对象
    stream_tracer_with_custom_source.UpdatePipeline()

    SaveData(output, proxy=stream_tracer_with_custom_source,
             PointDataArrays=['AngularVelocity', 'IntegrationTime', 'Normals', 'Rotation', 'Vectors', 'Vorticity'],
             CellDataArrays=['ReasonForTermination', 'SeedIds'])

    Delete(stream_tracer_with_custom_source)
    del stream_tracer_with_custom_source

    Delete(point_source)
    del point_source

    Delete(grid)
    del grid


generate_streamline(filename="/Users/yy/GithubProjects/GPT-flow-vis/experiment/flow/temp/grid.vtk",
                    output='/Users/yy/GithubProjects/GPT-flow-vis/experiment/flow/temp/streamline.vtk',
                    center=[369.96175149530234, 242.28417484032448, 15.894009023304633],
                    number_of_points=1000,
                    radius=200)
