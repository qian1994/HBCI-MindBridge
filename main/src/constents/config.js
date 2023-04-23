const config = {
    "timeSerise": {
        name: "timeSerise",
        title: "采集参数设置",
        id: 1,
        desc: "实时脑电数据分析",
        config: ["open"],
        icon: require('../assets/eeg-data.png')
    }, 
    "ssvep": {
        name: "SSVEP",
        title: "SSVEP",
        id: 2,
        desc: "ssvep 字符拼写器刺激模块",
        config: ["update", "open"],
        icon: require('../assets/eeg-ssvep.png')

    }, 
    "p300": {
        name: "p300",
        title: "p300",
        id: 3,
        desc: "",
        config: ["open"],
        icon: require('../assets/eeg-p300.png')

    }, 
    "mi": {
        name: 'MI',
        title: "MI",
        id: 4,
        desc: "MI 刺激范式",
        config: ["open"],
        icon: require('../assets/eeg-mi.png')
    },
    'custom': {
        name: "custom",
        title: "自定义",
        id: 5,
        dest: "上次自定义范式，或者打开范式连接",
        config: ["open"],
        icon: require('../assets/coustom1.png')
    }
}

export default config