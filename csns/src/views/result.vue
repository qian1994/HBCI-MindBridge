<template>
    <div class="get-ssvep-result">
        <div class="qi">
            <span>结果文件：</span>
            <el-button @click="fileChoose"> 选择文件</el-button>
            <span class="choose-current-edf-file">{{ currentEDFFile.split('/')[currentEDFFile.split('/').length - 1]
            }}</span>
        </div>
        <div v-if="currentEDFFile">
            <HeadPlot :show-info="showChannels" :radius="radius" @point-click="chooseElectron"></HeadPlot>
        </div>
        <div class="ssvep-res-scroe">
           <span>{{currentLabel}} </span> <span  v-for="score in zscore">{{score[0]}} : {{score[1]}}</span>
        </div>
        <div class="chart">
            <div class="main"></div>
        </div>
    </div>
</template>
<script>
import * as echarts from 'echarts'
import HeadPlot from '../Components/HeadPlot/electrodePositions.vue'
import { getResultInfoByFileName, openFileDialog } from '../api/index'
export default {
    data() {
        this.myChart = ''
        return {
            radius: 450,
            resultInfo: [],
            currentEDFFile: '',
            zscore: [],
            currentLabel: ''
        }
    },
    components: {
        HeadPlot
    },
    computed: {
        showChannels() {
            const channels = {}
            for (let key in this.resultInfo) {
                let color = '#ccc'
                const item = this.resultInfo[key]
                if (item['base'] > 0) {
                    color = 'red'
                }
                if (item['odd'] >= 2) {
                    color = 'blue'
                }
                if (item['base'] > 0 && item['odd'] >= 2) {
                    color = 'purple'
                }
                channels[key] = {
                    label: key.replace(' ', ''),
                    show: 'result',
                    color: color
                }
            }
            return channels
        }
    },
    async mounted() {
        this.myChart = echarts.init(document.querySelector('.main'));
    },
    methods: {
        async fileChoose() {
            const res = await openFileDialog()
            if (res.indexOf('.json') < 0) {
                this.$message('请选择json文件');
                return true
            }
            this.currentEDFFile = res
            this.getResultInfoByFileName()
        },
        async getResultInfoByFileName() {
            const res = await getResultInfoByFileName({ fileName: this.currentEDFFile })
            this.resultInfo = res
        },
        chooseElectron(point) {
            let data = this.resultInfo[point['label']]
            this.currentLabel = point['label']
            this.zscore = data['zScore']
            let xindex = data['freq-index']
            let show = data['patsnr'].map((item, index) => {
                return [data['freq'][index], data['patsnr'][index]]
            })
            let markerLine = xindex.map(item => {
                return {
                    name: 'markLine',
                    xAxis: item,
                    label: {
                        value: data['freq'][item]
                    }
                }
            })
            let option = {
                // 配置 x 轴
                xAxis: {
                    type: 'category',
                    data: data['freq'],
                    axisLabel: {
                        interval: 0,
                        formatter: function (value, index) {
                            if (xindex.indexOf(index) >= 0) {
                                return data['freq'][index].toFixed(1)
                            }
                        }
                    },
                },
                // 配置 y 轴
                yAxis: {
                    type: 'value'
                },
                // 配置数据系列
                series: [{
                    symbol: 'none',
                    data: data['patsnr'],
                    type: 'line', // 数据系列类型为折线图
                    markLine: {
                        symbol: 'none',
                        lineStyle: {
                            color: '#FF0000'
                        },
                        data:markerLine
                    }
                }, {

                }]
            };
            // 使用 setOption 方法设置图表选项
            this.myChart.setOption(option);
        }
    }

}
</script>
<style>

.choose-current-edf-file {
    display: inline-block;
    margin-left: 30px;
}
.get-ssvep-result {
    max-width: 900px;
    background: white;
    margin: 5px auto;
    min-height: 500px;
    padding: 30px;
    box-sizing: border-box;
}

.get-ssvep-result .main {
    width: 800;
    height: 500px;
}

.ssvep-res-scroe {
    text-align: center;
    margin: 20px auto;
    padding: 10px 0;
    border-top: 1px solid #ddd;
}

.ssvep-res-scroe span{
    display: inline-block;
    margin: 10px 30px;
    font-size: 14px;
}
</style>