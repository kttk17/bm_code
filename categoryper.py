import sys
import argparse
from urllib.parse import urlparse
import re
import locale
from collections import defaultdict
import collections

# コマンドライン引数についての設定
parser = argparse.ArgumentParser()
parser.add_argument('inputfile1', type=str,
                    help='inputfile1')
args = parser.parse_args()

# ファイル読み込み
user_category_first = defaultdict(list)
with open(args.inputfile1, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.rstrip()
        if line == '':
            continue
        user, date, url, category = line.split(',', 4)
        if category == '':
            continue
        user_category_first[user.rstrip()].append(category.rstrip())
user_category_percentage = {}
for id in user_category_first.keys():
    id_categorynum_percentage = {}
    rength = len(user_category_first[id])
    if rength > 10:
        c = collections.Counter(user_category_first[id])
        for category_num in c.keys():
            percentage = c[category_num] / len(user_category_first[id])
            if category_num not in id_categorynum_percentage:
                id_categorynum_percentage[category_num] = {percentage}
            else:
                id_categorynum_percentage[category_num].add(percentage)
        with open('userid_timestamp_bookmark_url_' + args.inputfile1.split('_')[4] + '_re_categoryper.txt', mode='a') as per:
            print(id, ',', id_categorynum_percentage, file=per)
