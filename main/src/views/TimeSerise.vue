<template>
  <div class="timeSerise">
    <div class="channels-container">
      <el-form>
        <el-form-item label="图像组件：">
          <el-checkbox-group v-model="form.checkList">
            <el-checkbox value="timeserise" label="timeserise" @change="timeSeriseEvent"></el-checkbox>
            <el-checkbox label="fft" value="fft" @change="fftEvent"></el-checkbox>
            <el-checkbox label="psd" disabled value="psd" @change="psdEvent"></el-checkbox>
            <el-checkbox label="headplot" disabled value="headplot" @change="headPlotEvent"></el-checkbox>
          </el-checkbox-group>
          <el-button class="home-page-button" type="warning" @click="homePage">返回首页</el-button>
        </el-form-item>
        <div class="filter-type">
          <el-col :span="12" class="time-fregament-col-6">
            <el-form-item label="滤波类型">
              <div class="time-fregament time-fregament-first">
                <el-select v-model="form.model">
                  <el-option value="0" label="带通滤波" name="带通滤波"></el-option>
                  <!-- <el-option value="1" label="带阻滤波" name="带租滤波"></el-option> -->
                </el-select>
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="滤波名称">
              <el-select v-model="form.filter">
                <el-option value="0" label="巴特沃斯" name="巴特沃斯"></el-option>
                <el-option value="1" label="切比雪夫" name="切比雪夫"></el-option>
                <el-option value="2" label="贝叶斯" name="贝叶斯"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </div>
        <div class="time-fregament time-fregament-second">
          <el-col :span="12">
            <el-form-item label="滤波范围:">
              <el-col :span="6">
                <el-input type="text" label="low" v-model="form.low" placeholder="请输入滤波的起始值"></el-input>
              </el-col>
              <el-col :span="1">
                <div class="time-filter-split">--</div>
              </el-col>
              <el-col :span="6">
                <el-input type="text" label="heigh" v-model="form.high" placeholder="请输入滤波的z值"></el-input>
              </el-col>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="滤波阶数:">
                <el-select v-model="form.order">
                  <el-option value="1" label="1" name="1"></el-option>
                  <el-option value="2" label="2" name="2"></el-option>
                  <el-option value="3" label="3" name="3"></el-option>
                  <el-option value="3" label="3" name="4"></el-option>
                </el-select>
            </el-form-item>
          </el-col>
        </div>
          <div class="data-config-apply-container">
            <el-button class="data-config-apply" @click="apply" type="primary">应用</el-button>
          </div>
      </el-form>
      <div class="channel-button">
        <ElectrodePositions :show-info="showChannels" :radius="radius" @point-click="toggle"></ElectrodePositions>
        <!-- <span>通道名：</span> <el-button class="" :type="showAll ? 'success' : ''" @click="showAllToggle">All</el-button>
        <el-button v-for="item in showChannels" :type="selectChannels.includes(item) ? 'success' : ''"
          @click="toggle(item)">{{ item }}</el-button> -->
      </div>
    </div>
  </div>
</template>
<script>
import CompoentConfig from '../Components/index.js'
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'

import { 
  openTimeSeriseWindow, 
  homePage, 
  getConfigFromServe, 
  postSelectChannel, 
  initDevTools, 
  startStream, 
  stopStream, 
  filterBoardData, 
  openFFTWindow, 
  closeTimeSeriseWindow
} from '../api/index'
export default {
  data() {
    return {
      activeName: 'first',
      filterShow: false,
      showAll: false,
      selectChannels: [],
      channels: [],
      currentChannels: [],
      radius: 400,
      form: {
        productId: "5",
        ip: "",
        model: "0",
        low: 5,
        high: 45,
        filter: 0,
        order: 2,
        checkList: [],
      },
    }
  },
  components: {
    "time-serise-config": CompoentConfig["TimeSeriseConfig"],
    "fft-config": CompoentConfig["fftConfig"],
    "head-plot-config": CompoentConfig['headPlotConfig'],
    ElectrodePositions
  },
  destroyed() {
    if (this.timmer) {
      clearInterval(this.timmer)
    }
  },
  computed: {
    showChannels() {
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
      let info = {}
      this.currentChannels = channels
      channels.forEach((item, index) => {
        info[item]={
          switch: this.selectChannels.indexOf(item) >=0 ? true: false,
          label: item,
          show: 'switch',
          name: item,
        }
      })
      return info
    }
  },
  async mounted() {
    const config = JSON.parse(localStorage.getItem('mindbridgeinfo'))
    if (config) {
      this.form.productId = config.productId
      this.form.ip = config.ip
    }
    setTimeout(async () => {
      const data = await getConfigFromServe("msg")
      this.channels = JSON.parse(data)['channels']
      this.products = JSON.parse(data)['products']
    }, 300);
  },
  methods: {
    homePage() {
      homePage()
    },
    handleClick() {
    },
    async home() {
      this.$router.back()
    },
    timeSeriseEvent(chacked) {
      if (chacked) {
        openTimeSeriseWindow({...this.form, "currentFigure": 'timeserise'})
        setTimeout(() => {
          this.showAllToggle(true)
        }, 1000);
      } else {
        closeTimeSeriseWindow()
      }
    },
    headPlotEvent(chacked) {
      if (chacked) {
        if (!this.showAll) {
          setTimeout(() => {
            this.showAllToggle(true)
          }, 1000);
        }
      } else {
      }
    },
    fftEvent(chacked) {
      if (chacked) {
        openFFTWindow({...this.form, "currentFigure": 'fft'})
        setTimeout(() => {
          this.showAllToggle(true)
        }, 1000);
      } else {
        openFFTWindow()
      }
    },
    psdEvent(chacked) {
    },
    async apply() {
      const res =  await filterBoardData(this.form)
    },
    toggle(point) {
      const channel = point['label']
      if (this.selectChannels.indexOf(channel) >= 0) {
        this.selectChannels = this.selectChannels.filter(item => item != channel)
      } else {
        this.selectChannels.push(channel)
      }
      postSelectChannel(this.selectChannels)
    },
    showAllToggle() {
      if (this.form.checkList.length == 0) {
        return
      }
      if (this.showAll == true) {
        this.selectChannels = []
        this.showAll = false
        postSelectChannel(this.selectChannels)
        return
      }
      this.showAll = true
      this.selectChannels = this.currentChannels
      postSelectChannel(this.selectChannels)
    }
  }
};
</script>
  
<style>
.timeSerise {
  max-width: 900px;
  margin: 0 auto;
  margin-top: 5px;
  background-color: white;
  padding: 30px 20px;
  box-sizing: border-box;
}

.timeSerise .el-form {
  overflow: hidden;
}

.timeSerise-content {
  margin-left: 30px;
}

.el-table .el-table__cell {
  padding: 3px 0;
}

.timeSerise-result {
  display: flex;
}

.timeSerise-form {
  padding: 0 20px;
}

.timeSerise-pass {
  margin-bottom: 30px;
}

.channels-container .el-button {
  margin-bottom: 10px;
}

.time-fregament {
  overflow: hidden;
}


.channels-container .el-form-item__label {
  font-size: 14px;
  font-weight: 900;
}

.time-filter-split {
  text-align: center;
}

.time-fregament-first .el-button {
  width: 100%;
}

.time-fregament-col-6.el-col-6 {
  width: 31%;
}

.el-col-5 .el-select {
  margin: 0;
  margin-left: 10px;
}

.time-serise-title {
  margin-bottom: 20px;
}

.home-page-button {
  position: absolute;
  right: 0;
  top: 0;
}

.filter-type {
  overflow: hidden;
}

.channel-button {
  margin-right: 10px;
  margin-bottom: 10px;
}

.data-config-apply {
  width: 400px;
}

.data-config-apply-container {
  text-align: center;
  padding-bottom: 30px;
  border-bottom: 1px solid #ddd ;
  margin-bottom: 20px;
}
</style>
  