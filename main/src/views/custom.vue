<template>
    <div class="custom">
        <el-form ref="form" :model="form" label-width="150px">
            <!-- <el-form-item label="文件名">
                <el-input type="text" v-model="form.link" disabled placeholder="功能未开启"> </el-input>
            </el-form-item> -->
            <el-form-item label="ip">
                <el-input type="text" v-model="form.customIp" placeholder="请输入ip"> </el-input>
            </el-form-item>
            <el-form-item label="port">
                <el-input type="text" v-model="form.customPort" placeholder="请输入端口"> </el-input>
            </el-form-item>
            <el-form-item label="数据保存路径">
                <el-button @click="dirChoose"> 选择保存数据路径</el-button> 
                <div v-if="!form.filePath">文件默认保存在软件data文件夹下</div>
                <div v-if="form.filePath">{{form.filePath}}</div>

            </el-form-item>
            <el-form-item label="">
                <el-button @click="back" size="medium">
                    返回首页
                </el-button>
                <el-button @click="start">
                    开始实验
                </el-button>
                <el-button @click="end">
                    结束实验
                </el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
<script>
import { addParadigmFromLocal, startCustomParadigm, startSession, openDirDialog, stopCustomParadigm} from '../api/index'
export default {
    data() {
        return {
            form: {
                filePath: '',
                link: "",
                customIp: '',
                customPort: '',
                ip: '',
                productId: ''
            }
        }
    },
    methods: {
        async dirChoose() {
            const dirPath = await openDirDialog()
            if (dirPath) {
                this.form.filePath = dirPath
            }
        },
        submit() {
            // addParadigmFromLocal({
            //     link: this.form.link,
            //     filePath: this.form.filePath
            // })
        },
        async start() {
            const sres = await startSession({ip: this.ip, productId: this.productId})
            if (sres == 'ok') {
               const res = await startCustomParadigm(this.form)
               if (res == 'ok') {
                    this.$message('第三方socket 连接成功')
               }else {
                    this.$message('请确保第三方socket服务已启动')
               }
            }else {
                this.$message('未连接硬件设备，请先确定放大器已经连接')
            }
            
        },
        async end() {
            const res = await stopCustomParadigm(this.form)
            if (res == 'ok') {
                    this.$message('服务停止')
               }
        },
        back() {
            this.$router.back()
        }
    },
    mounted() {
       this.ip = this.$router.currentRoute.params.ip 
       this.productId = this.$router.currentRoute.params.productId
    }
}
</script>

<style>
.custom {
    max-width: 900px;
    height: 500px;
    background-color: white;
    padding: 30px;
    box-sizing: border-box;
    margin: 5px auto;
}
</style>