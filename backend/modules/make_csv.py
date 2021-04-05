import bs4
import csv
import gensim
import numpy as np
import csv
import pandas as pd
from tqdm import tqdm


num_topics = 11


soup = bs4.BeautifulSoup(open('../data/xml/minkeiki_fin4.xml',encoding='utf-8'), 'xml')
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

iterations = 400
passes = 50
lda = gensim.models.ldamodel.LdaModel(
    corpus=corpus,
    num_topics=num_topics,
    id2word=dictionary,
    iterations=iterations,
    passes=passes,
    random_state=0
)

person = pd.read_csv('../data/csv/minkeiki_person_list.csv')
person_label = person['Label']
chara = person_label[~person_label.duplicated()]
chara = chara.reset_index(drop=True)
bow = []
for i in range(len(chara)):
    bow.append(chara[i].split('、')[0])
    if "、" in chara[i]:
        bow.append(chara[i].split('、')[1]+chara[i].split('、')[0])


topics_list = []
words_list = []
for k in range(num_topics):
    tmp_list = []
    tmp2_list=[]
    x = lda.show_topic(k,1000)
    for i in range(1000):
        if x[i][0] in bow:
            tmp_list.append(x[i])
        else:
            tmp2_list.append(x[i])
    topics_list.append(tmp_list)
    words_list.append(tmp2_list)

# all_chara = []
# for num in range(num_topics):
#     topic_chara = []
#     for t in topics_list[num][0:30]:
#         tmp = chara[bow.index(t[0])]
#         if len(tmp.split('、')) > 1:
#             topic_chara.append({'name':tmp.split('、')[1] + tmp.split('、')[0],'point':t[1]})
#         else:
#             topic_chara.append({'name':tmp,'point':t[1]})
#     all_chara.append(topic_chara)

topic = []
for j in range(30):
    tmp_dic = {}
    for i in range(num_topics):
        tmp_dic['topic{}_person_name'.format(i)] = topics_list[i][j][0]
        tmp_dic['topic{}_word'.format(i)]=words_list[i][j][0]
    topic.append(tmp_dic)

header=[]
for i in range(num_topics):
    header.append('topic{}_person_name'.format(i))
    header.append('topic{}_word'.format(i))

#csvの保存方法を整えておく
with open('../data/csv/1219/{}_topics_LDA.csv'.format(num_topics), 'w', newline="") as f:
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    writer.writerows(topic)

topic2 = []
for j in range(30):
    tmp_dic2 = {}
    for i in range(num_topics):
        tmp_dic2['topic{}_person_name'.format(i)] = topics_list[i][j][1]
        tmp_dic2['topic{}_word'.format(i)]=words_list[i][j][1]
    topic2.append(tmp_dic2)

#csvの保存方法を整えておく
with open('../data/csv/1219/{}_topics_LDA_num.csv'.format(num_topics), 'w', newline="") as f:
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    writer.writerows(topic2)

coherence_model_lda = gensim.models.CoherenceModel(model=lda, texts=text_list, dictionary=dictionary, coherence='u_mass')
u_mass = coherence_model_lda.get_coherence()
perplexity = np.exp2(-lda.log_perplexity(corpus))

s = 'u_mass' + str(u_mass)
s2 = 'perplexity' + str(perplexity)

with open('../data/csv/1219/{}_topics_LDA_log.txt'.format(num_topics), mode='w') as f:
    f.write(s)
    f.write(s2)