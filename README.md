# de_fencing

### 目录

* [依赖库](###依赖库)
* [文件说明](###文件说明)
* [运行方法](###运行方法)
* [原理](###原理)
    * [一、识别栅栏](####一、识别栅栏)
    * [二、修复](####二、修复)
* [测试报告](###测试报告)

### 依赖库

* opencv
* numpy
* matplotlib
* scikit-image

### 文件说明
* 实现说明.docx
    简要说明实现过程
* color_feature(file)
    通过栅栏颜色特征找栅栏范围
* line_feature(file)
    通过栅栏边界的直线特征找栅栏范围
* de_fencing(file)
    * Parameter.py 
        设定参数
    * Setting.py
        修改输入图片位置、输出图片位置等
    * main1.py
        利用颜色特征检测栅栏
    * main2.py
        利用直线特征和颜色特征检测栅栏
    * EvaluateResult.py
        评估检测效果并进行修补
* test(file)
    原始图片和标准栅栏掩膜图片呢位置
* result(file)
    检测结果、修复结果存储位置

### 运行方法
运行文件夹`de_fencing`中的`main1.py`和`main2.py`可以直接运行，检测栅栏区域，可以通过更改`Setting.py`程序中的图片位置来测试不同的图片。  
`EvaluateResult.py`可以直接运行，用于评估检测效果并进行图像修补

### 原理
具体见小论文

### 测试报告
![图片1](https://github.com/wu-zero/de_fencing/blob/master/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8Aforshow-1.jpg)
![图片2](https://github.com/wu-zero/de_fencing/blob/master/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8Aforshow-2.jpg)
![图片3](https://github.com/wu-zero/de_fencing/blob/master/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8Aforshow-3.jpg)
![图片4](https://github.com/wu-zero/de_fencing/blob/master/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8Aforshow-4.jpg)
![图片5](https://github.com/wu-zero/de_fencing/blob/master/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8Aforshow-5.jpg)
![图片6](https://github.com/wu-zero/de_fencing/blob/master/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8A/%E6%B5%8B%E8%AF%95%E6%8A%A5%E5%91%8Aforshow-6.jpg)


