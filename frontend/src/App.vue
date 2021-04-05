<template>
  <div id="app">
    <el-menu :default-active="activeIndex" mode="horizontal" router>
      <el-menu-item index="home" :route="{ name:'home' }">Home</el-menu-item>
      <el-submenu>
        <template slot="title">Topic</template>
        <el-menu-item index="topic" v-for="n of num_data" :key="n" :route="{ name:'topic' , params : { id: n , num_topics: num_data}}" >topic{{n}}</el-menu-item>
      </el-submenu>
      <el-menu-item index="document" :route="{ name:'document',params:{num_topics:num_data, text_id:textId} }">Text</el-menu-item>
      <el-menu-item index="word" :route="{ name:'word' ,params:{num_topics:num_data,word:w} }" >Word</el-menu-item>
      <!-- <el-menu-item index="about" :route="{ name:'about' }">About</el-menu-item>
      <el-menu-item index="fortune" :route="{ name:'fortune' }">Fortune</el-menu-item> -->
      <!-- <el-menu-item index="randomchart" :route="{ name:'randomchart' }">Chart</el-menu-item>
      <el-menu-item index="input" :route="{ name:'input' }">Input</el-menu-item> -->
      <el-menu-item index="settings" :route="{ name:'settings' }" >Settings</el-menu-item>
      <!-- <el-menu-item>
        <a href="https://element.eleme.io" target="_blank">Link</a>
      </el-menu-item> -->
    </el-menu>
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      activeIndex: this.$route.name,
      num_data: 10,
      w:'word',
      textId: 0,
    }
  }
}
</script>

<style scoped>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
}
a {
  text-decoration: none;
}
</style>