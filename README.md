# de_fencing

### 目录

* [依赖库](###依赖库)
* [文件说明](###文件说明)
* [运行方法](###运行方法)
* [原理](###原理)
    * [一、识别栅栏](####一、识别栅栏)
    * [二、修复](####二、修复)


### 依赖库

* opencv
* numpy
* matplotlib
* scikit-image

### 文件说明
* 实现说明.docx
    简要说明实现过程
* picture(file)
    原始图片位置
* 其他(file)
    代码文件，其中wyw1_ ~ wyw4_ 为现在的使用代码，wywz_为正在测试的代码，以后可能会用于使用。具体说明如下：
    * wyw1_bianyuanjiance 
        三种边缘检测的方法，最后选用Canny边缘检测 
    * wyw2_zhixianjiance
        Hough直线检测
    * wyw3_zhaozhixianxielv
        用统计学的方法找栅栏的边缘直线斜率
    * wyw4_zhaozhalanfanwei
        粗略找到栅栏范围
    * wywz_ 
        超像素分割、图像细化等，不做介绍。
#### 运行方法
运行文件夹`wyw4_zhaozhalanfanwei`中的`find_fence.py`文件可以直接运行，利用栅栏的直线特性粗略识别栅栏，可以通过更改程序中的图片位置来测试不同的图片。


