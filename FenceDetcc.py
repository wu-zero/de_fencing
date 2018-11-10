import numpy as np
import cv2
from GetPoint import get_point_from_img, getPoint
from Setting import resize

def fenceDetcc(img, R, G, B, points_num, wind_size, treshold):
    img = img.copy()
    y_length, x_length, _ = img.shape
    wSize = wind_size * wind_size
    hwSize = int(wind_size / 2)

    S_points_num = points_num * wSize  # 区域点个数
    k = 1 / S_points_num

    mewR = np.sum(R) / S_points_num
    mewG = np.sum(G) / S_points_num
    mewB = np.sum(B) / S_points_num


    r_error = R - mewR
    g_error = G - mewG
    b_error = B - mewB
    Srr = k * np.sum(np.multiply(r_error, r_error))
    Srg = k * np.sum(np.multiply(r_error, g_error))
    Srb = k * np.sum(np.multiply(r_error, b_error))

    Sgr = k * np.sum(np.multiply(g_error, r_error))
    Sgg = k * np.sum(np.multiply(g_error, g_error))
    Sgb = k * np.sum(np.multiply(g_error, b_error))

    Sbr = k * np.sum(np.multiply(b_error, r_error))
    Sbg = k * np.sum(np.multiply(b_error, g_error))
    Sbb = k * np.sum(np.multiply(b_error, b_error))


    Sigma = [[Srr,Srg,Srb],
             [Sgr,Sgg,Sgb],
             [Sbr,Sbg,Sbb]]

    Sigma_mat = np.mat(Sigma)
    iSigma = Sigma_mat.I


    mask = np.zeros((y_length,x_length),dtype=np.uint8)
    for i in range(y_length):
        for j in range(x_length):
            cB = img[i,j,0]
            cG = img[i,j,1]
            cR = img[i,j,2]

            A = np.mat([cR - mewR,cG - mewG, cB -mewB])

            d = A * iSigma * A.T
            if d < treshold:
                img[i,j,:] = 0
                mask[i,j] = 255

    cv2.imshow("img with original mask", img)
    cv2.waitKey(0)
    cv2.imshow("original mask",mask)
    cv2.waitKey(0)
    return mask


if __name__ == '__main__':
    # 获得要处理的图片
    img = cv2.imread("data/exp1.jpg")
    #img = resize(img)
    # 获得栅栏样本像素点  获得样本点周围像素点
    points = get_point_from_img(img)
    R, G, B, points_num, points = getPoint(img, points, wind_size=7)
    # 获得原始栅栏mask
    mask = fenceDetcc(img, R, G, B, points_num, wind_size=7, treshold=7)



