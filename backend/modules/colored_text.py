import bs4
import csv
import gensim
import numpy as np
import json

soup = bs4.BeautifulSoup(open('../data/xml/minkeiki_fin4.xml',encoding='utf-8'), 'xml')
abs = soup.find("text").find_all("ab")

color_list = [
    'ff0029', '377eb8', '66a61e', '984ea3', '00d2d5', 'ff7f00', 'af8d00',
    '7f80cd', 'b3e900', 'c42e60', 'a65628', 'f781bf', '8dd3c7', 'bebada',
    'fb8072', '80b1d3', 'fdb462', 'fccde5', 'bc80bd', 'ffed6f', 'c4eaff',
    'cf8c00', '1b9e77', 'd95f02', 'e7298a', 'e6ab02', 'a6761d', '0097ff',
    '00d067', '000000', '252525', '525252', '737373', '969696', 'bdbdbd',
    'f43600', '4ba93b', '5779bb', '927acc', '97ee3f', 'bf3947', '9f5b00',
    'f48758', '8caed6', 'f2b94f', 'eff26e', 'e43872', 'd9b100', '9d7a00',
    '698cff', 'd9d9d9', '00d27e', 'd06800', '009f82', 'c49200', 'cbe8ff',
    'fecddf', 'c27eb6', '8cd2ce', 'c4b8d9', 'f883b0', 'a49100', 'f48800',
    '27d0df', 'a04a9b'
  ]



dic_open = open('../data/json/dictionary.json', 'r')
dic_dict = json.load(dic_open)

#json ファイル読み込み

for topic_num in range(1,20):
    json_open = open('../data/json/{}_doc.json'.format(int(topic_num)), 'r')
    json_load = json.load(json_open)
    text_list =[]
    for n in range(len(abs)):
        n_abs = abs[n]
        text = str(n_abs)
        select_words = n_abs.find_all(["name","seg","rs"])
        document_data = json_load[str(n)]
        word_list = [dic_dict[str(i[0])] for i in document_data[1]]
        for s in select_words:
            if "seg" in str(s):
                tx = s.text.replace(" ", "").replace("\n", "")
                if tx in word_list:
                    if len(document_data[1][word_list.index(tx)][1]) >0:
                        topic_color = color_list[document_data[1][word_list.index(tx)][1][0]] 
                        after_word = '<font color="#' + topic_color + '">'+ tx+'</font>'
                        text = text.replace(s.text,after_word)
            else:
                role = s["ref"]
                if "none" not in role:
                    #noneの場合何もしない
                    tx = role.replace("#","")
                    if tx in word_list:
                        if len(document_data[1][word_list.index(tx)][1]) >0:
                            topic_color = color_list[document_data[1][word_list.index(tx)][1][0]] 
                            after_word = '<font color="#' + topic_color + '" '+ 'title="'+ tx + '">'+ s.text+'</font>'
                            text = text.replace(s.text,after_word)
        text_list.append(text.replace("\n", "").replace("fontcolor","font color").replace("\u3000",""))


    with open('../data/json/color_text/{}_text.json'.format(topic_num), 'w') as f:
            json.dump({'data':text_list},f)   