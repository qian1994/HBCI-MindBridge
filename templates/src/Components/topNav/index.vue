<template>
  <div class="top-nav">
    <div class="start-session" v-if="connectSession">
      <el-popover
        placement="bottom"
        title="请选择不同的模式"
        width="300"
        trigger="click"
      >
        <ModelPanel @startSession="_startSession" />
        <el-button slot="reference">选择硬件</el-button>
      </el-popover>
    </div>
    <div class="stop-session " v-else>
        <el-button type="danger" slot="reference" @click="_stopSession">结束试验</el-button>
    </div>
  </div>
</template>
<script>
import ModelPanel from "../modelPanel/index.vue";
import { startSession, stopSession } from "../../api";
export default {
  name: "TopNav",
  props: ["connectSession"],
  data() {
    return {
      type: "primary",
      message: "模式选择",
      streamJson: "",
    };
  },
  components: {
    ModelPanel,
  },
  mounted() {},
  methods: {
    _startSession(msg) {
      startSession(msg)
        .then((Response) => {
          this.type = "danger";
          this.message = "退出";
          this.$router.push("/pannels");
        })
        .catch((error) => {
          alert(error);
          console.error(error);
        });
    },
    receive(msg) {
      let time = this.dateToString(new Date());
      this.msg.receiveMsg += `[${time}] QT: ${msg}\n`;
    },
    _stopSession() {
      stopSession(meg)
        .then((Response) => {
          this.$router.goback(1);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
