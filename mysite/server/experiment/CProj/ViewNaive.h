//
// Created by 岳润璞 on 2023/5/31.
//

#ifndef VTKM_FLOW_VIEWNAIVE_H
#define VTKM_FLOW_VIEWNAIVE_H

#include <vtkm/rendering/View.h>
#include <vtkm/rendering/BoundingBoxAnnotation.h>
#include <vtkm/rendering/AxisAnnotation3D.h>
#include <vtkm/rendering/ColorBarAnnotation.h>

class ViewNaive : public vtkm::rendering::View {
public:
    ViewNaive(const vtkm::rendering::Scene &scene,
              const vtkm::rendering::Mapper &mapper,
              const vtkm::rendering::Canvas &canvas);

    ~ViewNaive();

    void Paint() override;

    void RenderScreenAnnotations() override;

    void RenderWorldAnnotations() override;

    void SetShowBoundingBox(bool);

    void SetShowAxisAnnotation(bool);

    void SetShowColorBar(bool);

private:
    bool ShowBoundingBox;
    bool ShowAxisAnnotation;
    bool ShowColorBar;
    vtkm::Bounds SpatialBounds;
    vtkm::Range Range;
    // 3D-specific annotations
    vtkm::rendering::BoundingBoxAnnotation BoxAnnotation;
    vtkm::rendering::AxisAnnotation3D XAxisAnnotation;
    vtkm::rendering::AxisAnnotation3D YAxisAnnotation;
    vtkm::rendering::AxisAnnotation3D ZAxisAnnotation;
    vtkm::rendering::ColorBarAnnotation ColorBarAnnotation;
};


#endif //VTKM_FLOW_VIEWNAIVE_H
