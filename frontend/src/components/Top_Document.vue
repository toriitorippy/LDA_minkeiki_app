<template>
    <el-table
        :data="tableData"
        @row-click="handleClick">
        <el-table-column
        prop="id"
        label="ID"
        width="60">
        </el-table-column>
        <el-table-column
        prop="source"
        label="日付"
        width="160">
        </el-table-column>
        <el-table-column label="weight" align="center" width="150">
          <template slot-scope="scope">
            <el-progress :percentage="scope.row.weight" :show-text='false' :color="customColor"></el-progress>
          </template>
        </el-table-column>
        <el-table-column
        prop="text_init"
        label="テキスト"
        width="300">
        </el-table-column>
    </el-table>
</template>

<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
    name: 'DocumentTable',
    props: {
        num: Number,
        total_num: Number,
    },
    methods: {
        getData() {
            this.topic_data = this.getDataTopic()
        },
        getDataTopic () {
            const path = BACKEND_URL + '/topdoc/' + this.total_num +'/' +this.num 
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
            console.log(val['id'])
            this.$router.push({
            name: 'document',
            params: { num_topics:this.total_num,text_id:val['id'] }
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
    }
}
</script>