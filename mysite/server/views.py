import os.path

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json
from .experiment.flow.nc2vtk import nc2vtk
from django.views.decorators.csrf import csrf_exempt

nc_base_dir = 'server/experiment/data/nc_flow_field'
vtk_base_dir = 'server/experiment/data/vtk_flow_field'


def my_view(request):
    return HttpResponse("Hello, World!")


def test(request):
    print(request)
    data = {'data': "OK"}
    response = JsonResponse(data)
    # response['Access-Control-Allow-Origin'] = '*'

    return response


@csrf_exempt
def uploadNC(request):
    if request.method == 'POST':
        # 获取POST请求的原始数据
        data = request.body.decode('utf-8')
        # 解析JSON数据为Python字典
        json_data = json.loads(data)
        # 获取文件名
        file_name = json_data.get('file_name')
        print("nc2vtk: ", file_name)
        try:
            nc2vtk(file_name, nc_base_dir, vtk_base_dir)
        except Exception as e:
            print(e)

        data = {'data': "OK"}
        response = JsonResponse(data)
        return response
    pass
