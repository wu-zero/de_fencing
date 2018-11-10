# de_fencing

###目录

* [一、识别栅栏](###一、识别栅栏)
* [二、修复](###二、修复)

###一、识别栅栏
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

###二、修复
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
修补方法：  

*   **INPAINT_NS** 基于纳维尔－斯托克斯方程的修补方法  
[参考](https://wenku.baidu.com/view/97679916e87101f69e319536.html)
*  **INPAINT_TELEA** elea在2004年提出的基于快速行进的修复算法  
[参考](https://blog.csdn.net/carson2005/article/details/6844025)



