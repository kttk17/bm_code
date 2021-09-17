#!/bin/bash

# 使用方法
usage=""
usage=${usage}"usage: $0"
usage=${usage}" [-h|--help]"
usage=${usage}" [--url request_url]"
usage=${usage}" [--version csux_if_version]"
usage=${usage}" [--policy csux_policy]"
usage=${usage}" [--access csux_access_key]"
usage=${usage}" [--host csux_hostname_or_ip]"
usage=${usage}" [--port csux_port]"
usage=${usage}" [--mode csux_mode<automatic or manual or category>]"

# オプションの指定と解析
GETOPT=$(getopt -o h --long help,url:,version:,policy:,access:,host:,port:,dummy-body-size:,mode: -- "$@")
eval set -- "$GETOPT"

# リクエストURL
request_url=$(<url.txt)

# リクエストポリシー
request_policy="y_kids:20120829-01"
#request_policy="PFU-EN:20120829-01"
# リクエストバージョン
request_ver="3.0-102"
# アクセスキー
request_acckey="iybtZoty7jdeZenTXcwpIid9wW9pMJNk"
# CSUX server name or server IP address
csux_host="yc-ux.netstar-inc.com"
# CSUX port number
csux_port="80"
# CSUX mode (automatic or manual or category)
#csux_mode="automatic"
csux_mode="manual"
#csux_mode="category"

while true
do
        case $1 in
        --url)          request_url=$2     ; shift 2
                ;;
        --version)      request_ver=$2     ; shift 2
                ;;
        --policy)       request_policy=$2  ; shift 2
                ;;
        --access)       request_acckey=$2  ; shift 2
                ;;
        --host)         csux_host=$2  ; shift 2
                ;;
        --port)         csux_port=$2  ; shift 2
                ;;
        --dummy-body-size)  dummy_body_size=$2  ; shift 2
                ;;
        --mode)         csux_mode=$2  ; shift 2
                ;;
        --)   shift ; break
                ;;
        -h|--help)   echo $usage ; exit 0
                ;;
        *)    echo $usage ; break
                ;;
        esac
done

# tcp接続
exec 5<>/dev/tcp/${csux_host}/${csux_port}

# body for Manual
manual_body=$(cat <<EOF
{
    "Version":"$request_ver",
    "Command":"Check",
    "Policy":["Manual","$request_policy"],
    "Count":1,
    "Urls":[
    {
        "Url":"$request_url",
        "Id":"1"
    }]
}
EOF
)

# body for Automatic
automatic_body=$(cat <<EOF
{
    "Version":"$request_ver",
    "Command":"Check",
    "Policy":["Manual","$request_policy"],
    "Count":1,
    "Urls":[
    {
        "Url":"$request_url",
        "Id":"1"
    }]
}
EOF
)

# body for Automatic
automatic_body=$(cat <<EOF
{
    "Version":"$request_ver",
    "Command":"Check",
    "Url":"$request_url",
    "Policy":["Automatic","$request_policy"],
    "Format":"String"
}
EOF
)

# body for GetCategory
category_body=$(cat <<EOF
{
    "Version":"$request_ver",
    "Command":"GetCategory",
    "CategoryVersion":"$request_policy"
}
EOF
)

# CSUX mode
if [ "${csux_mode}" == "automatic" ];
then
          body=${automatic_body}
  elif [ "${csux_mode}" == "manual" ];
  then
            body=${manual_body}
    elif [ "${csux_mode}" == "category" ];
    then
              body=${category_body}
fi

# ボディサイズ
content_length=${#body}
if [ "${dummy_body_size}" != "" ];
then
          content_length=${dummy_body_size}
fi

# リクエスト送信
cat >&5 <<EOF
POST / HTTP/1.1
User-Agent: CategoryServerUX_y_kids/${request_ver}
Host: ${csux_host}
Accept: application/json
Content-Type: application/json
NS-Access: ${request_acckey}
Content-Length: ${content_length}

${body}
EOF

# レスポンス表示
# cat <&5 | grep -Eo "\"Category\":\[\".[0-9]+\"\]"
# echo
categ=`cat <&5 | grep -Eo "\"Category\":\[\".[0-9]+\"\]"`
echo $categ | tr -dc '0-9'　> url.txt
