<template>
  <div class="container">
    <el-form ref="form" :model="form" label-width="auto" width class="productBox-content">
      <el-form-item label="生成文件类型：">
        <el-select v-model="form.type" placeholder="请选择需要转换的文件类型">
          <el-option v-for="item in listFileType" :label="item" :value="item"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="选择原始数据:">
        <el-button size="small" type="primary" @click="openFileDialogEvent">点击上传</el-button>
        <div slot="tip" class="el-upload__tip" v-if="!form.fileList.length">请选择需要转换的文件</div>
        <div class="" v-else>
          <div v-for="item in showFiles" :key="item"> {{ item }} <span class="files-delete"
              @click="deleteFile(item)"></span></div>
        </div>
      </el-form-item>
      <el-form-item label="选择保存路径:">
        <el-button size="small" type="primary" @click="opendir">选择</el-button>
        <div slot="tip" class="el-upload__tip" v-if="!form.savePath">请选择保存路径，默认与上传文件同路径</div>
        <div v-else>
          <div> {{ form.savePath }} <span class="files-delete" @click="deleteSavePath(item)"></span></div>
        </div>
      </el-form-item>
      <el-form-item label="操作者" v-if="form.type == 'edf'">
        <el-input v-model="form.technician" placeholder="操作者名字或编号"></el-input>
      </el-form-item>
      <el-form-item label="被试名字" v-if="form.type == 'edf'">
        <el-input v-model="form.patientname" placeholder="请输入被试的名字"></el-input>
      </el-form-item>
      <el-form-item label="被试编号" v-if="form.type == 'edf'">
        <el-input v-model="form.patientcode" placeholder="请输入被试编号"></el-input>
      </el-form-item>
      <el-form-item label="被试附加信息" v-if="form.type == 'edf'">
        <el-input v-model="form.patient_additional" placeholder="请输入被试相关信息"></el-input>
      </el-form-item>
      <el-form-item label="被试年龄" v-if="form.type == 'edf'">
        <el-input v-model="form.gender" type="number" placeholder="请输入被试的年龄"></el-input>
      </el-form-item>
      <el-form-item label="被试生日" v-if="form.type == 'edf'">
        <el-popover v-model="visible" placement="right" title="被试生日" width="600" trigger="click">
          <el-Calendar v-model="form.birthdate"></el-Calendar>
          <div style="text-align: right; margin: 0">
            <el-button size="mini" type="text" @click="visible = false">取消</el-button>
            <el-button type="primary" size="mini" @click="visible = false">确定</el-button>
          </div>
          <el-button slot="reference">{{ birthdate }}</el-button>
        </el-popover>
      </el-form-item>
      <el-form-item label="">
        <el-button @click="createFile">生成文件</el-button> <el-button @click="goToHomePage">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import { openFileDialog, convertFileFormat, openDirDialog, homePage } from '../api/index'
export default {
  components: {
  },
  data() {
    return {
      visible: false,
      form: {
        type: 'mne',
        savePath: '',
        fileList: [],
        technician: '',
        patientname: '',
        patient_additional: '',
        patientcode: '',
        equipment: '',
        admincode: '',
        startDate: '',
        birthdate: new Date()
      },
      listFileType: ['openbci', 'mne', 'edf']
    }
  },
  computed: {
    showFiles() {
      return this.form.fileList.map(item => {
        return item.split('/')[item.split('/').length - 1]
      })
    },
    birthdate() {
      return this.getyyyyMMdd(this.form.birthdate)
    }
  },
  methods: {
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
    async createFile() {
      const res = await convertFileFormat(this.form)
      console.log('res', res)
      if (res == 'ok') {
        this.$alert('', "生成"+this.form.type+"文件成功", {
          confirmButtonText: '确定',
        });
      }
    },
    async openFileDialogEvent() {
      const res = await openFileDialog({})
      if (res) {
        this.form.fileList = this.form.fileList.concat(res)
      }
    },
    async opendir() {
      const res = await openDirDialog()
      if (res) {
        this.form.savePath = res
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
    goToHomePage() {
      homePage()
    }
  }
};
</script>

<style>
.container {
  max-width: 800px;
  background: white;
  margin: 5px auto;
  min-height: 500px;
  padding: 20px;
  box-sizing: border-box;
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
