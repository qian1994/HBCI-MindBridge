<template>
  <div class="container">
    <el-form ref="form" :model="form" label-width="auto" width class="productBox-content">
      <el-form-item label="File type：">
        <el-select v-model="form.type" placeholder="请选择需要转换的文件类型">
          <el-option v-for="item in listFileType" :label="item" :value="item"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="Choose file:">
        <el-button size="small" type="primary" @click="openFileDialogEvent">Uploader</el-button>
        <div slot="tip" class="el-upload__tip" v-if="!form.fileList.length">Selected files</div>
        <div class="" v-else>
          <div v-for="item in showFiles" :key="item"> {{ item }} <span class="files-delete"
              @click="deleteFile(item)"></span></div>
        </div>
      </el-form-item>
      <el-form-item label="Save Path:">
        <el-button size="small" type="primary" @click="opendir">Select</el-button>
        <div slot="tip" class="el-upload__tip" v-if="!form.savePath">Select a path for saving the file. By default, the path is the same as that for uploading the file</div>
        <div v-else>
          <div> {{ form.savePath }} <span class="files-delete" @click="deleteSavePath(item)"></span></div>
        </div>
      </el-form-item>
      <el-form-item label="operator" v-if="form.type == 'edf'">
        <el-input v-model="form.technician" placeholder="place enter operator name"></el-input>
      </el-form-item>
      <el-form-item label="Name" v-if="form.type == 'edf'">
        <el-input v-model="form.patientname" placeholder="place enter subject name"></el-input>
      </el-form-item>
      <el-form-item label="ID" v-if="form.type == 'edf'">
        <el-input v-model="form.patientcode" placeholder="place enter subject ID"></el-input>
      </el-form-item>
      <el-form-item label="additional" v-if="form.type == 'edf'">
        <el-input v-model="form.patient_additional" placeholder="place enter subject addition information"></el-input>
      </el-form-item>
      <el-form-item label="age" v-if="form.type == 'edf'">
        <el-input v-model="form.gender" type="number" placeholder="place enter subject age"></el-input>
      </el-form-item>
      <el-form-item label="birthday" v-if="form.type == 'edf'">
        <el-popover v-model="visible" placement="right" title="birthday" width="600" trigger="click">
          <el-Calendar v-model="form.birthdate"></el-Calendar>
          <div style="text-align: right; margin: 0">
            <el-button size="mini" type="text" @click="visible = false">Cancel</el-button>
            <el-button type="primary" size="mini" @click="visible = false">Confirm</el-button>
          </div>
          <el-button slot="reference">{{ birthdate }}</el-button>
        </el-popover>
      </el-form-item>
      <el-form-item label="">
        <el-button @click="createFile">Save</el-button> <el-button @click="goToHomePage">Back</el-button>
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
