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
      const array = root.state.timeSerise;
      root.state.timeSerise = array.concat(timeSerise)
    },
    changeFFT: (root, fft) => {
      const array = root.state.fft;
      root.state.fft = array.concat(fft)
    }
  },
  modules: {
  }
})
