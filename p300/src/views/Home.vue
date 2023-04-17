<template>
  <div class="p300-container">
    <div class="reset-model" v-if="!selectMode" >
      <el-button @click="reset" type="warning">重选模式</el-button>
    </div>
    <el-form ref="form" :model="form" label-width="120px" v-if="selectMode">
      <el-form-item label="请选择功能">
        <el-select v-model="form.type" placeholder="请选择实验目的" @change="changeType">
          <el-option label="p300 实验采集数据" value="0"></el-option>
          <el-option label="实时检测" value="1"></el-option>
          <el-option label="生成模型" value="2"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="请选择训练数据" v-if="form.type=='2'">
        <el-button size="small" type="primary" @click="openFileDialogEvent">点击上传</el-button>
        <div slot="tip" class="el-upload__tip" v-if="!form.fileList.length">请选项需要进行模型的数据文件</div>
        <div class="" v-else>
          <div v-for="item in showFiles" :key="item"> {{item}} <span class="files-delete" @click="deleteFile(item)"></span></div>
        </div>
      </el-form-item>
      <el-form-item label="请选择模式" v-if="form.type == '0'">
        <el-select v-model="form.model" placeholder="请选择产品型号">
          <el-option label="number" value="0"></el-option>
          <el-option label="keyboard" value="1"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="请选择模型类别" v-if="form.type=='1'">
        <el-select  v-model="form.dectectModel"  placeholder="模型名称"> 
          <el-option label="RandomForestClassifier" value="RandomForestClassifier"></el-option>
          <el-option label="Perceptron" value="Perceptron"></el-option>
          <el-option label="KNeighborsClassifier" value="KNeighborsClassifier"></el-option>
          <el-option label="SVC" value="SVC"></el-option>
          <el-option label="DecisionTreeClassifier" value="DecisionTreeClassifier"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="请选择训练模型" v-if="form.type=='2'">
        <el-select  
          multiple
          filterable
          allow-create
          default-first-option
           v-model="form.trainModel"  
         placeholder="请选择模型"> 
          <el-option label="RandomForestClassifier" value="RandomForestClassifier"></el-option>
          <el-option label="Perceptron" value="Perceptron"></el-option>
          <el-option label="KNeighborsClassifier" value="KNeighborsClassifier"></el-option>
          <el-option label="SVC" value="SVC"></el-option>
          <el-option label="DecisionTreeClassifier" value="DecisionTreeClassifier"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button  @click="homePage"> 回到首页 </el-button>
        <el-button type="primary"  @click="start" v-if="form.type== '0' || form.type == '1'">进入</el-button>
        <el-button  type="primary" size="large" @click="train" v-if="form.type=='2'">生成p300模型</el-button>
      </el-form-item>
    </el-form>
    <div class="p300-word-container" v-if="!selectMode">
      <div v-for="item in showP300Word" class="p300-character" @click="chooseWord(item)">
        <span>{{ item }}</span>
      </div>
    </div>
    <div v-if="!selectMode">
      <div class="p300-choose-word">
        <div>选中：</div>
        <div>
          <span v-for="index in word_array">{{ index }}</span>
        </div>
      </div>
      <div class="p300-operater">
        <el-button type="primary" @click="enter">进入</el-button>
        <el-button type="danger" @click="deleteW">删除</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import { character } from '../constents/config'
import {  startSession, getConfigFromServe, initDevTools, homePage, openFilesDialog, createMechainLearnP300 } from "../api/index";
import { Loading } from 'element-ui';
export default {
  components: {
  },
  data() {
    return {
      character: character,
      word_array: [],
      numbers: new Array(10).fill(0).map((item, index) => {
          return index
      }),
      form: {
        productId: "532",
        ip: "192.168.31.56",
        model: "1",
        type: '1',
        dectectModel: 'SVC',
        trainModel: [],
        files: [],
        fileList: []
      },
      files: [],
      selectMode: true
    }
  },
  async mounted() {
    const config = localStorage.getItem('mindbridgeinfo')
    if(config) {
      const infor = JSON.parse(config)
      this.form.productId = infor.productId
      this.form.ip = infor.ip
    }
  },
  computed:{
    showP300Word() {
      if(this.form.model == '1') {
        return character
      }
      return this.numbers
    },
    showFiles() {
      return this.form.fileList.map(item => {
        return item.split('/')[item.split('/').length - 1]
      })
    }
  },
  methods: {
    async train() {
      this.loadingInstance = Loading.service({ fullscreen: true, text: '模型生成中请稍等' });
      const res = await createMechainLearnP300({ ...this.form, fileList: this.showFiles})
      this.loadingInstance.close()
    },
    changeType(value) {
      if (value == '0') {
        
      }
    },
    deleteFile(file) {
      this.form.fileList = this.form.fileList.filter(item => {
        const data = item.split('/')[item.split('/').length - 1]
        if (data == file) {
          return false
        }
        return true
      })
    },
    async enter() {
      if (this.word_array.length == 0 && this.form.type == '1') {
        this.$alert('', "请选择实验字符", {
          confirmButtonText: '确定',
        });
        return;
      }
      const res = await startSession(this.form)
      if (res == 'ok'){
        this.$router.push({ name: "paradigm", params: { words: this.word_array, character: this.showP300Word, type: this.form.type, dectectModel: this.dectectModel } })
      }
    },
    chooseWord(item) {
      this.word_array.push(item)
    },
    deleteW() {
      this.word_array.pop()
    },
    reset() {
      this.selectMode = true
    },
    async start() {
      if(this.form.type == '0') {
        this.selectMode = false
        return
      }
      const res = await startSession(this.form)
      console.log('res', res)
      if (res == 'ok'){
        this.$router.push({ name: "paradigm", params: { words: this.word_array, character: this.showP300Word } })
      }
    },
    async homePage() {
      const res = await homePage('')
    },
    async openFileDialogEvent(){
      console.log('this is place open file dialog event')
      const res = await openFilesDialog({})
      if(res) {
        this.form.fileList = this.form.fileList.concat(res)
      }
    }
  },
};
</script>
<style>
.p300-container {
  box-sizing: border-box;
  position: relative;
  padding-bottom: 20px;
  width: 800px;
  margin: 0 auto;
  background: white;
  margin-top: 5px;
}

.el-form {
  width:  600px;
  height: 500px;
  padding-top: 50px;
  box-sizing: border-box;
  margin: 0 auto;
  background-color: white;
  border-radius: 0px 0px 4px 4px;
}

.p300-character {
  width: 64px;
  height: 36px;
  background: #FFFFFF;
  border-radius: 4px 4px 4px 4px;
  opacity: 1;
  border: 1px solid #DCDFE6;
  display: inline-block;
  margin-left: 12px;
  margin-top: 12px;
  text-align: center;
  line-height: 36px;
  cursor: pointer;
}

.p300-word-container {
  width: 408px;
  height: 412px;
  background: #F5F7F8;
  border-radius: 0px 0px 4px 4px;
  opacity: 1;
  margin: 0 auto;
}

.p300-footer {
  text-align: center;
}

button.p300-button {
  width: 300px;
  margin: 20px 50px;
  height: 40px;
}

.p300-choose-word {
  margin: 20px 0;
  padding: 50px 100px;
  text-align: center;
  color: orange;
  background-color: white;
  font-size: 20px;

}

.p300-choose-word span {
  display: inline-block;
  width: 80px;
  height: 40px;
  background: #F0F2F5;
  border-radius: 4px 4px 4px 4px;
  opacity: 1;
  border: 1px solid #DCDFE6;
  text-align: center;
  line-height: 40px;
  margin-right: 10px;
  margin-top: 10px;
}

.p300-operater {
  text-align: center;
}
.reset-model {
  text-align: right;
  padding-right: 20px;
  box-sizing: border-box;
  margin-bottom: 40px;
  padding-top: 20px;
}

.files-delete {
  display: inline-block;
  width: 15px;
  height: 15px;
  background: url("../assets/delete.png");
  background-size: 100% 100%;
  margin-left: 30px;
  cursor: pointer;
  position: relative;
  top: 3px;
}
</style>