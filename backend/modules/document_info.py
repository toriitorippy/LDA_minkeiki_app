import bs4
import csv
import gensim
import numpy as np
import json

#minkeiki.xmlの情報をまとめたjson作成

from lxml import etree

soup = bs4.BeautifulSoup(open('../data/xml/minkeiki_fin.xml',encoding='utf-8'), 'xml')

tree = etree.parse('../data/xml/minkeiki.xml')
root = tree.getroot()

states = root[1][0][0].xpath('.//div')

pb = root[1][0][0].xpath('.//pb')

zone_list = []
for pb_child in pb:
    zone_list.append(pb_child.attrib['facs'])
graphic = soup.find_all("graphic")
t_zone = soup.find_all('zone')

zone_dict = {}
for i in range(len(t_zone)):
    zone_dict['#' + t_zone[i]['xml:id']] = graphic[i]['url']

t_id = 0
data_dict = {}
if len(states):
    for j in range(len(states)):
        state = states[j]
        for child in state:
            this_dict = {'id':t_id,'source':state.attrib['source'],'child_id':child.attrib['{http://www.w3.org/XML/1998/namespace}id'], 'parent_id ':state.attrib['{http://www.w3.org/XML/1998/namespace}id'],'rend':state.attrib['rend'],'text':child.text, 'zone':zone_list[j], 'image':zone_dict[zone_list[j]]}
            data_dict[t_id] = this_dict
            t_id +=1
            
with open('../data/json/document_info.json', 'w') as f:
            json.dump(data_dict,f)   