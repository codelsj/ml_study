#coding=utf-8

from numpy import *

import matplotlib.pyplot as plt
import knn
'''
author:liushaojiang
date:2016/10/23
email:foglsj@126.com
desc: ����Լ����վ�ĸ������ԣ�����Ⱥ���࣬ ���ԡ�����ѧϰʵս��
'''

def file2matrix(filename):
    '''
        ���ı�����ת��Ϊ����
        col1��ÿ����о���
        col2������Ƶ��Ϸ����ʱ��ٷֱ�
        col3��ÿ�����ѵı���ܹ�����
        col4��lable  largeDoses smallDoses didntLike
    '''
    
    fr = open(filename)
    arraryLines = fr.readlines()
    numOfLines = len(arraryLines)
    returnMat = zeros((numOfLines,3))  #numOfline * 3 ȫΪ0�Ķ�ά����
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
        ��ͼչʾЧ��
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.scatter(dataMat[:,1],dataMat[:,2])
    #print 15.0*array(classLabelVector)
    #�����е�ÿ�����Ա�ǩֵ*15�����������Сû��
    #����������Ϊs������Ĵ�С
    #���ĸ�����Ϊc����color
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
        ���Ժ���
    '''
    testRatio = 0.1  #ѡȡ10%��Ϊ���Լ�
    dataSet,classLabelVector = file2matrix('datingTestSet2.txt')
    normData, ranges, minVal = knn.autoNormal(dataSet)
    m = normData.shape[0]      
    numTest = int(m*testRatio)      #���Լ��ϴ�С
    
    rightCount = 0
    
    #ǰnumTest�����Լ�
    for i in range(numTest):
    
        classRet = knn.classfiy0(normData[i,:],normData[numTest:m,:],classLabelVector[numTest:m],11)
        realRet = classLabelVector[i]
        print "real:%s,class:%s"%(realRet,classRet)
        if classRet == realRet:
            rightCount += 1
    print 'total=%s,rightCount=%s,right rate=%.2f%%'%(numTest,rightCount,rightCount*100.0/numTest)
       
        
    
    
if __name__ == '__main__':
    dataTest()
    
  
   