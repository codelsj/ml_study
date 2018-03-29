#coding=utf-8

'''
    手写体识别
    date:2016/11/06
'''
from numpy import *
import os
import knn

def img2vector(filename):
    '''
        图形格式（32*32）转换为1*1024的向量
    '''
    dataMat = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            dataMat[0,i*32+j] = int(line[j])
    fr.close()
    return dataMat
    
    
def handwriteTest():
    '''
        测试
    '''
    hw_labels = []
    tranning_path = 'digits/trainingDigits'
    training_files = os.listdir(tranning_path)
    m = len(training_files)
    trainingMat = zeros((m,1024))
    for i in range(m):
        filename = training_files[i]
        items = filename.split('.')[0].split('_')
        class_label = int(items[0])
        hw_labels.append(class_label)
        trainingMat[i,:] = img2vector('%s/%s'%(tranning_path,filename))
        
    #test
    test_path = 'digits/testDigits'
    test_files = os.listdir(test_path)
    numTest = len(test_files)
    rightCount = 0
    for filename in test_files:
        items = filename.split('.')[0].split('_')
        real_label = int(items[0])
        dataMat = img2vector('%s/%s'%(test_path,filename))
        call_label =  knn.classfiy0(dataMat,trainingMat,hw_labels,3)
        print "real:%s,class:%s"%(real_label,call_label)
        if real_label == call_label:
            rightCount += 1
    print 'total=%s,rightCount=%s,right rate=%.2f%%'%(numTest,rightCount,rightCount*100.0/numTest)
        

    

if __name__ == '__main__':
    #dataMat = img2vector('digits/testDigits/0_0.txt')
    #print dataMat
    handwriteTest()