import os.path

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from .experiment.flow.glo_var import gInfo


def my_view(request):
    return HttpResponse("Hello, World!")


def test(request):
    print(request)
    data = {'data': "OK"}
    response = JsonResponse(data)

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
        gInfo.file_name = file_name

        print("select: ", gInfo.file_name)

        data = {'data': "OK"}
        response = JsonResponse(data)
        return response

    return JsonResponse({'data': "Error"})
