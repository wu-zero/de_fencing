import cv2
import numpy as np
from skimage import measure

from color_feature.GetPoint import choose_points_from_img, get_points_sample
from color_feature.FenceDetcc import fenceDetcc


import de_fencing.Parameter as PARM


wind_size = PARM.windSize
manhattan_distance_threshold = PARM.manhattanDistanceThreshold


def find_fence_mask_through_color(img):
    # 获得栅栏样本像素点  获得样本点周围像素点
    points = choose_points_from_img(img)
    R, G, B, points_num, points = get_points_sample(img, points, wind_size=wind_size)
    # 获得原始栅栏mask
    mask = fenceDetcc(img, R, G, B, points_num, wind_size=wind_size, treshold=manhattan_distance_threshold)

    # 膨胀处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilation = cv2.dilate(mask, kernel)
    cv2.imshow('image dilation', dilation)
    cv2.waitKey(0)

    # 联通区域划分
    labels, num = measure.label(dilation, neighbors=8, background=0, connectivity=2, return_num=True)
    print('联通区域数目：', num)

    labels_num_dict = {}
    for i in range(1, num+1):  # 这里从1开始，防止将背景设置为最大连通域
        labels_num_dict[i] = np.sum(labels == i)
    print('联通区域标签和包含像素个数:\n', labels_num_dict)

    # 联通区域面积从大到小排序
    labels_num_dict_sorted = sorted(labels_num_dict.items(), key=lambda d: d[1], reverse=True)
    print('排序后联通区域标签和包含像素个数:\n', labels_num_dict_sorted)

    # 选择标签  2个条件
    labels_choose = []
    for i in range(0, min(15, num - 1)):
        if labels_num_dict_sorted[i][1] > 100:
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
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask_choose_dilation = cv2.dilate(mask_choose, kernel1)
    mask_choose_dilation = cv2.erode(mask_choose_dilation,kernel2)
    cv2.imshow('mask_choose_dilation', mask_choose_dilation)
    cv2.waitKey(0)

    return mask_choose_dilation







if __name__ == '__main__':
    from de_fencing.Setting import Setting
    # 获得要处理的图片
    st = Setting()
    img = st.img_to_solve
    mask = find_fence_mask_through_color(img)

    # # 保存
    # cv2.imwrite(result_file_path+str(1)+img_name,img)
    # cv2.imwrite(result_file_path + str(2) + img_name, mask_choose_dilation)

    # 修复
    new_img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)  # cv2.INPAINT_NS  # cv2.INPAINT_TELEA
    cv2.imshow('new_img', new_img)
    cv2.waitKey(0)
    # cv2.imwrite(result_file_path + img_name, new_img)


