#include "utils.h"
#include <vtkm/cont/DataSet.h>
#include <vtkm/rendering/Color.h>
#include <vtkm/cont/Algorithm.h>


/*
 * 编译方法：
 * 1. Clion build project
 * 2. 手动编译
 *      mkdir build
 *      cd build
 *      cmake -DCMAKE_PREFIX_PATH=xxx ..
 *      make
 */

extern "C" {
void gen(const char* file_path, int width, int height, const char* output_path){

    std::cout << std::string(file_path) << std::endl;

    vtkm::cont::DataSet ds = load(file_path);

    vtkm::cont::ArrayHandle<vtkm::Float32> fieldArray;
    fieldArray.Allocate(ds.GetNumberOfPoints());
    vtkm::cont::ArrayHandleConstant<vtkm::Float32> constantField(1.0f, ds.GetNumberOfPoints());
    vtkm::cont::Algorithm::Copy(constantField, fieldArray);
    vtkm::cont::Field cField("constant", vtkm::cont::Field::Association::Points, fieldArray);
    ds.AddField(cField);


    do_mapper_wire_framer("constant", ds, width, height, output_path);
}
}

void gen1(const char* file_path, int width, int height, const char* output_path){
    std::cout << std::string(file_path) << std::endl;
    vtkm::cont::DataSet ds = load(file_path);

    vtkm::cont::ArrayHandle<vtkm::Float32> fieldArray;
    fieldArray.Allocate(ds.GetNumberOfPoints());
    vtkm::cont::ArrayHandleConstant<vtkm::Float32> constantField(1.0f, ds.GetNumberOfPoints());
    vtkm::cont::Algorithm::Copy(constantField, fieldArray);
    vtkm::cont::Field cField("constant", vtkm::cont::Field::Association::Points, fieldArray);
    ds.AddField(cField);


    do_mapper_wire_framer("constant", ds, width, height, output_path);
}