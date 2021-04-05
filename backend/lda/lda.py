
import bs4
import csv
import gensim
import numpy as np
import csv
import pandas as pd
from tqdm import tqdm
import sys
import json
import numpy
sys.path.append('../public')
from constants  import *
#後でいらないモジュール削除


#MLDAはMinkeiki_LDAの略
class MLDA:
    def __init__(self, num_topics, random_state):
        self.num_topics = num_topics
        self.iterations = ITERATIONS
        self.passes = PASSES
        self.random_state = 0 #後で変えられるようにする
        self.corpus = corpus
        self.dictionary= dictionary
        self.text_list = text_list
        self.chara_list= chara_list
        self.time_list = time_list
        self.make_csv=False
        self.make_json=True

    #lda実行
    def run_LDA(self):
        print("run lda")
        lda = gensim.models.ldamodel.LdaModel(
            corpus=self.corpus,
            num_topics=self.num_topics,
            id2word=self.dictionary,
            iterations=self.iterations,
            passes=self.passes,
            random_state=self.random_state,
            per_word_topics=True #文書何の単語のトピックを抽出するか
        )
        lda.save('../data/model/{}_lda'.format(self.num_topics))
        return lda
    
    def get_result(self):
        #run lda
        lda = self.run_LDA()
        #wordとrateのリストを返す
        top_chara_list = []
        top_words_list = []
        for k in range(self.num_topics):
            tmp_list = []
            tmp2_list=[]
            x = lda.show_topic(k,1000)
            for i in range(1000):
                if x[i][0] in self.chara_list:
                    tmp_list.append(x[i])
                else:
                    tmp2_list.append(x[i])
            top_chara_list.append(tmp_list)
            top_words_list.append(tmp2_list)
        lda_document = lda.get_document_topics(bow=self.corpus, minimum_probability=0, minimum_phi_value=None, per_word_topics=True)

        if self.make_csv:
            #人物と単語の上位30単語出力(select=0)
            self.make_top_data(0,top_chara_list,top_words_list)
            #人物と単語の上位30数値(select=1)
            self.make_top_data(1,top_chara_list,top_words_list)
            #文書ごとのトピックの割合
            self.per_document_topic(lda_document)
            #年号ごとのトピックの割合
            self.per_nengo_topic(lda_document)
            #めんどくさいのでここからはcsvでやらない
            # #単語ごとのトピックの割合
            # self.per_word_topic()
            # #トピックごとの文書の割合
            # self.per_topic_term()
            # #文書ごとの単語整形

        if self.make_json:
            # 人物と単語の上位30単語出力
            self.make_top_data_json(top_chara_list,top_words_list)
            #lda_document保存
            self.make_document_json(lda_document)
            #単語ごとのトピック割合
            self.per_word_topic_json(lda)
            #年号ごとのトピックの割合
            self.per_document_topic_json(lda_document)


    "for make csv function"
    def make_top_data(self,select,top_chara_list,top_words_list):
        topic = []
        for j in range(30):
            tmp_list = []
            for i in range(self.num_topics):
                tmp_list.append(top_chara_list[i][j][select])
                tmp_list.append(top_words_list[i][j][select])
            topic.append(tmp_list)
        #csvの保存方法を整えておく
        if select == 0:
            with open('../data/csv/0120/{}_topics_word.csv'.format(self.num_topics), 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(topic)
        if select == 1:
            with open('../data/csv/0120/{}_topics_word_rate.csv'.format(self.num_topics), 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(topic)

    def per_document_topic(self,lda_document):
        document_list = []
        for d in range(len(self.text_list)):
            document_list.append([lda_document[d][0][i][1] for i in range(self.num_topics)])
        with open('../data/csv/0120/{}_document_topic.csv'.format(self.num_topics), 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(document_list)

    def per_nengo_topic(self,lda_document):
        nengo_list = []
        for time in self.time_list:
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
        for i in range(len(self.time_list)):
            try:
                nengo_str = str(self.time_list[i]).split('年')[0] + '年'
                number_of_nengo_list[true_nengo_list.index(nengo_str)] += 1
            except:
                print(self.time_list[i])
        all_topic_rate = []
        for k in range(len(true_nengo_list)):
            num = 0
            topic_rate=[0]*self.num_topics 
            for i in range(len(self.time_list)):
                if true_nengo_list[k] in self.time_list[i]:
                    if not lda_document[i][0][0][1] == lda_document[i][0][1][1] :
                        num += 1
                        for j in range(self.num_topics):
                            topic_rate[j] += lda_document[i][0][j][1]
            if not num ==0:
                all_topic_rate.append([w/num for w in topic_rate])
            else:
                all_topic_rate.append([w for w in topic_rate])
        with open('../data/csv/0120/{}_nengo_topic.csv'.format(self.num_topics), 'w', newline="",encoding='shift_jis') as f:
            writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
            writer.writerows(all_topic_rate) 

    "for make json function"
    def make_top_data_json(self,top_chara_list,top_words_list):
        data_dict = {"chara":top_chara_list,"words":top_words_list}
        with open('../data/json/{}_lda_top.json'.format(self.num_topics), 'w') as f:
            json.dump(data_dict, f,cls = MyEncoder)
    
    def make_document_json(self,lda_document):
        doc_dict = {}
        for i in range(len(lda_document)):
            doc_dict[i] = lda_document[i]
        with open('../data/json/{}_doc.json'.format(self.num_topics), 'w') as f:
            json.dump(doc_dict, f,cls = MyEncoder)

    def per_word_topic_json(self,lda):
        word_dict = {}
        for i in range(len(dictionary)):
            word_dict[dictionary[i]] = lda.get_document_topics(dictionary.doc2bow([dictionary[i]]))
        with open('../data/json/{}_per_word.json'.format(self.num_topics), 'w') as f:
            json.dump(word_dict, f,cls = MyEncoder)

    def per_document_topic_json(self,lda_document):
        nengo_list = []
        for time in self.time_list:
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
        for i in range(len(self.time_list)):
            try:
                nengo_str = str(self.time_list[i]).split('年')[0] + '年'
                number_of_nengo_list[true_nengo_list.index(nengo_str)] += 1
            except:
                print(self.time_list[i])
        all_topic_rate = {}
        for k in range(len(true_nengo_list)):
            num = 0
            topic_rate=[0]*self.num_topics 
            for i in range(len(self.time_list)):
                if true_nengo_list[k] in self.time_list[i]:
                    if not lda_document[i][0][0][1] == lda_document[i][0][1][1] :
                        num += 1
                        for j in range(self.num_topics):
                            topic_rate[j] += lda_document[i][0][j][1]
            if not num ==0:
                all_topic_rate[true_nengo_list[k]] = [w/num for w in topic_rate]
            else:
                all_topic_rate[true_nengo_list[k]] = [w for w in topic_rate]

        with open('../data/json/{}_per_nengo.json'.format(self.num_topics), 'w') as f:
            json.dump(all_topic_rate, f, indent=1,cls = MyEncoder)

        with open('../data/json/nengo_data.json', 'w') as f:
            nengo_data = {"年号":true_nengo_list, "文書数":number_of_nengo_list}
            json.dump(nengo_data, f,cls = MyEncoder)   



if __name__ == '__main__':
    for i in range(2,21):
        print(i)
        mlda = MLDA(i,0)
        mlda.run_LDA()
        # mlda.get_result()