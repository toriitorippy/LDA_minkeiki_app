<template>
  <div class="topic">

			<b-row>
                <b-col cols = "10">
                        <br>
                        <h1>Topic{{number_of_document}}</h1>
                        <br>
                        <b-row>
                            <b-col cols="3">
                            <h3>Top characters</h3>
                            <Table v-bind:num="id-1" :total_num="num_topics"/>
                            </b-col>
                            <b-col cols="3">
                            <h3>Top words</h3>
                            <WordTable v-bind:num="id-1" :total_num="num_topics"/>
                            </b-col>
                            <b-col cols="4">
                            <Memo v-bind:num="id-1" :total_num="num_topics"/>
                            <Chart v-bind:num="id-1" :total_num="num_topics"/>
                            <h3>Top documents</h3>
                            <document-table/>
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
import Table from '../components/Top_Name.vue';
import WordTable from '../components/Top_Word.vue';
import Chart from '../components/Chart_per_topic.vue';
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
  },
  props: ['num_topics'],
  mounted () {
    this.getData()
    return;
  },
  data() {
    return {
      activeName: 1,
      number_of_document:1,
      isCollapse: false,
      count: 0
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
  getData () {
    const path = BACKEND_URL + '/doc/' + this.num_topics
    axios.get(path)
        .then(response => {
        this.number_of_document= Object.keys(response.data['data']).length;
        console.log(this.number_of_document)
        this.topic_data = response.data['data']
        console.log(this.topic_data[0]['source'])

        })
        .catch(error => {
        console.log(error)
        })
    },
        created () {
        this.getData()
  },
    watch: {
      num: function(){
        this.getData()
      },
    }
}
}
</script>