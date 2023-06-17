
class Errors:
    SUCCESS = 0
    DEFAULT = 1
    FILE_FORMAT = 2
    UNKNOWN_INSTRUCT = 3
    GPT_ACCESS = 4
    FILE_HANDLE = 5


err_msg = {
    Errors.SUCCESS: "success",
    Errors.DEFAULT: "服务器内部错误",
    Errors.FILE_FORMAT: "数据格式错误",
    Errors.UNKNOWN_INSTRUCT: "指令无法解析",
    Errors.GPT_ACCESS: "网络连接出现错误，请稍后重试",
    Errors.FILE_HANDLE: "文件解析失败",
}