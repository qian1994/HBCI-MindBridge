<template>
  <div class="container">
    <el-form :label-width="'150px'" ref="formF" :model="form" :inline="true">
      <div class="container-box">
        <el-row :gutter="50">
          <el-col :span="12">
            <div class="container-modelBox">
              <img class="container-modelBox-img" src="../assets/monitor.png" alt="">
              <el-form-item>
                <div>产品型号</div>
                <el-select disabled v-model="form.productId" placeholder="请选择产品型号">
                  <el-option v-for="item in products" :label="item.name" :value="item.id"></el-option>
                </el-select>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="container-modelBox">
              <img class="container-modelBox-img" src="../assets/link.png" alt="">
              <el-form-item disabled>
                <div>设备ip</div>
                <el-input v-model="form.ip" placeholder="请输入放大器ip"></el-input>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
        <el-row :gutter="50">
          <el-col :span="12">
            <div class="container-modelBox">
              <img class="container-modelBox-img" src="../assets/wallet.png" alt="">
              <el-form-item>
                <div>被试id</div>
                <el-input v-model="form.pationCode" placeholder="实验名"></el-input>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="container-modelBox">
              <img class="container-modelBox-img" src="../assets/receiving.png" alt="">
              <el-form-item>
                <div>被试姓名</div>
                <el-input v-model="form.userName" placeholder="脑电实验文件名称"></el-input>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </div>
      <el-col :span="12">
        <el-form-item label="文件名">
          <el-input v-model="form.fileName" placeholder=""> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="操作者">
          <el-input v-model="form.technician" placeholder="操作者名字或编号"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="被试附加信息">
          <el-input v-model="form.patient_additional" placeholder="请输入被试相关信息"></el-input>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="被试年龄">
          <el-input v-model="form.age" type="number" placeholder="请输入被试的年龄"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-select disabled v-model="form.gender" placeholder="请选择被试性别">
          <el-option valu="male" label="male"></el-option>
          <el-option valu="female" label="female"></el-option>
        </el-select>
      </el-col>
      <el-col :span="12">
        <el-form-item label="被试生日">
          <el-popover v-model="visible" placement="right" title="被试生日" width="600" trigger="click">
            <el-Calendar v-model="form.birthdate"></el-Calendar>
            <div style="text-align: right; margin: 0">
              <el-button size="mini" type="text" @click="visible = false">取消</el-button>
              <el-button type="primary" size="mini" @click="visible = false">确定</el-button>
            </div>
            <el-button slot="reference">{{ birthdate }}</el-button>
          </el-popover>
        </el-form-item>
      </el-col>

      <el-col :span="12">
        <el-form-item label="打标数字">
          <el-input v-model="form.marker" disabled placeholder=""> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="刺激模式">
          <el-select v-model="form.selectModel" placeholder="请选择刺激的模式">
            <el-option v-for="item in models" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="点数量" v-if="form.selectModel == '6motion'">
          <el-input v-model="form.motionNumber" placeholder="请选择小球数量"> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="trial间隔时长">
          <el-input v-model="form.trialLantency" type="number" placeholder="请输入每次trial间隔休息时长：毫秒"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="中心距离" v-if="form.selectModel == '6motion'">
          <el-input v-model="form.motionDistance" placeholder="请输入中心距离"> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="目标位置">
          <el-select v-model="form.targetIndex" placeholder="请选择目标再第几次出现">
            <el-option v-for="item in trial" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="移动速度" v-if="form.selectModel == '6motion'">
          <el-input v-model="form.motionSpeed" placeholder="请输入移动速度"> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="总共trial">
          <el-input v-model="form.totalTrial" type="number" placeholder="请输入进行的trial 的总数"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="点宽" v-if="form.selectModel == '6motion'">
          <el-input v-model="form.motionWidth" placeholder="请输入宽度"> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="单次trial数量">
          <el-select v-model="form.trialNumber" placeholder="请选择一个trial显示的照片数量">
            <el-option v-for="item in trial" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="点高" v-if="form.selectModel == '6motion'">
          <el-input v-model="form.motionHeight" placeholder="请输入高度"> </el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="刺激持续时长">
          <el-input v-model="form.instance" type="number" placeholder="请输入每次刺激持续的时长：毫秒"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="间隔时长">
          <el-input v-model="form.lantency" type="number" placeholder="请输入每次刺激间隔休息时长：毫秒"></el-input>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="oddball颜色" v-if="form.selectModel == '3color'">
          <el-select v-model="form.colorObject" placeholder="请选择oddball颜色">
            <el-option label="红" value="r"></el-option>
            <el-option label="绿" value="g"></el-option>
            <el-option label="蓝" value="b"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="12">
        <el-form-item label="base颜色" v-if="form.selectModel == '3color'">
          <el-select v-model="form.colorTarget" placeholder="请选择base颜色">
            <el-option label="红" value="r"></el-option>
            <el-option label="绿" value="g"></el-option>
            <el-option label="蓝" value="b"></el-option>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="24" class="btnBox">
        <el-form-item>
          <el-button>取消</el-button>
          <el-button type="primary" :disabled="disableEnter" @click="onSubmit">开始实验</el-button>
          <el-button class="create-new-expriment" type="warning" @click="createNewExpriment"> 新建实验 </el-button>
        </el-form-item>
      </el-col>
    </el-form>
  </div>
</template>
<script>
import { getModels, msgListener, getConfigFromServe, startSsvepTask, homePage, initDevTools, trigger } from '../api/index'
import { Loading } from 'element-ui';
export default {
  data() {
    this.loadingInstance = ''
    return {
      trial: new Array(10).fill(0).map((item, index) => index + 1),
      models: [],
      loadingModels: true,
      disableEnter: false,
      visible: false,
      form: {
        motionNumber: 1000,
        motionDistance: 100,
        motionWidth: 3,
        motionHeight: 3,
        motionSpeed: 7,
        selectModel: '6motion',
        colorObject: 'r',
        colorTarget: 'g',
        userName: '',
        ip: '192.168.31.98',
        triggerTrialStart: -1,
        triggerRoundStart: 1,
        triggerRoundTarget: 2,
        productId: 5,
        fileName: "FPVS",
        boardId: "",
        marker: -1,
        images: [],
        age: 0,
        pationCode: 0,
        passedImpedence: false,
        targetIndex: 0,
        trialNumber: 0,
        totalTrial: 0,
        lantency: 0,
        instance: 0,
        trialLantency: 0,
        technician: '',
        patient_additional: '',
        patientcode: '',
        equipment: '',
        admincode: '',
        startDate: '',
        birthdate: new Date()
      },
      products: []
    }
  },
  computed: {
    birthdate() {
      return this.getyyyyMMdd(this.form.birthdate)
    }
  },
  created() {
    const config = localStorage.getItem('mindbridgeinfo')
    if (config) {
      const infor = JSON.parse(config)
      this.form.productId = infor.productId
      this.form.ip = infor.ip
    }
    else {
      setTimeout(async () => {
        const data = await getConfigFromServe("msg")
      }, 300);
    }
  },
  destroyed() {
    localStorage.setItem('config', JSON.stringify(this.form))
  },
  mounted() {
    const config = JSON.parse(localStorage.getItem('config'))
    if (config && config.products) {
      this.products = config.products
    }
    this.loadingModels = true
    msgListener.add(this.flashTaskEnd)
    setTimeout(async () => {
      const models = await getModels("msg")
      this.models = models
      this.loadingModels = false
      const data = await getConfigFromServe("msg")
      this.products = JSON.parse(data)['products']
    }, 300);
  },
  methods: {
    async createNewExpriment() {
      const res = await createNewExpriment(this.form)
      if (res == 'ok') {
        this.$confirm('', "请输入正确ip", {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          center: true
          
        }).then(() => {
          this.onSubmit()
        });
      }
    },
    homePage() {
      homePage()
    },
    isChina(s) {
      let patrn = /.*[\u4e00-\u9fa5]+.*$/
      if (!patrn.exec(s)) {
        return false;
      } else {
        return true;
      }
    },
    flashTaskEnd(res) {
    },
    async onSubmit() {
      const flag = this.isChina(this.form.fileName)
      const regexIP = /^((25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))$/;
      if (flag) {
        this.$alert('', "请输入英文文件名", {
          confirmButtonText: '确定',
        });
        return
      }
      if (this.form.model == '') {
        this.$alert('', "请选择输入模式", {
          confirmButtonText: '确定',
        });
        return
      }
      if (this.form.ip == '' || !regexIP.test(this.form.ip)) {
        this.$alert('', "请输入正确ip", {
          confirmButtonText: '确定',
        });
        return
      }
      if (this.form.pationCode == '') {
        this.$alert('', "请输入被试id", {
          confirmButtonText: '确定',
        });
        return
      }
      this.loadingInstance = Loading.service({ fullscreen: true, text: '设备初始化请稍等' });
      const res = await startSsvepTask({ ...this.form, images: [] })
      if (res == 'ok') {
        this.$router.push({ name: 'enter', params: this.form })
        this.loadingInstance.close()
        localStorage.setItem('config', JSON.stringify(this.form))
      } else {
        this.loadingInstance.close()
        this.$alert('', "任务开始失败，请确认设备连接正常", {
          confirmButtonText: '确定',
        });
      }
    },
    getyyyyMMdd(d) {
      if (typeof (d) !== 'object') {
        return ''
      }
      let curr_date = d.getDate();
      let curr_month = d.getMonth() + 1;
      let curr_year = d.getFullYear();
      String(curr_month).length < 2 ? (curr_month = "0" + curr_month) : curr_month;
      String(curr_date).length < 2 ? (curr_date = "0" + curr_date) : curr_date;
      let yyyyMMdd = curr_year + "-" + curr_month + "-" + curr_date;
      return yyyyMMdd;
    },
  }
};
</script>
<style >
.container {
  padding: 30px;
  background: white;
  overflow: hidden;
  max-width: 900px;
  margin: 0 auto;
  box-sizing: border-box;
}

.container .container-box .el-form-item {
  margin: 0;
}

.container .container-modelBox .el-form-item__content {
  margin-left: 22px;
}

.container-box {
  /* display: flex;
  flex-direction: row;
  flex-wrap: wrap; */
}

.container-modelBox {
  display: flex;
  flex-direction: row;
  align-items: center;
  width: 100%;
  /* width: 284px; */
  height: 80px;
  padding: 8px 18px;
  background: #F5F7FA;
  margin-right: 12px;
  margin-bottom: 12px;
}

.container-modelBox .el-input__inner {
  background-color: #F5F7FA;
  height: 30px;
  font-size: 12px;
  line-height: 30px;
}

.container .el-input__icon {
  line-height: 30px;
}

.container .el-input__inner {
  line-height: 30px;
  height: 30px;
}

.container-modelBox .el-form-item__content {
  line-height: 30px;
}

.container-modelBox-img {
  width: 24px;
  height: 24px;
}

.btnBox .el-form-item {
  float: right;
}

.el-form {
  overflow: hidden;
}

.container .el-form-item {
  margin-bottom: 16px;
}
</style>
