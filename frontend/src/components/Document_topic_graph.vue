<template>
    <div>
        <piechart :labels="data.labels" :datasets="data.datasets" :options="options"/>
    </div>
</template>


<script>
import piechart from '../assets/PieChart.vue'
import * as palette from 'google-palette'

export default {
  name: 'DocumentTopicGraph',
    props: {
        topic_data: Object,
    },
    components: {
        piechart,
    },
  data () {
    return {
      data: {
        labels: ['topic1'],
        datasets: [
          {
            // label: this.topic_data['topic_number'],
            data: [0],
            backgroundColor: palette('mpn65', 1).map(
              function(hex) {
                return '#' + hex
              }
            ),
          },
        ]
      },
      options: {
        onClick:this.handle
        // scales: {
        //   xAxes: [{
        //     scaleLabel: {
        //       display: true,
        //       labelString: 'Month'
        //     }
        //   }],
        //   yAxes: [{
        //     ticks: {
        //       beginAtZero: true,
        //       stepSize: 10,
        //     }
        //   }]
        // }
      }
    }
  },
//   created () {
//     this.getData()
//   },
  mounted () {
    // this.renderChart(this.data, this.options)
    // console.log("render")
  },

  methods: {
      handle (point, event) {
        console.log('click')
        const item = event[0]
        console.log(item._index)
        this.$router.push({
            name: 'topic',
            params: { num_topics: this.topic_data['topic_rate'].length ,id:item._index+1 }
      })
        // this.$emit('on-receive', {
        //   index: item._index,
        //   backgroundColor: item._view.backgroundColor,
        //   value: this.values[item._index]
        // })
      },
      fill_data(){
          this.data.labels = this.topic_data['topic_number']
          this.data.datasets = [
          {
            // label: this.topic_data['topic_number'],
            data: this.topic_data['topic_rate'],
            backgroundColor: palette('mpn65', this.topic_data['topic_rate'].length).map(
              function(hex) {
                return '#' + hex
              }
            ),
          },
        ]
      }
  },
      watch: {
      topic_data: function(){
        console.log(this.topic_data['topic_number'])
        console.log('fill')
        this.fill_data()
      }
    },
}
</script>