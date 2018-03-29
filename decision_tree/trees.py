#!/usr/bin/env python
#coding=utf-8
 
'''
File: trees.py
Author: foglsj@126.com
Date: 2018/02/28 19:00:29
'''
import pickle
from math import log

def cal_ent(date_set):
    """计算香浓熵"""
    num_entries = len(date_set)
    label_count = {}
    for feat_ver in date_set:
        label = feat_ver[-1]
        if label not in label_count:
            label_count[label] = 0
        label_count[label] += 1
    ent = 0
    for key in label_count:
        prob = label_count[key] * 1.0 / num_entries
        ent += - prob * log(prob, 2)

    return ent

def create_dataset():
    date_set = [[1, 1, 'yes'],
                [1, 1, 'yes'],
                [1, 0, 'no'],
                [0, 1, 'no'],
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return date_set, labels


def split_dataset(data_set, axis, value):
    """
    指定特征和值，返回该特征为给定值的数据集（删除该特征）
    Attrs:
        axis: 轴，即第n列（第几个特征)
        value: 返回值
    """
    data_set_mod = []
    for feat_ver in data_set:
        if feat_ver[axis] == value:
            #删除此特征后的结果
            deleted_ver = feat_ver[:axis] + feat_ver[axis + 1:]
            data_set_mod.append(deleted_ver)
    return data_set_mod


def choose_best_feat(data_set):
    """选择最好的特征进行划分
      遍历每个特征
      选择max（含该特征熵-不含该特征时的熵）
      即哪个特征带来的熵增量最大
            
    """
    #特征数
    len_feat = len(data_set[0][:-1])
    base_ent = cal_ent(data_set)
    max_delta_ent = 0 #最大信息增益
    best_feat = -1    #最大信息增益对应的特征
    for i in range(len_feat):
        #选取第i列作为向量
        feat_list = [e[i] for e in data_set]
        feat_vals = set(feat_list)
        
        #计算第i个特征划分数据后的墒,
        #把划分后的n个数据子集又可以看做一次计算墒期望
        #ent_i = ∑ p * ent  
        
        ent_i = 0
        for val in feat_vals:
            sub_dataset = split_dataset(data_set, i, val)
            prob = len(sub_dataset) * 1.0 / len(data_set)
            ent_i += prob * cal_ent(sub_dataset)
        
        delta_ent = base_ent - ent_i
        if delta_ent > max_delta_ent:
            max_delta_ent = delta_ent
            best_feat = i
    return best_feat

def major_cnt(class_list):
    """投票表决法，当特征使用完时，选择最多的类来代表整体"""
    class_count = {}
    for vote in class_list:
        if vote not in class_count:
            class_count[vote] = 0
        class_count[vote] += 1
    sort_class = sorted(class_count.items(), key=lambda x: x[1], reverse=True)
    return sort_class[0][0]
        

def create_tree(data_set, labels):
    """构建决策树
        采用递归法，若类别都相同，则停止划分
       """
    class_list = [e[-1] for e in data_set]
    if len(set(class_list)) == 1:
       return class_list[0]

    if len(data_set[0]) == 1:
        return major_cnt(class_list)

    best_feat_index = choose_best_feat(data_set)
    best_feat_label = labels[best_feat_index]
    desc_tree = {best_feat_label:{}}
    feat_value_list = [e[best_feat_index] for e in data_set]
    uniq_values = set(feat_value_list)
    for value in uniq_values:
        sub_labels = labels[:best_feat_index] + labels[best_feat_index+1:]
        sub_dataset = split_dataset(data_set, best_feat_index, value)
        desc_tree[best_feat_label][value] = create_tree(sub_dataset, sub_labels)

    return desc_tree

            


def test():
    mat, labels = create_dataset()

    #print  cal_ent(mat)

    #print split_dataset(mat, 0, 1) #选取第0个特征等于1的数据集
    #print split_dataset(mat, 0, 0) #选取第0个特征等于1的数据集

    #print choose_best_feat(mat)
    tree =  create_tree(mat, labels)
    #print classify(tree, labels, [1, 0])
    #print classify(tree, labels, [1, 1])
    store_tree(tree, 'tree.data')
    print grab_tree('tree.data')


def classify(tree, feat_labels, test_vec):
    first_key = tree.keys()[0]
    index = feat_labels.index(first_key)


    second_dict = tree[first_key]
    class_label = '-'  #未分类
    for key in second_dict:
        if test_vec[index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                #此时，长度已经为为1
                class_label = second_dict[key]
    return class_label


def store_tree(tree, filename):
    """持久化"""
    fw = open(filename, 'w')
    pickle.dump(tree, fw)
    fw.close()


def grab_tree(filename):
    fr = open(filename)
    tree = pickle.load(fr)
    fr.close()
    return tree


if __name__ == '__main__':
    test()

        
