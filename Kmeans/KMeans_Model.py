# coding: utf-8
# dataSet样本点,k 簇的个数
# disMeas距离量度，默认为欧几里得距离
# createCent,初始点的选取
from numpy import *

def loadDataSet(fileName):#自己重写了一个
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split()
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def distEclud(a, b):#计算欧式距离
    return sqrt(sum(power(a - b, 2)))

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))#创建质心矩阵
    for j in range(n):#在每个维度的范围内创建随机聚类中心
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = mat(minJ + rangeJ * random.rand(k,1))
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):#这里distMeans方便以后使用别的距离计算，闵科夫斯基的什么。。以后再写
    m = shape(dataSet)[0] #样本数
    clusterAssment = mat(zeros((m,2))) #m*2的矩阵
    centroids = createCent(dataSet, k) #初始化k个中心
    clusterChanged = True#来个布尔变量
    while clusterChanged:      #当质心的位置不再变化了
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k): #找到最近的质心
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            # 第1列为所属质心，第2列为距离
            clusterAssment[i,:] = minIndex,minDist**2
        #print centroids

        # 更改质心位置
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment

def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    # 这里第一列为类别，第二列为SSE
    clusterAssment = mat(zeros((m,2)))
    # 看成一个簇是的质心
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList =[centroid0] #创建一个带有一个质心的列表
    for j in range(m):    #计算只有一个簇时的误差
        clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2

    # 核心代码
    while (len(centList) < k):
        lowestSSE = inf
        # 对于每一个质心，尝试的进行划分
        for i in range(len(centList)):
            # 得到属于该质心的数据
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
            # 对该质心划分成两类
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            # 计算该簇划分后的SSE
            sseSplit = sum(splitClustAss[:,1])
            # 没有参与划分的簇的SSE
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            #print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
            # 寻找最小的SSE进行划分
            # 即对哪一个簇进行划分后SSE最小
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit

        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss
    return mat(centList), clusterAssment


