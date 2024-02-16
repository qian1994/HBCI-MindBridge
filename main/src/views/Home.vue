<template>
  <div class="container">
    <div class="app-menu">
      <div v-for="item in paradigms">
        <eeg-plugins :info="item" :form="form"> </eeg-plugins>
      </div>
    </div>
    <div class="app-window">
      <div class="productBox">
        <div class="productBox-title">
          <img class="productBox-img" src="../assets/s-marketing.png" />
          Device type
        </div>
        <el-form ref="form" label-position="top" :model="form" label-width="auto" width class="productBox-content">
          <div class="productBox-model">
            <img class="productBox-model-img" src="../assets/monitor.png" alt="">
            <el-form-item label="">
              <el-select v-model="form.productId" placeholder="请选择产品型号">
                <el-option v-for="item in products" :label="item.name" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </div>
          <div class="productBox-model">
            <img class="productBox-model-img" src="../assets/link.png" alt="">
            <el-form-item label="Device IP">
              <el-input v-model="form.ip" placeholder="请输入放大器ip"></el-input>
            </el-form-item>
          </div>
        </el-form>
      </div>
      <div class="app-window-content">
        <div>
          <div class="productBox-title">
            <img class="productBox-img" src="../assets/s-marketing.png" />
            <span>HBCI </span>
          </div>
          <p>
            This team was established in August 2019 and is led by Professor  Jiahui Pan. It includes 12 graduate student advisors, such as  Yan Liang,  Lina Qiu,  Fei Wang,  Jingcong Li,  Chengju Zhou,  Chao Qu,  Le Wei He,  Haiyun Huang,  Jin Liang,  Qi You,  Wei Gao, along with six postdoctoral researchers, over 60 master's students, and several undergraduate research groups. The team focuses on key core technologies in the fields of brain-computer interfaces (BCI) and computer vision, researching new-generation human-machine interaction and human-machine hybrid intelligence.

          Specific research directions include multimodal BCI technology for consciousness and motor disorders, emotion recognition based on facial expressions and EEG signals, real-time monitoring and regulation of sleep EEG, gait recognition, health assessment, medical image processing, and human-machine interaction technologies for hybrid intelligence.

          BCI, or brain-computer interface, establishes a direct communication and control channel between the human brain and computers or other electronic devices. Through this channel, individuals can express thoughts or manipulate devices directly through the brain without the need for language or physical movements. BCI technology is recognized as the "information highway" for communication between the human brain and the external world, and it is considered a key core technology for the new generation of human-machine interaction and human-machine hybrid intelligence, listed by the U.S. Department of Commerce as one of the 14 controlled export technologies.

          Just as mountains do not refuse soil, making them high, and seas do not refuse water, making them deep, we welcome students with aspirations in BCI and hybrid intelligent technology to choose and apply for our team.
          </p>
          <div>
            <img src="" alt="">
          </div>
        </div>
      </div>
      <div class="app-contact">
        <div>
          <p> Contact us</p>
          <p>Address: School of Software, South China Normal University, Shishan Town, Nanhai District, Foshan City, Guangdong Province</p>
          <p>website：https://www.scholat.com/team/hbci</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import eegPlugins from '../Components/eeg-plugins/index.vue'
import localConfig from '../constents/config'
import { getConfigFromServe, getCurrentBoardData, openFileDialog, getBatteryProportion, initDevTools } from '../api/index'
export default {
  props: ["config"],
  components: {
    eegPlugins
  },
  data() {
    return {
      form: {
        ip: '192.168.31.156',
        productId: '532'
      },
      products: [],
    }
  },
  computed: {
    paradigms() {
      let paradigm = []
      paradigm.push(localConfig['timeSerise'])
      this.config.forEach((item, index) => {
        if (item == 'ssvep') {
          // paradigm.push(localConfig['ssvep'])
        } else if (item == 'mi') {
          // paradigm.push(localConfig['mi'])
        } else if (item == 'p300') {
          // paradigm.push(localConfig['p300'])
        } else {
          let title = item
          if (item == 'impendance') {
            title = 'impedance'
          } else if (item == 'transfile') {
            title = 'transfer'
          }else if (item == 'processing') {
            title = 'analysis'
          }else if (item == 'report') {
            title = '评估报告'
          }else if (item == 'svp1_2') {
            title = '视觉评估'
          } if (item == 'app') {
            return
          }
          paradigm.push({
            name: item,
            title: title,
            id: index + 6,
            config: ['open', 'delete'],
            icon: require('../assets/coustom' + (index % 5 + 1) + '.png')
          })
        }
      })
      paradigm.push({
        name: 'custom',
        title: 'custom',
        id: this.config.length + 1,
        config: ['open'],
        icon: require('../assets/coustom' +1 + '.png')
      })
      console.log('asdfasdf', paradigm)
      return paradigm
    }
  },
  mounted() {
    const config = localStorage.getItem('mindbridgeinfo')
    // initDevTools()
    if (config) {
      const infor = JSON.parse(config)
      this.form.productId = infor.productId
      this.form.ip = infor.ip
    }
    setTimeout(async () => {
      const data = await getConfigFromServe("msg")
      this.products = JSON.parse(data)['products']
    }, 100);
  },
};
</script>
<style >
.container {
  width: 100%;
  height: calc(100% - 80px);
  display: flex;
}

.app-menu {
  width: 200px;
  height: 100%;
  border-right: 1px solid gainsboro;
  overflow: hidden;
  background: white;

}

.app-window {
  height: 100%;
  width: calc(100% - 200px);
  padding: 24px;
  box-sizing: border-box;
  background-color: #F5F7FA;
}

.productBox {
  width: 100%;
  height: 170px;
  padding: 20px;
  box-sizing: border-box;
  background-color: #fff;
  margin-bottom: 20px;
}

.productBox-title {
  height: 24px;
  font-size: 14px;
  display: flex;
  align-items: center;
  color: #131414;
}

.productBox-img {
  height: 14px;
  width: 14px;
  margin-right: 8px;
}

.productBox-content {
  display: flex;
  justify-content: space-between;
}

.productBox-model {
  display: flex;
  align-items: center;
  width: 46%;
  height: 80px;
  padding: 0 16px;
  background-color: #F5F7FA;
}

.productBox-model-img {
  width: 24px;
  height: 24px;
  margin-right: 20px;
}

.productBox .productBox-model .el-form-item {
  margin: 0;
}

.productBox .productBox-model .el-form-item__label {
  height: 20px;
  line-height: 20px;
  padding: 0;
}

.app-window-content {
  width: 100%;
  display: flex;
  font-size: 14px;
  padding: 20px;
  box-sizing: border-box;
  background-color: #fff;
  margin-bottom: 20px;
}

.app-window-content h1 {
  margin-bottom: 50px;
}

.app-window-content p {
  font-size: 14px;
  line-height: 24px;
  color: #767676;
  margin-top: 12px;
}

.app-contact {
  display: flex;
  flex-direction: row;
  height: 116px;
  box-sizing: border-box;
  padding: 20px;
  background-color: #fff;
  margin-top: 20px;
  font-size: 12px;
  color: #3D3D3D;
  align-items: center;
  line-height: 24px;
}

.app-contact img {
  margin-left: 30px;
  width: 76px;
  height: 76px;
}

.el-input__inner {
  line-height: 30px;
  height: 30px;
}
</style>