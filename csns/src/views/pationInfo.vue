<template>
    <div class="container">
        <el-form ref="info" :model="info" label-width="120px">
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
                technician: '',
                patientname: '',
                patient_additional: '',
                patientcode: '',
                equipment: '',
                admincode: '',
                startDate: '',
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
            const res = await addPatientInfo({...this.info, additional:this.$router.currentRoute.params.additional , birthdate: this.birthdate})
            if (res == 'ok'){
                this.$alert('', "成功添加被试信息", {
                    confirmButtonText: '确定',
                });
                this.$router.push({ name: 'result', params: this.form })
            }
        }
    }
};
</script>
  
<style>
.container {
    padding: 30px;
}

</style>
  