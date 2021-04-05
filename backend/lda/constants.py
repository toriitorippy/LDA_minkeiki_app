from my_modules import *

"minkeiki_xml_file"
MINKEIKI_XML = "../data/xml/minkeiki_fin4.xml"

"person_list"
PERSON_LIST = '../data/csv/minkeiki_person_list.csv'

"defalut parametor"
ITERATIONS = 400
PASSES = 50

"text_list/dictionary/corpus"
text_list,time_list,dictionary,corpus = make_text(MINKEIKI_XML)

"chara_list"
chara_list = make_chara(PERSON_LIST)