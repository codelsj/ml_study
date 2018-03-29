#coding=utf-8

from numpy import *

import matplotlib.pyplot as plt
import knn
'''
author:liushaojiang
date:2016/10/23
email:foglsj@126.com
desc: 根据约会网站的个人属性，将人群分类， 来自《机器学习实战》
'''

def file2matrix(filename):
    '''
        将文本特性转换为数组
        col1：每年飞行距离
        col2：玩视频游戏所耗时间百分比
        col3：每周消费的冰淇淋公升数
        col4：lable  largeDoses smallDoses didntLike
    '''
    
    fr = open(filename)
    arraryLines = fr.readlines()
    numOfLines = len(arraryLines)
    returnMat = zeros((numOfLines,3))  #numOfline * 3 全为0的二维数组
    classLabelVector =  []
    index = 0
    
    for line in arraryLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector
    

def show(dataMat,classLabelVector):
    '''
        绘图展示效果
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.scatter(dataMat[:,1],dataMat[:,2])
    #print 15.0*array(classLabelVector)
    #给其中的每个属性标签值*15，整个数组大小没变
    #第三个参数为s，即点的大小
    #第四个参数为c，即color
    #ax.scatter(dataMat[:,1],dataMat[:,2],15.0*array(classLabelVector),array(classLabelVector))
    ax.scatter(dataMat[:,0],dataMat[:,1],15.0*array(classLabelVector),array(classLabelVector))
    plt.show()
    
def run():
    returnMat,classLabelVector = file2matrix('datingTestSet2.txt')
    #show(returnMat,classLabelVector)
    normaData, ranges, minVal = knn.autoNormal(returnMat)
    print normaData
    print ranges
    print minVal

    
def dataTest(): 
    '''
        测试函数
    '''
    testRatio = 0.1  #选取10%作为测试集
    dataSet,classLabelVector = file2matrix('datingTestSet2.txt')
    normData, ranges, minVal = knn.autoNormal(dataSet)
    m = normData.shape[0]      
    numTest = int(m*testRatio)      #测试集合大小
    
    rightCount = 0
    
    #前numTest做测试集
    for i in range(numTest):
    
        classRet = knn.classfiy0(normData[i,:],normData[numTest:m,:],classLabelVector[numTest:m],11)
        realRet = classLabelVector[i]
        print "real:%s,class:%s"%(realRet,classRet)
        if classRet == realRet:
            rightCount += 1
    print 'total=%s,rightCount=%s,right rate=%.2f%%'%(numTest,rightCount,rightCount*100.0/numTest)
       
        
    
    
if __name__ == '__main__':
    dataTest()
    
  
   