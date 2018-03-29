#!/usr/bin/env python
 
'''
File: lenses.py
Author: foglsj@126.com
Date: 2018/03/05 16:53:54
'''
import trees
import tree_plotter

fr = open('lenses.data')
lenses = [line.strip().split('\t') for line in fr]
print lenses
labels = ['age', 'presctipt', 'astigmatic', 'tearRate']
fr.close()
lenses_tree = trees.create_tree(lenses, labels)
print lenses_tree
tree_plotter.create_plot(lenses_tree)

