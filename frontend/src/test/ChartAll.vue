<template>
  <div class="small">
    <line-chart :chart-data="datacollection" :options="options"></line-chart>
    <!-- <button @click="fillData()">Randomize</button> -->
  </div>
</template>

<script>
  import LineChart from './LineChart.js'
  import axios from 'axios'
  import {BACKEND_URL} from '../../util/const'

  export default {
    components: {
      LineChart
    },
    data () {
      return {
        datacollection: null,
        topic_data: null,
        options: {     
              title: {                           //タイトル設定
              display: true,                 //表示設定
              fontSize: 18,                  //フォントサイズ
              text: 'トピックの時系列変化'                //ラベル
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
    methods: {
      getData() {
        this.topic_data = this.getDataTopic()
        },
      getDataTopic () {
        const path = BACKEND_URL + '/data'
        axios.get(path)
            .then(response => {
            this.topic_data = response.data
            this.fillData()
            })
            .catch(error => {
            console.log(error)
            })
        },
      fillData () {
        this.datacollection = {
          labels: this.topic_data['topic1'],
          datasets: [
            {
              label: 'topic1',
              backgroundColor: '#f87979',
              data: this.topic_data['topic1'],
            },
            {
              label: 'topic2',
              backgroundColor: 'rgba(255, 159, 64, 0.2)',
              data: this.topic_data['topic2'],
            },
            {
              label: 'topic3',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              data: this.topic_data['topic3'],
            },
          ],
         
        }
      },
    }
  }
</script>

<style>
  .small {
    max-width: 600px;
    margin:  150px auto;
  }
</style>