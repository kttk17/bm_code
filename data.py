import sys
import argparse
# from urllib.parse import urlparse
import re
import datetime
import os

parser = argparse.ArgumentParser()
parser.add_argument('inputfile1', type=str)
args = parser.parse_args()

f = open(args.inputfile1, mode='r')
line2 = f.readlines()

# for line in line2:
#     line = line.strip()
#     type = line.split(',', 4)[2]
#     if type == 'auto_bookmark':
#         user = line.split(',', 4)[0]
#         time = line.split(',', 4)[1]
#         time = datetime.datetime.fromtimestamp(int(time[0:10]))
#         url = line.split(',', 4)[3]
#         with open(args.inputfile1.split('.')[0] + '_re.txt', 'a')as reb:
#             print(user + ',' + str(time) + ',' + url, file=reb)
#             # print(user + ',' + url, file=reb)
for line in line2:
    line = line.strip()
    user = line.split(',', 3)[0]
    time = line.split(',', 3)[1]
    url = line.split(',', 3)[2]
    with open('url.txt', mode='w') as wurl:
        print(url, file=wurl)
    os.system('./csux_req.sh')
    with open('url.txt', mode='r') as rurl:
        category = rurl.read()
    with open(args.inputfile1.split('.')[0] + '_ca.txt', 'a')as reb:
        print(user + ',' + str(time) + ',' + url + ',' + category, file=reb)
