<template>
    <div class="container-p300-pationInfo">
        <el-form ref="info" :model="info" label-width="120px">
            <el-form-item label="操作者">
                <el-input v-model="info.technician" placeholder="操作者名字或编号"></el-input>
            </el-form-item>
            <el-form-item label="被试名字">
                <el-input v-model="info.patientname" placeholder="请输入被试的名字"></el-input>
            </el-form-item>
            <el-form-item label="被试编号">
                <el-input v-model="info.patientcode" placeholder="请输入被试编号"></el-input>
            </el-form-item>
            <el-form-item label="被试年龄">
                <el-input v-model="info.gender" type="number" placeholder="请输入被试的年龄"></el-input>
            </el-form-item>
            <el-form-item label="被试生日">
                <el-popover v-model="visible" placement="right" title="被试生日" width="600" trigger="click">
                    <el-Calendar v-model="info.birthdate"></el-Calendar>
                    <div style="text-align: right; margin: 0">
                        <el-button size="mini" type="text" @click="visible = false">取消</el-button>
                        <el-button type="primary" size="mini" @click="visible = false">确定</el-button>
                    </div>
                    <el-button slot="reference">{{ birthdate }}</el-button>
                </el-popover>
            </el-form-item>
            <el-form-item label="请输入打标描述"> 
                <textarea class="" v-model="info.marks" type="number" placeholder="请输入打标的描述： 如 1： 注意集中， 2： 放松"></textarea>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="saveEDFFile">添加被试信息存储edf文件</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script>
import { addPatientInfo } from '../api/index'
export default {
    data() {
        this.loadingInstance = ''
        return {
            trial: new Array(10).fill(0).map((item, index) => index + 1),
            models: [],
            visible: false,
            activeName: "1",
            loadingModels: true,
            disableEnter: false,
            info: {
                marks: '',
                technician: '',
                patientname: '',
                patientcode: '',
                equipment: '',
                admincode: '',
                birthdate: new Date()
            }
        }
    },
    computed: {
        birthdate() {
            return this.getyyyyMMdd(this.info.birthdate)
        }
    },
    methods: {
        getyyyyMMdd(d) {
            if (typeof(d) !== 'object') {
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
        async saveEDFFile() {
            if (!this.info.marks) {
                this.$alert('', "请输入打标的相关信息", {
                    confirmButtonText: '确定',
                });
                return
            }
            this.info['additional'] = {
                marks: this.info['marks'],
                words: this.$router.history.current.params.words.join(','),
                model: this.$router.history.current.params.model,
            }
            this.info['equipment'] =  this.$router.history.current.params.productId
            console.log(this.info, this.$router.history.current.params)
            const res = await addPatientInfo({...this.info, birthdate: this.birthdate})
            if (res == 'ok'){
                this.$alert('', "成功添加被试信息", {
                    confirmButtonText: '确定',
                });
                this.$router.push({ name: 'Home', params: this.form })
            }
        }
    }
};
</script>
  
<style>

.container-p300-pationInfo textarea{
    width: 200px;
    height: 100px;
    padding: 6px;
    
}

.container-p300-pationInfo {
    width: 700px;
    margin: 5px auto;
    background-color: white;
    padding: 50px ;
    padding-top: 0;
}
</style>
  