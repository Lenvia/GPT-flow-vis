import os.path

from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from .experiment.flow.glo_var import gInfo, nc_base_dir
from .experiment.flow.vtk_helper import quicklook
from server import connection


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

        quicklook(os.path.join(nc_base_dir, gInfo.file_name))

        data = {'data': gInfo.dataset_info}
        response = JsonResponse(data)

        # consumer = connection.active_consumer
        # if consumer:
        #     async_to_sync(consumer.send(text_data=json.dumps({
        #         "id": 0,
        #         "content": "数据集已加载",
        #     })))
        #     print("已发送")

        return response

    return JsonResponse({'data': "Error"})
