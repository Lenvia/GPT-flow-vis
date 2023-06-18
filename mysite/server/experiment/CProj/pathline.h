//
// Created by 岳润璞 on 2023/6/13.
//

#ifndef VTKM_FLOW_PATHLINE_H
#define VTKM_FLOW_PATHLINE_H

#endif //VTKM_FLOW_PATHLINE_H

#include "utils.h"

#include <iostream>
#include <vector>
#include <vtkm/filter/Pathline.h>
#include <cstring>  // for std::strcpy
#include <string>

extern "C" void gen_pathline(char** file_list, vtkm::Id num_file, float* xrange, float *yrange, int nseeds,
                             vtkm::Id num_step, vtkm::Float32 step_size, int inter_num, const char* out_put);

void gen_seeds(std::vector<vtkm::Particle>& seeds, float* xrange, float *yrange, int nseeds);

vtkm::cont::DataSet do_pathline(std::vector<std::string>& file_list,
                                vtkm::Id num_file, vtkm::Float32 step_size, vtkm::Id num_step,
                                std::vector<vtkm::Particle>& seeds, int inter_num);