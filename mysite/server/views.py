from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse


def my_view(request):
    return HttpResponse("Hello, World!")


def test(request):
    print(request)
    data = {'data': "OK"}
    response = JsonResponse(data)
    # response['Access-Control-Allow-Origin'] = '*'

    return response
