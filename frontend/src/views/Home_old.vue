<template>
  <div class="home">
    <br>
    <h1>民経記--LDA</h1>
    <br>
    <b-container >
    <el-tabs class="el-card" :class="shadow ? 'is-' + shadow + '-shadow' : 'is-always-shadow'" type="card" v-model="activeName" @tab-click="handleClick">
    <el-tab-pane v-for="n of number_of_topic" :key="n" :label="n" :name="n">topic{{n}}
      <b-row>
      <b-col cols="1">
      </b-col>
      <b-col cols="4">
      <Table v-bind:num="n-1" />
      </b-col>
      <b-col cols="4">
      <Chart v-bind:num="n"/>
      </b-col>
    </b-row>
    </el-tab-pane>
  </el-tabs>
  </b-container>
  </div>
</template>

<script>
import Table from '../components/LDA_Table.vue';
import Chart from '../test/RandomChart.vue';
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
  name: 'home',
  components: {
    Table,
    Chart
  },
  mounted () {
    this.getData()
  },
  data() {
    return {
      activeName: 1,
      number_of_topic:10,
    };
  },
  methods: {
  handleClick(tab, event) {
    console.log(tab, event);
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