import cv2

# 缩放图片用的
def resize(img, ratio=None):

    height, width = img.shape[:2]
    if height > 500 and width > 500:
        if ratio == None:
            ratio = ((500*500)/(height*width))**0.5
        # 缩小图像
        size = (int(width * ratio), int(height * ratio))
        img_shrink = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

        # 显示
        cv2.imshow("img", img)
        cv2.imshow("img_shrink", img_shrink)
        cv2.waitKey(0)
        cv2.destroyWindow("img")
        cv2.destroyWindow("img_shrink")
        return img_shrink
    else:
        return img

if __name__ == '__main__':
    # img = cv2.imread("data/test1.jpg")
    # img_shrink = resize(img,0.5)
    # print(img_shrink.shape)
    pass