<template>
  <div class="topic">
    <br>
    <h1>Topic{{id}}</h1>
    <br>
    <b-container>
			<b-row>
				<b-col cols="3">
				<h3>Top characters</h3>
				<Table v-bind:num="id-1" :total_num="num_topics"/>
				</b-col>
				<b-col cols="3">
				<h3>Top words</h3>
				<WordTable v-bind:num="id-1" :total_num="num_topics"/>
				</b-col>
				<b-col cols="6">
				<Memo v-bind:num="id-1" :total_num="num_topics"/>
        <div style="margin: 50px 0;"></div>
				<Chart v-bind:num="id-1" :total_num="num_topics" v-if="isPush"/>
        <ChartMonth v-bind:num="id-1" :total_num="num_topics" v-if="!isPush"/>
        <b-button v-on:click="toggleBtn" v-bind:disabled="isPush">年別</b-button> <b-button v-on:click="toggleBtn" v-bind:disabled="!isPush">月別</b-button> 
        <div style="margin: 50px 0;"></div>
				<h3>Top documents</h3>
				<DocumentTable v-bind:num="id-1" :total_num="num_topics"/>
				</b-col>
			</b-row>
    </b-container>
  </div>
</template>

<script>
import Table from '../components/Top_Name.vue';
import WordTable from '../components/Top_Word.vue';
import Chart from '../components/Chart_per_topic.vue';
import ChartMonth from '../components/Chart_per_topic_month.vue';
import Memo from '../components/Memo.vue'
import DocumentTable from '../components/Top_Document.vue'
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
  name: 'home',
  components: {
    Table,
    Chart,
    WordTable,
    DocumentTable,
    Memo,
    ChartMonth,
  },
  props: ['id','num_topics'],
  mounted () {
    this.getData()
  },
  data() {
    return {
      activeName: 1,
      number_of_topic:10,
      isPush: true,
    };
  },
  methods: {
  handleClick(tab, event) {
    console.log(tab, event);
  },
    toggleBtn : function(){
    this.isPush = !this.isPush;
  },
  getData () {
    const path = BACKEND_URL + '/data'
    axios.get(path)
        .then(response => {
        this.number_of_topic= Object.keys(response.data).length;
        })
        .catch(error => {
        console.log(error)
        })
    },
}
}
</script>