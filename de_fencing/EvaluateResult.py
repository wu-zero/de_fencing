import numpy as np
import cv2


def evaluate_result_and_show(original, standard_mask, own_mask):
    assert own_mask.shape == standard_mask.shape
    mask_shape = own_mask.shape
    masked = original.copy()
    mask_compare = np.zeros(original.shape, dtype=np.uint8)
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for row in range(mask_shape[0]):
        for col in range(mask_shape[1]):
            # True Positive
            if own_mask[row, col] >= 128 and standard_mask[row, col] >= 128:
                masked[row, col] = [0, 0, 0]
                mask_compare[row, col] = [0, 255, 0]
                TP += 1
            # True Negative
            elif own_mask[row, col] < 128 and standard_mask[row, col] < 128:
                TN += 1
            # False Positive
            elif own_mask[row, col] >= 128 and standard_mask[row, col] < 128:
                masked[row, col] = [0, 0, 0]
                mask_compare[row, col] = [0, 0, 255]
                FP += 1
            # False Negative
            elif own_mask[row, col] < 128 and standard_mask[row, col] >= 128:
                mask_compare[row, col] = [255, 0, 0]
                FN += 1
    print(TP + TN + FP + FN)
    return masked, mask_compare,TP/(TP+FP), TP/(TP+FN)



if __name__ == '__main__':
    data_file_path = '../result/person/'

    img_original = cv2.imread(data_file_path + 'original.jpg')
    own_mask = cv2.imread(data_file_path + 'own_mask.jpg', cv2.IMREAD_GRAYSCALE)
    standard_mask = cv2.imread(data_file_path + 'standard_mask.jpg', cv2.IMREAD_GRAYSCALE)
    standard_mask[standard_mask < 128] = 0
    masked, mask_compare, precision_ratio, recall_ratio = evaluate_result_and_show(img_original, standard_mask, own_mask)
    print("查准率:", precision_ratio, " 查全率:", recall_ratio)
    with open(data_file_path+'data.txt', 'w') as f:  # 设置文件对象
        f.write("查准率: %f, 查全率: %f" %(precision_ratio,recall_ratio))
        f.close()

    # 显示保存mask覆盖的原图
    cv2.imshow('masked', masked)
    cv2.imwrite(data_file_path + 'masked.jpg',masked)
    cv2.waitKey()

    # 显示保存mask_compare图
    cv2.imshow('mask_compare', mask_compare)
    cv2.imwrite(data_file_path + 'mask_compare.jpg', mask_compare)
    cv2.waitKey()


    # inpainting
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    standard_mask_dilated= cv2.dilate(standard_mask, kernel)
    inpainting_with_standard_mask = cv2.inpaint(img_original, standard_mask_dilated, 3, cv2.INPAINT_TELEA)  # cv2.INPAINT_NS  # cv2.INPAINT_TELEA
    cv2.imshow('inpainting_with_standard_mask', inpainting_with_standard_mask)
    cv2.imwrite(data_file_path + 'inpainting_with_standard_mask.jpg', inpainting_with_standard_mask)
    cv2.waitKey()

    #
    inpainting_with_own_mask = cv2.inpaint(img_original, own_mask, 3, cv2.INPAINT_TELEA)  # cv2.INPAINT_NS  # cv2.INPAINT_TELEA
    cv2.imshow('inpainting_with_own_mask', inpainting_with_own_mask)
    cv2.imwrite(data_file_path + 'inpainting_with_own_mask.jpg', inpainting_with_own_mask)
    cv2.waitKey()


