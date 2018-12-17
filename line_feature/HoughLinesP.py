import cv2
import numpy as np
import de_fencing.Parameter as PARM


def find_line_through_hough(img):
    img = cv2.GaussianBlur(img,(5,5),0)
    #  边缘检测
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#灰度图像
    edges = cv2.Canny(gray, 30, 120, apertureSize=3) # 50 150
    cv2.imshow('edges', edges)
    cv2.waitKey()
    #  hough检测
    lines = cv2.HoughLinesP(edges, 1.0, np.pi/180, threshold=PARM.threshold, minLineLength=PARM.minLineLength,
                            maxLineGap=PARM.maxLineGap)  # threshold=*, minLineLength=*,maxLineGap=*)
    lines1 = lines[:,0,:]  # 提取为二维
    #print('检测到的直线',lines1)
    for x1,y1,x2,y2 in lines1[:]:
        cv2.line(img, (x1,y1),(x2,y2),(255,0,0),2)
    cv2.imshow('lines',img)
    cv2.waitKey()
    # cv2.imwrite('3_lines.jpg', img)
    return lines1


if __name__ == '__main__':
    pass
