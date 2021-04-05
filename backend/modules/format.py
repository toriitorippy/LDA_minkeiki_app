import sys
import bs4
import hashlib
import json
import csv
#https://github.com/nakamura196/hi_kokiroku/blob/master/10_project/02_minkeki/02_torii/01_format.py

key = "a"

data = {
    "a" : {
        "inputpath" : "../data/xml/minkeiki_fin3.xml",
        "outputpath" : "../data/xml/minkeiki_fin4.xml"
    },
    "b" : {
        "inputpath" : "../data/xml/minkeiki_fin3.xml",
        "outputpath" : "../data/xml/fin2_minkeiki4.xml"
    }
}


inputpath = data[key]["inputpath"]
outputpath = data[key]["outputpath"]

soup = bs4.BeautifulSoup(open(inputpath,encoding='utf-8'), 'xml')

# 人物情報の整形

persNames = soup.find("body").findAll("persName")

for persName in persNames:

    if persName.get("role"):
        rs = soup.new_tag("rs")
        rs["ref"] = persName.get("corresp")
        rs["role"] = persName.get("role")
        rs.string = persName.text

        persName.replace_with(rs)

    else:
        el = soup.new_tag("name")
        el["type"] = "person"
        el["ref"] = persName.get("corresp")
        el.string = persName.text

        persName.replace_with(el)

# div構造の修正

divs = soup.find("body").findAll("div")

for div in divs:
    if div.get("source"):
        date = div.get("source")
        del div["source"]

        el = soup.new_tag("head")

        el.string = date
        div.insert(1, el)

# pb修正

segs = soup.find("body").findAll("persWord")

for seg in segs:
    el = soup.new_tag("seg")
    el.string = seg.text

    seg.replace_with(el)
    
listWord = soup.find("listWord")
if listWord:
    listWord.decompose()

# pb修正

pbs = soup.find("body").findAll("pb")

duplicates = []

for pb in pbs:
    facs = pb.get("facs")

    if facs not in duplicates:
        duplicates.append(facs)
    else:
        pb.decompose()

# listPerson
import glob
files = glob.glob("/Users/nakamurasatoru/git/d_hi/dd/knowledge/docs/api/entity/chname/*.json")

for file in files:
    fd = open(file, mode='r')
    data = json.load(fd)[0]
    fd.close()
    

    if "http://schema.org/description" in data:
        arr = []
        for obj in data["http://schema.org/description"]:
            arr.append(obj["@value"])
            break # 一件のみ

        el = soup.new_tag("note")
        el.string = ", ".join(arr)

        id = file.split("/")[-1].split(".json")[0]

        person = soup.find("person", {"xml:id" : id})
        person.append(el)


        

# # 出力
# f = open(outputpath, "w")
# f.write(soup.prettify("utf-8")) #.prettify())
# f.close()

html = soup.prettify("utf-8")
with open(outputpath, "wb") as file:
    file.write(html)
