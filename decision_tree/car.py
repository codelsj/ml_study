#!/usr/bin/env python
#coding=utf-8
 
'''
File: lenses.py
Author: foglsj@126.com
Date: 2018/03/05 16:53:54
'''
import trees
import tree_plotter
import random

fr = open('car.data')
lenses = [line.strip().split(',') for line in fr]
labels = ['buying', 'maint', 'doors', 'doors', 'persons', 'safety']
fr.close()
random.shuffle(lenses)
train = lenses[:1000]
test = lenses[1000:]

lenses_tree = trees.create_tree(train, labels)
#print lenses_tree
#tree_plotter.create_plot(lenses_tree)

err = 0
total = 0
call = 0
for vec in test:
    real = vec[-1]
    test_vec = vec[:-1]
    ret = trees.classify(lenses_tree, labels, test_vec)
    total += 1
    if ret == '-':
        continue
    call += 1
    if real != ret:
        err += 1
print '总体，召回，错误数，召回率，错误率'
print total, call, err, call * 1.0/total, err*1.0/call
    


