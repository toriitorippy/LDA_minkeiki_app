<script>
import { Doughnut } from "vue-chartjs";

export default {
  extends: Doughnut,
  props: {
    labels: Array,
    datasets: Array,
    options: {
      type: Object,
      default: () => {
        return {
          elements: {
            line: {
              fill: false,
              borderCapStyle: "round",
              borderJoinStyle: "round",
              tension: 0
            }
          },
          responsive: true,
          maintainAspectRatio: false,
          segmentStrokeColor: "transparent"
        };
      }
    }
  },
  mounted: function() {
    this.renderChart(
      {
        labels: this.labels,
        datasets:this.datasets,
      },
      this.options
    );
  },
        watch: {
      datasets: function(){
      this.renderChart(
            {
              labels: this.labels,
              datasets:this.datasets,
            },
            this.options
          );
      }
    },
  
};
</script>
