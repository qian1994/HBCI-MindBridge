<template>
    <div class="eeg-plugins" @click="open(info.name)">
        <div class="icon">
            <img :src="info && info.icon" alt="">
        </div>
        <div class="right">
            <div class="name">
                <span class="name-word">{{ info && info.title }} </span>
            </div>
            <div class="desc" v-if="info && info.id > 1"><span>{{ info.desc }}</span></div>
            <div class="mask" v-if="showMask"></div>
        </div>
    </div>
</template>
<script>
import { openHtml, initTestBoard, startSession } from '../../api'
export default {
    props: {
        info: {},
        form: {}
    },
    data() {
        return {
            show: false,
            count: 0,
            showMask: false
        }
    },
    mounted() {
        console.log('info', this.info)
    },
    methods: {
        update(name) {
            console.log('this is update button', name)
        },
        async open(name) {
            if (name == 'report') {
                const data = await openHtml(name)
                return
            }
            if (this.count >= 3) {
                this.$alert('', "请确认wifi连接正常，wifi名为Mindbrige", {
                    confirmButtonText: '确定',
                });
                return
            }
            if (!this.form || !this.form.productId || !this.form.ip) {
                this.$alert('', "请选择产品型号，并且请输入ip", {
                    confirmButtonText: '确定',
                });
                return
            }
            this.loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)',
                target: document.documentElement
            });
            this.$nextTick(async () => {
                try {
                    
                    if (name == 'custom') {
                        this.$router.push({ 'name': "Custom", params: {...this.form} })
                        return
                    }

                    if (name == 'processing') {
                        const data = await openHtml(name)
                        return
                    }
                    const res = await initTestBoard(this.form)
                    if (res == 'ok') {
                        localStorage.setItem('mindbridgeinfo', JSON.stringify(this.form))
                        this.loading.close()
                        if (name == 'timeSerise') {
                            startSession(this.form)
                            this.$router.push({ 'name': "TimeSerise" })
                            return
                        }
                        // if (name == 'impedence') {
                        //     this.$router.push({ 'name': "Custom" })
                        //     return
                        // }
                        const data = await openHtml(name)
                    } else {
                        this.loading.close()
                        this.$alert('', "请选择产品型号，并且请输入设备ip", {
                            confirmButtonText: '确定',
                        })
                        this.count += 1
                        return
                    }
                } catch (error) {
                    this.count += 1
                    this.loading.close()
                    this.$alert('', "请选择产品型号，并且请输入设备ip", {
                        confirmButtonText: '确定',
                    })
                    return
                }
                this.loading.close()
            });
        },
        get() {
            console.log('this is get button')
        },
        deleteBtn(name) {
            console.log("this is delete button", name)
        }
    }
}
</script>
<style>
.eeg-plugins {
    display: flex;
    align-items: center;
    height: 56px;
    padding: 0 20px;
    display: flex;
    justify-content: start;
    width: 200px;
    border-bottom: 1px solid #ddd;
    cursor: pointer;
    box-sizing: border-box;
    font-size: 14px;
}

.eeg-plugins .icon {
    margin-right: 8px;
}

.eeg-plugins .icon img {
    width: 18px;
    height: 18px;
}

.eeg-plugins .right {
    width: calc(100% - 22px);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.eeg-plugins .name {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: space-between;
}

.eeg-plugins .button {
    display: inline-block;
    color: white;
    cursor: pointer;
    font-size: 14px;

}


.eeg-plugins .button-update {
    float: left;
    background-color: white;
}

.eeg-plugins .button img {
    width: 16px;
    height: 16px;
}
</style>