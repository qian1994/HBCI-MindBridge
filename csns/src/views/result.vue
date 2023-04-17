<template>
    <div class="res-container">
        <el-collapse v-model="activeNames">
            <el-collapse-item title="生成图片" name="1">
                <div class="res-container-form-container">
                    <el-col :span="24">
                        <el-form class="res-select-form" ref="form" label-width="120px">
                            <el-col :span="12">
                                <el-form-item label="参数">
                                    <el-select v-model="form.fileId" filterable placeholder="请选择文件" @change="getImageByFileName">
                                        <el-option v-for="item in resultFiles" :label="item.id" :value="item.name"></el-option>
                                    </el-select>
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
                            <el-col :span="12">
                                <el-form-item label="计算分数">
                                    <el-input v-model="form.number" placeholder="请选择计算信噪比的前后值"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item label="打标前时间">
                                    <el-input v-model="form.startTrialTime" placeholder="请输入打标前时间"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
        
                                <el-form-item label="计算结束时间">
                                    <el-input v-model="form.endTrialTime" placeholder="请输入结束时间"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
        
                                <el-form-item label="滤波器">
                                    <el-input v-model="form.filter" placeholder="请选择低通滤波最大值"></el-input>
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
                                <el-form-item label="目标频率">
                                    <el-select v-model="form.frequency" multiple placeholder="请选择">
                                        <el-option v-for="item in options" :key="item.value" :label="item.label"
                                            :value="item.value">
                                        </el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="24">
                                <el-form-item label="实验trial">
                                    <el-button class="trial-button" v-for="item, index in trials"
                                        :type="item == '1' ? 'primary' : 'info'" disabled @click="troggle(index)">trial {{ index + 1
                                        }}</el-button>
                                </el-form-item>
                            </el-col>
                            <el-col :span="24">
                                <el-form-item label="选择trial">
                                    <el-button class="trial-button" v-for="item, index in trials"
                                        :type="selectTrial.split(',')[index] == '1' ? 'primary' : ''" @click="troggle(index)">trial
                                        {{ index + 1 }}</el-button>
                                </el-form-item>
                            </el-col>
                            <el-col :span="24">
                                <el-form-item>
                                    <el-button class="create-image" type="primary" @click="showAnnaly">生成图片</el-button>
                                </el-form-item>
                            </el-col>
                        </el-form>
                    </el-col>
                </div>
            </el-collapse-item>
            <el-collapse-item title="查看图片" name="2">
                <div>
                    <div class="eeg-position">
                        <ElectrodePositions :eeg-info="selectedChannel" :radius="radius" @point-click="pointClick"> 
                            <div class="img" v-if="this.images.length">
                                <img :src="selectedImg" alt="" srcset="">
                            </div>
                        </ElectrodePositions>
                    </div>
                    
                </div>
            </el-collapse-item>
          </el-collapse>
    </div>
</template>
<script>
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'
import { getResultFiles, drawExperimentImages, getChannelImageByFiles, initDevTools, getEEGElectronPosition } from '../api/index'
export default {
    data() {
        return {
            files: [],
            maxFrequency: 10,
            images: [],
            currentImage: '',
            trials: [],
            text: "",
            activeNames: '1',
            eegInfo: [],
            form: {
                startTrialTime: 0.5,
                endTrialTime: 20,
                fileId: 0,
                region: [],
                config: [],
                number: 10,
                frequency: [1.2, 2.4, 3.6, 4.8, 6, 7.2],
                filter: 100,
                rereference: "0",
            },
            selectTrial: '',
            radius: 400
        }
    },
    components: {
        ElectrodePositions
    },
    computed: {
        selectedImg() {
            return "file:///" + this.currentImage
        },
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
            let channels = this.showImages.map(item => item.label)
            console.log(this.eegInfo)
            if (!this.eegInfo || this.eegInfo.length == 0){
                return []
            }
            this.eegInfo[0] = this.eegInfo[0].map(item => {
                return item.toUpperCase()
            })
            let info = channels.map((item, index) => {
                const id = this.eegInfo[0].indexOf(item)
                let label = ''
                let x = ''
                let y = ''
                if (id >= 0) {
                    x = this.eegInfo[1][id]
                    y = this.eegInfo[2][id]
                    label = this.eegInfo[0][id]
                }
                const data = {
                    label: label,
                    show: 'label',
                    x: x,
                    y: y,
                    name: item,
                    value: 0,
                    impedence:  0
                }
                return data
            })
            console.log(info)
            return info
        }
    },
    methods: {
        pointClick(data) {
            this.showImages.forEach(item => {
                if (item.label == data['label']){
                    this.currentImage = item.value
                    console.log(this.currentImage, item.value, data['label'])
                }
            })
        },
        troggle(index) {
            this.selectTrial = this.selectTrial.split(',').map((item, id) => {
                if (id == index) {
                    return Math.abs(parseInt(item) - 1)
                }
                return item
            }).join(',')
        },
        async showAnnaly() {
            if (this.selectTrial.indexOf(1) < 0) {
                this.$alert('', "请选择要分析的trial， 至少一个", {
                    confirmButtonText: '确定',
                });
                return
            }
            const data = { ...this.form, fileName: this.files[this.form.fileId], rereference: parseInt(this.form.rereference), additional: this.selectTrial }
            const res = await drawExperimentImages(data)
            if (res == 'ok') {
                this.$alert('', "获取生成图片成功", {
                    confirmButtonText: '确定',
                });
                setTimeout(() => {
                    this.getImageByFileName()
                }, 1000);
            } else {
                this.$alert('', "参数错误，请输入正确参数", {
                    confirmButtonText: '确定',
                });
            }
        },
        async getImageByFileName() {
            const res = await getChannelImageByFiles(this.files[this.form.fileId])
            const info = res
            if (!info || !info.images || info.images.length == 0) {
                this.images = []
            } else {
                this.images = info.images.split(',')
            }
            if (info && info.trialInfo) {
                this.trials = info.trialInfo.replaceAll('"', '').split(',')
                this.selectTrial = info.trialInfo.replaceAll('"', '')
            }
        }
    },
    async mounted() {
        const data = await getResultFiles()
        this.files = data.split(',')
        this.getImageByFileName()
        const res = await getEEGElectronPosition()
        console.log(res)
        this.eegInfo = res
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

.res-container .create-image {
    margin: 10px;
    width: 400px;
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
</style>
  