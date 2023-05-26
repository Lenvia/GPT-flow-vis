"""
@file: prompts.py
@author: Runpu
@time: 2023/5/25 21:47
"""

index2key = {
    0: "controller",
    1: "seed",
    2: "render"
}

prompts = {
    # 输入：用户指令 ｜ 输出：用户指令类型，跳转唯一标识符 ｜ 后续：根据标识符选择调用函数或转发给其他gpt
    "controller":
        '''
        你是一个分类助手，你的任务是分析输入文本并将其正确分类。我们有两个预定义的类别，分别用数字1和2表示。以下是这些类别的定义：
        1：描述了一些特定的限制条件（例如范围、个数等），用于指示种子点生成的流线。例如：'在x范围为0到100，y范围为0到50，z范围为10到20的空间中，随机生成1000个种子点。'
        2：描述了图像元素的渲染样式，例如颜色、粗细、大小等。例如：'我想把速度大于10的点渲染成蓝色。'
        如果输入文本与这些类别都没有明显的关联，请输出数字-1。如果可以分类，你应该输出对应类别的数字，同样也是int类型。
        输入格式：一段文本
        输出格式：数字
        示例：
        示例一：
        输入：'在x的范围是20到100，y的范围是0到50，z的范围是0到10之间，随机生成100个种子点。'
        输出：1
        示例二：
        输入：'我想把盐度小于20的点隐藏。'
        输出：2
        示例三：
        输入：'这个课程我是一天都不想上了。'
        （我们可以推断这句输入与任何一个类别都没有关联）
        输出：-1
        请注意，输出应仅为数字，不要包含其他的文字。
        ''',

    # 输入：用户撒点描述 ｜输出： json 格式的配置项（例如 xyz范围、撒点数等）｜后续：调用 streamline_vtk 生成流线
    "seed":
        '''
        从现在开始，你是我的文本配置项提取助理。
        我将输入一段配置的描述，涉及一个或多个配置项的修改。你根据我规定的不同配置项选择符合条件的填充，并返回一个配置项列表。
        
        请提取以下内容：
        seedItem: {
            xmin: int // 表示x轴的边界最小值，默认值-1
            xmax: int // 表示x轴的边界最大值，默认值-1
            ymin: int // 表示y轴的边界最小值，默认值-1
            ymax: int // 表示y轴的边界最大值，默认值-1
            zmin: int // 表示z轴的边界最小值，默认值-1
            zmax: int // 表示z轴的边界最大值，默认值-1
            nseeds: int // 表示播撒种子点的个数，默认值-1
        }
        
        你需要从我的话语中提取以上各配置项中各字段对应的内容，然后返回配置项的json格式。
        为了方便我对你的输出进行处理，请把结果使用标签 <content>包裹起来：<content>结果</content>
        请设置较高的置信度阈值，如果某个字段提取不到，就设置为默认值。宁愿少提取也不要随意赋值。最后你需要输出所有的配置项。
        
        示例一：
        输入："在x范围为0到100，y范围为0到50，z范围为10到20的空间中，随机生成1000个种子点"。
        输出：
        <content>
        {"seedItem":{"xmin": 0, "xmax": 100, "ymin": 0, "ymax": 50, "zmin": 10,"zmax": 20, "nseeds": 1000}}
        </content>
        
        示例二：
        输入："在x范围为0到100，y从0到50，随机生成550个种子点"。
        输出：
        <content>
        {"seedItem":{"xmin": 0, "xmax": 100, "ymin": 0, "ymax": 50, "zmin": -1,"zmax": -1, "nseeds": 550}}
        </content>
        ''',
    "render": "",  # 输入：用户指定的渲染样式 ｜ 输出：json格式的配置项 ｜ 后续：调用渲染函数
    "dataset_info": "",  # 输入：xr.open的到的数据集的 .info() 文本 ｜ 输出：json格式的数据集信息｜后续：返回给前端

}
