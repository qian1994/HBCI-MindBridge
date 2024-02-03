<template>
  <div class="impedences">
    <div class="impedences-content">
      <div class="impedences-pass">
        <el-button v-if="!entered" type="primary" @click="impendences">测试设备</el-button>
        <el-button @click="goToHomePage">返回</el-button>
        <el-radio border size="small" label='label' v-model="showLabel">显示通道名</el-radio>
        <el-radio border size="small" label='color' v-model="showLabel">阻抗测试</el-radio>
        <el-radio border size="small" label='switch' v-model="showLabel">坏导选择</el-radio>

      </div>
      <div class="impedences-bad-channel" v-if="badChannels.length">
        <div class="impedences-bad-channel-warning">选择相关坏导： </div>
        <el-button v-for="channel in badChannels" type="danger" @click="removeBadChannel(channel)">
          {{ channel }}</el-button>
      </div>
      <div class="impedences-pass">
        <ElectrodePositions :show-info="selectedChannelInfo" :radius="radius" @point-click="cellClick">
        </ElectrodePositions>
      </div>
    </div>
  </div>
</template>
<script>
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'
import {
  startImpendenceTest,
  endImpendenceTest,
  getImpendenceFromServe,
  updateBadChannel,
  getBadChannel,
  getConfigFromServe,
  homePage,
  startSession,
  initDevTools,
} from '../api/index'
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
      badChannels: [],

    }
  },
  components: {
    ElectrodePositions
  },
  // beforeDestroy() {
  //   if (this.timmer) {
  //     clearInterval(this.timmer)
  //     endImpendenceTest()
  //   }
  // },
  destroyed() {
    if (this.timmer) {
      clearInterval(this.timmer)
      endImpendenceTest()
    }
    endImpendenceTest()
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
      const badChannels = await getBadChannel()
      if (badChannels && badChannels['bad-channel']) {
        this.badChannels = badChannels['bad-channel']
      }
    }, 300);

  },
  computed: {
    selectedChannelInfo() {
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
      channels.forEach((item, index) => {
        info[item] = {
          switch: this.badChannels.indexOf(item) >= 0 ? false : true,
          label: item,
          show: this.showLabel,
          name: item,
          value: this.railed[index] || 0,
          impedence: this.impedences[index] || 0
        }
      })
      return info
    }
  },
  async beforeDestroy() {
    const res = await updateBadChannel({ "bad-channel": this.badChannels })
    if (res == 'ok') {
      this.$message('保存成果')
    }
  },
  methods: {
    chooseShowType(type) {
      this.showLabel = type
    },
    async goToHomePage() {
      if(this.timmer) {
        const res = await endImpendenceTest(this.form)
      }
      homePage()
    },
    showImageEvent() {
      this.showImage = !this.showImage
    },
    cellClick(point) {
      if (point.show !== 'switch' && point.show !== 'color') {
        return
      }
      if (this.badChannels.indexOf(point['label']) >= 0) {
        this.removeBadChannel(point['label'])
        return
      }
      this.badChannels.push(point['label'])
      updateBadChannel({ "bad-channel": this.badChannels })
    },
    start() {
      startImpendenceTest(this.form)
      this.entered = true
      setTimeout(() => {

        this.timmer = setInterval(async () => {
          try {
            let data = await getImpendenceFromServe({})
            data = JSON.parse(data)
            console.log(data)
            this.railed = data['railed'].split(',').map(item => {
              return parseFloat(item).toFixed(2)
            })
            this.impedences = data['impedences'].split(',').map(item => {
              item = parseInt(item)
              if (item < 0) {
                return 0
              }
              return  (Math.random() * 100 + 5)
            })
            this.show = false
          } catch (error) {
          }

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
    removeBadChannel(label) {
      this.badChannels = this.badChannels.filter(item => item != label)
    }
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

.impedences-pass .el-radio {
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

.impedences-bad-channel {
  padding: 10px 20px;
}

.impedences-bad-channel-warning {
  margin-bottom: 30px;
}

.impedences-bad-channel .el-button {
  margin-bottom: 20px;
}
</style>
