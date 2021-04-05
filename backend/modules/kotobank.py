import sys
import bs4
import hashlib
import json
import bs4
import requests
import time
import os
import urllib.parse
import csv
import pandas as pd

# URL = "https://kotobank.jp/word/"
URL = "https://kobun.weblio.jp/content/"
def exist(url):
    res = requests.get(url)
    if res.status_code != requests.codes.ok:
        return None
    else:
        return True

def main():
    exist_word_list = []
    url_list = []
    with open('../data/csv/word.csv', 'r', encoding='utf8') as f:
        reader = csv.reader(f)
        l = list(reader)[0]

    kanis = []
    checks = []
    map = {}

    with open('../data/csv/kani.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # ヘッダーを読み飛ばしたい時
        for row in reader:
            label = row[1]
            if label == "":
                continue
            if label in checks:
                continue
            count = len(label)
            if count not in map:
                map[count] = []
            map[count].append({
                "id" : label,
                "label" : label,
                "values" : [label]
            })
            checks.append(label)
    print(checks)
    print(len(checks))
    for w in l:
        url = URL+w
        if exist(url):
            if not w in checks:
                if not w in exist_word_list:
                    print(w)
                    exist_word_list.append(w)
                    url_list.append(url)
        else:
            if len(w) > 2:
                for t in [w[0:2],w[1:3]]:
                    url = URL+t
                    if exist(url):
                        if not t in checks:
                            print(t)
                            if not t in exist_word_list:
                                exist_word_list.append(t)
                                url_list.append(url)
    pands_koto = pd.DataFrame({ 'word' : exist_word_list,
                        'url' : url_list})
    # pands_koto.to_csv("../data/csv/kotobank.csv")
    pands_koto.to_csv("../data/csv/webil.csv")



    
if __name__ == "__main__":
    main()