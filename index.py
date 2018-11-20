 # coding=utf-8
#导入必要的包
#需要argparse模块来处理命令行参数、glob来获取图像的文件路径，以及cv2来使用OpenCV的接口
from pyimagesearch.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

#构造参数解析器并解析参数
ap = argparse.ArgumentParser()
#处理命令行指令。这里需要两个指令，–dataset，表示假期相册的路径。–index，表示输出的CSV文件含有图像文件名和对应的特征
ap.add_argument("-d","--dataset",required = True,
                help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
	            help = "Path to where the computed index will be stored")
args = vars(ap.parse_args())

#初始化ColorDescriptor
cd = ColorDescriptor((8,12,3))

#打开输出文件
output = open(args["index"],"w")

#遍历数据集中的所有图像
for imagePath in glob.glob(args["dataset"]+"/*.jpg"):
    #从图像路径提取图像ID（即唯一文件名）并加载图像本身
    imageID = imagePath[imagePath.rfind("/")+1:]
    print(imageID)
    image = cv2.imread(imagePath)

    #对图像使用图像描述符并提取特征,ColorDescriptor的describe方法返回由浮点数构成的列表，用来量化并表示图像
    try:
        features = cd.describe(image)
    except:
        print(imageID)
    #将图像的文件名和管理的特征向量写入文件
    features = [str(f) for f in features]
    output.write("%s,%s" % (imageID, ",".join(features))+'\n')

#关闭输出文件
output.close()