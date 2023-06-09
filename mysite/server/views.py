from asgiref.sync import async_to_sync
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from .experiment.flow.glo_var import gInfo, nc_base_dir
from .experiment.flow.vtk_helper import quicklook
from server import connection

from .utils import get_nc_dir
from .errors import err_msg, Errors


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
        file_name_list = json_data.get('file_name_list')

        print(file_name_list)

        if len(file_name_list) == 1:  # 单时间流线
            gInfo.file_name = file_name_list[0]
            print("select: ", gInfo.file_name)

            try:
                quicklook(get_nc_dir(gInfo.file_name))
            except Exception as e:
                print(e)
                rsp = {
                    'code': Errors.FILE_HANDLE,
                    'data': err_msg[Errors.FILE_HANDLE]
                }
                return JsonResponse(rsp)

            rsp = {
                'code': Errors.SUCCESS,
                'data': gInfo.dataset_info
            }

        else:  # 轨迹线
            print(file_name_list)
            rsp = {
                'code': Errors.SUCCESS,
                'data': "多项文件已加载"
            }

        response = JsonResponse(rsp)

        # 响应信息
        consumer = connection.active_consumer
        if consumer:
            async_to_sync(consumer.send)(text_data=json.dumps({
                "id": 0,
                "content": "数据集已加载",
            }))

        return response

    return JsonResponse({
        'code': Errors.DEFAULT,
        'data': err_msg[Errors.DEFAULT]}
    )
