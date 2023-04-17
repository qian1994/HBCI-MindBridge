<template>
    <div class="custom">
        <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="文件名">
                <el-input type="text" v-model="form.link" disabled placeholder="功能未开启"> </el-input>
            </el-form-item>
            <el-form-item label="ip">
                <el-input type="text" v-model="form.ip" disabled placeholder="请输入ip"> </el-input>
            </el-form-item>
            <el-form-item label="port">
                <el-input type="text" v-model="form.port" disabled placeholder="请输入端口"> </el-input>
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
import { addParadigmFromLocal, startSession} from '../api/index'
export default {
    data() {
        return {
            form: {
                filePath: '',
                link: ""
            }
        }
    },
    methods: {
        submit() {
            addParadigmFromLocal({
                link: this.form.link,
                filePath: this.form.filePath
            })
        },
        async start() {
            const res = await startSession({})
        },
        async end() {
            const res = await end
        },
        back() {
            this.$router.back()
        }
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