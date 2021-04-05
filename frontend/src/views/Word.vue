<template>
  <div class="home">
    <br>
    <br>
    <b-container >
      <b-row>
        <b-col cols="3">
          <el-card class="box-card">
            <h2>Input</h2>
            <el-autocomplete
                class="inline-input"
                v-model="input"
                :fetch-suggestions="querySearch"
                placeholder="Enter a word"
                @select="handleSelect"
              ></el-autocomplete>
            <div style="margin: 20px 0;"></div>
            <el-button type="primary" icon="el-icon-search" @click="searchWord">get data</el-button>
            <div style="margin: 10px 0;"></div>
            <p>※人物名または語句を入力してください</p>
          </el-card>
        </b-col>
        <b-col cols="9">
          <h2>{{input}}</h2>
          {{info_text}}
        </b-col>
      </b-row>
      <div style="margin: 50px 0;"></div>
      <b-row>
        <b-col cols ='5'>
          <DocumentTopicGraph v-bind:topic_data="word_data" :total_num="num_topics"/>
        </b-col>
        <b-col cols='7'>
          <h3>関連単語</h3>
          <b-row>
            <b-col cols='6'>
            <p>人物名</p>
            <WordList v-bind:list_data="word_data['chara']" @update="getData"/>
            </b-col>
            <b-col cols='6'>
            <p>語句</p>
            <WordList v-bind:list_data="word_data['word']" @update="getData"/>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'
import DocumentTopicGraph from '../components/Document_topic_graph.vue';
import WordList from '../components/WordList.vue';

export default {
  name: 'word',
  components: {
    DocumentTopicGraph,
    WordList,
  },
  props: ['num_topics','word'],
  mounted () {
    this.links = this.loadAll();
    this.getData(this.word);
  },
  data() {
    return {
      word_data: {},
      activeName: 1,
      input:'',
      links: [],
      info_text:'人名の情報が表示されます',
    };
  },
  methods: {
    searchWord () {
      this.getData(this.input)
    },
    querySearch(queryString, cb) {
      var links = this.links;
      var results = queryString ? links.filter(this.createFilter(queryString)) : links;
      // call callback function to return suggestions
      cb(results);
    },
    createFilter(queryString) {
      return (link) => {
        return (link.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
      };
    },
    loadAll() {
      return [
        { "value": "藤原経光" },
        { "value": "藤原宗氏" },
        { "value": "源通方" },
        { "value": "藤原頼資"},
        { "value": "平知宗"},
        { "value": "相円"},
        { "value": "嵯峨天皇"},
        { "value": "神吉"},
        { "value": "布施"},
        { "value": "大嘗会"},
        ];
      },
      handleSelect(item) {
        console.log(item);
      },
      getData (input) {
        this.input = input;
        axios.get('https://w3id.org/hi/api/entity/chname/' + this.input)
          .then(response => {
            this.info_text = response.data[0]['http://schema.org/description'][0]['@value']
          })
          .catch(error => {
          console.log(error)
          this.info_text ='説明データがありませんでした'
          })
        this.loading = true
        const path = BACKEND_URL + '/word/' + this.num_topics +'/' + input
        axios.get(path)
            .then(response => {
            this.word_data= response.data;
            })
            .catch(error => {
            console.log(error)
            this.loading = false
            this.input='None'
            })
    },
}
}
</script>