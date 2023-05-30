"""
@file: testclib.py
@author: Runpu
@time: 2023/5/30 15:19
"""
import ctypes

# 加载库
lib = ctypes.cdll.LoadLibrary('/Users/yy/CLionProjects/dylib_demo/cmake-build-debug/libaaaaaa.dylib')

# 调用函数
say_hello = lib.sayHello
say_hello.restype = None
say_hello.argtypes = []
say_hello()