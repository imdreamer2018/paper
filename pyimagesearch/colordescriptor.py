# coding=utf-8
import numpy as np
import cv2

#定义了ColorDescriptor类。该类用来封装所有用于提取图像中3D HSV颜色直方图的逻辑
class ColorDescriptor:
    def __init__(self,bins):
        #存储对于3D直方图的bins的数量
        self.bins = bins

    def describe(self,image):
        #将从RGB颜色空间（或是BGR颜色空间，OpenCV以NumPy数组的形式反序表示RGB图像）转换为HSV颜色空间并初始化
        #初始化用于量化图像的特征列表features
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []

        #获取图像维度并计算图像的中心(x,y)
        (h,w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))

        #将图像分成四个矩形/分段（左上角，右上角，右下角，左下角）
        segments = [(0,cX,0,cY),(cX,w,0,cY),(cX,w,cY,h),(0,cX,cY,h)]

        #构建一个椭圆用来表示图像的中央区域
        #定义一个长短轴分别为图像长宽75%的椭圆。
        (axesX, axesY) = (int(w * 0.75) / 2, int(h * 0.75) / 2)
        #初始化一个空白图像（将图像填充0，表示黑色的背景），该图像与需要描述的图像大小相同
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        #cv2.ellipse函数绘制实际的椭圆
        cv2.ellipse(ellipMask, (int(cX), int(cY)), (int(axesX), int(axesY)), 0, 0, 360, (255,255,255), -1)


        for (startX, endX, startY, endY) in segments:
            # 为图像的每个角掩模分配内存，从中减去椭圆形的中心
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            #为图像的每个角绘制白色矩形
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            #将矩形减去中间的椭圆
            cornerMask = cv2.subtract(cornerMask, ellipMask)

            # 从图像中提取颜色直方图，然后更新特征向量
            hist = self.histogram(image, cornerMask)
            features.extend(hist)

            #从椭圆区域提取颜色直方图并更新特征向量
            hist = self.histogram(image, ellipMask)
            features.extend(hist)
            #返回特征向量
            return features

    #histogram方法需要两个参数，第一个是需要描述的图像，第二个是mask，描述需要描述的图像区域
    def histogram(self, image, mask):
        # 通过调用cv2.calcHist计算图像掩模区域的直方图，使用构造器中的bin数目作为参数
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                            [0, 180, 0, 256, 0, 256])
        #对直方图归一化
        hist = cv2.normalize(hist,hist).flatten()
        # 向调用函数返回归一化后的3D HSV颜色直方图
        return hist