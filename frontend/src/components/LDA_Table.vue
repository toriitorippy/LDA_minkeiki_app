<template>
    <el-table
        :data="tableData"
        style="width: 100%">
        <el-table-column
        prop="id"
        label="ID"
        width="50">
        </el-table-column>
        <el-table-column
        prop="name"
        label="Name"
        width="180">
        </el-table-column>
        <el-table-column
        prop="link"
        label="Link"
        width="100">
        <template slot-scope="scope">
            <el-link :href="scope.row.link" >Link</el-link>
            <!-- <el-button
                size="mini"
                @click="pushDetail(scope.row.id)">
                <p>{{scope.row.id}}</p>
                <i class="el-icon-edit-outline"></i>
            </el-button> -->
        </template>
    </el-table-column>
    </el-table>
</template>

<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
    name: 'LDA_Table',
    props: {
        num: Number
    },
    methods: {
        getData() {
            this.topic_data = this.getDataTopic()
        },
        getDataTopic () {
            const path = BACKEND_URL + '/name' 
            axios.get(path)
                .then(response => {
                this.topic_data = response.data
                this.filldata()
                })
                .catch(error => {
                console.log(error)
            })
        },
        filldata () {
            this.tableData = this.topic_data['data'][this.num]['data']
        }
    },
    data() {
    return {
        topic_data: null,
        tableData: null,
    }
    },
    created () {
        this.getData()
  }
}
</script>