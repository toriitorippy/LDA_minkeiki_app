import gensim
import pandas as pd
# import numpy as np
# from collections import Counter
# from sklearn import datasets
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
# import spacy
# from spacy import displacy
import csv
# import xml.etree.ElementTree as ET 
from lxml import etree


def main(num_topics):
    data_path = './data' #localかdocker上かで変える
    #data_path = '../data'
    tree = etree.parse(data_path + '/xml/minkeiki.xml')
    root = tree.getroot()
    time_list = []
    word_list = []
    states = root[1][0][0].xpath('.//div')
    if len(states):
        for state in states:
            time_list.append(state.attrib['source'])
            text = ''
            for child in state:
                text += child.text
            word_list.append(text)

    person = pd.read_csv(data_path + '/csv/minkeiki_person_list.csv')
    person_label = person['Label']
    chara = person_label[~person_label.duplicated()]
    chara = chara.reset_index(drop=True)
    #名前だけ抽出し、bowを作る
    bow = []
    for i in range(len(chara)):
        bow.append(chara[i].split('、')[0])
    #bowにあるwordだけのtextを作成
    texts = [
        [w for w in bow if w in doc]
            for doc in word_list
    ]
    #明、幸だけ修正する
    bow.index('明')
    #明、幸だけ修正する
    bow[2403] = '源幸'
    bow[1681] = '源明'
    #bowにあるwordだけのtextを作成
    texts = [
        [w for w in bow if w in doc]
            for doc in word_list
    ]
    # count = Counter(w for doc in texts for w in doc)
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
 
    lda = gensim.models.ldamodel.LdaModel(
        corpus=corpus,
        num_topics=num_topics,
        id2word=dictionary
    )
    # plt.figure(figsize=(30,30))
    # FONT_FILE = "C:\Windows\Fonts\MSGOTHIC.TTC"
    # for t in range(lda.num_topics):
    #     plt.subplot(5,4,t+1)
    #     x = dict(lda.show_topic(t,200))
    #     im = WordCloud(font_path=FONT_FILE,collocations=False, regexp=r"[\w']+").generate_from_frequencies(x)
    #     plt.imshow(im)
    #     plt.axis("off")
    #     plt.title("Topic #" + str(t))
    # x = lda.show_topic(0,10)
    all_chara = []
    for num in range(num_topics ):
        topic_chara = []
        topic = lda.show_topic(num,10)
        for t in topic:
            tmp = chara[bow.index(t[0])]
            topic_chara.append(str(bow.index(t[0])))
            # if len(tmp.split('、')) > 1:
            #     topic_chara.append(tmp.split('、')[1] + tmp.split('、')[0])
            # else:
            #     topic_chara.append(tmp)
        all_chara.append(topic_chara)
    print(all_chara)
    with open(data_path + "/new/new_minkeiki_lda_top.csv", "w") as f:
        writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
        writer.writerows(all_chara)
    all_topics = lda.get_document_topics(corpus, minimum_probability=0) 
    nengo_list = []
    for time in time_list:
        if '年' in time:
            nengo = str(time).split('年')[0] + '年'
            if nengo not in nengo_list:
                nengo_list.append(nengo)
    nengo_list.remove('年')
    kamakura_time_list = ['建久','嘉禄','安貞','寛喜','貞永','天福','文暦','嘉禎','暦仁','延応','仁治','寛元','宝治','建長','康元','正嘉','正元','文応','弘長','文永','建治','弘安','正応','永仁','正安','乾元','嘉元','徳治','延慶','応長','正和','文保','元応','元亨','正中','嘉暦','元徳','元弘','正慶','延元','貞和','延文','康応','応永','大永','天文','文明']
    nengo_true_list = [[]]*len(kamakura_time_list)
    nengo_index =[0]*len(nengo_list)
    for i in range(len(nengo_list)):
        gou = nengo_list[i][0] + nengo_list[i][1]
        gou_index = kamakura_time_list.index(gou)
        nengo_index[i] = gou_index
    true_nengo_list = []
    for i in range(46):
        tmp_nengo_list = []
        for j in range(len(nengo_index)):
            if nengo_index[j] ==i:
                tmp_nengo_list.append(nengo_list[j])
        newlist = sorted(tmp_nengo_list)
        true_nengo_list += newlist
    number_of_nengo_list = [0]*len(true_nengo_list)
    for i in range(len(time_list)):
        try:
            nengo_str = str(time_list[i]).split('年')[0] + '年'
            number_of_nengo_list[true_nengo_list.index(nengo_str)] += 1
        except:
            print(time_list[i])
    all_topic_rate = []
    for k in range(len(true_nengo_list)):
        num = 0
        topic_rate=[0]*num_topics 
        for i in range(len(time_list)):
            if true_nengo_list[k] in time_list[i]:
                if not all_topics[i][0][1] == all_topics[i][1][1] :
                    num += 1
                    for j in range(num_topics):
                        topic_rate[j] += all_topics[i][j][1]
        if not num ==0:
            all_topic_rate.append([w/num for w in topic_rate])
        else:
            all_topic_rate.append([w for w in topic_rate])
    with open(data_path + "/new/new_minkeiki_topic_rate.csv", "w",  encoding='shift_jis') as f:
        writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
        writer.writerows(all_topic_rate) 
    
if __name__ == "__main__":
    main(10)

