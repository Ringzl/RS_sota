
import math
from tqdm import tqdm
import numpy as np
import pandas as pd
from collections import Counter
from scipy.sparse import csc_matrix
from sklearn.metrics.pairwise import cosine_similarity



def load_data(user_path, item_path, train_path, test_path):
    """
    载入数据
    """
    
    user_dct = {}
    item_dct = {}

    with open(user_path, 'r') as fp:
        next(fp)
        for line in fp:
            ll = line.strip().split(' ')
            if len(ll) == 2:
                org_id, remap_id = ll
                user_dct[remap_id] = org_id
            

    with open(item_path, 'r') as fp:
        next(fp)
        for line in fp:
            ll = line.strip().split(' ')
            if len(ll) == 2:
                org_id, remap_id = ll
                item_dct[remap_id] = org_id

    
    user_item_dct_train = {}
    with open(train_path, 'r') as fp:
        next(fp)
        cnt = 0
        for line in fp:
            ll = line.strip().split(' ')
            
            uid = ll[0]
            item_lst = ll[1:]
            user_item_dct_train[uid] = item_lst
            cnt += 1

            if cnt == 10:
                break

    user_item_dct_test = {}
    with open(test_path, 'r') as fp:
        next(fp)
        for line in fp:
            ll = line.strip().split(' ')
            
            uid = ll[0]
            item_lst = ll[1:]
            user_item_dct_test[uid] = item_lst

    return user_dct, item_dct, user_item_dct_train, user_item_dct_test




def usercf_sim(user_item_dct):
    """
    用户相似性矩阵计算 (优化：避免重复计算对称相似度)
    """
   
    # O(N^2) 很多用户之间并没有交集,稀疏数据
    # u2u_sim = {} 
    # for u1 in user_item_dct.keys():
    #     u2u_sim.setdefault(u1, {})
    #     for u2 in user_item_dct.keys():
    #         if u1 == u2:
    #             continue
    #         u1_set = set(user_item_dct[u1])
    #         u2_set = set(user_item_dct[u2])
    #         u2u_sim[u1][u2] = len(u1_set & u2_set) / math.sqrt(len(u1_set) * len(u2_set))
    
    # 优化： 建立物品到用户的倒排表，扫描倒排表，建立用户相似度矩阵分子部分
    item_user_dct = {}
    for u, items in tqdm(user_item_dct.items()):
        for i in items:
            item_user_dct.setdefault(i, set())
            item_user_dct[i].add(u)
    
    u2u_cnt = {} # 两个用户都评价过的物品数量
    u_cnt = {} # 用户总共评价过几个物品
    for i, users in tqdm(item_user_dct.items()):
        for u in users:
            u_cnt.setdefault(u, 0)
            u_cnt[u] += 1
            
            u2u_cnt.setdefault(u, {})
            for v in users:
                u2u_cnt[u].setdefault(v, 0)
                if u == v:
                    continue
                u2u_cnt[u][v] += 1
    
    u2u_sim = {} 
    for u1, u2 in tqdm(u2u_cnt.items()):
        u2u_sim.setdefault(u1, {})
        for v,num in u2.items():
            if u1 == v:
                continue

            u2u_sim[u1].setdefault(v, 0.0)
            u2u_sim[u1][v] = num / math.sqrt(u_cnt[u1] * u_cnt[v])
    
    return u2u_sim


# 推荐

def predict(userA, item, u2u_sim):
    """
    预测
    """
    score = 0.0

    for user in u2u_sim[userA].keys():
        if user != userA:
            score += u2u_sim[userA][user] 
    return score

def user_cf(userA, item_dct, user_item_dct, u2u_sim):
    """
    找出top相似用户
    """
    user_item_score_dict = dict()
    for item in item_dct.keys():
        if item not in user_item_dct[userA]:
            user_item_score_dict[item] = predict(userA, item, u2u_sim)

    return user_item_score_dict
    

def main():
    

    # 读取训练数据
    user_path = '/home/yongcun/work/RS_sota/data/AmazonBooks_m1/user_list.txt'
    item_path = '/home/yongcun/work/RS_sota/data/AmazonBooks_m1/item_list.txt'
    train_path = '/home/yongcun/work/RS_sota/data/AmazonBooks_m1/train.txt'
    test_path = '/home/yongcun/work/RS_sota/data/AmazonBooks_m1/test.txt'
    user_dct, item_dct, user_item_dct_train, user_item_dct_test = load_data(user_path, item_path, train_path, test_path)
    u2u_sim = usercf_sim(user_item_dct_train)
    user_item_score_dict = user_cf('1', item_dct, user_item_dct_train, u2u_sim)
    print(u2u_sim)
    print(user_item_score_dict)

if __name__ == "__main__":
    main()

