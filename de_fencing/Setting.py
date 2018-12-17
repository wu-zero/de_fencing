import cv2
import os

data_file_path = '../test/'
img_name = 'monkey.jpg'
result_file_path = '../result/'

use_line_feature_flag = True


class Setting:
    def __init__(self):
        self.img_original = None
        self.img_to_solve = None
        self.ratio = 1
        self._img_init()
        self.img_original_shape = tuple(self.img_original.shape[1::-1])
        self.img_to_solve_shape = tuple(self.img_to_solve.shape[1::-1])

        self.use_line_feature_flag = use_line_feature_flag

        self.result_file_path = result_file_path + img_name[0:-4]
        self._make_dir(self.result_file_path)
        cv2.imwrite(self.result_file_path + os.sep + 'original.jpg',self.img_original)
        if self.img_mask is not None:
            cv2.imwrite(self.result_file_path + os.sep + 'standard_mask.jpg',self.img_mask)


    def _img_init(self):
        img_path = data_file_path + img_name
        mask_path = data_file_path + img_name[:-4]+'_mask.png'
        #print(mask_path)
        # 获得要处理的图片
        self.img_original = cv2.imread(img_path)
        self.img_mask = cv2.imread(mask_path)
        print('图片大小', self.img_original.shape)
        self.img_to_solve, self.ratio = self._resize(self.img_original)
        print('缩放后图片大小', self.img_to_solve.shape)


    def recovery_resize(self, img):
        return cv2.resize(img, self.img_original_shape, interpolation=cv2.INTER_AREA)

    # 缩放图片用的
    @staticmethod
    def _resize(img, ratio=None):
        height, width = img.shape[:2]
        if ratio is None:
            ratio = ((480 * 640) / (height * width)) ** 0.5
        # 缩小图像
        size = (int(width * ratio), int(height * ratio))
        img_shrink = cv2.resize(img, size, interpolation=cv2.INTER_AREA)

        # 显示
        cv2.imshow("img", img)
        cv2.imshow("img_resize", img_shrink)
        cv2.waitKey(0)
        cv2.destroyWindow("img")
        cv2.destroyWindow("img_resize")
        return img_shrink, ratio

    @staticmethod
    def _make_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)
            print('文件夹新建成功')
        else:
            print('文件夹存在')


if __name__ == '__main__':
    st = Setting()
