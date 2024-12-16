# coding=utf-8  
from numpy import *
import time          
import re          
import os  
import sys
import codecs
import shutil
import numpy as np
import matplotlib
import scipy
import matplotlib.pyplot as plt
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer 

if __name__ == "__main__":
    
    #第一步 计算TFIDF
    
    #文档预料 空格连接
    corpus = []
    
    #读取预料 一行预料为一个文档
    for line in open('/Users/cuihongzhen/Desktop/01-材料/04-北京科技大学/95-论文4-材料知识库抽取及构建/RAKE-master/zhibiao2.txt', 'r').readlines():
        corpus.append(line.strip())
    
    #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    #该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    #获取词袋模型中的所有词语  
    word = vectorizer.get_feature_names()

    #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()

    #打印特征向量文本内容
    print('Features length: ' + str(len(word)))
    resName = "BHTfidf_Result.txt"
    result = codecs.open(resName, 'w', 'utf-8')
    for j in range(len(word)):
        result.write(word[j] + ' ')
    result.write('\r\n\r\n')

    #打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重  
    for i in range(len(weight)):
        #print u"-------这里输出第", i, u"类文本的词语tf-idf权重------"  
        for j in range(len(word)):
            #print weight[i][j],
            result.write(str(weight[i][j]) + ' ')
        result.write('\r\n\r\n')

    result.close()


    #第二步 聚类Kmeans
    print('Start Kmeans:')
    from sklearn.cluster import KMeans
    clf = KMeans(n_clusters=7)   #聚类分析分？类
    s = clf.fit(weight)
    print(s)

    #中心点
    print(clf.cluster_centers_)
    
    #每个样本所属的簇
    label = []               #存储1000个类标 4个类
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i-1])
        label.append(clf.labels_[i-1])
        i = i + 1

    #用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
    print(clf.inertia_)



    #第三步 图形输出 降维
    print('图形输出，降维：')
    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)             #输出两维
    newData = pca.fit_transform(weight)   #载入N维
    print("打印newData:")
    print(newData)

    x=[]
    y=[]
    t=0
    while t<135:
        x.append((newData[t][0]))
        y.append((newData[t][1]))
        t += 1

    #5A景区-
    x1 = []
    y1 = []
    i=0
    while i<15:
        print("测试：进入到while了：")
        print(i)
        x1.append(newData[i][0])
        y1.append(newData[i][1])
        i += 1

    #Ti knowledge 1
    x2 = []
    y2 = []
    i = 15
    while i<30:
        x2.append(newData[i][0])
        y2.append(newData[i][1])
        i += 1

    #Ti knowledge 2
    x3 = []
    y3 = []
    i = 30
    while i<45:
        x3.append(newData[i][0])
        y3.append(newData[i][1])
        i += 1

    #Ti knowledge 3
    x4 = []
    y4 = []
    i = 45
    while i < 78:
        x4.append(newData[i][0])
        y4.append(newData[i][1])
        i += 1

    #Ti knowledge 4
    x5 = []
    y5 = []
    i = 78
    while i < 96:
        x5.append(newData[i][0])
        y5.append(newData[i][1])
        i += 1

    #Ti knowledge 5
    x6 = []
    y6 = []
    i = 96
    while i < 118:
        x6.append(newData[i][0])
        y6.append(newData[i][1])
        i += 1

    #Ti knowledge 6
    x7 = []
    y7 = []
    i = 118
    while i<135:
        x7.append(newData[i][0])
        y7.append(newData[i][1])
        i += 1


    # 分开展示图-重要
    # plt.subplot(3, 3, 1)
    # plt.plot(x1, y1, 'or', markersize=3)
    # xx1 = array(mat(x1))
    # yy1 = array(mat(y1))
    # plt.scatter(xx1[:,0], yy1[:,-1], marker='X', c='black', s=30)
    # plt.title("(a)")
    #
    # plt.subplot(3, 3, 2)
    # plt.plot(x2, y2, 'og', markersize=3)
    # xx2 = array(mat(x2))
    # yy2 = array(mat(y2))
    # plt.scatter(xx2[:, 0], yy2[:, 3], marker='X', c='red', s=30)
    # plt.title("(b)")
    #
    # plt.subplot(3, 3, 3)
    # plt.plot(x3, y3, 'oy', markersize=3)
    # xx3 = array(mat(x3))
    # yy3 = array(mat(y3))
    # plt.scatter(xx3[:, -1], yy3[:, 2], marker='X', c='red', s=30)
    # plt.title("(c)")
    #
    # plt.subplot(3, 3, 4)
    # plt.plot(x4, y4, 'ob', markersize=3)
    # xx4 = array(mat(x4))
    # yy4 = array(mat(y4))
    # plt.scatter(xx4[:, 1], yy4[:, 0], marker='X', c='red', s=30)
    # plt.title("(d)")
    #
    # plt.subplot(3, 3, 5)
    # plt.plot(x5, y5, 'oc', markersize=3)
    # xx5 = array(mat(x5))
    # yy5 = array(mat(y5))
    # plt.scatter(xx5[:, 1], yy5[:, 0], marker='X', c='red', s=30)
    # plt.title("(e)")
    #
    # plt.subplot(3, 3, 6)
    # plt.plot(x6, y6, 'om', markersize=3)
    # xx6 = array(mat(x6))
    # yy6 = array(mat(y6))
    # plt.scatter(xx6[:, 2], yy6[:, 1], marker='X', c='red', s=30)
    # plt.title("(f)")
    #
    # plt.subplot(3, 3, 7)
    # plt.plot(x7, y7, 'ok', markersize=3)
    # plt.title("(g)")
    #
    # plt.subplot(3,3,8)
    # plt.plot(x, y, 'or', markersize=3)
    # plt.title("(h)")
    #
    # plt.subplot(3, 3, 9)
    # plt.plot(label, y, 'or', markersize=3)
    # plt.title("(i)")

    # 调整图间距
    # plt.subplots_adjust(left=0.08, bottom=0.05, right=0.97, top=0.95, wspace=0.5, hspace=0.6)

    # 综合展示图
    plt.plot(x1, y1, 'or')
    plt.plot(x2, y2, 'og')
    plt.plot(x3, y3, 'oy')
    plt.plot(x4, y4, 'ob')
    plt.plot(x5, y5, 'oc')
    plt.plot(x6, y6, 'om')
    plt.plot(x7, y7, 'ok')

    plt.subplots_adjust(left=0.08, bottom=0.07, right=0.97, top=0.95)

    plt.savefig("./details_all.svg")
    plt.savefig("./details_all.pdf")
    plt.show()


