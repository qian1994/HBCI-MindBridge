import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './plugins/element.js';
// import {Chart} from '@antv/g2';
new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');