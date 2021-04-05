from nltk import ngrams
import gensim
import numpy as np
from collections import Counter
from sklearn import datasets
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from spacy import displacy
import csv
import pandas as pd
import re

def collect_ngram_words(docs, n):
    u'''文書集合 docs から n-gram のコードブックを生成。
    docs は1文書を1要素とするリストで保存しているものとする。
    句読点等の処理は無し。
    '''
    codebook = []
    ngram_dict = {}
    for doc in docs:
        this_words = ngrams(doc, n)
        for word in this_words:
            if word not in ngram_dict:
                ngram_dict[word] = 0
            ngram_dict[word] += 1
            if word not in codebook:
                codebook.append(word)
    return ngram_dict

def ngram_count(text):
    #単語ないで一番頻度が高い単語を抽出
    leng = len(text)
    max_count = 10
    ini_index =0
    bow_list =[]
    for i in range(leng-3):
        n_count = all_word_list.count(text[i:i+3])
        if n_count >= 50:
            bow_list.append(text[i:i+3])
    return bow_list

def remove_unrelated(word_list):
    new_text_list = []
    for words in word_list:
        s1 = words.replace("〈", "")
        s2 = s1.replace("〉", "")
        new_text_list.append(s2)
    return new_text_list

def fix_xml(word_list):
    words_list = []
    for words in word_list:
        l = re.split('[、\u3000」・「  ]',words)
        tmp = [i for i in l if not len(i) == 0]
        while '  'in tmp:
            tmp.remove('  ')
        words_list.append(tmp)
        #その前に()がある場所で要素を分割したい
    new_words_lists = []
    for words in words_list:
        new_words_list = []
        for w in words:
            if '（' in w:
                s = re.findall(".*?）",w)
                for s_w in s:
                    new_words_list.append(s_w)
            else:
                new_words_list.append(w)
        new_words_lists.append(new_words_list)
    return new_words_lists

#名前だけのものをすべて苗字まで含め()で囲う
def revise_wordlist(text_list):
    chara = chara_list['name']
    for i,c in enumerate(chara):
        for j,text in enumerate(text_list):
            for k,t in enumerate(text):
                if c in t:
                    if not pattern1[i] is None:
                        if pattern1[i] in t:
                            text_list[j][k] = t.replace(pattern1[i], '（' + full_name[i]+'）')
                        elif not full_name[i] in t:
                            if not '（' in t:
                                text_list[j][k] = t.replace(c, '（' + full_name[i]+'）')
    return text_list


from lxml import etree
n = 3
tree = etree.parse('../data/xml/minkeiki.xml')
root = tree.getroot()

states = root[1][0][0].xpath('.//div')
time_list = []
word_list = []
rend_list = []
if len(states):
    for state in states:
        time_list.append(state.attrib['source'])
        rend_list.append(state.attrib['rend'])
        text = ''
        for child in state:
            text += child.text
        word_list.append(text)
person = pd.read_csv('../data/csv/minkeiki_person_list.csv')
person_label = person['Label']
person_list = person_label[~person_label.duplicated()].reset_index()['Label']
full_chara = []
name = []
simei = []
for p in person_list:
        tmp = p
        if len(tmp.split('、')) > 1:
            name.append(tmp.split('、')[0])
            simei.append(tmp.split('、')[1])
            full_chara.append(tmp.split('、')[1] + tmp.split('、')[0])
        else:
            full_chara.append(tmp)
            name.append(tmp)
            simei.append(None)
#経光（藤原）パターン
pattern1 = []
for p in person_list:
    tmp = p
    if len(tmp.split('、')) > 1:
        pattern1.append(tmp.split('、')[0] +'（'+ tmp.split('、')[1] + '）')
    else:
        pattern1.append(None)   
chara_list = pd.DataFrame({ 'chara' : person_list,
                        'full_name' : full_chara, 
                        'name' : name, 
                        'simei' : simei, 
                          'pattern1':pattern1})
chara = chara_list['name']
pattern1 = chara_list['pattern1']
full_name = chara_list['full_name']

text_list = fix_xml(remove_unrelated(word_list))
test_text_list = revise_wordlist(text_list)
text_new = []
for t_t in test_text_list:
    tmp_text_new = []
    for words in t_t:
        l = re.split('[『』）（》《]',words)
        tmp = [i for i in l if not len(i) == 0]
        while '  'in tmp:
            tmp.remove('  ')
        for tmp_t in tmp:
            tmp_text_new.append(tmp_t)
    text_new.append(tmp_text_new)

all_word_list = ''
for word in word_list:
    all_word_list += word


word_bow = []
for texts in text_new:
    for ts in texts:
        if not ts in full_name.tolist():
            if len(ts)==2 or len(ts) == 3:
                if not ts in word_bow:
                    word_bow.append(ts)
            else:
                tmp_word_bow = ngram_count(ts)
                for tmp in tmp_word_bow:
                    if not tmp in word_bow:
                        word_bow.append(tmp)

print(word_bow)
with open("../data/csv/word.csv", "w",  encoding='utf-8') as f:
    writer = csv.writer(f) # writerオブジェクトの作成 改行記号で行を区切る
    writer.writerow(word_bow) 