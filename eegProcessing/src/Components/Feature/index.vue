<template>
    <div class="feature-widgets">
        <h2 class="feature-widget"> Extra feature </h2>
        <el-form ref="form" :model="feature" label-width="80px" size="mini">
            <div class="features">
                <el-form-item size="large">
                    <el-checkbox-group v-model="feature.checkList">
                        <el-checkbox label="statistic" value="statistic" class="feature"
                            style="margin-left: -70px;">Statistic</el-checkbox>
                        <el-checkbox label="psd" value="psd" class="feature">PSD</el-checkbox>
                        <el-checkbox label="DE" value="DE" class="feature">DE</el-checkbox>
                        <el-checkbox label="spatialPattern" value="spatialPattern" class="feature">Spatial Pattern</el-checkbox>
                        <el-checkbox label="characteristicWave" value="characteristicWave"
                            class="feature"> Feature band</el-checkbox>
                        <el-checkbox disabled label="PLV" value="PLV" class="feature">PLV</el-checkbox>
                    </el-checkbox-group>
                </el-form-item>
            </div>

            

        </el-form>
        <div>
            <div class="characteristic_waves">
                <label for="特征波" style=" width:130px; display: inline-block;">Band</label>
                <div v-for="item, index in feature.characteristicWave" class="feature-slice"
                    style="margin-top: 15px;">
                    <label for="low: "
                        style="width:160px; display: inline-block;">low：</label><el-input
                        v-model="item[0]" style="width: 100px;height: 40px;display: inline-block;">
                    </el-input>
                    <label for="high: "
                        style="width:160px; display: inline-block;margin-left: 70px;">high：</label><el-input
                        v-model="item[1]" style="width: 100px;height: 40px;display: inline-block;;">
                    </el-input>
                    <div style="float: right;margin-right: 40px;">
                        <el-button @click="addCharacteristicWave"
                            style="background: #2868C9;color: white;width: 90px;height: 40px;border-radius: 4px;">Add
                            +</el-button>
                        <el-button @click="removeCharacteristicWave(index)"
                            style="background: #FA5151;color: white;width: 90px;height: 40px;border-radius: 4px;">Remove</el-button>
                    </div>
                </div>
            </div>

        </div>
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
    watch: {
        feature: {
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
            this.$emit('saveFeatureData', clonedObj)
        },
        addCharacteristicWave() {
            this.feature.characteristicWave.push([1, 45])
        },
        removeCharacteristicWave(index) {
            this.feature.characteristicWave = this.feature.characteristicWave.filter((item, id) => index != id)
        }
    }
}
</script>

<style>
.feature-widget {
    margin-top: 10px;
    flex: 1;
    font-weight: bold;
    font-size: 15px;
    color: #3D3D3D;
}

.features {
    width: 840px;
    height: 20px;
    color: #3D3D3D;
    margin: auto;
    padding: 10px 0px 30px 0px;
    background-color: #F2F7FC;
    margin-top: 6px;
    padding-left: -30px;
    border-radius: 4px;
    margin: 10px 0px;
}

.feature {
    color: #000000;
    margin-top: 10px;
    height: 22px;
    width: 110px;
    font-size: 14px;
    line-height: 10px;
}

.characteristic_waves {
    height: 70px;
    margin-top: 10px;
}</style>