import sys
import time
import argparse
from urllib.parse import urlparse

# コマンドライン引数についての設定

parser = argparse.ArgumentParser()
parser.add_argument('userurl_first', type=str,
                    help='inputfile1 (first half period): each record includes userid and url (bookmarked)')
parser.add_argument('userurl_second', type=str,
                    help='inputfile2 (second half period): same to inputfile1 but period is different')
parser.add_argument('-m', '--method', type=str, required=True,
                    help='select method to calculate the similarity between sets (jaccard, dice, simpson, intersection)')
args = parser.parse_args()

# 集合間の類似度を求める関数


def jaccard(set_a, set_b):
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union


def dice(set_a, set_b):
    intersection = len(set_a & set_b)
    return 2*intersection / (len(set_a) + len(set_b))


def simpson(set_a, set_b):
    intersection = len(set_a & set_b)
    return intersection / min(len(set_a), len(set_b))

# 共通要素の数を数える関数（上３つと同様に集合間の類似度合を測る）

def count_intersection(set_a, set_b):
    return len(set_a & set_b)

# 前半期間のファイルを読み込んでユーザをkey、そのユーザがアクセスしたURLの集合をvalueとする辞書の作成

users_first = set()
urls_first = set()
user_urls_first = {}

with open(args.userurl_first, mode='r') as inputfile1:
    for line in inputfile1:
        line = line.rstrip()
        if line == '':
            continue
        user, date, url = line.split(',', 3)
        url = urlparse(url.rstrip()).netloc
        users_first.add(user.rstrip())
        urls_first.add(url.rstrip())
        if user not in user_urls_first:
            user_urls_first[user.rstrip()] = {url.rstrip()}
        else:
            user_urls_first[user.rstrip()].add(url.rstrip())

# 後半期間のファイルを読み込んでユーザをkey、そのユーザがアクセスしたURLの集合をvalueとする辞書の作成

users_second = set()
urls_second = set()
user_urls_second = {}

with open(args.userurl_second, mode='r') as inputfile2:
    for line in inputfile2:
        line = line.rstrip()
        if line == '':
            continue
        user, date, url = line.split(',', 3)
        url = urlparse(url.rstrip()).netloc
        users_second.add(user.rstrip())
        urls_second.add(url.rstrip())
        if user not in user_urls_second:
            user_urls_second[user.rstrip()] = {url.rstrip()}
        else:
            user_urls_second[user.rstrip()].add(url.rstrip())

# 共通ユーザ取得

users = users_first & users_second

# 異なる期間で最も類似度が高くなるユーザが自分自身かどうかの判定

sim_method = {'jaccard': jaccard, 'dice': dice,
              'simpson': simpson, 'intersection': count_intersection}

match = 0

for user in users:
    # 後半期間のデータ内で最も類似度の高いユーザが自分かどうかを調べる
    max_similarity = -1
    urls = user_urls_first[user]
    for _user, _urls in user_urls_second.items():
        similarity = sim_method[args.method](urls, _urls)
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
    urls = user_urls_second[user]
    for _user, _urls in user_urls_first.items():
        similarity = sim_method[args.method](urls, _urls)
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

# ユーザの一致率を出力
print('Match rate: {}'.format(match / (2 * len(users))))
