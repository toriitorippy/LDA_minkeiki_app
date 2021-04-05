<!-- HTMLを記述 -->
<template>
  <div class="fortune">
    <p>Fortune</p>
    <button @click="getRandom">占う</button>
    <p>Random number from backend: {{ randomNum }}</p>
    <h1 v-if="randomNum%4==0">Awesome!!!</h1>
    <h2 v-if="randomNum%4==1">Good</h2>
    <h2 v-if="randomNum%4==2">Bad...</h2>
    <h1 v-if="randomNum%4==3">S〇〇ks!!!</h1>
    <h2>{{ topic_data['data'][0] }}</h2>
  </div>
</template>

<!-- JavaScriptを記述 -->
<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
  name: 'Fortune',
  data () {
    return {
      randomNum: 0,
      topic_data: null,
    }
  },
  methods: {
    getRandom () {
      this.randomNum = this.getRandomNum()
    },
    getRandomNum () {
      const path = BACKEND_URL + '/rand'
      axios.get(path)
        .then(response => {
          this.randomNum = response.data.randomNum
        })
        .catch(error => {
          console.log(error)
        })
    },
    getData() {
      this.topic_data = this.getDataTopic()
    },
    getDataTopic () {
      const path = BACKEND_URL + '/name'
      axios.get(path)
        .then(response => {
          this.topic_data = response.data
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  created () {
    this.getRandom()
    this.getData()
  }
}
</script>
<!--一行空行を入れてください-->