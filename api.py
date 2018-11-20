# coding=utf-8
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2

# #构造参数解析器并解析参数
# ap = argparse.ArgumentParser()
# #–index来表示index.csv文件的位置
# ap.add_argument("-i", "--index", required = True,
# 	help = "Path to where the computed index will be stored")
# #–query来表示带搜索图像的存储路径。该图像将与数据集中的每幅图像进行比较。
# # 目标是找到数据集中欧给你与待搜索图像相似的图像
# ap.add_argument("-q", "--query", required = True,
# 	help = "Path to the query image")
# #–result-path，用来表示相册数据集的路径。
# # 通过这个命令可以选择不同的数据集，向用户显示他们所需要的最终结果
# ap.add_argument("-r", "--result-path", required = True,
# 	help = "Path to the result path")
# args = vars(ap.parse_args())
def check(limit):
    args={"query":"queries/a.jpg","index":"whpu.csv"}
    #初始化图像描述符
    cd = ColorDescriptor((8, 12, 3))

    #从磁盘读取待搜索图像
    query = cv2.imread(args["query"])
    #提取该图像的特征
    features = cd.describe(query)

    #执行搜索
    #使用提取到的特征进行搜索，返回经过排序后的结果列表
    searcher = Searcher(args["index"])
    results = searcher.search(features,limit)

    #显示出待搜索的图像
    #cv2.imshow("Query", query)
    result_files_data=[]

    #遍历搜索结果，将相应的图像显示在屏幕上
    for (score, resultID) in results:
        result = "dataset/" + resultID
        result_files_data.append([score, result])

    return result_files_data

