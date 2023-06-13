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


vtkm::cont::DataSet do_pathline(std::vector<std::string> file_list,
                                vtkm::Id num_file, vtkm::Float32 step_size, vtkm::Id num_step,
                                std::vector<vtkm::Particle>& seeds, int inter_num);