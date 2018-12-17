import cv2

from de_fencing.Setting import Setting
from color_feature.FindMaskThroughColor import find_fence_mask_through_color

if __name__ == '__main__':
    st = Setting()

    img = st.img_to_solve

    mask = find_fence_mask_through_color(img)
    mask = st.recovery_resize(mask)
    mask[mask > 0] = 255
    #cv2.imshow('mask',mask)

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
