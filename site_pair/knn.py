#coding=utf-8

from numpy import *
import operator

#knn


def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classfiy0(inX,dataSet,labels,k):
    '''
        inX:未知类别数据
        dataSet:已知类别数据
        labels：dataSet对应类别
        k：knn的系数
    '''
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
    
def autoNormal(dataSet):
    '''
        按列维度把区间缩小到0-1，即等比例缩小
    '''

    #找出三列中每一列最小/大值组成一个数组
    minVal = dataSet.min(0)
    maxVal = dataSet.max(0)
    ranges = maxVal - minVal
    normaData = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normaData = dataSet - tile(minVal,(m,1))     #tile(minVal,(m-1)) 将minVal数组0维copy m 。赋值意思是，将每个值和该列最小值做差
    normaData = normaData/tile(ranges,(m,1))     #差值（此位置值-此列最小值）/（此列最大值-此列最小值） 即把所有值归一到0-1之间
    return normaData, ranges, minVal
   


if __name__ == '__main__':
    group,labels = createDataSet()
    classfiy0([0,0],group,labels,3)
    #print group
    # print labels
        
