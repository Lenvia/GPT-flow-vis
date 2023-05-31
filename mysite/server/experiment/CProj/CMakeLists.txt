cmake_minimum_required(VERSION 3.20)
project(vtkm_flow)

set(CMAKE_CXX_STANDARD 14)

find_package(VTKm CONFIG REQUIRED)

IF(VTKm_FOUND)
    message("VTKm Founded")
ENDIF()



# add_executable(vtkm_flow main.cpp utils.cpp draw.cpp draw.h utils.h ViewNaive.cpp ViewNaive.h savePic.cpp savePic.h)

add_library(streamline SHARED savePic.cpp utils.cpp utils.h ViewNaive.cpp ViewNaive.h)

target_link_libraries(streamline PRIVATE vtkm_filter vtkm_rendering vtkm_io vtkm_cont)

# target_link_libraries(vtkm_flow PRIVATE vtkm_filter vtkm_rendering vtkm_io vtkm_cont)
