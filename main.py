import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure, color
from GetPoint import get_point_from_img, getPoint
from FenceDetcc import fenceDetcc
from Setting import resize

data_file_path = 'data/'
result_file_path = 'results/'
img_name = 'test003.jpg'
img_path = data_file_path + img_name
wind_size = 7 # 7
manhattan_distance_treshold = 7 #7

if __name__ == '__main__':
    # 获得要处理的图片
    img = cv2.imread(img_path)
    print('图片大小',img.shape)
    img = resize(img)
    # 获得栅栏样本像素点  获得样本点周围像素点
    points = get_point_from_img(img)
    R, G, B, points_num, points = getPoint(img, points, wind_size=wind_size)
    # 获得原始栅栏mask
    mask = fenceDetcc(img, R, G, B, points_num, wind_size=wind_size, treshold=manhattan_distance_treshold)

    # # 开运算
    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    # opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    # cv2.imshow('image opening', opening)
    # cv2.waitKey(0)

    # 膨胀处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilation = cv2.dilate(mask,kernel)
    cv2.imshow('image dilation', dilation)
    cv2.waitKey(0)



    # 联通区域划分
    labels, num = measure.label(dilation, neighbors=8, background=0, connectivity=2,return_num=True)
    print('联通区域数目：', num)

    labels_num_dict = {}
    for i in range(1, num):  # 这里从1开始，防止将背景设置为最大连通域
        labels_num_dict[i] = np.sum(labels == i)
    print('联通区域标签和包含像素个数:\n', labels_num_dict)


    # 联通区域面积从大到小排序
    labels_num_dict_sorted = sorted(labels_num_dict.items(), key=lambda d:d[1], reverse=True)
    print('排序后联通区域标签和包含像素个数:\n', labels_num_dict_sorted)

    #选择标签  2个条件
    labels_choose = []
    for i in range(0, min(15, num-1)):
        if labels_num_dict_sorted[i][1] > 21:
            labels_choose.append(labels_num_dict_sorted[i][0])

    print('选择的标签:', labels_choose)

    # 选择栅栏区域
    mask_choose = np.zeros(labels.shape, dtype=np.uint8)
    for i in range(mask_choose.shape[0]):
        for j in range(mask_choose.shape[1]):
            if labels[i][j] in labels_choose:
                mask_choose[i][j] = 255
    cv2.imshow('mask_choose', mask_choose)
    cv2.waitKey(0)

    # 膨胀处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask_choose_dilation = cv2.dilate(mask_choose, kernel)
    cv2.imshow('mask_choose_dilation', mask_choose_dilation)
    cv2.waitKey(0)

    # # 保存
    # cv2.imwrite(result_file_path+str(1)+img_name,img)
    # cv2.imwrite(result_file_path + str(2) + img_name, mask_choose_dilation)


    # 修复
    new_img = cv2.inpaint(img, mask_choose_dilation, 3, cv2.INPAINT_TELEA) # cv2.INPAINT_NS  # cv2.INPAINT_TELEA
    cv2.imshow('new_img', new_img)
    cv2.waitKey(0)
    cv2.imwrite(result_file_path + img_name, new_img)