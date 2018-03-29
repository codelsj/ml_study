#coding=utf-8

from numpy import *
import operator

#knn


def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classfiy0(inX,dataSet,labels,k):
    dataSetSize = dataSet.shape[0]      #shape (row_num,col num) tuple
    diffMat = tile(inX,(dataSetSize,1)) - dataSet       #copy四份和已知数据求差
    sqDiffMat = diffMat**2                  #对数组的每个值平方
    sqDistances = sqDiffMat.sum(axis=1)     #将每行相加
    distances = sqDistances**0.5            #对每个值开方
    sortDist = distances.argsort()          #得到排序后的数据原来位置下标

    classCount = {}
    for i in range(k):
        voteLable = labels[sortDist[i]]
        classCount[voteLable] = classCount.get(voteLable,0) + 1

    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)   #按字典值排序,classCount.iteritems()生成迭代器，可看做（k,v）列表，operator.itemgetter(1) 相当于lambda x:x[1]

    
    return sortedClassCount[0][0]
    


if __name__ == '__main__':
    group,labels = createDataSet()
    classfiy0([0,0],group,labels,3)
    #print group
    # print labels
        
