//
// Created by 岳润璞 on 2023/5/30.
//

#include <vtkm/io/VTKDataSetReader.h>
#include <vtkm/io/VTKDataSetWriter.h>
#include <vtkm/rendering/Actor.h>
#include <vtkm/rendering/CanvasRayTracer.h>
#include <vtkm/rendering/MapperRayTracer.h>
#include <vtkm/rendering/MapperVolume.h>
#include <vtkm/rendering/MapperWireframer.h>
#include <vtkm/rendering/MapperPoint.h>
#include <vtkm/rendering/MapperCylinder.h>
#include <vtkm/rendering/MapperQuad.h>
#include <vtkm/rendering/Scene.h>
#include <vtkm/rendering/View3D.h>

#include <vtkm/cont/Initialize.h>
#include <vtkm/cont/ArrayHandle.h>
#include <vtkm/cont/DataSetBuilderExplicit.h>
#include <vtkm/cont/DataSetBuilderUniform.h>

#include <vtkm/filter/ClipWithImplicitFunction.h>
#include <vtkm/filter/Contour.h>
#include <vtkm/filter/Threshold.h>
#include <vtkm/filter/WarpScalar.h>
#include <vtkm/filter/ExtractStructured.h>
#include <vtkm/filter/Streamline.h>
#include <vtkm/filter/LagrangianStructures.h>
#include <vtkm/filter/Gradient.h>


#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <filesystem>


#ifndef VTKM_FLOW_UTILS_H
#define VTKM_FLOW_UTILS_H

#endif //VTKM_FLOW_UTILS_H

using vtkm::rendering::CanvasRayTracer;


vtkm::cont::DataSet load(const std::string &address);
void save_vtk(const std::string &address, vtkm::cont::DataSet output);


void do_mapper_wire_framer(std::string field_name, vtkm::cont::DataSet do_set, vtkm::Id canvas_width, vtkm::Id canvas_height, std::string save_address);