import cv2
import numpy as np


# coding: utf-8
import cv2
import numpy as np


points = []

# 鼠标左键单击事件
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])

# 从图片中选取栅栏参考点
def get_point_from_img(img):
    img  = img.copy()
    cv2.namedWindow("choose point")
    cv2.setMouseCallback("choose point", on_EVENT_LBUTTONDOWN)
    cv2.imshow("choose point", img)
    while True:
        for point in points:
            x, y = point[0], point[1]
            xy = "%d,%d" % (x, y)
            cv2.circle(img, (x, y), 2, (255, 0, 0), thickness=1)
            cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 255), thickness=2)
            cv2.imshow("choose point", img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    cv2.destroyWindow("choose point")
    return points


def getPoint(img, points, wind_size):
    points_num = len(points)
    counter = 0
    wSize = wind_size * wind_size
    hwSize = int(wind_size/2)
    R = np.zeros(points_num * wSize, dtype=np.uint8)
    G = np.zeros(points_num * wSize, dtype=np.uint8)
    B = np.zeros(points_num * wSize, dtype=np.uint8)


    for i in range(points_num):
        row,col = points[i][1], points[i][0]
        for j in range(-hwSize,hwSize+1):
            for k in range(-hwSize,hwSize+1):
                B[wSize * i + counter] = img[row + j, col + k, 0]
                G[wSize * i + counter] = img[row + j, col + k, 1]
                R[wSize * i + counter] = img[row + j, col + k, 2]
                counter = counter + 1
        counter = 0
    return R, G, B, points_num, points



if __name__ == '__main__':
    img = cv2.imread("data/test1.jpg")
    points = get_point_from_img(img)
    print(points)
    R, G, B, points_num, points = getPoint(img, points, wind_size=7)
    # print(R)
    # print(G)
    # print(B)
    d = 7  # Mahalanobis distance in fence detection
    th = 8  # thrash hold for connected components
    dilSize = 13  # dilation element size
