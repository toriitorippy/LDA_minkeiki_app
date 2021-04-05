<template>
<b-row>
    <el-table
        :data="tableData"
        @row-click="handleClick">
        <el-table-column
        prop="id"
        width="50">
        </el-table-column>
        <el-table-column
        prop="name"
        width="100">
        </el-table-column>
    </el-table>
    <el-table
        :data="tableData2"
        @row-click="handleClick">
        <el-table-column
        prop="id"
        width="50">
        </el-table-column>
        <el-table-column
        prop="name"
        width="100">
        </el-table-column>
    </el-table>
</b-row>
</template>

<script>
export default {
    name: 'word_list',
    props: {
        list_data: Array,
    },
    methods: {
        getData() {
            this.tableData=[]
            this.tableData2 =[]
            for (let i = 0; i < 10; i++) {
                 this.tableData.push({'id':i+1,'name' :this.list_data[i][0]});
                 this.tableData2.push({'id':i+11,'name' :this.list_data[i+10][0]});
            }

        },
         handleClick(val) {
            console.log(val['name'])
            this.$emit('update',val['name']);
      }
    },
    data() {
        return {
            tableData: [],
            tableData2: [],
            customColor: '#409eff',
        }
    },
    created () {
        console.log(this.list_data)
        this.getData()
  },
  watch: {
      list_data: function(){
        console.log(this.list_data)
        this.getData()
      }
    }
}
</script>