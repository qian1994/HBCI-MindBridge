<template>
  <div class="electrode-positions">
    <div class="electrode-positions-head" :style="'min-height: ' + radius + 'px;' + 'width:' + radius + 'px'">
      <div class="electrode-positions-head-cirle" :style="'width:' + radius + 'px;' + 'height:' + radius + 'px'">
        <div class="point-out" v-for="point in points" :style="point['position']" @click="pointClick(point)">
          <span class="point-out-color  point-out-color-label" v-if="point['show'] == 'label'"> {{ point['label']
          }}</span>
          <span class="point-out-color" v-if="point['show'] == 'color'"
            :style="`background:#${(-point['value'] * (parseInt('ff0000', 16) - parseInt('00ff00', 16)) + parseInt('ff0000', 16)).toString(16)}`">
            {{ parseInt(100 - point.value) }} %
          </span>
          <span :style="`background:${point['color']}`" @click="chooseBadChannel(point['label'])" v-if="point['show'] == 'result'"
            :class="'point-out-color'"> {{ point['label'] }}</span>
          <span :style="`background:${point.switch ? '#00ff00': '#ff0000'}`" @click="chooseBadChannel(point['label'])" v-if="point['show'] == 'switch'"
            :class="'point-out-color'"> {{ point['label'] }}</span>
        </div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>
<script>
import { getEEGElectronPosition } from '../../api/index'
export default {
  props: ['showInfo', 'radius', 'crosswise'],
  data() {
    return {
      line: 20,
      badChannel: [],
      eegInfo: []
    }
  },
  async mounted() {
    const res = await getEEGElectronPosition("1010")
    this.eegInfo = res
  },
  computed: {
    lines() {
      const array = []
      for (let i = 0; i < this.line; i++) {
        array.push(i)
      }
      return array
    },
    points() {
      if (!this.eegInfo || this.eegInfo.length == 0) {
        return []
      }
      if (!this.showInfo || this.showInfo.length == 0) {
        return []
      }
      const radius = this.radius / 2
      const showPoints = []
      this.eegInfo[0].forEach((item, index) => {
        item = item.toUpperCase()
        if (!this.showInfo[item.toUpperCase()]) {
          return
        }
        const res = [this.eegInfo[0][index], this.eegInfo[1][index], this.eegInfo[2][index]]
        showPoints.push({
          show: this.showInfo[item].show,
          label: this.showInfo[item].label,
          color: this.showInfo[item].color,
          switch: this.showInfo[item].switch,
          x: res[1] * radius + radius,
          y: res[2] * radius + radius,
          value: this.showInfo[item].value || 0,
          impedence: this.showInfo[item].impedence || 0,
          position: `top:${res[1] * radius + radius}px;left:${ res[2] * radius + radius}px`
        })
      })
      return showPoints
    }
  },
  methods: {
    chooseBadChannel(currentChannel) {
    },
    pointClick(data) {
      this.$emit('point-click', data)
    }
  }
}
</script>
  
<style>
.point-out {
  position: absolute;
  border: 1px solid #ddd;
  z-index: 100;
  width: 35px;
  height: 35px;
  color: white;
  font-size: 15px;
  border-radius: 100%;
  transform: translate(-50%, -50%)rotate(90deg);
  text-align: center;
  line-height: 35px;
  cursor: pointer;
  overflow: hidden;
}

.point-out-color {
  display: inline-block;
  width: 100%;
  height: 100%;

}

.point-out-color-label {
  color: black;
}

.electrode-positions {
  position: relative;
}

.electrode-positions-head {
  margin: 0 auto;
  position: relative;
  transform: rotateZ(-90deg);
}


.electrode-positions-head-cirle {
  margin: 0 auto;
  border: 1px solid black;
  border-radius: 100%;
  position: absolute;
  z-index: 100;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.circle-in {
  margin: 0 auto;
  border-radius: 100%;
  width: 575px;
  border: 1px solid black;
  height: 575px;
  position: absolute;
  z-index: 100;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.circle {
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: red;
  z-index: 100;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.line {
  width: 1px;
  height: 690px;
  position: absolute;
  background-color: red;
  z-index: 100;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  transform: rotateZ(60deg);
}
</style>
  