import cv2

from de_fencing.Setting import Setting
from color_feature.FindMaskThroughColor import find_fence_mask_through_color
from line_feature.FindMaskThroughLine import find_fence_mask_through_line

if __name__ == '__main__':
    st = Setting()

    img = st.img_to_solve

    cv2.imshow('original',st.img_original)
    mask1 = find_fence_mask_through_color(img)
    mask1 = st.recovery_resize(mask1)
    mask1[mask1 > 0] = 255

    cv2.imshow('mask1', mask1)

    img = st.img_to_solve
    mask2 = find_fence_mask_through_line(img)
    mask2 = st.recovery_resize(mask2)
    mask2[mask2 > 0] = 255

    cv2.imshow('mask2', mask2)

    mask = mask1 & mask2

    cv2.imwrite(st.result_file_path +'/own_mask.jpg', mask)
    cv2.imshow('mask', mask)
    cv2.waitKey()





    # # 保存
    # cv2.imwrite(result_file_path+str(1)+img_name,img)
    # cv2.imwrite(result_file_path + str(2) + img_name, mask_choose_dilation)

    # # 修复
    # new_img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)  # cv2.INPAINT_NS  # cv2.INPAINT_TELEA
    # cv2.imshow('new_img', new_img)
    # cv2.waitKey(0)
    # # cv2.imwrite(result_file_path + img_name, new_img)
