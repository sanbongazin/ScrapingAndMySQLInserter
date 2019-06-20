from urllib.parse import urlparse
import mysql.connector
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
import time

time_flag = True

url = urlparse('mysql://(username):(password)@(IPAdress):(PortNumber)/')

conn = mysql.connector.connect(
    host = url.hostname or '(IPAdress)',
    port = url.port or (portnumber),
    user = url.username or '(username)',
    password = url.password or '',
    database = url.path[1:],
)



print(conn.is_connected())
conn.ping(reconnect=True)
cur = conn.cursor()

# アクセスするURL
http = urllib3.PoolManager()
r = http.request('GET', 'https://www.nikkei.com/markets/worldidx/chart/nk225/?type=day')
soup = BeautifulSoup(r.data, 'html.parser')

# span要素全てを摘出する→全てのspan要素が配列に入ってかえされます→[<span class="m-wficon triDown"></span>, <span class="l-h...
span = soup.find_all("span")

# print時のエラーとならないように最初に宣言しておきます。
nikkei_heikin = ""
nikkei_heikin_defference = ""

# while True:
#     if datetime.now().minute != 59:
#         # 59分ではないので、１分待機。
#         time.sleep(58)
#         continue
# for分で全てのspan要素の中からClass="mkc-stock_prices"となっている物を探します
for tag in span:
    # classの設定がされていない要素は、tag.get("class").pop(0)を行うことのできないでエラーとなるため、tryでエラーを回避する
    try:
        # tagの中からclass="n"のnの文字列を摘出します。複数classが設定されている場合があるので
        # get関数では配列で帰ってくる。そのため配列の関数pop(0)により、配列の一番最初を摘出する
        # <span class="hoge" class="foo">  →   ["hoge","foo"]  →   hoge
        string_ = tag.get("class").pop(0)

        # 摘出したclassの文字列にmkc-stock_pricesと設定されているかを調べます
        if string_ in "economic_value_now a-fs26":
            # mkc-stock_pricesが設定されているのでtagで囲まれた文字列を.stringであぶり出します
            nikkei_heikin = tag.string

            # 摘出が完了したのでfor分を抜けます
            continue
            
        if string_ in "economic_balance_value a-fs18":
            nikkei_heikin_defference=tag.string.translate(str.maketrans({'＋':'+','ー':'-'}))
            break
    except:
        # パス→何も処理を行わない
        pass

# 摘出した日経平均株価を出力します。
print (nikkei_heikin)
print(nikkei_heikin_defference)

