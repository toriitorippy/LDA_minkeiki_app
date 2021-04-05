<template>
    <line-chart :chart-data="datacollection" :options="options" :height=250></line-chart>
    <!-- <button @click="fillData()">Randomize</button> -->
</template>

<script>
  import LineChart from '../assets/LineChart.js'
  import axios from 'axios'
  import {BACKEND_URL} from '../../util/const'

  export default {
    components: {
      LineChart
    },
    props: {
      num: Number,
      total_num: Number,
    },
    data () {
      return {
        data_id: '0',
        datacollection: null,
        topic_data: null,
        nengo_list: null,
        options: {     
              onClick:this.handle, 
              title: {        
                                //タイトル設定
              display: true,                 //表示設定
              fontSize: 18,                  //フォントサイズ
              text: '年別',                //ラベル
              responsive: true,
              maintainAspectRatio: false,
          },                        //◆オプション
          scales: {                          //軸設定
              yAxes: [{                      //y軸設定
                  ticks: {                      //最大値最小値設定
                      min: 0,                   //最小値
                      max: 1,                  //最大値
                  },
              }],
          },
        },
      }
    },
    mounted () {
      this.getData()
    },
    watch: {
      num: function(){
        this.getData()
      }
    },
    methods: {
        handle (point, event) {
        console.log('click')
        const item = event[0]
        console.log(item._index)
        const path_id = BACKEND_URL + '/getid/' + item._index
        axios.get(path_id)
            .then(response => {
              this.data_id = String(response.data['id']);
              console.log(response.data['id']);
              console.log(this.data_id)
            this.$router.push({
                    name: 'document',
                    params: { num_topics: this.total_num ,text_id:this.data_id }
              })
            })
            .catch(error => {
            console.log(error)
            console.log('error!')
            })
      },
      getData() {
        const path = BACKEND_URL + '/nengo'
        axios.get(path)
            .then(response => {
            this.nengo_list= response.data
            this.topic_data = this.getDataTopic()
            })
            .catch(error => {
            console.log(error)
            })
        },
      getDataTopic () {
        const path = BACKEND_URL +  '/getpernengo/'+ this.total_num +'/' + this.num
        axios.get(path)
            .then(response => {
            this.topic_data = response.data
            this.fillData()
            })
            .catch(error => {
            console.log(error)
            })
        },
    //   getLength(){
    //       length = len(this.topic_data)
    //       num_list =
    //       return 
    //   },
      fillData () {
        const topic_str = 'topic'
        this.datacollection = {
          labels: this.nengo_list['nengo'],
          datasets: [
            {
              label: topic_str,
              backgroundColor: '#409eff',
              data: this.topic_data['data'],
            },
            // { old #f87979
            //   label: 'Data Two',
            //   backgroundColor: 'rgba(255, 159, 64, 0.2)',
            //   data: this.topic_data['topci2'],
            // },
            // {
            //   label: 'Data Two',
            //   backgroundColor: 'rgba(153, 102, 255, 0.2)',
            //   data: this.topic_data['topci3'],
            // },
          ],
         
        }
      },
    }
  }
</script>

<style>

</style>