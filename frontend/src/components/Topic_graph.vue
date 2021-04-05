<script>
import { Bar } from 'vue-chartjs';
import axios from 'axios';
import {BACKEND_URL} from '../../util/const';

export default {
  extends: Bar,
  name: 'TopicGraph',
  methods: {
    getData() {
      this.topic_data = this.getDataTopic()
    },
    getDataTopic () {
      const paht = BACKEND_URL + '/data'
      axios.get(path)
        .then(response => {
          this.topic_data = response.data
          console.log(this.topic_data['topic1'][0])
          this.renderChart(this.data, this.options)
          console.log("render1")
        })
        .catch(error => {
          console.log(error)
        })
    }
  },
  data () {
    return {
      data: {
        topic_data: null,
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
          {
            label: this.topic_data,
            data: [10, 20, 30, 40, 50, 30],
            backgroundColor: [
              'rgba(255, 99, 132, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(255, 206, 86, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)',
              'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
          },
          {
            label: 'Line Dataset',
            data: [10, 50, 20, 30, 30, 40],
            borderColor: '#CFD8DC',
            fill: false,
            type: 'line',
            lineTension: 0.3,
          }
        ]
      },
      options: {
        scales: {
          xAxes: [{
            scaleLabel: {
              display: true,
              labelString: 'Month'
            }
          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
              stepSize: 10,
            }
          }]
        }
      }
    }
  },
  created () {
    this.getData()
  },
  mounted () {
    // this.renderChart(this.data, this.options)
    // console.log("render")
  }
}
</script>