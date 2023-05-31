"""
@file: testclib.py
@author: Runpu
@time: 2023/5/30 15:19
"""
import ctypes

# # 加载库
# lib = ctypes.cdll.LoadLibrary('/Users/yy/CLionProjects/dylib_demo/cmake-build-debug/libaaaaaa.dylib')
#
# # 调用函数
# say_hello = lib.sayHello
# say_hello.restype = None
# say_hello.argtypes = []
# say_hello()

# 加载库
lib = ctypes.cdll.LoadLibrary('CProj/build/libstreamline.dylib')

file_name = "/Users/yy/GithubProjects/GPT-flow-vis/mysite/server/experiment/data/streamlines/IWP_DAILY_20141123_531_1621.vtk"
width = 780
height = 480
output = "/Users/yy/GithubProjects/GPT-flow-vis/mysite/server/experiment/111.png"


# 调用函数
gen = lib.gen
gen.restype = None
gen.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_char_p]
gen(file_name.encode('utf-8'), width, height, output.encode('utf-8'))

