<template>
  <div class="impedences">
    <div class="impedences-content">
      <div class="impedences-pass">
        <el-button v-if="!entered" type="primary" @click="impendences">测试设备</el-button>
        <el-button  @click="goToHomePage">返回</el-button>
        <el-radio border size="small" label='label' v-model="showLabel">显示通道名</el-radio> 
        <el-radio border size="small" label='color' v-model="showLabel">脱落颜色</el-radio> 
      </div>
      <div>
        <ElectrodePositions :eeg-info="selectedImpedences" :radius="radius" ></ElectrodePositions>
      </div>
    </div>
  </div>
</template>
<script>
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'

import { startImpendenceTest, endImpendenceTest, getImpendenceFromServe,getEEGElectronPosition , getConfigFromServe, homePage, startSession , initDevTools} from '../api/index'
export default {
  data() {
    return {
      radius: 690,
      railed: [],
      impedences: [],
      show: true,
      showImage: false,
      showLabel: 'label',
      form: {
        productId: "532",
        ip: "192.168.31.222"
      },
      timmer: null,
      channels: [],
      entered: false,
      eegInfo: [],
    }
  },
  components:{
    ElectrodePositions
  },
  created() {
    startSession()
  },
  destroyed() {
    if (this.timmer) {
      clearInterval(this.timmer)
      endImpendenceTest()
    }
  },
  async mounted() {
    const config = localStorage.getItem('mindbridgeinfo')
    if (config) {
      const infor = JSON.parse(config)
      this.form.productId = infor.productId
      this.form.ip = infor.ip
    }
    setTimeout(async () => {
      const data = await getConfigFromServe("msg")
      this.channels = JSON.parse(data)['channels']
      this.products = JSON.parse(data)['products']
    }, 300);
    const res = await getEEGElectronPosition({system: '1010'})
    this.eegInfo = res
  },
  computed: {
    selectedImpedences() {
      let channels = []
      if (this.form.productId == '5') {
        channels = this.channels['8']
      }
      if (this.form.productId == '516') {
        channels = this.channels["16"]
      }
      if (this.form.productId == '520') {
        channels = this.channels["20"]
      }
      if (this.form.productId == '532') {
        channels = this.channels['32']
      }
      if (this.form.productId == '564') {
        channels = this.channels['64']
      }
      if (!channels || !channels.length) {
        return []
      }
      console.log(this.eegInfo)
      this.eegInfo[0] = this.eegInfo[0].map(item  => {
        return item.toUpperCase()
      })
      let info = channels.map((item, index) => {
        const id = this.eegInfo[0].indexOf(item)
        let label = ''
        let x = ''
        let y = ''
        
        if(id >=0) {
          x = this.eegInfo[1][id]
          y = this.eegInfo[2][id]
          label = this.eegInfo[0][id]
        }
        const data = {
          label: label,
          show: this.showLabel,
          x: x,
          y: y,
          name: item,
          value: this.railed[index] || 0,
          impedence: this.impedences[index] || 0
        }
        return data
      })
      return info
    },
  },
  methods: {
    chooseShowType(type) {
      this.showLabel = type
    },
    goToHomePage() {
      homePage()
    },
    showImageEvent() {
      this.showImage = !this.showImage
    },
    cellClick(row, column, cell, event) {
      console.log('click', row, column)
    },
    start() {
      startImpendenceTest(this.form)
      this.entered = true
      setTimeout(() => {
        this.timmer = setInterval(async () => {
          let data = await getImpendenceFromServe({})
          data = JSON.parse(data)
          this.railed = data['railed'].split(',').map(item => {
            return parseFloat(item).toFixed(2)
          })
          this.impedences = data['impedences'].split(',').map(item => {
            item = parseInt(item)
            if (item < 0) {
              return 0
            }
            return item
          })
          this.show = false
        }, 1000);
      }, 2000);

    },
    impendences() {
      if (this.form.ip == '') {
        this.$alert('', "请输入ip", {
          confirmButtonText: '确定',
        });
        return
      }
      this.start()
    },
  }
};
</script>

<style>

.impedences {
  width: 900px;
  margin: 5px auto;
  background: white;
  position: relative;
  min-height: 500px;
}
.impedences-content {
  margin-left: 30px;
  width: 100%;
}

.el-table .el-table__cell {
  padding: 3px 0;
}

.impedences-pass .el-radio{
  margin-left: 30px;
}

.impedences-result {
  display: flex;
}

.impedences {
  display: flex;
  justify-content: start;
  padding: 30px 0;
  box-sizing: border-box;
}

.impedences-pass {
  margin-bottom: 30px;
}
.impedences-image {
  display: inline-block;
  width: 100px;
  height: 100px;
  position: absolute;
  right: 0;
  top: 10px;
  cursor: pointer;
}
.impedences-image img {
  width: 100%;
  height: 100%;
}

.mask {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  left: 0;
  background: rgba(0, 0, 0, 0.4);
  text-align: center;
  padding-top: 30px;
  box-sizing: border-box;
  z-index: 100;
}

.mask img {
  width: 60%;
  height: auto;
}
</style>
