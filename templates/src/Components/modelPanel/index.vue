<template>
    <div class="control-panel">
        <div>
            <el-popover
            placement="right"
            title="填写相关配置"
            width="500"
            trigger="click"
            v-model="visible"
            >
            <el-form 
            label-position="top"
            :model="msg"
            >
                <el-form-item label="回话时间">
                    <el-input
                        v-model="msg.time"
                        type="input"
                        :rows="10"
                    ></el-input>
                </el-form-item>
                <el-form-item label="ip地址">
                    <el-input
                        v-model="msg.ip"
                        type="input"
                        :rows="10"
                    ></el-input>
                </el-form-item>
                <el-form-item label="频率选择">
                    <el-radio v-model="msg.frequency" label="250">250Hz</el-radio>
                    <el-radio v-model="msg.frequency" label="500">500Hz</el-radio>
                    <el-radio v-model="msg.frequency" label="1000">1000Hz</el-radio>
                </el-form-item>
                <el-form-item label="通道选择">
                    <el-radio v-model="msg.channelNum" label="8">8通道</el-radio>
                    <el-radio v-model="msg.channelNum" label="16">16通道</el-radio>
                    <el-radio v-model="msg.channelNum" label="32">32通道</el-radio>
                    <el-radio v-model="msg.channelNum" label="64">64通道</el-radio>
                </el-form-item>
                <el-form-item label="提交信息">
                    <el-button
                        @click="startSession"
                        type="primary"
                    >
                        进入试验
                    </el-button>
                    <el-button
                        @click="cancel"
                        type="primary"
                    >
                        取消
                    </el-button>
                </el-form-item>
            </el-form>
            <el-button slot="reference">MX HADWARE NO.1</el-button>
            </el-popover>
        </div>
        <div>
            <el-popover
                placement="right"
                title="请选择文件"
                width="200"
                trigger="click"
                >
                <div>asdfasdf</div>
                <el-button slot="reference">PLAYBACK</el-button>
            </el-popover>
        </div>
    </div>
</template>
<script>
export default {
    name: "ModelPanel",
    created(){
        // const time = new Date()
        // const string = `${time.getFullYear}-${time.getMonth}-${time.getDate}_${time.getHours}_${time.getMinutes}_${time.getSeconds}`
        // this.data.msg = string
    },
    data(){
        return {
            visible: false,
            msg: {
                time: '2022-10-03_17:00:00',
                ip: "127.0.0.1",
                channelNum: "8",
                frequency: "250",
            },
        }
    },
    methods:{
        async startSession() {
            let command = "~4";
            if(this.msg.frequency == "250") {
                command = "~4"
            }else if(this.msg.frequency == "500"){
                command = "~5"
            }else if(this.msg.frequency == "500"){
                command = "~6"
            }
            this.$emit('startSession',this.msg)
        },
        cancel() {
        
        }
    }
}
</script>