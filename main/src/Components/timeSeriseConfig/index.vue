<template>
    <div class="timeSerise-config">
        <div class="timeSerise-config-form">
            <div>
                <el-button v-if="!entered" type="primary" @click="opentimeSerise">查看实时数据</el-button>
                <el-button type="success" @click="home">返回首页</el-button>
            </div>
        </div>
    </div>
</template>
<script>
import { openTimeSeriseWindow, homePage, getConfigFromServe, postSelectChannel, initDevTools, getCurrentBoardData } from '../../api/index'
export default {
    name: 'time-serise-config',
    data() {
        return {
            activeNames: 'hahah',
            activeIndex: '0',
            railed: [],
            timeSerise: [],
            show: true,
            selectChannels: [],
            timmer: null,
            products: [],
            channels: [],
            entered: false,
            filterShow: false
        }
    },
    destroyed() {
        if (this.timmer) {
            clearInterval(this.timmer)
        }
    },
    async mounted() {
       
    },
    methods: {
        async opentimeSerise() {
            if (this.form.ip == '') {
                this.$alert('', "请输入ip", {
                    confirmButtonText: '确定',
                });
                return
            }
            const data = await openTimeSeriseWindow(this.form)
            if (data == 'ok') {
                setTimeout(() => {
                    this.showAllToggle()
                }, 1000);
            }
        },
        async home() {
            this.$router.back()
        },
    }
};
</script>
    
<style>
.timeSerise-config-content {
    margin-left: 30px;
}

.el-table .el-table__cell {
    padding: 3px 0;
}

.timeSerise-config-result {
    display: flex;
}

.timeSerise-config {
    padding: 30px 0;
    box-sizing: border-box;
}

.timeSerise-config-form {
    padding: 0 20px;
}

.timeSerise-config-pass {
    margin-bottom: 30px;
}

.timeSerise-config img {
    width: 500px;
}

.timeSerise-config .channels-container {
    width: 700px;
    padding: 20px 0;
    box-sizing: border-box;
}


.timeSerise-config .channels-container .el-button {
    margin: 10px;
}

.timeSerise-config .time-fregament {
    overflow: hidden;
}

.timeSerise-config .time-fregament-first .el-select {
    margin: 10px;
    margin-left: 30px;
}

.timeSerise-config .channels-container .el-form-item__label {
    height: 50px;
    line-height: 60px;
    font-size: 18px;
    font-weight: 900;
}

.timeSerise-config .time-fregament-second {
    margin-left: 64px;
}

.timeSerise-config .time-filter-split {
    text-align: center;
}

.timeSerise-config .time-fregament-first .el-button {
    width: 100%;
}

.timeSerise-config .time-fregament-col-6.el-col-6 {
    width: 31%;
}

.timeSerise-config .el-col-5 .el-select {
    margin: 0;
    margin-left: 10px;
}
</style>
    