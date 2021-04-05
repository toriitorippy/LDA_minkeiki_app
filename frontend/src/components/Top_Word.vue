<template>
    <el-table
        :data="tableData"
        style="width: 100%"
        @row-click="handleClick">
        <el-table-column
        prop="name"
        label="Word"
        width="100">
        </el-table-column>
        <el-table-column label="weight" align="center" width="100">
          <template slot-scope="scope">
            <el-progress :percentage="scope.row.weight" :show-text='false' :color="customColor"></el-progress>
          </template>
        </el-table-column>
        <!-- <el-table-column
        prop="weight"
        label="Weight"
        width="180"><el-progress :percentage=prop.row.weight></el-progress>
        </el-table-column> -->
        <!-- <el-table-column
        prop="link"
        label="Link"
        width="100">
        <template slot-scope="scope">
            <el-link :href="scope.row.link" >Link</el-link>
        </template>
        </el-table-column> -->
    </el-table>
</template>

<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
    name: 'LDA_Name',
    props: {
        num: Number,
        total_num: Number,
    },
    methods: {
        getData() {
            this.topic_data = this.getDataTopic()
        },
        getDataTopic () {
            const path = BACKEND_URL + '/topword/' + this.total_num +'/' + this.num 
            axios.get(path)
                .then(response => {
                this.topic_data = response.data['data']
                this.filldata()
                })
                .catch(error => {
                console.log(error)
            })
        },
        filldata () {
            this.tableData = this.topic_data
        },
        handleClick(val) {
            console.log(val['name'])
            this.$router.push({
            name: 'word',
            params: { num_topics:this.total_num,word:val['name'] }
      })
        }
    },
    data() {
    return {
        topic_data: null,
        tableData: null,
        customColor: '#409eff',
    }
    },
    created () {
        this.getData()
  },
    watch: {
      num: function(){
        this.getData()
      }
    },
}
</script>