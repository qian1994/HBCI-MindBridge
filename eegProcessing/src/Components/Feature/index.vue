<template>
    <div class="feature-widgets">
        <h2> 特征提取 </h2>
        <el-form ref="form" :model="feature" label-width="80px" size="mini" >
            <el-form-item size="large">
                <el-checkbox-group v-model="feature.checkList" >
                    <el-checkbox label="characteristicWave" value="characteristicWave">提取特征波段</el-checkbox>
                    <el-checkbox label="spatialPattern" value="spatialPattern">共空间模式</el-checkbox>
                    <el-checkbox label="psd" value="psd">PSD特征</el-checkbox>
                    <el-checkbox label="DE" value="DE">差分熵特征</el-checkbox>
                    <el-checkbox label="statistic" value="statistic">统计特征</el-checkbox>
                    <el-checkbox label="PLV" value="PLV">锁相值特征</el-checkbox>
                </el-checkbox-group>
            </el-form-item>
            <el-form-item label="特征波">
                <div v-for="item, index in feature.characteristicWave" class="processing-slice" >
                    <el-col :span="24">
                        <el-col :span="6">
                            <span>low： </span><el-input v-model="item[0]"> </el-input>
                        </el-col>
                        <el-col :span="2">
                        </el-col>
                        <el-col :span="6">
                            <span>hige: </span><el-input v-model="item[1]"> </el-input>
                        </el-col>
                        <el-col :span="2">
                            <el-button @click="removeCharacteristicWave(index)">X</el-button>
                        </el-col>
                    </el-col>
                </div>
            </el-form-item>
            <el-form-item >
                <el-button @click="addCharacteristicWave">添加 +</el-button> 
            </el-form-item>
        </el-form>
    </div>
</template>
<script>
export default {
    data() {
        return {
            feature: {
                checkList: [],
                characteristicWave: [[1, 45]]
            },
        }
    },
    watch:{
        feature:{
            handler: 'handlefeatureChange',
            deep: true
        }
        
    },
    methods: {
        handlefeatureChange(newVal, oldVal) {
            const clonedObj = JSON.parse(JSON.stringify(newVal));
            clonedObj.characteristicWave = clonedObj.characteristicWave.map(item => {
                return [parseFloat(item[0]), parseFloat(item[1])]
            })
            this.$emit('saveFeatureData',clonedObj)
        },
        addCharacteristicWave() {
            this.feature.characteristicWave.push([1, 45])
        },
        removeCharacteristicWave(index) {
            this.feature.characteristicWave = this.feature.characteristicWave.filter((item, id) => index != id )
        }
    }
}
</script>
