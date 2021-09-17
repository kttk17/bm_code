import sys
import argparse
from urllib.parse import urlparse
import re
import datetime
from datetime import datetime as dt
import locale
import jpholiday

# コマンドライン引数についての設定
parser = argparse.ArgumentParser()
parser.add_argument('inputfile1', type=str,
                    help='inputfile1')
args = parser.parse_args()

# 集合間の類似度を求める関数

def jaccard(set_a, set_b):
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union

# 平日か土日祝か判定(平日:1 土日祝:0)
def isBizDay(DATE):
    Date = datetime.date(int(DATE[0:4]), int(DATE[4:6]), int(DATE[6:8]))
    if Date.weekday() >= 5 or jpholiday.is_holiday(Date):
        return 0
    else:
        return 1

with open(args.inputfile1, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.rstrip()
        if line == '':
            continue
        user, date, url = line.split(',', 3)
        dt = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
        with open(user + '_timestamp.txt', mode='a') as time:
            print(date + ',' + url, file=time)
