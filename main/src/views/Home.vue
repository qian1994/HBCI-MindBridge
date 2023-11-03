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
          设备信息
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
            <el-form-item label="设备ip">
              <el-input v-model="form.ip" placeholder="请输入放大器ip"></el-input>
            </el-form-item>
          </div>
        </el-form>
      </div>
      <div class="app-window-content">
        <div>
          <div class="productBox-title">
            <img class="productBox-img" src="../assets/s-marketing.png" />
            <span>HBCI 团队简介</span>
          </div>
          <p>
            &#8195&#8195本团队创建于2019年8月，以潘家辉教授为召集人，现有梁艳、邱丽娜、王斐、李景聪、周成菊、曲超、何乐为、黄海云、梁瑾、游琪、高炜等12位研究生导师，6位在读博士后，60余位硕士研究生，以及多个本科生研究小组。团队主要围绕着脑机接口和计算机视觉领域，研究新一代人机交互和人机混合智能的关键核心技术。具体研究方向包括：面向意识障碍和运动障碍的多模态脑机接口技术、基于人脸表情和脑电信号的情绪识别、睡眠脑电的实时监测与调控、步态识别和健康评估、医学图像处理、以及混合智能的人机交互技术等。<br>
            &#8195&#8195脑机接口（brain-computer interface, BCI），是在人脑与计算机或其它电子设备之间建立的直接的交流和控制通道 。通过这种通道 ,人就可以直接通过脑来表达想法或操纵设备 ,而不需要语言或动作。脑机接口技术被誉为人脑与外界沟通交流的“信息高速公路”，是公认的新一代人机交互和人机混合智能的关键核心技术，被美国商务部列为14项出口管制技术之一。<br>
            &#8195&#8195山不辞土，故能成其高；海不辞水，故能成其深。欢迎有志于脑机交互与混合智能技术的同学选择和报考我们团队。
          </p>
          <div>
            <img src="" alt="">
          </div>
        </div>
      </div>
      <div class="app-contact">
        <div>
          <p> 联系我们</p>
          <p>地址：广东省佛山市南海区狮山镇华南师范大学软件学院</p>
          <p>网址：https://www.scholat.com/team/hbci</p>
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
            title = '阻抗测试'
          } else if (item == 'transfile') {
            title = '转换文件格式'
          }else if (item == 'processing') {
            title = '数据处理'
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
        title: '打标入口',
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