const config = [{
    name: 'timeserise',
    show: true,
    channels: [1,2,3,4,5,6,7,8],
    timelength: 1,
}, {
    name: 'fft',
    show: true,
    channels: [1,2,3,4,5,6,7,8],
    max: 10,
    model: "log"  
},{
    name: "specctrogram",
    show: true,
    channels: [1,2,3,4,5,6,7,8],
    max: 100,
    model: "log"
}, {
    name: "networking",
    show: true
}, {
    name: "headplot",
    show: true
}]