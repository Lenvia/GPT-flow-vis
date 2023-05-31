#include "utils.h"
#include "ViewNaive.h"

vtkm::cont::DataSet load(const std::string &address) {
    vtkm::cont::DataSet ds;
    vtkm::io::VTKDataSetReader reader(address);
    ds = reader.ReadDataSet();
    return ds;
}

void save_vtk(const std::string &address, vtkm::cont::DataSet output) {
    std::__fs::filesystem::path currentPath = std::__fs::filesystem::current_path();
    std::__fs::filesystem::create_directories(std::__fs::filesystem::path(address).parent_path());


    vtkm::io::VTKDataSetWriter writer(address);
    writer.WriteDataSet(output);

    std::cout << "Saved successfully." << std::endl;
}



void do_mapper_wire_framer(std::string field_name, vtkm::cont::DataSet ds, vtkm::Id canvas_width, vtkm::Id canvas_height, std::string save_address)
{

    // 创建渲染器和画布
    vtkm::rendering::MapperWireframer mapper;
    vtkm::rendering::CanvasRayTracer canvas(canvas_width, canvas_height);
    vtkm::rendering::Color bg_color(0.0f, 0.0f, 0.0f, 0.0f); // 黑色背景

    // 创建场景和演员
    vtkm::rendering::Scene scene;
    vtkm::rendering::Color actor_color(1.0f, 1.0f, 1.0f, 1.0f); // 白色流线
    vtkm::rendering::Actor actor(ds.GetCellSet(), ds.GetCoordinateSystem(), ds.GetField(field_name), actor_color);
    scene.AddActor(actor);

    // 创建视图并渲染
    ViewNaive view(scene, mapper, canvas);
    view.SetShowColorBar(false);
    view.SetShowAxisAnnotation(false);
    view.SetShowBoundingBox(false);
    view.SetBackgroundColor(bg_color);

    view.Paint();
    std::__fs::filesystem::create_directories(std::__fs::filesystem::path(save_address).parent_path());
    view.SaveAs(save_address); // 输出图片

}