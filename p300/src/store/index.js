import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    timeSerise: [],
    fft: []
  },
  mutations: {
    changeTimeSerise: (state, params) => {
    },
    changeFFT: (fft) => {
    }
  },
  actions: {
    changeTimeSerise: (root, timeSerise) => {
     
    },
    changeFFT: (root, fft) => {
    }
  },
  modules: {
  }
})
