<template>
    <div class="pannels-widgets">
        <h2>请选择注意力训练模式</h2>
        <el-row>
            <el-col v-for="item in games" :span="12">
                <div class="grid-content bg-purple">
                    <el-button @click="toAttentionTrain(item['name'])">{{ item.label }}</el-button>
                </div>
            </el-col>
        </el-row>
    </div>
</template>
<script>
export default {
    data() {
        return {

        }
    },
    computed: {
        games() {
            const games = [
                '注意力广度训练',
                '注意力集中性训练',
                '注意力稳定性训练',
                '注意力与大脑抑制功能训练',
                '注意力与反应速度训练',
                '注意力与记忆力训练',
                '注意力与观察力训练',
                '注意力与动作控制训练',
                '注意力与手眼协调训练',
                '脑力训练',

            ]
            const paths = [
                '/span-train',
                '/concentration-train',
                '/stable-train',
                '/inhibition-train',
                '/reaction-train',
                '/memory-train',
                '/JigsawPuzzle-train',
            ]
            const name = [
                'SpanTrain',
                'concentrationTrain',
                'stable',
                'inhibition',
                'reaction',
                'memory'
            ]
            return games.map((item, index) => {
                return {
                    label: item,
                    name: name[index] || '',
                    path: paths[index] || ''
                }
            })
        }
    },
    components: {
    },
    methods: {
        toAttentionTrain(path) {
            if(path == '') {
                this.$message('该功能暂时未开启')
                return
            }
            console.log(path)
            this.$router.push({ name: path, params: {...this.$router.currentRoute.params}})
        }
    }
}
</script>
<style>
.pannels-widgets {
    width: 600px;
    margin: 50px auto;
    background-color: white;
    padding: 30px;
}

.grid-content {
    padding: 5px 0;
}

.pannels-widgets .el-button {
    width: 250px;
}
</style>