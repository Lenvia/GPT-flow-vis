//
// Created by 岳润璞 on 2023/6/13.
//

#ifndef pathline_cpp
#define pathline_cpp

#include "pathline.h"

/***************************************************************
 *  @brief     生成迹线
 *  @param     file_list 数据集绝对路径的列表
               num_file 读取数据集文件数量（每个文件代表一天，即每条迹线经过的天数）
               step_size 种子每步的步长，控制迹线包含的线段数量(平滑程度)。step_size 越小，迹线越平滑
               num_step 每条迹线的步数，每条流线的折点数量为num_step/step_size（step_size > 1）
               seeds 种子点
               inter_num 每个文件重复读的次数，默认为1，即每一个数据集读1次
 *  @Sample usage:
        do_pathline(file_list, 2, 1.0f, 6, seeds);
        do_pathline(file_list, 2, 1.0f, 6, seeds, 12);
 **************************************************************/
vtkm::cont::DataSet do_pathline(std::vector<std::string> file_list,
                                vtkm::Id num_file, vtkm::Float32 step_size, vtkm::Id num_step,
                                std::vector<vtkm::Particle>& seeds, int inter_num)
{

    vtkm::filter::flow::Pathline pathlines;
    vtkm::cont::DataSet ds, ds_next, pathlineCurves;

    ds = load(file_list[0]);

    std::string field_name = ds.GetField(0).GetName();
    pathlines.SetActiveField(field_name);
    pathlines.SetStepSize(step_size);     //step size
    pathlines.SetNumberOfSteps(num_step); //step
    pathlines.SetSeeds(seeds);        //seed
    pathlines.SetPreviousTime(0.0f);

    int count = 1;
    for (int i = 1; i < num_file; i++)
    {
        ds_next = load(file_list[i]);
        for (int j = 0; j < inter_num; j++)
        {
            pathlines.SetNextTime(count);
            pathlines.SetNextDataSet(ds_next);
            count++;
        }
        if (i % 120 == 0)
            printf("%s succeed read %d times!\n now count = %d\n", file_list[i].c_str(), inter_num, count);

    }
    pathlineCurves = pathlines.Execute(ds); // pathline

    return pathlineCurves;

}



#endif