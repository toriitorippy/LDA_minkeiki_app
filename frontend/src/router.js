import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import About from './views/About.vue'
import Fortune from './views/Fortune.vue'
import NewLda from './views/NewLda.vue'
import Char from './views/Char.vue'
import Input from './views/Input.vue'
import RandomChart from './test/ChartAll.vue'
import Topic from './views/Topic.vue'
import Settings from './views/Settings.vue'
import Document from './views/Document.vue'
import Word from './views/Word.vue'
import EachDocument from './views/Each_document.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/topic/:num_topics/:id',
      name: 'topic',
      component: Topic,
      props: true
    },
    {
      path: '/document/:num_topics/:text_id',
      name: 'document',
      component: Document,
      props: true
    },
    {
      path: '/eachdocument/:doc_id',
      name: 'eachdocument',
      component: EachDocument,
      props: true
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/word/:num_topics/:word',
      name: 'word',
      component: Word,
      props: true
    },
    {
        path: '/fortune',
        name: 'fortune',
        component: Fortune
      },
      {
        path: '/char',
        name: 'char',
        component: Char
      },
      {
        path: '/randomchart',
        name: 'randomchart',
        component: RandomChart
      },
      {
        path: '/newlda',
        name: 'newlda',
        component: NewLda
      },
      {
        path: '/input',
        name: 'input',
        component: Input
      },
      {
        path: '/settings',
        name: 'settings',
        component: Settings
      },
  ]
})