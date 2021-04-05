<!-- HTMLを記述 -->
<template>
  <div class="fortune">
    <p>Enter the number of topics</p>
    <div id="app">
    <input type="text" v-model="textInput">
    </div>
    <button @click="getLda">get new lda</button>
    <p>{{status}}</p>

  </div>
</template>

<!-- JavaScriptを記述 -->
<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
  name: 'NewLda',
  data () {
    return {
      randomNum: 0,
      status: null,
      textInput: 10,
    }
  },
  methods: {
    getLda () {
      const path = BACKEND_URL + '/newdata/' +this.textInput
      this.status = 'now loading...'
      axios.get(path)
                .then(response => {
                this.status ='successs'
                console.log(response)
                })
                .catch(error => {
                console.log(error)
                
            })
    },
  },
  created () {
  }
}
</script>
<!--一行空行を入れてください-->