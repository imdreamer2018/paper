# coding=utf-8
import numpy as np
#csv用于方便的处理index.csv文件
import csv

class Searcher:
    #indexPath，用于表示index.csv文件在磁盘上的路径
    def __init__(self,indexPath):
        self.indexPath = indexPath
    #queryFeatures是提取自待搜索图像（如向CBIR系统提交并请求返回相似图像的图像），和返回图像的数目的最大值。
    def search(self,queryFeatures, limit=5):
        #初始化results字典
        #每个图像有唯一的imageID，可以作为字典的键，而相似度作为字典的值
        results = {}

        #打开index.csv文件
        with open(self.indexPath) as f:
            #获取CSV读取器的reader
            reader = csv.reader(f)
            #循环读取index.csv文件的每一行
            for row in reader:
                #解析出图像ID和特征，然后计算索引中的要素与查询要素之间的卡方距离
                features = [float(x) for x in row[1:]]

                #对于每一行，提取出索引化后的图像的颜色直方图,chi2_distance函数将其与待搜索的图像特征进行比较
                d = self.chi2_distance(features, queryFeatures)
                #现在我们有两个特征向量之间的距离，我们可以使用结果字典 -
                # 关键字是索引中的当前图像ID，
                # 值是我们刚刚计算的距离，表示索引中图像的“相似”程度是我们的查询
                results[row[0]] = d

            #关闭reader
            f.close()

        #对我们的结果进行排序，以便更小的距离（即更相关的图像位于列表的前面）
        #results字典根据相似读升序排序,卡方相似度为零的图片表示完全相同。相似度数值越高，表示两幅图像差别越大。
        results = sorted([(v, k) for (k, v) in results.items()])
        #返回我们限制数量的结果
        return results[:limit]

    #chi2_distance函数需要两个参数，即用来进行比较的两个直方图。可选的eps值用来预防除零错误
    def chi2_distance(self, histA, histB, eps=1e-10):
        # 计算卡方距离
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
                          for (a, b) in zip(histA, histB)])

        # 返回卡方距离
        return d
