import os
import re
import glob

#mobiledata.txtからのデータ抽出(userid、date,uerl)
def dataset(filename):
    f = open(filename , mode='r')
    line = f.readlines()
    a = 0
    b = 0
    userid = []
    userid_list1 = []
    userid_list2 = []
    date = []
    url = []

    for line2 in line:
        if a % 3 == 0:
            userid_list1.append(line2.strip())
            userid_list2.append(userid_list1[b].strip('"'))
            b = b + 1
        elif a % 3 == 1:
            date.append(line2.strip())
        elif a % 3 == 2:
            url.append(line2.strip())

        a = a + 1

    #useridにおいて同じ要素を削除したリスト作成
    for i in range(len(list(set(userid_list2)))):
        userid.append(list(set(userid_list2))[i])

    #print(len(userid_list2))
    #print(len(date))
    #print(len(url))

    #useridごとにdateとurlを振り分け
    for i in range(len(userid)):
        for j in range(len(userid_list2)):
            if userid[i] == userid_list2[j]:
                with open(userid[i] +'_06.txt', 'a') as data:
                    print(date[j] + '\n' + url[j] + '\n', file=data)

#urlのカテゴリー分類
def category(t):
    f= open(filename_list1[t], 'r')
    line = f.readlines()
    user_url = []
    c = 0

    #06.txtからurlのみ抽出
    for line2 in line:
        if line2 != '\"\"\n' and c % 3 == 1:
            user_url.append(line2.strip())
        c = c + 1

    #userごとにurlデータをsample.txtに出力
    for i in range(len(user_url)):
        with open('sample.txt', 'a') as ca:
            print('https://' + user_url[i].strip('"'), file=ca)

    #csux_req.shでカテゴリー分類
    os.system('./fileread.sh')

    #カテゴリーの出現頻度計算
    f = open('sample1.txt', 'r')
    line3 = f.readlines()

    category_list1 = []

    for line4 in line3:
        if line4 != '\n':
            category_list1.append(re.sub("\\D", "", line4.split()[0]))

    category_list2 = list(set(category_list1))

    for i in range(len(category_list2)):
        with open(filename_list1[t].split('_')[0]+'_cnum.txt', 'a') as cn:
            print(category_list2[i], ':', category_list1.count(category_list2[i]), file=cn)

    os.remove('/home/ec2-user/m202006/sample.txt')
    os.remove('/home/ec2-user/m202006/sample1.txt')


def cal(v):
    #カテゴリーの偏り(男性)
    c_percentage = {"201" : "0.70",
                    "401" : "0.69",
                    "602" : "0.65",
                    "1304" : "0.80",
                    "1306" : "0.70",
                    "1401" : "0.58",
                    "1402" : "0.40",
                    "1403" : "0.41",
                    "1404" : "0.41",
                    "1405" : "0.53",
                    "1406" : "0.55",
                    "1409" : "0.40",
                    "1411" : "0.30",
                    "1412" : "0.77",
                    "1414" : "0.80",
                    "1502" : "0.58",
                    "1503" : "0.70",
                    "1505" : "0.48",
                    "1509" : "0.40",
                    "1510" : "0.30",
                    "1517" : "0.30",
                    "1602" : "0.10",
                    "1603" : "0.30",
                    "1605" : "0.20",
                    "1801" : "0.57",
                    "1802" : "0.57",
                    "1803" : "0.57",
                    "1804" : "0.57",
                    "1805" : "0.57",
                    "2204" : "0.10",
                    "2205" : "0.60"}

    f = open(filename_list3[v], 'r')
    line = f.readlines()

    per_man = 0
    per_woman = 0

    for line2 in line:
        for key in c_percentage:
            if line2 == key:
                per_man = per_man + (c_percentage[key] * (c_percentage[key] - 0.5))
                per_woman = per_woman + ((1.0 - c_percentage[key]) * (0.5 - c_percentage[key]))



if __name__ == '__main__':
    #dataset('mobiledata.txt')

    filename_list1 = []
    filename_list1 = [os.path.basename(f1) for f1 in glob.glob('/home/ec2-user/m202006/*_06.txt', recursive=True) if os.path.isfile(f1)]
    length1 = len(filename_list1)

    for t in range(length1):
        category(t)

    #filename_list2 = []
    #filename_list2 = [os.path.basename(f2) for f2 in glob.glob('/home/ec2-user/m202006/*_06category.txt', recursive=True) if os.path.isfile(f)]
    #length2 = len(filename_list2)

    #for u in range(length):
        #c_num(u)
        
