# de_fencing

### 目录

* [依赖库](#依赖库)
* [文件说明](#文件说明)
* [运行方法](#运行方法)
* [原理](#原理)
    * [一、识别栅栏](#一识别栅栏)
    * [二、修复](#二修复)


### 依赖库

* opencv
* numpy
* scikit-image

### 文件说明

* **实现说明.docx**
  简要说明实现结果和实现过程
* **picture(file)**
  原始图片位置
* **results(file)**
  运行结果位置
* **de_fencing(file)**
  代码文件夹
    * **Setting.py** 包含一个根据图片原始大小缩放图片的子函数
    * **GetPoint.py** 从图片中选取栅栏的样本点的程序
    * **FenceDetcc.py** 利用选取的样本点及邻近的点建立栅栏像素的模型，粗略识别栅栏
    * **main.py** 给定任意图片执行上述操作后，利用膨胀、开运算、闭运算等操作精确识别栅栏，并修补栅栏区域

### 运行方法
更改main.py中的图片名，选择不同的图片。
运行，对于过大的图片会自动缩小，在`choose point`窗口选择栅栏样本像素，选好后按`q`键退出，然后一直按`Enter`键显示中间过程，直到最后显示修补后的图片并保存。


### 原理
整个过程可以分为两步：识别栅栏；修补栅栏区域。
#### 一、识别栅栏
参考论文：  
 https://www.researchgate.net/publication/296626086_Image_de-fencing_framework_with_hybrid_inpainting_algorithm  

分为四步：

* 手动标记n个栅栏像素坐标
* 用标记点像素及邻近像素作为样本，计算栅栏像素的均值和协方差
* 根据每个点像素与栅栏像素的马氏距离粗略识别栅栏
* 利用图像腐蚀、膨胀、联通区域的面积精确识别栅栏

缺点：

* 需要栅栏像素与图片其他区域像素差距较大
* 不同图片适用的参数不同
* 需要手动标注点

代码：  
```python
pass
```

#### 二、修复
用`opencv`自带的修复函数：
```python
def inpaint(src, inpaintMask, inpaintRadius, flags, dst=None):
    pass
'''
第一个参数src，为8位单通道或者三通道图像的输入图像（要修复的图像）；
第二个参数inpaintMask,为修复掩膜，为8位单通道图像，其中非零像素表示要修补的区域；
第三个参数是double类型的inpaintRadius，需要修复点的附近的圆形区域，该值为修复区域的半径；
第四个参数是int型的flags，为修补方法的标识符，两种修饰方法;
第三个参数为dst，该函数的输出结果就放在这里，它和src图像类型是一样的；
'''
```
`opencv`自带修补方法：  

*   **INPAINT_NS** 基于纳维尔－斯托克斯方程的修补方法  
[参考](https://wenku.baidu.com/view/97679916e87101f69e319536.html)
*  **INPAINT_TELEA** elea在2004年提出的基于快速行进的修复算法  
[参考](https://blog.csdn.net/carson2005/article/details/6844025)



