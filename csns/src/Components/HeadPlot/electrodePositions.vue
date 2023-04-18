<template>
  <div class="electrode-positions">
    <div class="electrode-positions-head" :style="'min-height: ' + radius + 'px;' +'width:' + radius + 'px'">
      <div class="electrode-positions-head-cirle" :style="'width:' + radius +'px;'+'height:' + radius + 'px'">
        <div class="point-out" v-for="point in points" :style="point['position']" @click="pointClick(point)">
          <span class="point-out-color  point-out-color-label" v-if="point['show'] == 'label'">  {{  point['label']  }}</span>
          <span class="point-out-color" v-if="point['show'] == 'color'" :style="`background:#${(-point['value'] *(parseInt('ff0000', 16)- parseInt('00ff00', 16))+ parseInt('ff0000', 16)).toString(16)}` ">
            {{parseInt(100 - point.value)}} %
          </span>
          <span @click="chooseBadChannel(point['label'])" v-if="point['show'] == 'bad-channel'"  :class="'point-out-color'"> {{  point['label']  }}</span>
        </div>
      </div>
    </div>
    <slot></slot>
  </div>
</template>
<script>
export default {
  props:['eegInfo', 'radius', 'crosswise'],
  data() {
    return {
      line: 20,
      badChannel: []
    }
  },
  computed:{
    lines() {
      const array = []
      for(let i =0; i < this.line; i++) {
        array.push(i)
      }
      return array
    },
    points() {
      if(!this.eegInfo || this.eegInfo.length == 0){
        return []
      }
      const radius = this.radius/2
      return this.eegInfo.map((res) => {
        return {
          show: res.show,
          label: res.label,
          x: res.x * radius + radius,
          y: res.y * radius + radius,
          value: res.value || 0,
          impedence: res.impedence||0,
          position: `top:${res.x  * radius + radius}px;left:${res.y * radius+ radius}px`
        }
      })
    }
  },
  methods:{
    chooseBadChannel(currentChannel){
      console.log(currentChannel)
      
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
  