<template>
  <div class="container">
    <div >
      <h2> 选择文件</h2>
      <el-button @click="chooseFile">选择文件</el-button>
      <el-button @click="addFiles">添加文件</el-button>
      <!-- <el-button @click="chooseDir">选择文件夹</el-button> -->
    </div>

    <div v-if="files.length">
      <div v-for="file in files"> <span> {{file}} </span>  <span class="remove-btn" @click="removeFiles(file)">X</span> <span class="remove-btn" @click="plotEEGData(file)">plot</span></div>
    </div>
    <div class="" v-if="files.length">
      <h2> 选择预处理步骤</h2>
      <el-checkbox-group v-model="form.checkList">
        <el-checkbox label="detrend" value="detrend">基线漂移</el-checkbox>
        <el-checkbox label="wlt_denoising" value="wlt_denoising">去噪</el-checkbox>
        <el-checkbox label="badChannel" value="badChannel">去坏导</el-checkbox>
        <el-checkbox label="filter" value="">基础滤波</el-checkbox>
        <el-checkbox label="refrence" value="refrence">重参考</el-checkbox>
        <el-checkbox label="sample" value="sample">切片</el-checkbox>
        <el-checkbox label="segmentation" value="segmentation">样本分段</el-checkbox>
        <el-checkbox label="sample_filter" value="sample_filter">样本滤波</el-checkbox>
        <el-checkbox label="sample_detrend" value="sample_detrend">样本矫正基线</el-checkbox>
        <el-checkbox label="down_sample" value="down_sample">降采样</el-checkbox>
        <el-checkbox disabled label="ica" value="ica"></el-checkbox>
      </el-checkbox-group>
    </div>
    <div class=""  v-if="files.length">
      <el-form ref="form" :model="form" label-width="80px" size="mini">
        <el-form-item label="选择放大器型号">
          <el-radio v-model="form.productId" border :label="5" value="0">MindBridge-8</el-radio>
          <el-radio  v-model="form.productId" border :label="516" value="1">MindBridge-16</el-radio>
          <el-radio  v-model="form.productId" border :label="520" value="2">MindBridge-20</el-radio>
          <el-radio  v-model="form.productId" border :label="532" value="2">MindBridge-32</el-radio>
          <el-radio  v-model="form.productId" border :label="564" value="2">MindBridge-64</el-radio>
        </el-form-item>
        
        <h2> 预处理参数选择</h2>
        <el-form-item label="基线漂移" v-if="form.checkList.indexOf('detrend') >=0">
          <el-radio v-model="form.detrend" border label="0" value="0">是</el-radio>
          <el-radio  v-model="form.detrend" border label="1" value="1">否</el-radio>
        </el-form-item>
        <el-form-item label="去噪" v-if="form.checkList.indexOf('wlt_denoising') >=0">
          <el-radio v-model="form.wlt_denoising" border label="0" value="0">小波去噪</el-radio>
          <el-radio  v-model="form.wlt_denoising" border label="1" value="1">公频干扰</el-radio>
          <el-radio  v-model="form.wlt_denoising" border label="2" value="2">小波和公频</el-radio>
        </el-form-item>
        <el-form-item label="去坏导" v-if="form.checkList.indexOf('badChannel') >=0">
          <div  class="badChannel-pass">
            <ElectrodePositions :show-info="selectedChannelInfo" :radius="radius" @point-click="cellClick"> </ElectrodePositions> 
          </div>
        </el-form-item>
        <el-form-item label="基础滤波"  v-if="form.checkList.indexOf('filter') >=0">
          <el-col :span="4">
           <el-input v-model="form.low"> </el-input>
          </el-col>
          <el-col :span="2">
            <div class="split-line">--</div>
          </el-col>
          <el-col :span="4">
            <el-input v-model="form.high"> </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="重参考" v-if="form.checkList.indexOf('refrence') >=0">
          <el-radio v-model="form.refrence" border label="0" value="0">单个电极</el-radio>
          <el-radio v-model="form.refrence" border label="1" value="1">多个电极</el-radio>
          <el-radio v-model="form.refrence" border label="2" value="2">全部电极</el-radio>
        </el-form-item>
        <el-form-item label="选择参考电极" v-if="form.checkList.indexOf('refrence') >=0 && form.refrence != 2">
          <div  class="badChannel-pass">
            <ElectrodePositions :show-info="chooseRefrenceChannel" :radius="radius" @point-click="refrenceCellClick"> </ElectrodePositions> 
          </div>
        </el-form-item>
        <el-form-item label="时间切片" v-if="form.checkList.indexOf('sample') >=0">
          <div  v-for="item in form.triggers" class="processing-slice">
            <el-col class="line" :span="8">
              <span>打标数据： </span> <el-select v-model="item.trigger" placeholder="请选择有用打标">
                <el-option v-for="item in triggerNumbers" :label="item" :value="item"></el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <span>开始时间： </span><el-input v-model="item.startTime"> </el-input>
            </el-col>
            <el-col :span="2">
            </el-col>
            <el-col :span="6">
              <span>结束时间： </span><el-input  v-model="item.endTime"> </el-input>
            </el-col>
            <el-col :span="2">
              <el-button @click="removeTriggerSlice(item)">X</el-button>
            </el-col>
          </div>
        </el-form-item>
        <el-form-item v-if="form.checkList.indexOf('sample') >=0">
          <el-col :span="24">
            <el-button @click="addTrigger"> 添加 + </el-button>
          </el-col>
        </el-form-item> 
        <el-form-item label="样本分段"  v-if="form.checkList.indexOf('segmentation') >=0">
          <el-input v-model="form.segmentation"></el-input> <span>段</span>
        </el-form-item>
        <el-form-item label="样本滤波" v-if="form.checkList.indexOf('sample_filter') >=0">
          <el-col :span="4">
           <el-input v-model="form.samplelow"> </el-input>
          </el-col>
          <el-col :span="2">
            <div class="split-line">--</div>
          </el-col>
          <el-col :span="4">
            <el-input v-model="form.samplehigh"> </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="样本基线"  v-if="form.checkList.indexOf('sample_detrend') >=0">
          <el-radio v-model="form.sampleDetrend" border label="0" >平均</el-radio>
          <el-radio v-model="form.sampleDetrend" border label="1" >选择时间</el-radio>
        </el-form-item>
        <el-form-item label="样本固定时间基线" v-if="form.checkList.indexOf('sample_detrend') >=0 && form.sampleDetrend == 1">
          <el-col :span="11">
           <span>trigger 开始时刻</span> <el-input v-model="form.sampleDetrendStart"> </el-input>
          </el-col>
          <el-col :span="2">
            <div class="split-line">--</div>
          </el-col>
          <el-col :span="11">
            <span>trigger 时刻时刻</span> <el-input v-model="form.sampleDetrendEnd"> </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="降采样"  v-if="form.checkList.indexOf('down_sample') >=0">
         <el-input v-model="form.downSample"></el-input> <span>HZ</span>
        </el-form-item>
        <el-form-item label="ica" v-if="form.checkList.indexOf('ica') >=0">
          <el-radio v-model="form.ica" border label="0" value="0">是</el-radio>
          <el-radio  v-model="form.ica" border label="1" value="1">否</el-radio>
        </el-form-item>
        <el-form-item label="是否保存数据式">
          <el-radio v-model="form.isOutPutData" border label="1" value="1">是</el-radio>
          <el-radio  v-model="form.isOutPutData" border label="0" value="0">否</el-radio>
        </el-form-item>
        
        <el-form-item label="创建脚本">
          <el-radio v-model="form.createScript" border label="1" value="1">是</el-radio>
          <el-radio  v-model="form.createScript" border label="0" value="0">否</el-radio>
        </el-form-item>
        <div class=""  v-if="files.length">
          <Feature @saveFeatureData="getFeatureConfig"></Feature>
        </div>
        <el-form-item label="存储地址">
          <el-button @click="saveDataDir">选择文件夹</el-button>
          <div> {{this.form.saveDataPath}}</div>
        </el-form-item>
      </el-form>
    </div>
    <div class="create-feature-btn" v-if="files.length">
      <el-button type="primary" :disabled="form.checkList.length == 0" @click="onSubmit">确定</el-button>
    </div>
  </div>
</template>
<script>
import { 
  openFileDialog, 
  openDirDialog, 
  initDevTools,
  processingOriginData, 
  getConfigFromServe, 
  getLabelByFileName, 
  plotOriginEEGDataByFile 
} from '../api/index'
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'
import Feature from '../Components/Feature/index.vue'
export default {
  data() {
    return {
      form:{
        checkList: [],
        detrend: 0,
        trigger: [],
        low: 0,
        high: 100,
        triggers: [
          {
            startTime: 0,
            endTime: 0,
            trigger: 0
          }
        ],
        segmentation: 1,
        selectTriggers: [],
        samplelow: 0.5,
        samplehigh: 50,
        sampleDetrendStart: '',
        sampleDetrendEnd: '',
        sampleDetrend: '0',
        downSample: 200,
        isOutPutData: '1',
        ica: 0,
        productId: 5,
        badChannel: [],
        refrenceChannel: [],
        refrence: 0,
        feature: {},
        createScript: '0',
        saveDataPath: '',
      },
     
      radius: 400,
      triggerNumbers: [],
      files: ['C:/Users/admin/Desktop/mindBridgeSoftware/cnsc/data/svp1_2/922_2size_2023_04_05_20_06_56.csv'],
      channels: [],
      channelsName: []
    }
  },
  components:{
    Feature,
    ElectrodePositions
  },
  watch:{
    async files(oldValue, newValue) {
      const res = await getLabelByFileName(newValue)
      this.triggerNumbers = [...new Set(res)];   
    }
  },
  computed:{
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
          switch: this.form.badChannel.indexOf(item) >=0 ? false: true,
          label: item,
          show: 'switch',
          name: item,
          value:0,
          impedence:  0
        }
      })
      return info
    },
    chooseRefrenceChannel() {
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
          switch: this.form.refrenceChannel.indexOf(item) >=0 ? false: true,
          label: item,
          show: 'switch',
          name: item,
          value:0,
          impedence:  0
        }
      })
      return info
    }
  },
  mounted() {
    // initDevTools()
    setTimeout(async () => {
      const data = await getConfigFromServe("msg")
      this.channels = JSON.parse(data)['channels']
      this.products = JSON.parse(data)['products']
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
      this.channelsName = channels
    }, 300);
  },
  methods:{
    removeFiles(file) {
      console.log('this is remove file', file)
      this.files = this.files.filter(item => item != file)
    },
    async onSubmit() {
      const res = await processingOriginData({
        config: this.form,
        files: this.files,
        channels:this.channelsName,
        boardId: this.form.productId
      })
      console.log(res)
      if (res == 'ok') {
        this.$message('成功生成预处理数据')
      }
    },
    async getLabelsByFileName(files) {
      console.log('this is labels', files)   
    },
    async chooseFile() {
      const res = await openFileDialog()
      if (res == 'fail') {
        this.$message('获取文件失败')
        return
      }
      this.files.push(res)
    },
    async addFiles() {
      console.log("this is choose files")
      const res = await openFileDialog()
      if (res == 'fail') {
        this.$message('获取文件失败')
        return
      }
      console.log(res)
      this.files.push(res)
    },
    async chooseDir() {
      console.log('this is choose dirs')
      const res = await openDirDialog()
      if (res == 'fail') {
        this.$message('获取文件失败')
        return
      }
      console.log(res)
    },
    async saveDataDir() {
      console.log('this is choose dirs')
      const res = await openDirDialog()
      if (res == 'fail') {
        this.$message('获取文件失败')
        return
      }
      console.log(res)
      this.form.saveDataPath = res
    },
    getFeatureConfig(feature) {
      this.form.feature = feature
    },
    cellClick(point) {
      if (point.show !== 'switch'&& point.show !== 'color') {
        return
      }
      if(this.form.badChannel.indexOf(point['label']) >= 0) {
        this.removeBadChannel(point['label'])
        return
      } 
      this.form.badChannel.push(point['label'])
    },
    refrenceCellClick(point) {
      if (point.show !== 'switch'&& point.show !== 'color') {
        return
      }
      if(this.form.refrenceChannel.indexOf(point['label']) >= 0) {
        this.removeBadChannel(point['label'], 'refrence')
        return
      } 
      this.form.refrenceChannel.push(point['label'])
    },
    removeBadChannel(label, type) {
      if (type == 'refrence') {
        this.form.refrenceChannel =  this.form.refrenceChannel.filter(item => item != label)
        return
      }
      this.form.badChannel =  this.form.badChannel.filter(item => item != label)
    },
    async plotEEGData(file) {
      const res = await plotOriginEEGDataByFile({file: file, channels: this.channelsName, boardId: this.form.productId})
    },
    addTrigger() {
      this.form.triggers.push( {
        startTime: 0,
        endTime: 0,
        trigger: 0
      })
    },
    removeTriggerSlice(data) {
      this.form.triggers = this.form.triggers.filter(item => item.trigger != data.trigger)
    }
  }
};
</script>

<style>
.container {
  width: 900px;
  background-color: white;
  padding: 20px;
  box-sizing: border-box;
  margin: 5px auto;
}

.container h2 {
  margin: 10px;
  font-size: 15px;
}

.split-line {
  text-align: center;
}

.remove-btn {
  cursor: pointer;
  display: inline-block;
  margin-left:  30px;
}
.container .el-input {
  width: 100px;
}
.processing-slice .el-color-picker__icon, .processing-slice .el-input, .processing-slice .el-textarea {
  margin-bottom: 10px;
}

.create-feature-btn {
  margin-top: 10px;
}

</style>
