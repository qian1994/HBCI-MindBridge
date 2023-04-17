<template>
    <div class="container">
      <div class="p300-predict">
        <span v-for="(item, index) in show_word_array"
          :class="{ 'p300-predict-word': true, 'p300-predict-word--active': correct_index[index] }"> {{ item }}</span>
      </div>
      <div class="p300-content">
        <div v-for="(item, index) in word"
          :class="['p300-item', selected_index.includes(index) ? 'p300-item--selected' : '']">
          {{ item }}
          <span v-if="(index == selected_character)" class="p300-item--character"></span>
        </div>
        <div class="p300-footer">
          <el-button type="success" @click="start_p300_handler">开始</el-button>
          <el-button type="danger" @click="stop_p300_handler">结束</el-button>
          <el-button type="parimy" @click="back()"> 返回 </el-button>
        </div>
      </div>
    </div>
  </template>
  <script>
  import {  trigger,  endTotalTask, getP300DectectionResult } from "../api/index";
  export default {
    data() {
      return {
        word: [],
        current_index: 100,
        trial_index: 1,
        flash_array: [],
        flash_index: 0,
        predict_word: [],
        show_word_array: [],
        round_index: 0,
        type: 0,
        dectectModel: ''
      }
    },
    computed: {
      correct_index() {
        const data = this.show_word_array.map((item, index) => {
          if (item == this.predict_word[index]) {
            return true
          }
          return false
        })
        return data
      },
      selected_index() {
        if (this.current_index <= 6) {
          return new Array(6).fill(0).map((item, index) => {
            return (this.current_index - 1) * 6 + index
          })
        }
        return new Array(6).fill(0).map((item, index) => {
          return this.current_index - 7 + index * 6
        })
      },
      selected_character() {
        return this.word.indexOf(this.show_word_array[this.trial_index - 1])
      }
    },
    created() {
      this.show_word_array = this.$router.history.current.params.words
      this.word = this.$router.history.current.params.character
      this.dectectModel = this.$router.history.current.params.dectectModel
      this.type = this.$router.history.current.params.type
      this.productId = this.$router.history.current.params.productId
      this.model = this.$router.history.current.params.model
    },
    destroyed() {
      document.querySelector('.header').style.display = 'block'

    },
    methods: {
      back() {
        this.$router.back()
      },
      start_p300_handler() {
        this.flash()
      },
      async stop_p300_handler() {
        clearTimeout(this.timmer1)
        clearTimeout(this.timmer2)
        const res = await endTotalTask()
        if (res == 'ok'){
          this.$router.push({ name: "PationInfo", params:{words: this.show_word_array, productId: this.productId, model: this.model } })
        }
      },
      async new_around_flash() {
        let array = new Array(12).fill(0).map((item, index) => index + 1)
        this.flash_array = this.shuffle(array)
       
      },
      flash() {
        if (this.trial_index > this.show_word_array.length) {
          this.stop_p300_handler();
          return
        }
        this.current_index = this.flash_array[this.flash_index]
        this.flash_index += 1
        if (this.round_index >= 10) {
          this.round_index = 0
          this.new_around_flash()
          this.flash_index = 0
          this.trial_index += 1
          this.current_index = 1000
          // 进行p300 检测，延迟检测
          setTimeout(async () => {
            if(this.type == '1') {
              const res = await getP300DectectionResult(this.dectectModel)
              this.predict_word.push(res)
            }
          }, 1600);

          setTimeout(() => {
            this.flash()
          }, 2000);
          return
        }
        this.timmer2 = setTimeout(() => {
          if (this.flash_index >= this.flash_array.length) {
            this.round_index += 1
            this.flash_index = 0
            this.current_index = 1000
            this.new_around_flash()
            setTimeout(() => {
              this.flash()
            }, 1000);
            return
          }
          this.current_index = 1000
          this.timmer1 = setTimeout(() => {
            this.flash()
          }, 100);
        }, 120);
        trigger(this.trial_index*100+ this.current_index)
      },
      shuffle(arr) {
        var length = arr.length,
          randomIndex,
          temp;
        while (length) {
          randomIndex = Math.floor(Math.random() * (length--));
          temp = arr[randomIndex];
          arr[randomIndex] = arr[length];
          arr[length] = temp
        }
        return arr;
      }
    },
    mounted() {
      document.querySelector('.header').style.display = 'none'
      this.new_around_flash()
    }
  };
  </script>
  <style>
  .container {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    position: relative;
  }
  
  .p300-predict {
    text-align: center;
    position: absolute;
    left: 0;
    top: 20px;
    width: 100%;
    z-index: 10;
  }
  
  .p300-predict-word {
    display: inline-block;
    color: white;
    font-size: 18px;
    margin: 0 5px;
    opacity: 0.3;
  }
  
  .p300-predict-word--active {
    opacity: 1;
  }
  
  .p300-content {
    width: 100%;
    height: 100%;
    background-color: black;
    position: relative;
  }
  
  .p300-item {
    width: calc(100% / 6);
    height: calc(100% /7);
    padding: 20px;
    background-color: black;
    display: inline-block;
    color: white;
    text-align: center;
    vertical-align: center;
    font-size: 50px;
    box-sizing: border-box;
    padding-top: 30px;
    border: 5px solid black;
    position: relative;
  }
  
  .p300-item--selected {
    background-color: white;
    color: orange;
  }
  
  .p300-item--character {
    display: inline-block;
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: yellow;
    width: 20px;
    height: 20px;
    border-radius: 100%;
  }
  
  .p300-footer {
    position: absolute;
    width: 100%;
    height: 50px;
    bottom: 20px;
    left: 0;
    text-align: center;
  }
  
  .p300-footer button {
    width: 200px;
    font-size: 18px;
    margin: 0 10%;
  }
  </style>