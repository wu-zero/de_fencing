import cv2
import numpy as np

from de_fencing.Setting import Setting
from line_feature.HoughLinesP import find_line_through_hough
import de_fencing.Parameter as PARM






# 转换线段为：端点为图像边界，附加斜率（特殊值0,np.inf)
def convert_line(line, image_shape):
    # print(line)
    x1 = line[0]
    y1 = line[1]
    x2 = line[2]
    y2 = line[3]
    x_length = image_shape[1]
    y_length = image_shape[0]


    # result [[x1,y1],[x2,y2],k]
    if x1 == x2:
        result = [[x1,0],[x1,y_length],90.0]
    elif y1 == y2:
        result = [[0,y1],[x_length,y1],0.0]
    else:
        k = (y2 - y1) / (x2 - x1)
        b = y1 - x1 * k

        x_1 = 0
        y_1 = b

        x_2 = -b / k
        y_2 = 0

        x_3 = x_length
        y_3 = k * x_3 + b

        y_4 = y_length
        x_4 = (y_4 - b) / k

        result = []
        if 0 <= y_1 <= y_length:
            result.append([int(x_1), int(y_1)])
        if 0 <= x_2 <= x_length:
            result.append([int(x_2), int(y_2)])
        if 0 <= y_3 <= y_length:
            result.append([int(x_3), int(y_3)])
        if 0 <= x_4 <= x_length:
            result.append([int(x_4), int(y_4)])
        result.append(np.arctan((y2-y1)/(x2-x1))/np.pi*180)
    # print(result)
    return result


def convert_lines(lines, image_shape):
    lines_new = []
    for line in lines:
        line_convert = convert_line(line, image_shape)
        lines_new.append(line_convert)
    return lines_new


# 角度类
class LineAngle:

    def __init__(self,k):
        self.data = k
        self.num = 1
        self.data_list = [k]

    def if_include_k2(self, k2):
        if abs(k2 - self.data) < PARM.maxAngleError:
            self._add_line(k2)
            return True
        else:
            return False

    def _add_line(self, k2):
        self.data_list.append(k2)
        self.data = np.mean(self.data_list)
        self.num += 1


def find_fence_angle(lines):
    ratio_list = []

    flag = False
    for line in lines:
        for ratio in ratio_list:
            flag = flag | ratio.if_include_k2(line[2])
        if flag is False:
            k_new = LineAngle(line[2])
            ratio_list.append(k_new)
        flag = False

    print('========================')
    print('直线角度      包含的直线个数')

    for ratio in ratio_list:
        print("%10f  %10d" % (ratio.data, ratio.num))

    ratio_dict = {}
    for ratio in ratio_list:
        ratio_dict[ratio.data] = ratio.num
    ratio_sorted = sorted(ratio_dict.items(),key=lambda d: d[1])

    max1 = ratio_sorted[-1]
    max2 = ratio_sorted[-2]

    return [max1[0], max2[0]]



class Fence_center:
    def __init__(self, line):
        self.num = 0
        self.X1_list = []
        self.Y1_list = []
        self.X2_list = []
        self.Y2_list = []
        self.angle_list = []

        self.X1 = 0
        self.Y1 = 0
        self.X2 = 0
        self.Y2 = 0
        self.angle = 0
        self._add_line(line)

    def _add_line(self, line2):
        self.X1_list.append(line2[0][0])
        self.Y1_list.append(line2[0][1])
        self.X2_list.append(line2[1][0])
        self.Y2_list.append(line2[1][1])
        self.angle_list.append(line2[2])

        self.X1 = int((max(self.X1_list) + min(self.X1_list))/2)
        self.Y1 = int((max(self.Y1_list) + min(self.Y1_list))/2)
        self.X2 = int((max(self.X2_list) + min(self.X2_list))/2)
        self.Y2 = int((max(self.Y2_list) + min(self.Y2_list))/2)
        self.angle = np.mean(self.angle_list)
        self.num += 1

    def if_include_line2(self, line2):
        if abs(self.X1 - line2[0][0]) + abs(self.Y1 -line2[0][1]) + abs(self.X2 - line2[1][0]) + abs(self.Y2 - line2[1][1]) < PARM.maxCoordinateError:
            self._add_line(line2)
            return True
        else:
            return False




def find_fence_center(lines, angle_list):
    fence_center_list = []
    flag = False
    for ratio in angle_list:
        for line in lines:
            if abs(line[2]-ratio) < PARM.fenceAngleError:
                for fence_center in fence_center_list:
                    flag = flag | fence_center.if_include_line2(line)
                if flag == False:
                    fence_center = Fence_center(line)
                    fence_center_list.append(fence_center)
                flag = False

    # print(len(fence_center_list))
    # for fence_center in fence_center_list:
    #     print(fence_center.X1,fence_center.Y1,fence_center.X2,fence_center.Y2)
    result = []
    for fence_center in fence_center_list:
        if fence_center.num > 1:
            result.append(fence_center)
    return result #fence_center_list




def find_fence_mask_through_line(img):
    image_shape = img.shape
    lines1 = find_line_through_hough(img)

    # 找到栅栏的斜率
    lines_convert = convert_lines(lines1, image_shape)
    angle_list = find_fence_angle(lines_convert)

    print('=' * 40)
    print('ratio_list:', angle_list)
    print('=' * 40)

    img_2 = np.zeros((image_shape[0], image_shape[1]), np.uint8)
    fence_center_list = find_fence_center(lines_convert, angle_list)

    for i in fence_center_list:
        cv2.line(img_2, (i.X1, i.Y1), (i.X2, i.Y2), 255, PARM.fenceWidth)

    print('根据直线特征，大概找到栅栏位置')
    return img_2



if __name__ == '__main__':

    st = Setting()
    img = st.img_to_solve
    cv2.imshow('original', st.img_original)
    mask = find_fence_mask_through_line(img)
    mask = st.recovery_resize(mask)
    cv2.imshow('mask', mask)
    cv2.waitKey()
    # # 保存图片地址
    # cv2.imwrite('img_cu_3.jpg',img_2)





