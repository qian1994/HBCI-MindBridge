<template>
    <div class="res-container">
        <div class="res-container-form-container">
            <el-col :span="24">
                <el-form class="res-select-form" ref="form" label-width="120px">
                    <div class="divider"> 预处理参数 </div>
                    <el-col :span="24">
                        <el-form-item label="实验文件">
                            <!-- <el-select v-model="form.fileId" filterable placeholder="请选择文件" @change="getImageByFileName">
                                        <el-option v-for="item in resultFiles" :label="item.id" :value="item.name"></el-option>
                                    </el-select> -->
                            <el-button @click="fileChoose"> 选择文件</el-button>
                            <span class="choose-current-edf-file">{{currentEDFFile.split('/')[currentEDFFile.split('/').length -1]}}</span>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="基线时长">
                            <el-input v-model="form.baseLineTime" placeholder="请选择计算信噪比的前后值"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="刺激前时长">
                            <el-input v-model="form.startTrialTime" placeholder="请选择计算信噪比的前后值"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="刺激时长">
                            <el-input v-model="form.endTrialTime" placeholder="请选择计算信噪比的前后值"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="重参考">
                            <el-select v-model="form.rereference" filterable placeholder="请选择是否使用重参考">
                                <el-option label="是" value="1"></el-option>
                                <el-option label="否" value="0"></el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="24">
                        <el-form-item label="带通滤波">
                            <el-col :span="10">
                                <el-input v-model="form.filterlow" placeholder="带通滤波最小值"></el-input>
                            </el-col>
                            <el-col :span="2">
                                <div class="split-line-filter">---</div>
                            </el-col>
                            <el-col :span="10">
                                <el-input v-model="form.filterHigh" placeholder="带通滤波最大值"></el-input>
                            </el-col>

                        </el-form-item>
                    </el-col>
                    <el-col :span="24">
                        <div class="divider"> 频谱分析参数 </div>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="刺激时长">
                            <el-input v-model="form.paradigmTime" placeholder="请输入需要计算信噪比的值"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="频率范围">
                            <el-select v-model="maxFrequency" placeholder="请选择最大频率范围">
                                <el-option v-for="item in maxFrequencySelect" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="基础频率">
                            <el-select v-model="form.baseFrequency" placeholder="请选择">
                                <el-option v-for="item in options" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="奇异频率">
                            <el-select v-model="form.frequency" multiple placeholder="请选择">
                                <el-option v-for="item in options" :key="item.value" :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="24">
                        <div class="divider"> Z分数计算 </div>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="Z分数计算的窗口时间点 (整数)">
                            <el-input v-model="form.number" placeholder="请选择计算信噪比的前后值"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="显著的Z分数值">
                            <el-input v-model="form.ZScore" placeholder="请选择计算信噪比的前后值"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="24" v-if="this.trials.length">
                        <el-form-item label="实验trial">
                            <el-button class="trial-button" v-for="item, index in trials"
                                :type="item == '1' ? 'primary' : 'info'" disabled @click="troggle(index)">trial {{
                                    index + 1
                                }}</el-button>
                        </el-form-item>
                    </el-col>
                    <el-col :span="24" v-if="this.trials.length">
                        <el-form-item label="选择trial">
                            <el-button class="trial-button" v-for="item, index in trials"
                                :type="selectTrial[index] == '1' ? 'primary' : ''" @click="troggle(index)">trial
                                {{ index + 1 }}</el-button>
                        </el-form-item>
                    </el-col>
                    
                    <el-col :span="24" v-show="currentEDFFile">
                        <el-form-item label="通道选择">
                            <div class="bad-channel-choose">
                                <div class="eeg-position">
                                    <ElectrodePositions :show-info="selectedChannel" :radius="radius"
                                        @point-click="pointClick">
                                        <div class="img" v-if="this.images.length">
                                            <img :src="selectedImg" alt="" srcset="">
                                        </div>
                                    </ElectrodePositions>
                                </div>
                            </div>
                        </el-form-item>
                    </el-col>
                    <el-col :span="24" v-show="currentEDFFile">
                        <div class="bad-channel-container">
                            <span>坏导：</span> <el-button  type="info" disabled v-for="channel in badChannel">{{channel}}</el-button>
                        </div>
                        <div  class="computed-channel-container">
                            <span>选择计算电极：</span> <el-button type="primary" v-for="channel in selectComputedChannel" @click="reomveSelectComputedChannel(channel)">{{channel}}</el-button>
                        </div>
                    </el-col>
                    <el-col :span="24">
                        <el-form-item>
                            <el-button class="create-image" type="primary" @click="showAnnaly">生成报告</el-button>
                            <!-- <el-button class="create-report" type="primary" @click="showReport">生成报告</el-button> -->
                        </el-form-item>
                    </el-col>
                </el-form>
            </el-col>
        </div>
    </div>
</template>
<script>
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'
import { getResultFiles, createExprimentSsvepResult, getChannelImageByFiles, initDevTools, getEEGElectronPosition, openFileDialog , getInfoByFileName} from '../api/index'
export default {
    data() {
        return {
            files: [],
            maxFrequency: 10,
            images: [],
            trials: [],
            text: "",
            currentEDFFile: '',
            activeNames: '1',
            form: {
                baseLineTime: 0.1,
                paradigmTime: 20,
                filterlow: 0,
                filterHigh: 100,
                startTrialTime: 0.5,
                endTrialTime: 20,
                fileId: 0,
                region: [],
                config: [],
                number: 10,
                ZScore: 1.64,
                baseFrequency: 6,
                frequency: [1.2, 2.4, 3.6, 4.8, 6, 7.2],
                filter: 100,
                rereference: "0",
            },
            selectComputedChannel: [],
            badChannel: [],
            selectTrial: '',
            radius: 400,
            info: ''
        }
    },
    components: {
        ElectrodePositions
    },
    computed: {
        
        resultFiles() {
            if (this.files.length == 0) {
                return []
            }
            return this.files.map((item, index) => {
                return {
                    id: item,
                    name: index
                }
            })
        },
        showImages() {
            return this.images.map((item, index) => {
                return {
                    value: item,
                    label: item.split('-')[item.split('-').length - 1].replace('.jpg', ''),
                    key: index
                }
            })
        },
        maxFrequencySelect() {
            const a = new Array(100).fill(0).map((item, index) => {
                return {
                    value: index + 1,
                    key: index + 1,
                    label: index + 1
                }
            })
            return a
        },
        options() {
            return new Array(this.maxFrequency * 10).fill(0).map((item, index) => {
                return {
                    value: ((index + 1) / 10).toFixed(1),
                    key: ((index + 1) / 10).toFixed(1),
                    label: ((index + 1) / 10).toFixed(1)
                }
            })
        },
        selectedChannel() {
            let channels = this.info.channels
            let info = {}
            if(!this.info || channels.length == 0) {
                return info
            }

            channels.forEach((item, index) => {
                item = item.replaceAll(' ', '')
                let color = ''
                if(this.badChannel.indexOf(item) == -1) {
                    if (this.selectComputedChannel.indexOf(item) >=0) {
                        color = ''
                    }else {
                        color = '#ddd'
                    }
                }
                info[item] = {
                    label: item,
                    show: 'switch',
                    color: color,
                    switch: this.badChannel.indexOf(item) >=0 ? false:  true
                }
            })
            return info
        }
    },
    methods: {
        reomveSelectComputedChannel(channel) {
            this.selectComputedChannel = this.selectComputedChannel.filter(item => item != channel)
        },
        showReport(data) {
        },
        pointClick(data) {
            if(this.badChannel.indexOf(data['label']) >= 0) {
                this.$message('坏导不可参与计算')
                return
            }
            if(this.selectComputedChannel.indexOf(data['label']) >= 0) {
                this.selectComputedChannel = this.selectComputedChannel.filter(item => item != data['label'])
            }else {
                this.selectComputedChannel.push(data['label'])
            }
        },
        troggle(index) {
            this.selectTrial = this.selectTrial.map((item, id) => {
                if (id == index) {
                    return Math.abs(parseInt(item) - 1)
                }
                return item
            })
        },
        async showAnnaly() {
            if (this.selectTrial.length <= 0) {
                this.$alert('', "请选择要分析的trial， 至少一个", {
                    confirmButtonText: '确定',
                });
                return
            }
            const data = { ...this.form, fileName: this.currentEDFFile, selectComputedChannel: this.selectComputedChannel, rereference: parseInt(this.form.rereference), selectTrial: this.selectTrial }
            const res = await createExprimentSsvepResult(data)
            if (res == 'ok') {
                this.$alert('', "成功生成报告", {
                    confirmButtonText: '确定',
                });
               
            } else {
                this.$alert('', "参数错误，请输入正确参数", {
                    confirmButtonText: '确定',
                });
            }
        },
     
        async getInfoByFileName() {
            const res = await getInfoByFileName({fileName: this.currentEDFFile})
            if(res) {
                this.info = res
                this.trials = res.trial[0]
                this.selectTrial = res.trial[0]
                this.badChannel = res.badChannel.map(item => item.replaceAll(' ', ''))
                this.selectComputedChannel = this.info['channels'].map(item => item.replaceAll(' ', '')).filter(item => this.badChannel.indexOf(item) == -1).filter(item => item != 'marker')
            }
        },
        async fileChoose() {
            const res = await openFileDialog()
            if (res.indexOf('.mat') < 0) {
                this.$message('请选择mat文件');
                return true
            }
            this.currentEDFFile = res
            this.getInfoByFileName()
        }
    },
    async mounted() {
        
    }
};
</script>
  
<style>
.res-container {
    padding: 30px;
    box-sizing: border-box;
    max-width: 900px;
    background: white;
    margin: 0 auto;
    overflow: hidden;
}

.res-container .eeg-position {
    position: relative;
}

.img {
    margin: 30px auto;
    width: 600px;
    display: block;
}

.res-container img {
    width: 100%;
}

.res-container-no-data {
    margin: 30px;
    text-align: center;
    font-size: 20px;
    color: gray;
}

.res-container .trial-button {
    margin-bottom: 10px;
    margin-left: 0px;
    margin-right: 10px;
}

.res-container .create-image,
.res-container .create-report {
    margin: 10px;
    width: 200px;
    transform: translatex(-120px);
}

.res-container-form-container {
    overflow: hidden;
}

.split-line {
    width: 90%;
    height: 1px;
    background: #ddd;
    margin-bottom: 20px;
}

.res-container .el-select {
    width: 100%;
}

.res-container .el-input__inner {
    background-color: #F5F7FA;
    height: 30px;
    font-size: 12px;
    line-height: 30px;
}

.res-container .el-input__inner {
    line-height: 30px;
    height: 30px;
}

.res-container .el-form-item__content {
    line-height: 30px;
}

.res-container .el-form-item {
    margin-bottom: 16px;
}

.res-container .channel-select {
    width: 70%;
    margin-left: 30px;
}

.res-container .el-input__icon {
    line-height: 30px;
}

.res-container .channel-radio {
    margin-top: 8px;
    width: 60px;
}

.split-line-filter {
    text-align: center;
}

.divider {
    position: relative;
    text-align: center;
    line-height: 1;
    margin-bottom: 20px;
    font-size: 14px;
    font-weight: bold;
}

.divider::before,
.divider::after {
    content: "";
    position: absolute;
    top: 50%;
    width: 43%;
    height: 1px;
    background-color: #ddd;
}

.divider::before {
    left: 0;
}

.divider::after {
    right: 0;
}

.choose-current-edf-file {
    margin-left: 30px;
}

.bad-channel-container .el-button, .computed-channel-container .el-button {
    margin-bottom: 10px;
    margin-right: 10px;
}
</style>
  