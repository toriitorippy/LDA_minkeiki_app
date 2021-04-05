import sys
import bs4
import hashlib
import json
import re
import csv

#https://github.com/nakamura196/hi_kokiroku/blob/master/test/111_addKani.py
# inputpath = "../data/test/E16 - 民経記.xml"
# outputpath = "../data/test/E16 - 民経記_kani.xml"
inputpath = "../data/xml/minkeiki.xml"
outputpath = "../data/xml/minkeiki_fin3.xml"


kanis = []
persons = []
checks = []
words = []

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
        if len(label) <2:
            #殿は除外したい
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
        if len(labelSpl[0]) < 2:
            print(labelSpl[0])
            continue

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

with open('../data/csv/minkeiki_person_list.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        label = row[2]

        if "、" not in label:
            if label in checks:
                continue
            if label == "":
                continue
            label2 = label
            label3 = label
            persons.append({
                "id" :  label3,
                "label" : label3,
                "values" : [label2],
                "values2" : [label3, label]
            })

            if label not in test:
                test[label] = []

            if label3 not in test:
                test[label3] = [label3]
            print(label)
        checks.append(label)
kotoba = {}

with open('../data/csv/new_kotobank.csv', 'r', encoding='utf8') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    for row in reader:
        label = row[2]

        if label == "":
            continue

        if label in checks:
            continue

        count = len(label)

        if count not in kotoba:
            kotoba[count] = []

        kotoba[count].append({
            "id" : label,
            "label" : label,
            "values" : [label]
        })

        checks.append(label)
print(kotoba)
print(len(kotoba))

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

for key in sorted(kotoba, reverse=True):
    arr = kotoba[key]
    for obj in arr:
        words.append(obj)

print(words)

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

    # for value in person["values"]:
    #     e_value = value +person["id"]
    #     id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
    #     hashes[id] = "<persName corresp=\"#"+person["id"]+"\">"+value.split("（")[0]+"</persName>"

    # # 単独
    # for value in person["values2"]:
    #     e_value = value +person["id"]
    #     id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
    #     hashes[id] = "<persName corresp=\"#"+person["id"]+"\">"+value.split("（")[0]+"</persName>"

sourceDesc.append(listPerson)

listWord = soup.new_tag("listWord")

for word in words:

    abs = []
    sames = []
    html = '''
        <persWord xml:id="'''+word["id"]+'''"/>
    '''
    n_word = bs4.BeautifulSoup(html, 'xml')
    listWord.append(n_word)

    # for value in person["values"]:
    #     e_value = value +person["id"]
    #     id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
    #     hashes[id] = "<persName corresp=\"#"+person["id"]+"\">"+value.split("（")[0]+"</persName>"

    # 単独
    for value in word["values"]:
        e_value = value
        id = hashlib.md5(e_value.encode('utf-8')).hexdigest()
        hashes[id] = "<persWord corresp=\"#"+word["id"]+"\">"+value+"</persWord>"

sourceDesc.append(listWord)

def fix_text(text):
    l = re.split('[、\u3000」・「  <>]',text)
    tmp = [i for i in l if not len(i) == 0]
    while '  'in tmp:
        tmp.remove('  ')

    #その前に()がある場所で要素を分割したい
    new_words_list = []
    for w in tmp:
        if '（' in w:
            s = re.findall(".*?）",w)
            for s_w in s:
                new_words_list.append(s_w)
        else:
            new_words_list.append(w)

    
    return new_words_list

def remove_unrelated_text(text):
    s1 = text.replace("〈", "")
    s2 = s1.replace("〉", "")
    return s2

def add_person(text):

    ab_str = str(text)
    
    text_list = fix_text(remove_unrelated_text(ab_str))
    #人物を見つける
    for t in text_list:
        for person in persons:
            fullname = person["values2"][0] #fullname
            forename = person["values2"][1] #forename
            for_full = person["values"][0]  #forename(surname)
            for name in [fullname,forename,for_full]:
                if name in t:
                    e_value = name
                    before_name = t.split(e_value)[0]
                    point = 0 #見つけたか
                    for kani in kanis:
                        for value in kani["values"]:
                            if value in before_name:
                                #間の言葉抽出
                                interval_word = before_name.split(value)[1]
                                if len(interval_word)<5:
                                    #interval_wordが長すぎたら怪しい
                                    full_value = value + interval_word + name
                                    id = hashlib.md5(full_value.encode('utf-8')).hexdigest()
                                    hashes[id] = "<persName corresp=\"#"+person["id"]+"\" role=\"#"+value+"\">"+full_value+"</persName>"
                                    ab_str = ab_str.replace(full_value, hashlib.md5(full_value.encode('utf-8')).hexdigest())
                                    point +=1
                                    #roleをストック
                                    role[value] = person["id"]
                    #役職が書いていない場合
                    if point ==0:
                        value = name
                        id = hashlib.md5(value.encode('utf-8')).hexdigest()
                        hashes[id] = "<persName corresp=\"#"+person["id"]+"\">"+value+"</persName>"
                        ab_str = ab_str.replace(value, hashlib.md5(value.encode('utf-8')).hexdigest())

        for kani in kanis:
            value = kani['values'][0]
            if value in t:
                point = 0
                if value in role:
                    #以前の役職を参照、置き換え
                    r_value = role[value]
                    id_value = r_value + value
                    id = hashlib.md5(id_value.encode('utf-8')).hexdigest()
                    hashes[id] = "<persName corresp=\"#"+r_value+"\" role=\"#"+value+"\">"+value+"</persName>"
                    ab_str = ab_str.replace(value, hashlib.md5(id_value.encode('utf-8')).hexdigest())
                    point += 1
                if point ==0:
                    id = hashlib.md5(value.encode('utf-8')).hexdigest()
                    hashes[id] = "<persName corresp=\"#"+'none'+"\" role=\"#"+value+"\">"+value+"</persName>"
                    ab_str = ab_str.replace(value, hashlib.md5(value.encode('utf-8')).hexdigest())  
        for word in words:
            value = word['values'][0]
            if value in t:
                ab_str = ab_str.replace(value, hashlib.md5(value.encode('utf-8')).hexdigest())  

    n_ab = bs4.BeautifulSoup(ab_str, 'xml')
    text.replace_with(n_ab)

    return text

    
abs = soup.find("text").find_all("ab")
i = 0
role = {}
for ab in abs:
    ab = add_person(ab)
    i += 1
    if i % 1000 == 0:
        print(i)
        print(role)

# segs = soup.find("text").find_all("seg")
# for seg in segs:
#     ab = aaa(seg)

# 全体置換

body = soup.find("body")

body_str = str(body)

body_str = body_str.replace("（花押）", "<stamp>花押</stamp>")

#()内を見つけるやつは後でやろう
# import re
# m = re.findall("（(.+?)）", body_str)
# for i in range(len(m)):
#     e = m[len(m) - 1 -i]

#     body_str = body_str.replace("（"+e+"）", "<seg type='chu'>"+e+"</seg>")



for id in hashes:
    body_str = body_str.replace(id, hashes[id])

n_body = bs4.BeautifulSoup(body_str, 'xml')
body.replace_with(n_body)

# 出力

html = soup.prettify("utf-8")
with open(outputpath, "wb") as file:
    file.write(html)
