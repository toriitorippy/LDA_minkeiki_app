import bs4
import csv
import gensim
import numpy as np
import csv
import pandas as pd
from tqdm import tqdm
import json



"Import XML file"
def make_text(file):
    #text_list=文書のリスト
    #corpus:コーパス
    #dictionary:単語とid
    soup = bs4.BeautifulSoup(open(file,encoding='utf-8'), 'xml')
    abs = soup.find("text").find_all("ab")
    text_list = []
    for n_abs in abs:
        text = []
        select_words = n_abs.find_all(["name","seg","rs"])
        for s in select_words:
            if "seg" in str(s):
                tx = s.text.replace(" ", "").replace("\n", "")
                text.append(tx)
            else:
                role = s["ref"]
                if "none" not in role:
                    #noneの場合何もしない
                    tx = role.replace("#","")
                    text.append(tx)
        text_list.append(text)

    dictionary = gensim.corpora.Dictionary(text_list)
    corpus = [dictionary.doc2bow(text) for text in text_list]

    #make time list
    time_list = []
    time_abs = soup.find('text').find_all('head')
    for t_abs in time_abs:
        time_list.append(t_abs.text.replace(" ", "").replace("\n", ""))

    return text_list, time_list, dictionary, corpus


"make chara list"
def make_chara(file):
    #chara_list:登場人物のリスト
    person = pd.read_csv(file)
    person_label = person['Label']
    chara = person_label[~person_label.duplicated()]
    chara = chara.reset_index(drop=True)
    chara_list = []
    for i in range(len(chara)):
        chara_list.append(chara[i].split('、')[0])
        if "、" in chara[i]:
            chara_list.append(chara[i].split('、')[1]+chara[i].split('、')[0])
    return chara_list

#copy from https://wtnvenga.hatenablog.com/entry/2018/05/27/113848
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)