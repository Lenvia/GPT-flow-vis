//
// Created by 岳润璞 on 2023/5/31.
//

#include "ViewNaive.h"

ViewNaive::ViewNaive(const vtkm::rendering::Scene& scene,
                     const vtkm::rendering::Mapper& mapper,
                     const vtkm::rendering::Canvas& canvas)
        : View(scene, mapper, canvas, vtkm::rendering::Color(0, 0, 0, 1), vtkm::rendering::Color(1, 1, 1, 1))
        , ShowBoundingBox(true)
        , ShowAxisAnnotation(true)
        , ShowColorBar(false)
{
}

ViewNaive::~ViewNaive() {}

void ViewNaive::SetShowBoundingBox(bool show)
{
    this->ShowBoundingBox = show;
}

void ViewNaive::SetShowAxisAnnotation(bool show)
{
    this->ShowAxisAnnotation = show;
}

void ViewNaive::SetShowColorBar(bool show)
{
    this->ShowColorBar = show;
}

void ViewNaive::Paint()
{
    this->GetCanvas().Clear();

    this->SetupForWorldSpace();
    if (this->WorldAnnotationsEnabled)
        this->RenderWorldAnnotations();
    this->GetScene().Render(this->GetMapper(), this->GetCanvas(), this->GetCamera());

    this->SetupForScreenSpace();
    if (this->ShowColorBar) {
        this->RenderAnnotations();
        this->RenderScreenAnnotations();
    }
}

void ViewNaive::RenderScreenAnnotations()
{
    if (this->GetScene().GetNumberOfActors() > 0)
    {
        //this->ColorBarAnnotation.SetAxisColor(vtkm::rendering::Color(1,1,1));
        this->ColorBarAnnotation.SetFieldName(this->GetScene().GetActor(0).GetScalarField().GetName());
        this->ColorBarAnnotation.SetRange(this->Range, 5);
        this->ColorBarAnnotation.SetColorTable(this->GetScene().GetActor(0).GetColorTable());
        this->ColorBarAnnotation.Render(
                this->GetCamera(), this->GetWorldAnnotator(), this->GetCanvas());
    }
}

void ViewNaive::RenderWorldAnnotations()
{
    vtkm::Bounds bounds = this->SpatialBounds;
    vtkm::Float64 xmin = bounds.X.Min, xmax = bounds.X.Max;
    vtkm::Float64 ymin = bounds.Y.Min, ymax = bounds.Y.Max;
    vtkm::Float64 zmin = bounds.Z.Min, zmax = bounds.Z.Max;
    vtkm::Float64 dx = xmax - xmin, dy = ymax - ymin, dz = zmax - zmin;
    vtkm::Float64 size = vtkm::Sqrt(dx * dx + dy * dy + dz * dz);

    if (this->ShowBoundingBox) {
        this->BoxAnnotation.SetColor(vtkm::rendering::Color(.5f, .5f, .5f));
        this->BoxAnnotation.SetExtents(bounds);
        this->BoxAnnotation.Render(this->GetCamera(), this->GetWorldAnnotator());
    }

    if (this->ShowAxisAnnotation) {
        vtkm::Vec3f_32 lookAt = this->GetCamera().GetLookAt();
        vtkm::Vec3f_32 position = this->GetCamera().GetPosition();
        bool xtest = lookAt[0] > position[0];
        bool ytest = lookAt[1] > position[1];
        bool ztest = lookAt[2] > position[2];

        const bool outsideedges = true; // if false, do closesttriad
        if (outsideedges)
        {
            xtest = !xtest;
            //ytest = !ytest;
        }

        vtkm::Float64 xrel = vtkm::Abs(dx) / size;
        vtkm::Float64 yrel = vtkm::Abs(dy) / size;
        vtkm::Float64 zrel = vtkm::Abs(dz) / size;

        this->XAxisAnnotation.SetAxis(0);
        this->XAxisAnnotation.SetColor(AxisColor);
        this->XAxisAnnotation.SetTickInvert(xtest, ytest, ztest);
        this->XAxisAnnotation.SetWorldPosition(
                xmin, ytest ? ymin : ymax, ztest ? zmin : zmax, xmax, ytest ? ymin : ymax, ztest ? zmin : zmax);
        this->XAxisAnnotation.SetRange(xmin, xmax);
        this->XAxisAnnotation.SetMajorTickSize(size / 40.f, 0);
        this->XAxisAnnotation.SetMinorTickSize(size / 80.f, 0);
        this->XAxisAnnotation.SetLabelFontOffset(vtkm::Float32(size / 15.f));
        this->XAxisAnnotation.SetMoreOrLessTickAdjustment(xrel < .3 ? -1 : 0);
        this->XAxisAnnotation.Render(this->GetCamera(), this->GetWorldAnnotator(), this->GetCanvas());

        this->YAxisAnnotation.SetAxis(1);
        this->YAxisAnnotation.SetColor(AxisColor);
        this->YAxisAnnotation.SetTickInvert(xtest, ytest, ztest);
        this->YAxisAnnotation.SetWorldPosition(
                xtest ? xmin : xmax, ymin, ztest ? zmin : zmax, xtest ? xmin : xmax, ymax, ztest ? zmin : zmax);
        this->YAxisAnnotation.SetRange(ymin, ymax);
        this->YAxisAnnotation.SetMajorTickSize(size / 40.f, 0);
        this->YAxisAnnotation.SetMinorTickSize(size / 80.f, 0);
        this->YAxisAnnotation.SetLabelFontOffset(vtkm::Float32(size / 15.f));
        this->YAxisAnnotation.SetMoreOrLessTickAdjustment(yrel < .3 ? -1 : 0);
        this->YAxisAnnotation.Render(this->GetCamera(), this->GetWorldAnnotator(), this->GetCanvas());

        this->ZAxisAnnotation.SetAxis(2);
        this->ZAxisAnnotation.SetColor(AxisColor);
        this->ZAxisAnnotation.SetTickInvert(xtest, ytest, ztest);
        this->ZAxisAnnotation.SetWorldPosition(
                xtest ? xmin : xmax, ytest ? ymin : ymax, zmin, xtest ? xmin : xmax, ytest ? ymin : ymax, zmax);
        this->ZAxisAnnotation.SetRange(zmin, zmax);
        this->ZAxisAnnotation.SetMajorTickSize(size / 40.f, 0);
        this->ZAxisAnnotation.SetMinorTickSize(size / 80.f, 0);
        this->ZAxisAnnotation.SetLabelFontOffset(vtkm::Float32(size / 15.f));
        this->ZAxisAnnotation.SetMoreOrLessTickAdjustment(zrel < .3 ? -1 : 0);
        this->ZAxisAnnotation.Render(this->GetCamera(), this->GetWorldAnnotator(), this->GetCanvas());
    }
}