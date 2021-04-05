<!-- HTMLを記述 -->
<template>
  <div class="fortune">
    <br>
    <p>Enter the number of topics</p>
    <div id="app">
    <el-input-number v-model="textInput" @change="handleChange" :min="2" :max="20"></el-input-number>
    </div>
    <br>
    <el-button type="primary" round @click="getLda">get lda</el-button>

  </div>
</template>

<!-- JavaScriptを記述 -->
<script>
export default {
  name: 'Settings',
  data () {
    return {
      randomNum: 0,
      status: null,
      textInput: 10,
    }
  },
  methods: {
    getLda () {
      this.$parent.num_data = Number(this.textInput);
    },
  },
  created () {
  }
}
</script>
<!--一行空行を入れてください-->