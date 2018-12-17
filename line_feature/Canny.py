import cv2
from de_fencing.Setting import Setting


def canny(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  # 将图像转化为灰度图像
    cv2.imshow("Image", img)  # 显示图像
    cv2.waitKey()

    # Canny边缘检测
    img_canny = cv2.Canny(img,30,120)
    cv2.imshow("Canny", img_canny)
    cv2.waitKey()


if __name__ == '__main__':
    st = Setting()
    image = st.img_to_solve
    canny(image)
