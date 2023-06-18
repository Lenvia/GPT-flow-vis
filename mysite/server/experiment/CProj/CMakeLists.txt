cmake_minimum_required(VERSION 3.20)
project(vtkm_flow)

set(CMAKE_CXX_STANDARD 14)

# 设置 C 和 C++ 编译器标识文件
set(CMAKE_C_COMPILER_ID_RUN TRUE)
set(CMAKE_CXX_COMPILER_ID_RUN TRUE)

# 设置链接库的相关选项
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-t")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-t")

find_package(VTKm CONFIG REQUIRED)

IF(VTKm_FOUND)
    message("VTKm Founded")
ENDIF()

add_library(render SHARED savePic.cpp utils.cpp utils.h ViewNaive.cpp ViewNaive.h)
add_library(pathline SHARED pathline.cpp utils.cpp utils.h ViewNaive.cpp ViewNaive.h)

target_link_libraries(render PRIVATE vtkm_filter vtkm_rendering vtkm_io vtkm_cont)
target_link_libraries(pathline PRIVATE vtkm_filter vtkm_rendering vtkm_io vtkm_cont)
