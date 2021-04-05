# render_template：参照するテンプレートを指定
# jsonify：json出力
from flask import Flask, render_template, jsonify,request, make_response

# CORS：Ajax通信するためのライブラリ
from flask_cors import CORS
from random import *
import csv
import lda.get_new_lda as lda
import lda.load_lda as load_lda
import pandas as pd
import json 
from modules.Encoder import *
# CORS：Ajax通信するためのライブラリ
from flask_restful import Api, Resource


# static_folder：vueでビルドした静的ファイルのパスを指定
# template_folder：vueでビルドしたindex.htmlのパスを指定
app = Flask(__name__, static_folder = "./dist/static", template_folder="./dist")

app.config.from_object(__name__)
#日本語
app.config['JSON_AS_ASCII'] = False
#CORS=Ajaxで安全に通信するための規約
api = Api(app)

CORS(app)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# 任意のリクエストを受け取った時、index.htmlを参照
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch(path):
    return render_template("index.html")

# '/rand'が叩かれた時、乱数を生成
@app.route('/rand')
def random():
    response = {
        'randomNum': randint(1,100)
    }
    return jsonify(response)

#民経記の年号とトピックの割合対応を送る
@app.route('/data')
def get_data():
    topic_list = []
    with open('./data/new/new_minkeiki_topic_rate.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            topic_list.append(row)
    topics = []
    response = {}
    for i in range(len(topic_list[0])):
        t = [x[i] for x in topic_list]
        topics.append(t)
        this_topic = 'topic' + str(i+1)
        response.update({this_topic:t})
    return jsonify(response)

@app.route('/time')
def get_tme():
    json_open = open('./data/json/time_data.json', 'r')
    json_load = json.load(json_open)
    return jsonify(json_load)

@app.route('/niki')
def get_niki():
    json_open = open('./data/json/niki_data.json', 'r')
    json_load = json.load(json_open)
    json_open2 = open('./data/json/month_data.json', 'r')
    json_load2 = json.load(json_open2)
    return jsonify({'data':json_load,'month':json_load2})


#民経記のトピックごと単語リストを送る
@app.route('/name')
def get_name_data():
    topic_name_list = []
    person = pd.read_csv('./data/csv/minkeiki_person_list.csv')
    person_label = person['Label']
    chara = person_label[~person_label.duplicated()]
    chara = chara.reset_index(drop=True)
    with open('./data/new/new_minkeiki_lda_top.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            topic_name_list.append(row)
    # topic_name_lst = []
    # for i in range(10):
    #     topic_name.append([x[i] for x in topic_list])
    topic_name = []
    for i in range(len(topic_name_list)):
        n_topic_name = []
        for j in range(len(topic_name_list[0])):
            tmp = chara[int(topic_name_list[i][j])]
            if len(tmp.split('、')) > 1:
                name=tmp.split('、')[1] + tmp.split('、')[0]
            else:
                name=tmp
            n_topic_name.append({'id': j, 'name_id': topic_name_list[i][j], 'name': name, 'link': 'https://nakamura196.github.io/hi_person/test/person.html?u=https%3A%2F%2Fnakamura196.github.io%2Fhi_person%2Fentity%2Fchname%2F%E8%97%A4%E5%8E%9F%E7%B5%8C%E5%85%89.json'})
        topic_name.append({'topic': i,'data': n_topic_name})
    response = {'data': topic_name}

    return jsonify(response)

#新しくデータを作成
@app.route('/newdata/<num>')
def get_new_data(num=10):
    lda.main(int(num))
    response = {'data': 'make new data'}

    return jsonify(response)


#年号データと文書数（変化なし）
@app.route('/nengo')
def get_nengo():
    nengo_list = []
    with open('./data/csv/minkeiki_nengo.csv', encoding="shift-jis") as f:
        reader = csv.reader(f)
        for row in reader:
            nengo_list.append(row)
    response = {'nengo':nengo_list[0], 'num':nengo_list[1]}
    return jsonify(response)

#年号とトピックの割合
@app.route('/nengo3')
def get_nengo2():
    json_open = open('./data/json/nengo_data.json', 'r')
    json_load = json.load(json_open)
    return jsonify(json_load)

#10_doc_json(文書ごとのトピック割合)
@app.route('/doc')
def get_doc():
    json_open = open('./data/json/10_doc.json', 'r')
    json_load = json.load(json_open)
    return jsonify(json_load)

#lda_top(ldaの上位単語)
@app.route('/topword_old')
def get_top():
    json_open = open('./data/json/10_lda_top.json', 'r')
    json_load = json.load(json_open)
    return jsonify(json_load)

@app.route('/topname/<total_num>/<num>')
def get_top_name(total_num =10, num=10):
    json_open = open('./data/json/{}_lda_top.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    word_list = []
    basis = max(json_load['chara'][int(num)][0][1],json_load['words'][int(num)][0][1])
    for i in range(30):
        word_dict = {}
        word_dict['name'] = json_load['chara'][int(num)][i][0]
        word_dict['weight'] = json_load['chara'][int(num)][i][1]/basis*100
        word_list.append(word_dict)
    return jsonify({'data':word_list})

@app.route('/topword/<total_num>/<num>')
def get_top_words(total_num =10, num=10):
    json_open = open('./data/json/{}_lda_top.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    word_list = []
    basis = max(json_load['chara'][int(num)][0][1],json_load['words'][int(num)][0][1])
    for i in range(30):
        word_dict = {}
        word_dict['name'] = json_load['words'][int(num)][i][0]
        word_dict['weight'] = json_load['words'][int(num)][i][1]/basis*100
        word_list.append(word_dict)
    return jsonify({'data':word_list})

#10_per_nengo(年号ごとのトピック割合)
@app.route('/pernengo')
def get_per_nengo():
    json_open = open('./data/json/10_per_nengo.json', 'r')
    json_load = json.load(json_open)
    return jsonify(json_load)

#10_per_nengo(年号ごとのトピック割合_topic_num)
@app.route('/getpernengo/<total_num>/<num>')
def get_per_nengo_num(total_num = 10,num=10):
    json_open = open('./data/json/{}_per_nengo.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    rate_list = []
    for val in json_load.values():
        rate_list.append(val[int(num)])
    return jsonify({'data':rate_list})

#10_per_nengo(年号ごとのトピック割合_topic_num)
@app.route('/getpermonth/<total_num>/<num>')
def get_per_month_num(total_num = 10,num=10):
    json_open = open('./data/json/{}_per_month.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    rate_list = []
    for val in json_load.values():
        rate_list.append(val[int(num)])
    return jsonify({'data':rate_list})

#10_per_word(単語ごとのトピック割合)
@app.route('/perword')
def get_per_word():
    json_open = open('./data/json/10_per_word.json', 'r')
    json_load = json.load(json_open)
    return jsonify(json_load)

@app.route('/memo/<total_num>/<num>')
def get_memo(total_num=10,num=10):
    json_open = open('./data/json/memo/{}_memo.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    return jsonify({'data':json_load[str(num)]})

#新しくmemoを作成
@app.route('/makememo/<total_num>/<num>/<data>')
def make_memo(total_num=10,num=10,data=''):
    json_open = open('./data/json/memo/{}_memo.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    json_load[str(num)] = data
    response = {'data': 'make new data'}
    with open('./data/json/memo/{}_memo.json'.format(int(total_num)), 'w') as f:
        json.dump(json_load, f)  
    return jsonify(response)

@app.route('/topdoc/<total_num>/<num>')
def get_top_doc(total_num=10,num=10):
    json_open = open('./data/json/{}_doc.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    document_list = {}
    topic_num = int(num)
    for i in range(len(json_load)):
        document_list[i] = json_load[str(i)][0][topic_num][1]
    score_sorted = sorted(document_list.items(), key=lambda x:x[1], reverse=True)
    doc_data = open('./data/json/document_info.json', 'r')
    data_dict = json.load(doc_data)
    #上位15個
    #とりあえず軽量化のため、テキストと加増urlは保持しない
    document_list = []
    top_weight = score_sorted[0][1]
    for i in range(10):
        text_init = data_dict[str(score_sorted[i][0])]['text'][0:30].replace(" ", "").replace("\n", "").replace("\u3000","")
        tmp_dict = {'id':score_sorted[i][0], 'weight':score_sorted[i][1]/top_weight*100,'source':data_dict[str(score_sorted[i][0])]['source'],'text_init':text_init}
        document_list.append(tmp_dict)
    return jsonify({'data':document_list})

@app.route('/doc/<total_num>')
def get_per_doc(total_num=10,num=10):
    json_open = open('./data/json/{}_doc.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    doc_data = open('./data/json/document_info.json', 'r')
    data_dict = json.load(doc_data)
    document_list = []
    text_open = open('./data/json/color_text/{}_text.json'.format(int(total_num)), 'r')
    text_list = json.load(text_open)['data']
    for j in range(len(json_load)):
        document_data = json_load[str(j)]
        topic_rate = [x[1] for x in document_data[0]]
        topic_number = ['topic' + str(x[0]+1) for x in document_data[0]]
        text_init = text_list[j]
        tmp_dict = {'id':j, 'text':text_init, 'topic_rate':topic_rate, 'topic_number':topic_number, 'text_topic':document_data[1],'text_topic_rate':document_data[2],'source':data_dict[str(j)]['source'],'image':data_dict[str(j)]['image']}
        document_list.append(tmp_dict)
    return jsonify({'data':document_list})

@app.route('/text/<total_num>/<text_id>')
def get_per_text(total_num=10,text_id=0):
    json_open = open('./data/json/{}_doc.json'.format(int(total_num)), 'r')
    json_load = json.load(json_open)
    doc_data = open('./data/json/document_info.json', 'r')
    data_dict = json.load(doc_data)
    text_open = open('./data/json/color_text/{}_text.json'.format(int(total_num)), 'r')
    text_list = json.load(text_open)['data']
    document_data = json_load[str(text_id)]
    topic_rate = [x[1] for x in document_data[0]]
    topic_number = ['topic' + str(x+1) for x in range(int(total_num))]
    text_init = text_list[int(text_id)]
    text_dict = {'id':int(text_id), 'text':text_init, 'topic_rate':topic_rate, 'topic_number':topic_number, 'text_topic':document_data[1],'text_topic_rate':document_data[2],'source':data_dict[str(text_id)]['source'],'image':data_dict[str(text_id)]['image']}
    return jsonify(text_dict)

@app.route('/word/<total_num>/<word>')
def get_word_info(total_num=10,word=''):
    word_topic_info, related_chara, related_word = load_lda.word_info(int(total_num),word)
    topic_number = ['topic' + str(x+1) for x in range(int(total_num))]
    topic_rate=[0]*int(total_num)
    for p in word_topic_info:
        topic_rate[p[0]] = p[1]
    response = {'info':word_topic_info,'chara':related_chara,'word':related_word,'topic_number':topic_number,'topic_rate':topic_rate}
    return jsonify(response)

@app.route('/getid/<num>')
def get_id_text(num=0):
    json_open = open('./data/json/change_dic.json', 'r')
    json_load = json.load(json_open)
    return jsonify({'id':json_load[num]})

@app.route('/getid_m/<num>')
def get_id_text2(num=0):
    json_open = open('./data/json/change_dic_mon.json', 'r')
    json_load = json.load(json_open)
    return jsonify({'id':json_load[num]})

#年号データと文書数（変化なし）
@app.route('/month')
def get_mon():
    json_open = open('./data/json/month.json', 'r')
    json_load = json.load(json_open)
    month_list = []
    for j in json_load:
        month_list.append(json_load[j])
    response = {'month':month_list}
    return jsonify(response)


#example
@app.route('/classification', methods=['POST'])
def uploadImage():
    if request.method == 'POST':
        # base64_png =  request.form['image']
        # code = base64.b64decode(base64_png.split(',')[1]) 
        # image_decoded = Image.open(BytesIO(code))
        # image_decoded.save(Path(app.config['UPLOAD_FOLDER']) / 'image.png')
        if 'file' not in request.files:
            return 'ファイル未指定'

        # fileの取得（FileStorage型で取れる）
        # https://tedboy.github.io/flask/generated/generated/werkzeug.FileStorage.html
        fs = request.files['file']

        # 下記のような情報がFileStorageからは取れる
        app.logger.info('file_name={}'.format(fs.filename))
        app.logger.info('content_type={} content_length={}, mimetype={}, mimetype_params={}'.format(
            fs.content_type, fs.content_length, fs.mimetype, fs.mimetype_params))

        # ファイルを保存
        fs.save('./data/new/{}'.format(fs.filename))

        # return "フィアルアップロード成功"
        # return request.get_data()
        return make_response(jsonify({'result': fs.filename}))
    else: 
        return make_response(jsonify({'result': 'invalid method'}), 400)


    

# app.run(host, port)：hostとportを指定してflaskサーバを起動
if __name__ == '__main__':
    # get_new_data(9)
    # get_name_data()
    # get_nengo()
    app.run(debug=False,host='0.0.0.0', port=5000)