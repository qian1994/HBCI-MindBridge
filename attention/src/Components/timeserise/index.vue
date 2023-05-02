<template>
  <div>
    {{ title }}
    <div>
      <div class="line-chart"></div>
      <!-- <div id="Linechart">
        <svg :width="width" height="400">
          <g>
            <g
              class="lines"
              clip-path="url(#clip)"
              v-for="(item, index) in lineData"
              :key="index"
            >
              <g>
                <path
                  class="data"
                  :d="item"
                  :style="`stroke: ${
                    colors[index % 8]
                  }; stroke-width: 1; fill: none`"
                ></path>
              </g>
            </g>
          </g>
        </svg>
      </div> -->
    </div>
  </div>
</template>
<script>
import colors from "../../constents/color";
import dagreD3 from "dagre-d3";
import * as d3 from "d3";
import { mapState } from "vuex";
export default {
  name: "TimeSerise",
  data() {
    return {
      g: null,
      gW: 0,
      gH: 0,
      width: 300,
      height: 500,
      title: "TIMESERISE",
      width: window.innerWidth / 2 - 20,
    };
  },  
  mounted() {

  },
  computed: {
    lineData() {},
    timeSerise() {
      const data = [];
      for (let j = 0; j < 8; j++) {
        const array = [];
        for (let i = 0; i < 1000; i++) {
          array.push(Math.random() * 185000);
        }
        data.push(array);
      }
      console.log(data);
      return data;
    },
    colors() {
      return colors;
    },
  },
};
</script>