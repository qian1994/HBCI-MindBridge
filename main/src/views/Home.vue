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
            <el-form-item label="产品型号">
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
            <span>团队简介</span>
          </div>
          <p>视动脑科技团队是以华南师范大学陈娟教授为首的脑科学研究团队。陈娟教授入选国家重要海外人才引进计划青年项目，专注于视觉与动作方面的研究。团队专业采用心理物理学，眼球追踪，运动追踪，脑电图，磁共振成像，神经干预，深度学习及计算建模的方法，从事大脑视觉和动作方面的科学研究，功能评估和康复训练系统的开发、建设及应用，致力于为健康人群的视觉与动作系统功能增强，以及病人的临床神经疾病诊断、治疗与康复提供专业指导</p>
          <div>
            <img src="" alt="">
          </div>
        </div>
      </div>
    <div class="app-contact">
      <div>
        <p> 联系我们</p>
        <p>地址：广东省广州市天河区中山大道西55号华南师范大学心理学院</p>
        <p>网址：http://juanchenpsy.scnu.edu.cn</p>
      </div>
    </div>
  </div>
  </div>
</template>
<script>
import eegPlugins from '../Components/eeg-plugins/index.vue'
import localConfig from '../constents/config'
import { getConfigFromServe, getCurrentBoardData, openFileDialog, getBatteryProportion, initDevTools} from '../api/index'
export default {
  props:["config"],
  components: {
    eegPlugins
  },
  data() {
    return {
      form: {
        ip: '192.168.31.156',
        productId: '5'
      },
      products: [],
    }
  },
  computed:{
    paradigms() {
      let paradigm= []
      paradigm.push(localConfig['timeSerise'])
      this.config.forEach((item, index)  => {
        if (item == 'ssvep') {
          paradigm.push(localConfig['ssvep'])
        }else if (item == 'mi') {
          paradigm.push(localConfig['mi'])
        }else if (item == 'p300') {
          paradigm.push(localConfig['p300'])
        }else {
          paradigm.push({
            name: item,
            title: item,
            id: index+ 6,
            config: ['open', 'delete'],
            icon: require('../assets/coustom'+(index%5 +1)+'.png')
          })
        }
      })
      paradigm.push(localConfig['custom'])
      return paradigm
    }
  },
  mounted() {
    const config = localStorage.getItem('mindbridgeinfo')

    if(config) {
      const infor = JSON.parse(config)
      this.form.productId = infor.productId
      this.form.ip = infor.ip
    }
    setTimeout(async() => {
      const data = await getConfigFromServe("msg")
      this.products = JSON.parse(data)['products']
      const res = await getBatteryProportion(this.form)
      const elements = document.querySelectorAll('.battery') 
      for(let i = 0 ; i < elements.length; i++) {
        const element = elements[i]
        element.style.display = 'none'
      }
      if (res > 90) {
        document.querySelector('.battery-4').style.display = 'block'
        return
      }
      if(res > 70) {
        document.querySelector('.battery-3').style.display = 'block'
        return
      }

      if(res > 40) {
        document.querySelector('.battery-2').style.display = 'block'
        return
      }

      if(res > 15) {
        document.querySelector('.battery-1').style.display = 'block'
        return
      }
      document.querySelector('.battery-0').style.display = 'block'
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
  height: 170px;
  display: flex;
  font-size: 14px;
  padding: 20px ;
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

.app-contact  img{
  margin-left: 30px;
  width: 76px;
  height: 76px;
}

.el-input__inner {
  line-height: 30px;
  height: 30px;
}
</style>