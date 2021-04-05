import gensim
import numpy as np
import sys
import pandas as pd
PERSON_LIST = './data/csv/minkeiki_person_list.csv'

def cos_sim(v1,v2):
    return np.dot(v1,v2)/np.linalg.norm(v1)/np.linalg.norm(v2)

def euclid(v1,v2):
    return np.sqrt(np.power(np.array(v1)-np.array(v2), 2).sum())

def make_chara():
    #chara_list:登場人物のリスト
    person = pd.read_csv(PERSON_LIST)
    person_label = person['Label']
    chara = person_label[~person_label.duplicated()]
    chara = chara.reset_index(drop=True)
    chara_list = []
    for i in range(len(chara)):
        chara_list.append(chara[i].split('、')[0])
        if "、" in chara[i]:
            chara_list.append(chara[i].split('、')[1]+chara[i].split('、')[0])
    return chara_list

def word_info(total_num,word):
    lda = gensim.models.ldamodel.LdaModel.load('./data/model/{}_lda'.format(total_num))
    word_info = lda.get_term_topics(word, minimum_probability=0)
    word_list = []
    for wi in word_info:
        word_list.append((wi[0],float(wi[1])))
    #ユークリッド距離を計算
    lda_list = [0]*total_num
    for w in lda.get_term_topics(word, minimum_probability=0):
        lda_list[w[0]] = w[1]
    cos_list = []
    dictionary = gensim.corpora.Dictionary.load('./data/model/dictionary')
    for b in dictionary.values():
        if not b == word:
            try:
                w_vec = lda.get_term_topics(b, minimum_probability=0)
                b_list=[0]*total_num
                for w in w_vec:
                    b_list[w[0]] = w[1]
                if not b_list == [0]*total_num:
                    cos = euclid(lda_list,b_list)
                    cos_list.append([b,cos])
                
            except:
                w_vec = []
    sortsecond = lambda val: val[1]
    cos_list.sort(key=sortsecond) 
    w_list = []
    c_list = []
    kyoki = cos_list[0:300]
    chara_list = make_chara()
    for k in kyoki:
        if k[0] in chara_list:
            c_list.append(k)
        else:
            w_list.append(k)
    return word_list,c_list[0:30],w_list[0:30]
