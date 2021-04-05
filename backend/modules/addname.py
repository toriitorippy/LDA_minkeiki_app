import sys
import bs4
import hashlib
import json

#名前だけを構造化したxml作成
#()などは外したもの
#https://github.com/nakamura196/hi_kokiroku/blob/master/test/111_addKani.py
# inputpath = "../data/test/E16 - 民経記.xml"
# outputpath = "../data/test/E16 - 民経記_kani.xml"
inputpath = "../data/xml/minkeiki.xml"
outputpath = "../data/nameadd_minkeiki.xml"

import csv

kanis = []
persons = []
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

test = {}

with open('../data/csv/minkeiki_person_list.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        label = row[2]

        if "、" not in label:
            continue

        if label == "":
            continue

        if label in checks:
            continue

        labelSpl = label.split("、")

        label2 = labelSpl[0] + "（" + labelSpl[1] + "）"

        label3 = labelSpl[1] + labelSpl[0] 
        label3 = label3.replace(" ", "").replace("?", "_")

        persons.append({
            "id" :  label3,
            "label" : label3,
            "values" : [label2],
            "values2" : [label3, labelSpl[0]]
        })

        if labelSpl[0] not in test:
            test[labelSpl[0]] = []

        if label3 not in test:
            test[label3] = [label3]

        if labelSpl[1] not in test[labelSpl[0]]:
            test[labelSpl[0]].append(labelSpl[1])

        checks.append(label)

print(test)
print(len(test))

count = 0
for key in test:
    if len(test[key]) > 1:
        # print(key, test[key])
        count += 1

print(count)

for key in sorted(map, reverse=True):
    arr = map[key]
    for obj in arr:
        kanis.append(obj)

soup = bs4.BeautifulSoup(open(inputpath,encoding='utf-8'), 'xml')

hashes = {}

sourceDesc = soup.find("sourceDesc")

# listPerson

listNym = soup.new_tag("listNym")


for kani in kanis:

    abs = []
    sames = []

    # path = "/Users/nakamurasatoru/git/d_hi/hi_pnr2/docs/term/kani/"+kani["id"]+".json"

    # json_open = open(path, 'r')
    # json_load = json.load(json_open)[0]

    # if "http://schema.org/description" in json_load:

    #     descs = json_load["http://schema.org/description"]

    #     for desc in descs:
    #         abs.append("<ab>"+desc["@value"]+"</ab>")

    # if "http://www.w3.org/2002/07/owl#sameAs" in json_load:

    #     urls = json_load["http://www.w3.org/2002/07/owl#sameAs"]

    #     for url in urls:
    #         sames.append(url["@id"])

    html = '''
        <nym type="官位" xml:id="'''+kani["id"]+'''" '''+("sameAs=\""+" ".join(sames)+"\"" if len(sames) > 0 else "")+'''>
        ''' +"".join(abs)+ ''' 
        </nym>
    '''
    n_kani = bs4.BeautifulSoup(html, 'xml')
    listNym.append(n_kani)

    for value in kani["values"]:
        e_value = value +kani["id"]
        id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
        hashes[id] = "<name type=\"kani\" nymRef=\"#"+kani["id"]+"\">"+value+"</name>"

sourceDesc.append(listNym)

listPerson = soup.new_tag("listPerson")

for person in persons:

    abs = []
    sames = []

    # path = "/Users/nakamurasatoru/git/d_hi/hi_pnr2/docs/entity/chname/"+person["id"]+".json"

    # json_open = open(path, 'r')
    # json_load = json.load(json_open)[0]

    # if "http://schema.org/description" in json_load:

    #     descs = json_load["http://schema.org/description"]

    #     for desc in descs:
    #         abs.append("<note>"+desc["@value"]+"</note>")

    # if "http://www.w3.org/2002/07/owl#sameAs" in json_load:

    #     urls = json_load["http://www.w3.org/2002/07/owl#sameAs"]

    #     for url in urls:
    #         sames.append(url["@id"])

    html = '''
        <person xml:id="'''+person["id"]+'''">
            # <persName '''+("ref=\""+" ".join(sames)+"\"" if len(sames) > 0 else "")+'''>'''+person["id"]+'''</persName>
            # ''' +"".join(abs)+ ''' 
        </person>
    '''
    n_person = bs4.BeautifulSoup(html, 'xml')
    listPerson.append(n_person)

    for value in person["values"]:
        e_value = value +person["id"]
        id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
        hashes[id] = "<persName corresp=\"#"+person["id"]+"\">"+value.split("（")[0]+"</persName>"

    # 単独
    for value in person["values2"]:
        e_value = value +person["id"]
        id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
        hashes[id] = "<persName corresp=\"#"+person["id"]+"\">"+value.split("（")[0]+"</persName>"

sourceDesc.append(listPerson)

def aaa(text):

    ab_str = str(text)
    
    for kani in kanis:
        values = kani["values"]
        for value in values:
            if value in ab_str:
                e_value = value + kani["id"]
                ab_str = ab_str.replace(value, hashlib.md5(e_value.encode('utf-8')).hexdigest())
    
    for person in persons:
        values = person["values"]
        for value in values:
            if value in ab_str:
                e_value = value + person["id"]
                ab_str = ab_str.replace(value, hashlib.md5(e_value.encode('utf-8')).hexdigest())
    
    # 単独
    for person in persons:
        values = person["values2"]
        for value in values:
            if value in test and len(test[value]) == 1:
                # 一文字の場合はスキップ
                if len(value) == 1:
                    continue

                if value in ab_str:
                    e_value = value + person["id"]
                    ab_str = ab_str.replace(value, hashlib.md5(e_value.encode('utf-8')).hexdigest())
        
    n_ab = bs4.BeautifulSoup(ab_str, 'xml')
    text.replace_with(n_ab)

    return text
    
abs = soup.find("text").find_all("ab")
for ab in abs:
    ab = aaa(ab)

segs = soup.find("text").find_all("seg")
for seg in segs:
    ab = aaa(seg)

# 全体置換

body = soup.find("body")

body_str = str(body)

body_str = body_str.replace("（花押）", "<stamp>花押</stamp>")

import re
m = re.findall("（(.+?)）", body_str)
for i in range(len(m)):
    e = m[len(m) - 1 -i]

    body_str = body_str.replace("（"+e+"）", "<seg type='chu'>"+e+"</seg>")



for id in hashes:
    body_str = body_str.replace(id, hashes[id])

n_body = bs4.BeautifulSoup(body_str, 'xml')
body.replace_with(n_body)

# 出力

html = soup.prettify("utf-8")
with open(outputpath, "wb") as file:
    file.write(html)
