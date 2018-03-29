#!/usr/bin/env python
#coding=utf-8
 
'''
File: demo.py
Author: foglsj@126.com
Date: 2018/02/12 16:32:45
'''

import matplotlib.pyplot as plt

decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plot_node(text, center, parent, node_type):
    create_plot.ax1.annotate(text, xy=parent, xycoords="axes fraction" ,
    xytext=center, textcoords="axes fraction",
    va = "center", ha="center", bbox=node_type, arrowprops=arrow_args)

def plot_midtext(center, parent, text):
    """绘制连接中的文字"""
    x = (center[0] + parent[0]) / 2.0
    y = (center[1] + parent[1]) / 2.0
    create_plot.ax1.text(x, y, text)


def plot_tree(deci_tree, parent, mid_text):
    """绘制决策树
    Attrs:
        deci_tree: 树
        parent: 父节点位置，用于连接子父节点
        mid_text: 链接节点
    """
    num_leaf = get_num_leafs(deci_tree)
    depth = get_depth(deci_tree)

    #绘制节点
    #从左到右第一个节点文本
    first_text = deci_tree.keys()[0]
    
    node_center = (plot_tree.x_off + (1.0 + num_leaf) / 2.0 / plot_tree.total_w, plot_tree.y_off)
    plot_node(first_text, node_center, parent, decision_node)

    #绘制连接线上的文字
    plot_midtext(node_center, parent, mid_text)

    second_dict = deci_tree[first_text]

    plot_tree.y_off -= plot_tree.layer_d
    
    for key in second_dict:
        value = second_dict[key]
        if type(value).__name__ == 'dict':
            #子树
            plot_tree(value, node_center, key)
        else:
            plot_tree.x_off += plot_tree.layer_w
            #叶子节点
            plot_node(value, (plot_tree.x_off,  plot_tree.y_off), node_center, leaf_node)
            plot_midtext((plot_tree.x_off,  plot_tree.y_off), node_center, key)
    plot_tree.y_off += plot_tree.layer_d

            

'''
def create_plot():
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    #create_plot.ax1 给该函数定义的一个属性
    create_plot.ax1 = plt.subplot(111, frameon=False)
    plot_node(u'决策节点', (0.5, 0.1), (0.1, 0.5), decision_node)
    plot_node(u'叶子节点', (0.8, 0.1), (0.3, 0.8), leaf_node)
    plt.show()
'''
def create_plot(deci_tree):
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    #create_plot.ax1 给该函数定义的一个属性
    axprops = dict(xticks=[], yticks=[])
    create_plot.ax1 = plt.subplot(111, frameon=False, **axprops)

    plot_tree.total_w = get_num_leafs(deci_tree)
    plot_tree.total_d = get_depth(deci_tree)
    #一层深度距离
    plot_tree.layer_d = 1.0 / plot_tree.total_d 
    plot_tree.layer_w = 1.0 / plot_tree.total_w

    plot_tree.x_off = -0.5 / plot_tree.total_w
    plot_tree.y_off = 1.0
    plot_tree(deci_tree, (0.5, 1), '')
    plt.show()

    

def get_num_leafs(deci_tree):
    """得到决策树的叶子节点个数"""
    num = 0
    for key in deci_tree:
        value = deci_tree[key]
        if type(value).__name__ == 'dict':
            num += get_num_leafs(value)
        else:
            num += 1
    return num


def get_depth(deci_tree):
    """获取树的深度,对每次递归，找到子树中最大的深度"""
    max_depth = 0
    for key in deci_tree:
        value = deci_tree[key]
        if type(value).__name__ == 'dict':
            child_depth = 1 + get_depth(value)
        else:
            child_depth = 1
        if child_depth > max_depth:
            max_depth = child_depth
    return max_depth

            
def retrieve_tree():
    """测试树的长度和深度"""
    deci_tree = {'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}}
    #print get_num_leafs(deci_tree)
    #print get_depth(deci_tree)
    create_plot(deci_tree)


if __name__ == '__main__':
    retrieve_tree()
    #create_plot()

