#!/usr/bin/env python
#coding=utf-8
 
'''
File: bayes.py
Author: foglsj@126.com
Date: 2018/04/10 17:10:48
'''

import random
import pickle

import numpy as np
import feedparser

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            #returnVec[vocabList.index(word)] = 1   # set moudle
            returnVec[vocabList.index(word)] += 1 # bag moudle
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec


def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    #向量长度
    numWords = len(trainMatrix[0])
    #P(c1)
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    #p0Num = np.zeros(numWords)
    #p1Num = np.zeros(numWords)
    #p0Denom = 0.0 
    #p1Denom = 0.0
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)

    p0Denom = 2.0 
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])

        else:
            p0Num += trainMatrix[i]
            p0Denom +=  sum(trainMatrix[i])

    #p1Vect = p1Num / p1Denom  #分子，单词出现次数, 分母，该类别下所有单词总次数（句内去重）
    #p0Vect = p0Num / p0Denom
    p1Vect = np.log(p1Num / p1Denom)  #分子，单词出现次数, 分母，该类别下所有单词总次数（句内去重）
    p0Vect = np.log(p0Num / p0Denom)
    return p1Vect, p0Vect, pAbusive
    
def classifyNB(vec2Classify, p0v, p1v, pAbsuive):

    p1 = sum(vec2Classify * p1v) + np.log(pAbsuive)
    p0 = sum(vec2Classify * p0v) + np.log(1.0 - pAbsuive)
    #print p1, p0
    if p1 > p0:
        return 1
    else:
        return 0


def post_test():
    dataSet, trainCategory = loadDataSet()
    vocabList = createVocabList(dataSet)
    print vocabList
    trainMatrix = []
    for postDoc in dataSet:
        trainMatrix.append(setOfWords2Vec(vocabList, postDoc))
    p1Vect, p0Vect, pAbusive = trainNB0(trainMatrix, trainCategory)
    print p0Vect
    print p1Vect
    print pAbusive
    
    testEntry = ['love', 'my', 'dalmation']
    docList = setOfWords2Vec(vocabList, testEntry)
    print testEntry, classifyNB(docList, p0Vect, p1Vect, pAbusive) 

    testEntry = ['stupid', 'garbage']
    docList = setOfWords2Vec(vocabList, testEntry)
    print testEntry, classifyNB(docList, p0Vect, p1Vect, pAbusive) 


def textParse(text):
    import re
    listOfTokens = re.split(r'\W*', text)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]



def email_test():
    docList = []
    fullText = []
    classList = []
    for i in range(1, 26):
        wordList = textParse(open('email/spam/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)

        wordList = textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = createVocabList(docList)
    
    trainingSet = range(50); testSet = []
    #随机找10个测试集合
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []; trainClasses = []
    for i in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[i]))
        trainClasses.append(classList[i])

    #训练
    p1V, p0V, pSpam = trainNB0(trainMat, trainClasses)

    #测试
    error = 0
    for i in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[i])
        if classifyNB(wordVector, p0V, p1V, pSpam) != classList[i]:
            error += 1
            print 'error', docList[i]
    print 'error rate:', float(error) / len(testSet)
        

def calcMostFreq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(), key=operator.itemgetter(1), reverse=True)
    return [e[0] for e in sortedFreq[:30]]

def rss_test(feed0, feed1):
    docList = []
    fullText = []
    classList = []
    minLen = min(len(feed0['entries']), len(feed1['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)

        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = createVocabList(docList)
    topWords = calcMostFreq(vocabList, fullText)
    for w in topWords:
        vocabList.remove(w)

    trainingSet = range(2 * minLen); testSet = []
    #随机找10个测试集合
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []; trainClasses = []
    for i in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList, docList[i]))
        trainClasses.append(classList[i])

    #训练
    p1V, p0V, pSpam = trainNB0(trainMat, trainClasses)

    #测试
    error = 0
    for i in testSet:
        wordVector = setOfWords2Vec(vocabList, docList[i])
        if classifyNB(wordVector, p0V, p1V, pSpam) != classList[i]:
            error += 1
            print 'error', docList[i]
    print 'error rate:', float(error) / len(testSet)
    return  float(error) / len(testSet)

def pickdump(filename, feed):
    fw = open(filename, 'wb')
    pickle.dump(feed, fw)
    fw.close()


def pickload(filename):
    fr = open(filename)
    feed = pickle.load(fr)
    fr.close()
    return feed
        
def save_rss():
    import  pickle
    #feed0 = feedparser.parse('http://www.nasa.gov/rss/dyn/image_of_the_day.rss')
    #feed1 = feedparser.parse('http://sports.yahoo.com/nba/teams/hou/rss.xml')
    feed1 = feedparser.parse('http://feeds.newscientist.com/science-news')
    #pickdump('feed0', feed0)

    pickdump('feed1', feed1)

def printrss():
    feed0 = pickload('feed0')
    feed1 = pickload('feed1')
    for i in range(len(feed0['entries'])):
        print feed0['entries'][i]['summary'].encode('utf-8')
    print '-'* 10
    for i in range(len(feed1['entries'])):
        print feed1['entries'][i]['summary'].encode('utf-8')


if __name__ == '__main__':
    #email_test()

    #save_rss()
    #printrss()
    feed0 = pickload('feed0')
    feed1 = pickload('feed1')
    total = 0
    num = 0
    for i in range(10):

        err_rate = rss_test(feed0, feed1)
        num += 1
        total += err_rate
    print total/num
