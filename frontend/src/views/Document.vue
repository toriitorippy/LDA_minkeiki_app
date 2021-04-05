<template>

  <div class="topic" v-loading="loading"  element-loading-text="Loading... 10秒ほどお待ちください"> 
			<b-row>
            <b-col cols="2">
                <!-- <el-radio-group v-model="isCollapse" style="margin-bottom: 20px;">
                    <br>
                    <el-radio-button :label="false" >expand</el-radio-button>
                    <el-radio-button :label="true">collapse</el-radio-button>
                    </el-radio-group> -->
                    <!-- <el-button v-on:click="show = !show">
                      切り替え
                    </el-button> -->
                    <!-- <el-menu v-if="show" default-active="1"  class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
                      <el-submenu index="1" >
                          <template slot="title">
                          <i class="el-icon-location"></i>
                          <span slot="title">Minkeiki</span>
                          </template>
                          <el-menu-item-group>
                          <el-menu-item :index="getIndex(n)" v-for="n of number_of_document" :key="n" @click="ClickEvent(n)">{{time_data[n]}}</el-menu-item>
                          </el-menu-item-group>
                      </el-submenu>
                    </el-menu> -->
                    <el-menu v-if="!show" :default-active="activeIndex"  class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse">
                      <el-submenu :index="getIndex(a)" v-for="a of 10" :key="a">
                          <template slot="title">
                          <i class="el-icon-location"></i>
                          <span slot="title">第{{a}}冊目</span>
                          </template>
                          <el-submenu :index="getIndex(b)" v-for="(b) of month_list[a]" :key="getIndex(b)">
                            <template slot="title">
                            <span slot="title">{{b}}</span>
                            </template>
                              <el-menu-item-group>
                                <el-menu-item :index="getIndex(c)" v-for="c of niki_data[a][b]" :key="getIndex(c)" @click="ClickEvent(c)">{{time_data[c]}}</el-menu-item>
                              </el-menu-item-group>   
                          </el-submenu>
                      </el-submenu>
                    </el-menu>
                </b-col>
                <b-col cols = "10">
                        <br>
                         <h3 style="color:red">注：著作権のため公開版は機能が制限されています。
                         <br>一部を除きテキスト及びテキストの画像は閲覧することができません。</h3>
                        <h1>{{topic_data['source']}}</h1>
                        <br>
                        <el-card class="box-card">
                          <p v-html="topic_data_origin['text']"></p>
                        </el-card>
                        <br>
                        <b-row>
                            <b-col cols="5">
                            <h3>Topicの割合</h3>
                            <DocumentTopicGraph v-bind:topic_data="topic_data" :total_num="num_topics"/>
                            </b-col>
                            <b-col cols ="5">
                              <el-image
                              :src="topic_data_origin['image']"></el-image>
                            </b-col>
                        </b-row>
                </b-col>
			</b-row>
  </div>
</template>

<style>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    overflow-y: scroll;
    max-height: 1000px;
  }


</style>

<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'
import DocumentTopicGraph from '../components/Document_topic_graph.vue';

export default {
  name: 'home',
  components: {
    DocumentTopicGraph,
  },
  props: ['num_topics','text_id'],
  mounted () {
    this.getData()
  },
  data() {
    return {
      activeIndex: '0',
      show: false,
      month_list: {'1':['嘉禄２年４月','嘉禄２年５月','嘉禄２年６月','嘉禄２年７月']},
       url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      activeName: 1,
      number_of_document:1,
      isCollapse: false,
      niki_data: {'1':{'嘉禄２年４月':[1,2,3],'嘉禄２年５月':[4,5,6],'嘉禄２年６月':[7,8]}, '2':{'嘉禄２年7月':[9,11,12],'嘉禄２年５月':[13],'嘉禄２年６月':[14]}},
      time_data: ['嘉禄２年４月１日'],
      topic_data: {'id': 0,'image': "https://clioimg.hi.u-tokyo.ac.jp/viewer/api/image/idata%2F850%2F8500%2F06%2F1601%2F0001.jpg",
            'text': '<ab xml:id="t00043083">      （題簽）「『□』      <name ref="#藤原経光" type="person"><font color="#ff0029" title="藤原経光"><font color="#ff0029" title="藤原経光">       経光      </font></font></name>      卿記〈自      <seg><font color="#ff0029">嘉禄</font></seg>      二年四月一      <seg><font color="#ff0029">日至</font></seg>      九月卅日      <seg><font color="#ff0029">首尾</font></seg>      完〉〈      <seg><font color="#ff0029">自筆</font></seg>      本〉壱巻  『      <seg><font color="#ff0029">綴合</font></seg>      このまま』」      <seg><font color="#ff0029">嘉禄</font></seg>      二〈自四月至九月〉  経ー（光）御記全      <seg><font color="#ff0029">嘉禄</font></seg>      二年  九月十七日      <seg><font color="#ff0029">御参</font></seg><seg><font color="#ff0029">住吉</font></seg>      社詩歌〈件詩歌留有之、〉御奉納之事、被用松枝文臺事、  一見      <seg><font color="#00d2d5">取目</font></seg>      録、又所用事令影写了、  延宝五年九月二日前諌議      <rs ref="#藤原貞光" role="#大夫"><font color="#ff0029" title="藤原貞光">       大夫（広橋貞光      </font></rs>      ）      <stamp>       花押      </stamp>      （端裏）「第一      <seg><font color="#ff0029">嘉禄</font></seg>      二年四月愚記〈七月聴      <seg><font color="#00d2d5">昇殿</font></seg>      、自四月至九月、尤可秘、      <stamp>       花押      </stamp>      （藤原      <name ref="#藤原経光" type="person"><font color="#ff0029" title="藤原経光"><font color="#ff0029" title="藤原経光">       経光      </font></font></name>      ）〉」     </ab>',
            'topic_rate': [0.21544824540615082,
              0.0076963393948972225,
              0.007696245796978474,
              0.007699206937104464,
              0.09019748866558075,
              0.6404713988304138,
              0.007696337997913361,
              0.0076973289251327515,
              0.007700970396399498,
              0.007696411572396755],
            'topic_number': ['topic1',
              'topic2',
              'topic3',
              'topic4',
              'topic5',
              'topic6',
              'topic7',
              'topic8',
              'topic9',
              'topic10'],
            'text_topic': [[0, [0]],
              [1, [4]],
              [2, [0]],
              [3, [0]],
              [4, [0]],
              [5, [4]],
              [6, [0]],
              [7, [0]],
              [8, [0, 4]],
              [9, [0]],
              [10, [0]]],
            'text_topic_rate': [[0, [[0, 0.9999029040336609]]],
              [1, [[4, 0.9996411800384521]]],
              [2, [[0, 3.9998128414154053]]],
              [3, [[0, 0.9999729990959167]]],
              [4, [[0, 0.9999850392341614]]],
              [5, [[4, 0.999494731426239]]],
              [6, [[0, 0.9999637007713318]]],
              [7, [[0, 0.9999789595603943]]],
              [8, [[0, 1.9462515115737915], [4, 0.0537404902279377]]],
              [9, [[0, 0.9943040013313293]]],
              [10, [[0, 0.999851405620575]]]],
            'source': '嘉禄２年４月１日'},
      topic_data_origin: {'id': 0,'image': "https://clioimg.hi.u-tokyo.ac.jp/viewer/api/image/idata%2F850%2F8500%2F06%2F1601%2F0001.jpg",
            'text': '<ab xml:id="t00043083">      （題簽）「『□』      <name ref="#藤原経光" type="person"><font color="#ff0029" title="藤原経光"><font color="#ff0029" title="藤原経光">       経光      </font></font></name>      卿記〈自      <seg><font color="#ff0029">嘉禄</font></seg>      二年四月一      <seg><font color="#ff0029">日至</font></seg>      九月卅日      <seg><font color="#ff0029">首尾</font></seg>      完〉〈      <seg><font color="#ff0029">自筆</font></seg>      本〉壱巻  『      <seg><font color="#ff0029">綴合</font></seg>      このまま』」      <seg><font color="#ff0029">嘉禄</font></seg>      二〈自四月至九月〉  経ー（光）御記全      <seg><font color="#ff0029">嘉禄</font></seg>      二年  九月十七日      <seg><font color="#ff0029">御参</font></seg><seg><font color="#ff0029">住吉</font></seg>      社詩歌〈件詩歌留有之、〉御奉納之事、被用松枝文臺事、  一見      <seg><font color="#00d2d5">取目</font></seg>      録、又所用事令影写了、  延宝五年九月二日前諌議      <rs ref="#藤原貞光" role="#大夫"><font color="#ff0029" title="藤原貞光">       大夫（広橋貞光      </font></rs>      ）      <stamp>       花押      </stamp>      （端裏）「第一      <seg><font color="#ff0029">嘉禄</font></seg>      二年四月愚記〈七月聴      <seg><font color="#00d2d5">昇殿</font></seg>      、自四月至九月、尤可秘、      <stamp>       花押      </stamp>      （藤原      <name ref="#藤原経光" type="person"><font color="#ff0029" title="藤原経光"><font color="#ff0029" title="藤原経光">       経光      </font></font></name>      ）〉」     </ab>',
            'topic_rate': [0.21544824540615082,
              0.0076963393948972225,
              0.007696245796978474,
              0.007699206937104464,
              0.09019748866558075,
              0.6404713988304138,
              0.007696337997913361,
              0.0076973289251327515,
              0.007700970396399498,
              0.007696411572396755],
            'topic_number': ['topic1',
              'topic2',
              'topic3',
              'topic4',
              'topic5',
              'topic6',
              'topic7',
              'topic8',
              'topic9',
              'topic10'],
            'text_topic': [[0, [0]],
              [1, [4]],
              [2, [0]],
              [3, [0]],
              [4, [0]],
              [5, [4]],
              [6, [0]],
              [7, [0]],
              [8, [0, 4]],
              [9, [0]],
              [10, [0]]],
            'text_topic_rate': [[0, [[0, 0.9999029040336609]]],
              [1, [[4, 0.9996411800384521]]],
              [2, [[0, 3.9998128414154053]]],
              [3, [[0, 0.9999729990959167]]],
              [4, [[0, 0.9999850392341614]]],
              [5, [[4, 0.999494731426239]]],
              [6, [[0, 0.9999637007713318]]],
              [7, [[0, 0.9999789595603943]]],
              [8, [[0, 1.9462515115737915], [4, 0.0537404902279377]]],
              [9, [[0, 0.9943040013313293]]],
              [10, [[0, 0.999851405620575]]]],
            'source': '嘉禄２年４月１日'},
      count: 0,
      loading: true,
    };
  },
  methods: {
  handleClick(tab, event) {
    console.log(tab, event);
  },
 handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      },
  ClickEvent(n){
    this.text_id = n
    const path = BACKEND_URL + '/text/' + this.num_topics +'/' +this.text_id
    axios.get(path)
      .then(response => {
        this.topic_data = response.data
        console.log(this.topic_data)
        })
        .catch(error => {
        console.log(error)
        })
        
    
  },
  getData () {
    this.loading = true
    //年号一覧とid対応表取得
    const path = BACKEND_URL + '/time'
    axios.get(path)
      .then(response => {
      this.number_of_document= response.data['length'];
      this.time_data = response.data['fake_time_list'];
      })
      .catch(error => {
      console.log(error)
      })

    const path_niki = BACKEND_URL +'/niki'
    axios.get(path_niki)
      .then(response => {
      this.niki_data = response.data['data'];
      this.month_list = response.data['month']
      console.log(this.month_list)
      })
      .catch(error => {
      console.log(error)
      })

    this.activeIndex = String(this.text_id)
    const path2 = BACKEND_URL + '/text/' + this.num_topics +'/' + this.text_id
    axios.get(path2)
        .then(response => {
        this.topic_data = response.data
        console.log(this.topic_data)
        this.loading = false
        })
        .catch(error => {
        console.log(error)
        this.loading = false
        })
    },
  //       created () {
  //       this.getData()
  // },
  getIndex(n) {
      return String(n)
    }

}
}
</script>