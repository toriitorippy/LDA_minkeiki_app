<template>
    <el-card class="box-card">
    <div slot="header" class="clearfix">
        <span>Memo</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="dialogVisible = true">Edit</el-button>
        <el-dialog
        title="Edit"
        :visible.sync="dialogVisible"
        width="30%"
        :before-close="handleClose">
        <el-input
        type="textarea"
        :rows="3"
        placeholder="Please input"
        v-model="topic_data">
        </el-input>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">Cancel</el-button>
            <el-button type="primary" @click="clickEvent()" >Confirm</el-button>
        </span>
        </el-dialog>
    </div>
    <div>
        {{ topic_data }}
    </div>
    </el-card>
</template>



<script>
import axios from 'axios'
import {BACKEND_URL} from '../../util/const'

export default {
    name: 'MEMO',
    props: {
        num: Number,
        total_num: Number,
    },
    methods: {
        getData() {
            this.topic_data = this.getMemo()
        },
        getMemo () {
            const path = BACKEND_URL + '/memo/' + this.total_num +'/' + this.num 
            axios.get(path)
                .then(response => {
                this.topic_data = response.data['data']
                })
                .catch(error => {
                console.log(error)
            })
        },
        clickEvent() {
            this.dialogVisible = false
            const path = BACKEND_URL + '/makememo/' + this.total_num +'/' + this.num +'/' + this.topic_data
            axios.get(path)
                .then(response => {
                console.log(response)
                })
                .catch(error => {
                console.log(error)
            })
        },
    },
    data() {
    return {
        topic_data: null,
        tableData: null,
        dialogVisible: false,
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