<template>
  <div class="ssvep-report">
    <div class="pation-report">
      <el-tree ref="tree" :show-checkbox="false" :check-strictly="true" :data="loadNode" default-expand-all
        @node-click="handleNodeClick">
      </el-tree>
    </div>
    <div v-if="checkedlabel" class="choose-keys">
      选中： {{ checkedlabel }}
    </div>
    <div class="create-report">
      <el-button @click="getReportByPationInfo">获取报告</el-button>
    </div>
    <div>
      <el-table :data="tableContent" height="250" border style="width: 100%">
        <el-table-column v-for="item in tableHead" :prop="item.prop" :label="item.label" >
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import { getReportFileListSSVEP, initDevTools, createFileReportSSVEP } from '../api/index'
export default {
  data() {
    return {
      checkedid: '',
      checkedlabel: '',
      tree: [],
      loadNode: [],
      tableData: []
    }
  },
  computed: {
    tableHead() {
      if (this.tableData.length== 0) {
        return []
      }
      return [{
        label: "被试编号",
        prop: 'pationCode'
      }, {
        label: "实验时间",
        prop: 'time'

      }, {
        label: '条件',
        prop: 'mode'

      },{
        label: '基础频率',
        prop: 'base'

      }, {
        label: '奇异评率',
        prop: 'odd'

      }, {
        label: '备注',
        prop:  'remarks'
      }]
    },
    tableContent() {
      if (this.tableData.length == 0) {
        return []
      }
      return this.tableData.filter((item, index) => index != 0).map(row => {
        return {
          'pationCode': row[0],
          'time': row[1],
          'mode': row[2],
          'base': parseInt(row[3]) >= 5? '显著': '不显著',
          'odd':  parseInt(row[4]) >= 5? '显著': '不显著',
          'remarks': row[5]
        }
      })
    }
  },
  mounted() {
    setTimeout(async () => {
      const res = await getReportFileListSSVEP(this.checkedKeys)
      console.log(res)
      if (res) {
        const data = []
        for (let key in res) {
          data.push({
            label: key,
            id: key,
            children: res[key].map(item => {
              return {
                label: item,
                id: key + '/' + item
              }
            })
          })
          this.loadNode = data
        }
      }
    }, 300);
  },
  methods: {
    handleNodeClick(checkedKeys) {
      if (checkedKeys) {
        this.checkedid = checkedKeys.id
        this.checkedlabel = checkedKeys.label
      }
    },
    async getReportByPationInfo() {
      const info = this.checkedid.split('/')
      if (!this.checkedid) {
        this.$message('请选择需要生成报告的目录')
      }
      const data = {
        "pationcode": info[0],
        'time': info[1] || ''
      }
      const res = await createFileReportSSVEP(data)
      console.log(res)
      if (res != 'fail') {
        this.tableData = res
      }
    }
  }
}

</script>
<style>
.ssvep-report {
  max-width: 800px;
  margin: 5px auto;
  min-height: 500px;
  background-color: white;
  padding: 30px;
  box-sizing: border-box;
}

.create-report {
  margin-top: 20px;
  padding: 20px 0;
  border-bottom: 1px solid #ddd;
}

.choose-keys {
  margin: 10px 0;
}
</style>
