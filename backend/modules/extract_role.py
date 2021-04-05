#xmlから役職を抽出する
#現在は<lb/>を除いたxmlを使用
#role(full_name)のパターンのみ役職を表していると仮定
#require: minkeiki.xml,person_list
import re
from lxml import etree
import pandas as pd 

#文書の余計なものを取り除き、分割
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

def remove_unrelated(word_list):
    new_text_list = []
    for words in word_list:
        s1 = words.replace("〈", "")
        s2 = s1.replace("〉", "")
        new_text_list.append(s2)
    return new_text_list

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

tree = etree.parse('../data/xml/minkeiki.xml')
root = tree.getroot()

states = root[1][0][0].xpath('.//div')

#年号のリスト、文章のリスト、rendのリスト作成
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
topic_chara = []
for p in person_label:
        tmp = p
        if len(tmp.split('、')) > 1:
            topic_chara.append(tmp.split('、')[1] + tmp.split('、')[0])
        else:
            topic_chara.append(tmp)
person['full_Label'] =  topic_chara
person_list = person_label[~person_label.duplicated()].reset_index()['Label']

text_list = fix_xml(remove_unrelated(word_list))

#role(full_name)のパターンのみ役職を表していると仮定
o_role_list = {}
for old_text in text_list:
    for o in old_text:
        if '（' in o:
            #括弧の中抽出
            t_chara = re.findall("(?<=\（).+?(?=\）)", o)[0]
            if t_chara in person['full_Label'].tolist():
                yakusyoku = o.split('（')[0]
                if not len(yakusyoku) == 0:
                    if not yakusyoku in o_role_list:
                        o_role_list[yakusyoku] =1
                    else:
                        o_role_list[yakusyoku] +=1

dic2 = sorted(o_role_list.items(), key=lambda x:x[1], reverse=True)
all_word_list = ''
for word in word_list:
    all_word_list += word
new_dic = {}
new_role_list = []
for i in range(len(dic2)):
    count = all_word_list.count(dic2[i][0])
    #1文字以上
    if len(dic2[i][0])>1:
        tmp_word = dic2[i][0]
        if '》' in tmp_word:
            tmp_word = tmp_word.replace('》', '')
        if '《' in tmp_word:
            tmp_word = tmp_word.replace('《', '')
        if '【' in tmp_word:
            tmp_word = tmp_word.replace('【', '')
        #1個以下の表現は含めない
        if count > 1:
            new_dic[tmp_word] =count
            new_role_list.append(tmp_word)
        else:
            #2文字以上まで
            j = 0
            while len(tmp_word) - i >1:
                n_count = all_word_list.count(tmp_word[i:len(tmp_word)])
                if n_count > 1:
                    if tmp_word[j:tmp_word] in new_role_list:
                        new_dic[tmp_word[j:tmp_word]]= n_count
                        new_role_list.append(tmp_word[j:tmp_word])
                        break
dic3 = sorted(new_dic.items(), key=lambda x:x[1], reverse=True)
import csv
#一旦保存
with open("../data/csv/role.csv", "w",  encoding='utf-8') as f:
    writer = csv.writer(f) # writerオブジェクトの作成 改行記号で行を区切る
    writer.writerow(new_role_list) 