<template>
  <div class="impedences">
    <div class="impedences-content">
      <div class="impedences-pass">
        <el-button  class="impedences-pass-btn" v-if="!entered" type="primary" @click="impendences">测试设备</el-button>
        <el-button class="impedences-pass-btn" v-else type="success"  @click="enter">测试通过进入实验</el-button>
        <el-radio border size="small" label='label' v-model="showLabel">显示通道名</el-radio> 
        <el-radio border size="small" label='color' v-model="showLabel">脱落颜色</el-radio> 
        <el-radio border size="small" label='switch' v-model="showLabel">坏导选择</el-radio> 
      </div>
      <div class="impedences-bad-channel" v-if="badChannels.length">
        <div class="impedences-bad-channel-warning">选择相关坏导： </div>
        <el-button  v-for="channel in badChannels" type="danger" @click="removeBadChannel(channel)"> {{channel}}</el-button>
      </div>
      <div  class="impedences-pass">
        <ElectrodePositions :show-info="selectedChannelInfo" :radius="radius" @point-click="cellClick"> </ElectrodePositions> 
      </div>
    </div>
  </div>
</template>
<script>
import { 
  startImpendenceTest, 
  endImpendenceTest, 
  getImpendenceFromServe, 
  getConfigFromServe,
  updateBadChannel,
  getBadChannel
} from '../api/index'
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'
export default {
  data() {
    return {
      railed: [],
      impedences: [],
      show: true,
      imageSrc: '',
      form: {
        productId: "5",
        ip: "192.168.31.56"
      },
      timmer: null,
      channels: [],
      entered: false,
      radius: 690,
      badChannels: [],
      showLabel: 'label'  // label  color  impandence raild
    }
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

    const badChannels = await getBadChannel()
    if(badChannels && badChannels['bad-channel']) {
      this.badChannels = badChannels['bad-channel']
    }
  },
  components:{
    ElectrodePositions
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
        info[item]={
          switch: this.badChannels.indexOf(item) >=0 ? false: true,
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
  async beforeDestroy(){
    const res = await updateBadChannel({"bad-channel": this.badChannels})
    if (res == 'ok') {
      this.$message('保存成果')
    }
  },
  methods: {
    chooseShowType(type) {
      this.showLabel = type
    },
    cellClick(point) {
      if (point.show !== 'switch'&& point.show !== 'color') {
        return
      }
      if(this.badChannels.indexOf(point['label']) >= 0) {
        this.removeBadChannel(point['label'])
        return
      } 
      this.badChannels.push(point['label'])
      updateBadChannel({"bad-channel": this.badChannels})
    },
    enter() {
      const config = JSON.parse(localStorage.getItem('config'))
      config.passedImpedence = true
      config.ip = this.form.ip
      config.productId = this.form.productId
      config.products = this.products
      localStorage.setItem('config', JSON.stringify(config))
      this.$router.push({ name: 'Home' })
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
    removeBadChannel(label) {
      this.badChannels = this.badChannels.filter(item => item != label)
    }
  }
};
</script>

<style>

.impedences {
  background-color: white;
  max-width: 900px;
  margin: 0 auto;
  position: relative;
  min-height: 500px;

}

.el-table .el-table__cell {
  padding: 3px 0;
}

.impedences-pass-btn {
  margin: 0 20px;
}

.impedences {
  padding: 30px 0;
  box-sizing: border-box;
}

.impedences-pass {
  margin-bottom: 30px;
}

.impedences-image {
  position: absolute;
  top: 20px;
  right: 20px;
  height: 100px;
  width: 100px;
}
.impedences img {
  width: 100%;
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
