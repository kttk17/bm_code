import sys
import argparse
from urllib.parse import urlparse
import re
import locale
from collections import defaultdict
import collections
from math import sqrt

# コマンドライン引数についての設定
parser = argparse.ArgumentParser()
parser.add_argument('inputfile1', type=str,
                    help='inputfile1')
parser.add_argument('inputfile2', type=str,
                    help='inputfile2')
args = parser.parse_args()

# inputfile1
userid_category_num_per_first = {}
with open(args.inputfile1, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.strip()
        if line == '':
            continue
        category_percentage = ((line.split(',', 1)[1][2:-1]).replace('{','').replace('}', '').replace(' ', '')).split(',')
        for i in range(len(category_percentage)):
            category_num = category_percentage[i].split(':')[0][1:-1]
            category_per = category_percentage[i].split(':')[1]
            category_num_per = str(category_num) + ':' + str(category_per)
            if line.split(',')[0] not in userid_category_num_per_first:
                userid_category_num_per_first[line.split(',')[0]] = {category_num_per}
            else:
                userid_category_num_per_first[line.split(',')[0]].add(category_num_per)

#inputfile2
userid_category_num_per_second = {}
with open(args.inputfile2, mode='r') as inputfile2:
    for line in inputfile2:
        line = line.strip()
        if line == '':
            continue
        category_percentage = ((line.split(',', 1)[1][2:-1]).replace('{','').replace('}', '').replace(' ', '')).split(',')
        for i in range(len(category_percentage)):
            category_num = category_percentage[i].split(':')[0][1:-1]
            category_per = category_percentage[i].split(':')[1]
            category_num_per = str(category_num) + ':' + str(category_per)
            if line.split(',')[0] not in userid_category_num_per_second:
                userid_category_num_per_second[line.split(',')[0]] = {category_num_per}
            else:
                userid_category_num_per_second[line.split(',')[0]].add(category_num_per)
# calc
match = 0
# 前半
for first_id in userid_category_num_per_first.keys():
    user_data_first = list(userid_category_num_per_first[first_id])
    dict_user_data_first = {}
    for i in range(len(user_data_first)):
        if user_data_first[i].split(':')[0] not in dict_user_data_first:
            dict_user_data_first[user_data_first[i].split(':')[0]] = {user_data_first[i].split(':')[1]}
        else:
            dict_user_data_first[user_data_first[i].split(':')[0]].add(user_data_first[i].split(':')[1])
    first_keys = dict_user_data_first.keys()
    for second_id in userid_category_num_per_second.keys():
        user_data_second = list(userid_category_num_per_second[second_id])
        dict_user_data_second = {}
        for t in range(len(user_data_second)):
            if user_data_second[t].split(':')[0] not in dict_user_data_second:
                dict_user_data_second[user_data_second[t].split(':')[0]] = {user_data_second[t].split(':')[1]}
            else:
                dict_user_data_second[user_data_second[t].split(':')[0]].add(user_data_second[t].split(':')[1])
        second_keys = dict_user_data_second.keys()
        set_keys = set(first_keys) & set(second_keys)
        all_keys = set(list(first_keys) + list(second_keys))
        sum = 0
        for k in all_keys:
            if k in set_keys:
                sum += pow(float(str(dict_user_data_first[k])[2:-2])-float(str(dict_user_data_second[k])[2:-2]), 2)
            elif k not in set_keys:
                if k in first_keys:
                    sum += pow(float(str(dict_user_data_first[k])[2:-2]), 2)
                elif k in second_keys:
                    sum += pow(float(str(dict_user_data_second[k])[2:-2]), 2)
        # 評価
        max_sum = -1
        if sum > max_sum:
            max_sum = sum
            max_id = second_id
            same_id = {second_id}
        elif sum == max_sum:
            same_id.add(second_id)
        if len(same_id) == 1:
            if first_id == max_id:
                match += 1
        elif first_id in same_id:
            match += 1 / len(same_id)

# 後半
for second_id in userid_category_num_per_second.keys():
    user_data_second = list(userid_category_num_per_second[second_id])
    dict_user_data_second = {}
    for first_id in userid_category_num_per_first.keys():
        user_data_first = list(userid_category_num_per_first[first_id])
        dict_user_data_first = {}
        for t in range(len(user_data_second)):
            if user_data_second[t].split(':')[0] not in dict_user_data_second:
                dict_user_data_second[user_data_second[t].split(':')[0]] = {user_data_second[t].split(':')[1]}
            else:
                dict_user_data_second[user_data_second[t].split(':')[0]].add(user_data_second[t].split(':')[1])
        second_keys = dict_user_data_second.keys()
        for i in range(len(user_data_first)):
            if user_data_first[i].split(':')[0] not in dict_user_data_first:
                dict_user_data_first[user_data_first[i].split(':')[0]] = {user_data_first[i].split(':')[1]}
            else:
                dict_user_data_first[user_data_first[i].split(':')[0]].add(user_data_first[i].split(':')[1])

        first_keys = dict_user_data_first.keys()
        set_keys = set(first_keys) & set(second_keys)
        all_keys = set(list(first_keys) + list(second_keys))
        sum = 0
        for k in all_keys:
            if k in set_keys:
                sum += pow(float(str(dict_user_data_first[k])[2:-2])-float(str(dict_user_data_second[k])[2:-2]), 2)
            elif k not in set_keys:
                if k in first_keys:
                    sum += pow(float(str(dict_user_data_first[k])[2:-2]), 2)
                elif k in second_keys:
                    sum += pow(float(str(dict_user_data_second[k])[2:-2]), 2)
        # 評価
        max_sum = -1
        if sum > max_sum:
            max_sum = sum
            max_id = first_id
            same_id = {first_id}
        elif sum == max_sum:
            same_id.add(first_id)
        if len(same_id) == 1:
            if second_id == max_id:
                match += 1
        elif second_id in same_id:
            match += 1 / len(same_id)
# 結果
print('Match rate: {}'.format(match / (2 * (len(userid_category_num_per_first.keys()) + len(userid_category_num_per_second.keys())))))
