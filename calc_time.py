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
parser.add_argument('inputfile2', type=str,
                    help='inputfile2')
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

# 前半期間

users_first = set()
date_first = set()
urls_first = set()
user_date_first = {}
user_urls_first = {}

with open(args.inputfile1, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.rstrip()
        if line == '':
            continue
        user, date, url = line.split(',', 3)
        dt = dt.strptime(date, '%Y-%m-%d %H:%M:%S')

        # #　曜日(月から日曜)
        # dweek = str(dt.strftime('%a'))
        # 曜日(平日 or 土日祝)
        date_str = date.replace('-', '')
        dweek = str(isBizDay(date_str))

        dtime = date.split()[1]
        dtime = dtime.split(':')[0]

        # # url_domain
        # url = urlparse(url.rstrip()).netloc

        # #url+時間
        # du = url.strip() + dtime.rstrip()
        # #url+曜日
        # du = url.strip() + dweek.rstrip()
        # #時間
        # du = dtime.rstrip()
        # #曜日
        # du = dweek.rstrip()
        # 時間グルーピング
        dtime = int(dtime)
        if 0 <= dtime <= 5 and 22 <= dtime < 24:
            du = url.strip() + 'time=0'
        elif 5 < dtime < 11:
            du = url.strip() + 'time=1'
        elif 11 <= dtime <= 14:
            du = url.strip() + 'time=2'
        elif 14 < dtime < 17:
            du = url.strip() + 'time=3'
        elif 17 <= dtime < 22:
            du = url.strip() + 'time=4'
        #url+時間+曜日
        du = du + dweek.rstrip()

        users_first.add(user.rstrip())
        date_first.add(date.rstrip())
        urls_first.add(url.rstrip())

        if user not in user_date_first:
            user_date_first[user.rstrip()] = {du.rstrip()}
        else:
            user_date_first[user.rstrip()].add(du.rstrip())

        # if user not in user_urls_first:
        #     user_urls_first[user.rstrip()] = {url.rstrip()}
        # else:
        #     user_urls_first[user.rstrip()].add(url.rstrip())

# 後半期間

users_second = set()
date_second = set()
urls_second = set()
user_date_second = {}
user_urls_second = {}

with open(args.inputfile2, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.rstrip()
        if line == '':
            continue
        user, date, url = line.split(',', 3)
        dt = dt.strptime(date, '%Y-%m-%d %H:%M:%S')

        # #　曜日(月から日曜)
        # dweek = str(dt.strftime('%a'))
        # 曜日(平日 or 土日祝)
        date_str = date.replace('-', '')
        dweek = str(isBizDay(date_str))

        dtime = date.split()[1]
        dtime = dtime.split(':')[0]

        # # url_domain
        # url = urlparse(url.rstrip()).netloc

        # #url+時間
        # du = url.strip() + dtime.rstrip()
        # #url+曜日
        # du = url.strip() + dweek.rstrip()
        # #時間
        # du = dtime.rstrip()
        # #曜日
        # du = dweek.rstrip()
        # 時間グルーピング
        dtime = int(dtime)
        if 0 <= dtime <= 5 and 22 <= dtime < 24:
            du = url.strip() + 'time=0'
        elif 5 < dtime < 11:
            du = url.strip() + 'time=1'
        elif 11 <= dtime <= 14:
            du = url.strip() + 'time=2'
        elif 14 < dtime < 17:
            du = url.strip() + 'time=3'
        elif 17 <= dtime < 22:
            du = url.strip() + 'time=4'
        #url+時間+曜日
        du = du + dweek.rstrip()

        users_second.add(user.rstrip())
        date_second.add(date.rstrip())
        urls_second.add(url.rstrip())

        if user not in user_date_second:
            user_date_second[user.rstrip()] = {du.rstrip()}
        else:
            user_date_second[user.rstrip()].add(du.rstrip())
        #
        # if user not in user_urls_second:
        #     user_urls_second[user.rstrip()] = {url.rstrip()}
        # else:
        #     user_urls_second[user.rstrip()].add(url.rstrip())
# 共通ユーザ取得

users = users_first & users_second

match = 0

# 異なる期間で最も類似度が高くなるユーザが自分自身かどうかの判定(date)
for user in users:
    # 後半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
    max_similarity = -1
    dates = user_date_first[user]
    for _user, _dates in user_date_second.items():
        similarity = jaccard(dates, _dates)
        if similarity > max_similarity:
            max_similarity = similarity
            max_user = _user
            same_sim_users = {_user}
        elif similarity == max_similarity:
            same_sim_users.add(_user)
    if len(same_sim_users) == 1:
        if user == max_user:
            match += 1
    elif user in same_sim_users:
        match += 1 / len(same_sim_users)
    # 前半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
    max_similarity = -1
    dates = user_date_second[user]
    for _user, _dates in user_date_first.items():
        similarity = jaccard(dates, _dates)
        if similarity > max_similarity:
            max_similarity = similarity
            max_user = _user
            same_sim_users = {_user}
        elif similarity == max_similarity:
            same_sim_users.add(_user)
    if len(same_sim_users) == 1:
        if user == max_user:
            match += 1
    elif user in same_sim_users:
        match += 1 / len(same_sim_users)

# # 異なる期間で最も類似度が高くなるユーザが自分自身かどうかの判定(urls)
# for user in users:
#     # 後半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
#     max_similarity = -1
#     urls = user_urls_first[user]
#     for _user, _urls in user_urls_second.items():
#         similarity = jaccard(urls, _urls)
#         if similarity > max_similarity:
#             max_similarity = similarity
#             max_user = _user
#             same_sim_users = {_user}
#         elif similarity == max_similarity:
#             same_sim_users.add(_user)
#     if len(same_sim_users) == 1:
#         if user == max_user:
#             match += 1
#     elif user in same_sim_users:
#         match += 1 / len(same_sim_users)
#     # 前半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
#     max_similarity = -1
#     urls = user_urls_second[user]
#     for _user, _urls in user_urls_first.items():
#         similarity = jaccard(urls, _urls)
#         if similarity > max_similarity:
#             max_similarity = similarity
#             max_user = _user
#             same_sim_users = {_user}
#         elif similarity == max_similarity:
#             same_sim_users.add(_user)
#     if len(same_sim_users) == 1:
#         if user == max_user:
#             match += 1
#     elif user in same_sim_users:
#         match += 1 / len(same_sim_users)

# ユーザの一致率を出力
print('Match rate: {}'.format(match / (2 * len(users))))
