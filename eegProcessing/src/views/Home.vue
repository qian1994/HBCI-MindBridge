<template>
  <div class="container">
    <div class="file">
      <h2 class="select_file">选中文件</h2>
      <el-button @click="chooseFile"  style="background: #FAA629;color: white;">选择文件</el-button>
      <el-button @click="chooseDir"  style="background: #FAA629;color: white;">选择文件夹</el-button>
      <el-button @click="addFiles"  style="background: #2868C9;color: white;">添加文件</el-button>
    </div>
    <div class="border"></div>
    <div v-if="files.length" class="position">
      <div v-for="file in files" style="display: flex;padding-bottom: 15px;"><h2 class="position_name">地址：</h2><input :value= "file" class="address"><span class="remove-btn" @click="plotEEGData(file)"><el-button style="background: #2868C9;color: white;width: 90px;margin-left: 20px;">绘图</el-button></span><span class="remove-btn" @click="removeFiles(file)"><el-button style="background: #FA5151;color: white;width: 90px;margin-left: 20px;">删除</el-button></span> </div>
    </div>
    <div class="pre_dispose" v-if="files.length">
      <div>
        <h2 class="select_dispose"> 选中预处理步骤</h2>
      </div>
      <div style="margin-top: 6px;">
        <el-checkbox-group v-model="form.checkList">
          <el-checkbox label="detrend" value="detrend" class="checking">基线漂移</el-checkbox>
          <el-checkbox label="wlt_denoising" value="wlt_denoising" class="checking">去噪</el-checkbox>
          <el-checkbox label="filter" value="" class="checking">基础滤波</el-checkbox>
          <el-checkbox label="badChannel" value="badChannel" class="checking">去坏导</el-checkbox><br></br>
          <el-checkbox label="refrence" value="refrence" class="checking">重参考</el-checkbox>
          <el-checkbox label="sample" value="sample" class="checking">切片</el-checkbox>
          <el-checkbox label="sample_detrend" value="sample_detrend" class="checking">样本矫正基线</el-checkbox>
          <el-checkbox label="segmentation" value="segmentation" class="checking">样本分段</el-checkbox><br></br>
          <el-checkbox label="sample_filter" value="sample_filter" class="checking">样本滤波</el-checkbox>
          <el-checkbox label="down_sample" value="down_sample" class="checking">降采样</el-checkbox>
          <el-checkbox disabled label="ica" value="ica"></el-checkbox>
        </el-checkbox-group>
      </div>
    </div>

    <div class="pre_parameter"  v-if="files.length">
      <el-form ref="form" :model="form" label-width="80px" size="mini">
        <h2 class="select_parameter" style="padding-bottom: 20px;"> 预处理参数选择</h2>
        
        <el-form-item v-if="form.checkList.indexOf('detrend') >=0" style="flex: 1;">
          <div class="baseline_drift">
            <label for="基线漂移: " style=" width:100px; display: inline-block;">基线漂移：</label>
          <el-radio v-model="form.detrend" border label="0" value="0" style="width:110px;">是</el-radio>
          <el-radio  v-model="form.detrend" border label="1" value="1" style="width:110px;">否</el-radio>
        </div>
        </el-form-item>

        <el-form-item v-if="form.checkList.indexOf('wlt_denoising') >=0">
          <div class="denoising">
            <label for="去噪: " style=" width:70px; display: inline-block;">去噪：</label>
            <el-radio  v-model="form.wlt_denoising" border label="0" value="0">小波去噪</el-radio>
            <el-radio  v-model="form.wlt_denoising" border label="1" value="1">公频干扰</el-radio>
            <el-radio  v-model="form.wlt_denoising" border label="2" value="2">小波和公频</el-radio>
          </div>
        </el-form-item>

        <el-form-item v-if="form.checkList.indexOf('refrence') >=0">
          <div class="re-reference">
          <label for="重参考: " style=" width:70px; display: inline-block;">重参考：</label>
          <el-radio v-model="form.refrence" border label="0" value="0">单个电极</el-radio>
          <el-radio v-model="form.refrence" border label="1" value="1">多个电极</el-radio>
          <el-radio v-model="form.refrence" border label="2" value="2">全部电极</el-radio>
          </div>
        </el-form-item>

        <el-form-item v-if="form.checkList.indexOf('filter') >=0">
          <div class="basic_filtering"  style="display: flex;">
            <label for="基础滤波: " style=" width:83px; display: inline-block;">基础滤波：</label>
          <div>
          <el-col :span="6">
           <el-input v-model="form.low"> </el-input>
          </el-col>
          <el-col :span="2">
            <div class="split-line">--</div>
          </el-col>
          <el-col :span="6">
            <el-input v-model="form.high"> </el-input>
          </el-col>
        </div>
          </div>
        </el-form-item>

        <div style="display: flex;">
          <el-form-item label="" v-if="form.checkList.indexOf('badChannel') >=0" style="flex: 1;">
            <div class="to_bad_guide">
              <label for="去坏导: " style=" width:200px; display: inline-block;">去坏导：</label>
              <div class="badChannel-pass">
                <ElectrodePositions :show-info="selectedChannelInfo" :radius="radius" @point-click="cellClick"> </ElectrodePositions> 
              </div>
            </div>
          </el-form-item>

          <el-form-item v-if="form.checkList.indexOf('refrence') >=0 && form.refrence != 2">
            <div class="select_the_reference_electrode">
              <label for="选择参考电极: " style=" width:200px; display: inline-block;">选择参考电极：</label>
            <div  class="badChannel-pass">
              <ElectrodePositions :show-info="chooseRefrenceChannel" :radius="radius" @point-click="refrenceCellClick"> </ElectrodePositions> 
            </div>
            </div>
          </el-form-item>
        </div>

        <el-form-item v-if="form.checkList.indexOf('sample') >=0">
          <div class="time_slices">
            <label for="时间切片" style=" width:83px; display: inline-block;flex: 1;vertical-align:middle;">时间切片</label>
            <div style="margin-right: 30px;">
              <el-button  style="background: #FFFFFF;color: #262626;width: 80px;height: 40px;">重置</el-button>
              <el-button  style="background: #2868C9;color: white;width: 80px;height: 40px;">添加</el-button>
            </div>
          </div>
          <div class="border2"></div>
          <div  v-for="item in form.triggers" class="processing-slice">
            <div style="margin: 4px;">
              <el-col :span="6" style="padding: 5px;">
                <label for="开始时间: " style=" width:80px; display: inline-block;">开始时间：</label><el-input v-model="item.startTime" style="width: 100px;height: 40px;display: inline-block;"> </el-input>
              </el-col>
              <el-col :span="6" style="padding: 5px;">
                <label for="结束时间: " style=" width:80px; display: inline-block;">结束时间：</label><el-input  v-model="item.endTime" style="width: 100px;height: 40px;"> </el-input>
              </el-col>
              <el-col class="line" :span="8" style="padding: 5px;">
                <label for="打标数据: " style=" width:80px; display: inline-block;">打标数据：</label> <el-select v-model="item.trigger" placeholder="请选择有用打标"  style="width: 100px;height: 40px;">
                  <el-option v-for="item in triggerNumbers" :label="item" :value="item"></el-option>
                </el-select>
              </el-col>
          </div>
            <el-col :span="2">
            <el-button @click="addTrigger" style="background: #2868C9;color: white;width: 80px;height: 40px;margin-left: -53px;"> 添加 + </el-button>
          </el-col>
            <el-col :span="2">
              <el-button @click="removeTriggerSlice(item)" style="background: #FA5151;color: white;width: 80px;height: 40px;margin-left: -32px;">删除</el-button>
            </el-col>
          </div>
        </el-form-item>

        <el-form-item label="样本基线"  v-if="form.checkList.indexOf('sample_detrend') >=0">
          <div class="baseline">
            <label for="样本基线: " style=" width:100px; display: inline-block;margin-left: -64px;">样本基线：</label>
            <el-radio v-model="form.sampleDetrend" border label="0" style="width:110px;">平均</el-radio>
            <el-radio v-model="form.sampleDetrend" border label="1" style="width:110px;">选择时间</el-radio>
          </div>
        </el-form-item>

        <el-form-item v-if="form.checkList.indexOf('sample_detrend') >=0 && form.sampleDetrend == 1" style="margin-top: 30px;">
          <div class="sample_fixation"  style="display: flex;">
            <label for="样本固定: " style=" width:83px; display: inline-block;color: #999999;">样本固定</label>
            <el-col :span="10">
            <label for="trigger开始时刻: " style="width:160px; display: inline-block;">trigger开始时刻：</label><el-input v-model="form.sampleDetrendStart" style="width: 100px;height: 40px;display: inline-block;margin-left: -50px;"> </el-input>
            </el-col>
            <el-col :span="2">
              <div class="split-line" style="margin-left:-300px">--</div>
            </el-col>
            <el-col :span="10">
              <label for="trigger时刻时刻: " style="width:160px; display: inline-block;margin-left: -160px;">trigger时刻时刻：</label><el-input v-model="form.sampleDetrendEnd" style="width: 100px;height: 40px;display: inline-block;margin-left: -50px;"> </el-input>
            </el-col>
        </div>
        </el-form-item>
       
        <el-form-item  v-if="form.checkList.indexOf('segmentation') >=0">
          <div class="sample_segmentation">
            <label for="样本分段: " style=" width:100px; display: inline-block;">样本分段：</label>
          <el-input v-model="form.segmentation" style="width: 60px;"></el-input> <span>段</span>
        </div>
        </el-form-item>

        <el-form-item v-if="form.checkList.indexOf('sample_filter') >=0">
          <div class="sample_filtering"  style="display: flex;">
            <label for="样本滤波: " style=" width:83px; display: inline-block;">样本滤波：</label>
          <div>
          <el-col :span="6">
           <el-input v-model="form.samplelow"> </el-input>
          </el-col>
          <el-col :span="2">
            <div class="split-line">--</div>
          </el-col>
          <el-col :span="6">
            <el-input v-model="form.samplehigh"> </el-input>
          </el-col>
        </div>
          </div>
        </el-form-item>
      
        <el-form-item  v-if="form.checkList.indexOf('down_sample') >=0">
          <div class="downsampling"  style="display: flex;">
            <label for="时间基线: " style=" width:86px; display: inline-block;color: #999999;">时间基线</label>
            <label for="降采样: " style=" width:83px; display: inline-block;">降采样：</label>
            <el-input v-model="form.downSample" style="width: 80px;margin-left: -20px;"></el-input> <span style="margin-left: 5px;">HZ</span>
        </div>
        </el-form-item>

        <el-form-item label="ica" v-if="form.checkList.indexOf('ica') >=0">
          <el-radio v-model="form.ica" border label="0" value="0">是</el-radio>
          <el-radio  v-model="form.ica" border label="1" value="1">否</el-radio>
        </el-form-item>

        <el-form-item>
          <div class="save">
            <label for="是否保存数据式" style=" width:130px; display: inline-block;">是否保存数据式</label>
          <el-radio v-model="form.isOutPutData" border label="1" value="1" style="width:110px;">是</el-radio>
          <el-radio  v-model="form.isOutPutData" border label="0" value="0" style="width:110px;">否</el-radio>
        </div>
        </el-form-item>
        
        <el-form-item>
          <div class="create">
            <label for="创建脚本" style=" width:130px; display: inline-block;">创建脚本</label>
          <el-radio v-model="form.createScript" border label="1" value="1" style="width:110px;">是</el-radio>
          <el-radio  v-model="form.createScript" border label="0" value="0" style="width:110px;">否</el-radio>
        </div>
        </el-form-item>
        <div class=""  v-if="files.length">
          <Feature @saveFeatureData="getFeatureConfig"></Feature>
        </div>
      </el-form>
    </div>
    <div class="storage_address">
      <label for="存储地址" style=" width:130px; display: inline-block;">存储地址</label>
      <el-button @click="saveDataDir" style="margin-left: -50px;">选择文件夹</el-button>
      <div> {{this.form.saveDataPath}}</div>
    </div>
    <div class="create-feature-btn" v-if="files.length">
      <el-button type="primary" :disabled="form.checkList.length == 0" @click="onSubmit" style="background: #2868C9;color: white;width: 80px;height: 40px;">确定</el-button>
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
     
      radius: 300,
      triggerNumbers: [],
      files: ['a.csv'],
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
      this.files = this.files.filter(item => item != file)
    },
    async onSubmit() {
      
      // const res = await processingOriginData({
      //   config: this.form,
      //   files: this.files,
      //   channels:this.channelsName,
      //   boardId: this.form.productId
      // })

      console.log({
        config: this.form,
        files: this.files,
        channels:this.channelsName,
        boardId: this.form.productId
      })
      // if (res == 'ok') {
      //   this.$message('成功生成预处理数据')
      // }
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
  border-radius: 4px;
  box-sizing: border-box;
  margin: 50px auto;
  clear: both;
  overflow: hidden;
  padding-bottom: 30px;
}

.file{
  width: 840px;
  height: 40px;
  color: #3D3D3D;
  display: flex;
  margin: auto;
  padding: 30px 20px;
}

.select_file{
  margin-top: 10px;
  flex: 1;
  font-weight:bold;
  font-size: 15px;
  color: #3D3D3D;
}

.border {
    position: relative;
    width: 100%;
    height: 2px;
    background-color: #D8D8D8;
}

.position{
  width: 840px;
  height: auto;
  margin: auto;
  padding: 20px 20px;
}

.position_name{
  width: 60px;
  margin-top: 10px;
  margin-right: 10px;
  font-size: 15px;
  font-weight: 400;
  color: #3D3D3D;
}

.address{
  width: 340px;
  height: 40px;
  outline: none;
  padding-left: 10px;
  border: #DCDFE6 1px ;
  border-radius: 4px;
  background-color: #F0F2F5;
}

.pre_dispose{
  width: 840px;
  height: 150px;
  color: #3D3D3D;
  margin: auto;
  padding: 30px 0px 30px 30px;
  background-color: #F2F7FC;
}

.select_dispose{
  width: 120px;
  font-weight:bold;
  font-size: 15px;
  opacity: 1;
  color: #3D3D3D;
}

.checking{
  color: #000000;
  margin-top: 18px;
  height: 22px;
  width: 144px;
  font-size: 14px;
  line-height: 22px;
}

.pre_parameter{
  margin: auto;
  padding: 30px 0px 30px 30px;
  overflow: hidden;
}

.select_parameter{
  width: 120px;
  font-weight:bold;
  font-size: 15px;
  opacity: 1;
  color: #3D3D3D;
}

.denoising{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 470px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.re-reference{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 470px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.basic_filtering{
  margin-left: -76px;
}

 .split-line {
  text-align: center;
}

.to_bad_guide{
  margin-left: -76px;
}

.badChannel-pass{
  width: 400px;
}

.time_slices{
  display: flex;
  margin-left: -76px;
  margin-bottom: 20px;
}

.border2 {
    position: relative;
    width: 900px;
    height: 2px;
    background-color: #D8D8D8;
    margin: 0px 0px 0px -110px;
}

.processing-slice{
  margin:24px 0px 80px -76px;
}

.select_time{
  margin-top: 26px;
  
}

.baseline{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 400px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.baseline_drift{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 400px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.sample_segmentation{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 230px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.sample_filtering{
  margin-left: -76px;
}

.sample_fixation{
  margin-left: -76px;
}

.downsampling{
  margin-left: -76px;
}

.save{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 450px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.create{
  margin-left: -76px;
  padding: 10px 0px 20px 13px;
  align-self: center;
  height: 20px;
  width: 450px;
  background-color: #F2F7FC;
  border-radius: 4px;
}
/*
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
 */
.storage_address{
  margin-left: 25px;
  padding: 10px 10px 10px 13px;
  align-self: center;
  width: 200px;
  background-color: #F2F7FC;
  border-radius: 4px;
}

.create-feature-btn {
  margin-top: 20px;
  margin-left: 25px;
  padding-bottom: 30px;
}

</style>
