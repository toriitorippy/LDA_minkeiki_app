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
import re

df = pd.read_csv('../data/csv/kotobank.csv')

drop_str = ['一','二','三','四','五','六','七','八','九','十','丑','寅','卯','辰','巳','午','申','酉','戌','亥']
re_hiragana = re.compile(r'^[あ-ん]+$')
# status_hira = re_hiragana.fullmatch(word)

re_katakana = re.compile(r'[\u30A1-\u30F4]+')
# status_kata = re_katakana.fullmatch(word)

# drop = df.index[re.compile(r'^[あ-ん]+$').fullmatch(df['word'])]
index = []
for i in range(len(df)):
    word = df['word'][i]
    if re_hiragana.fullmatch(word):
        index.append(i)
    if re_katakana.fullmatch(word):
        index.append(i)
df = df.drop(index)

for d in drop_str:
    #条件にマッチしたIndexを取得
    drop_index = df.index[df['word'].str.contains(d)]
    #条件にマッチしたIndexを削除
    df = df.drop(drop_index)
df = df.reset_index(drop=True)



df.to_csv("../data/csv/new_kotobank.csv")