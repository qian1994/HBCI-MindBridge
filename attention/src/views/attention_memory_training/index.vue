<template>
	<div class="attention_memory_training">
		<h2>注意力与记忆训练</h2>
		<div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span> <span>总共： {{ 1 }}</span>
			<span>剩余：</span> <span>错误次数: {{ currentTrainResult.errorNumber
			}}</span>
		</div>
		<div class="attention_concentration-config" v-if="!start">
			<el-form :model="formData" ref="ruleForm" label-width="100px" class="demo-ruleForm">
				<el-form-item label="等级" prop="count">
                    <el-select v-model="formData.level" placeholder="请选择">
                        <el-option label="初级" value="1" key="1"> </el-option>
                        <el-option label="中级" value="2" key="2"> </el-option>
                        <el-option label="高级" value="3" key="3"> </el-option>
                    </el-select>
                </el-form-item>

                <el-form-item label="次数" prop="count">
                    <el-select v-model="formData.count" placeholder="请选择">
                        <el-option v-for="item, index in new Array(10).fill(0)" :label="index+1" :value="index+1" :key="'key' + index"> </el-option>
                    </el-select>
                </el-form-item>
				<el-form-item>
					<el-button size="large" @click="submit"> 开始 </el-button>
                    <el-button size="large" @click="$router.go(-1)"> 返回 </el-button>

				</el-form-item>
			</el-form>
		</div>
		<!-- Game container -->
		<section class="memory-game" v-if="start">
			<!-- 2 Set of Cards -->
			<card-component v-for="card in cards" :key="`${card.name}-1`" class="memory-card" :data-framework="card.name"
				:alt="card.name" :front="card.front" />
			<card-component v-for="card in cards" :key="`${card.name}-2`" class="memory-card" :data-framework="card.name"
				:alt="card.name" :front="card.front" />
			<!-- <card-component class="memory-card" :img-pwd="imgPwd" alt="angular" front="angular.svg" /> -->
			<!-- End 2 Set of Cards -->
		</section>

		<div class="attention_memory_training-count" v-if="timeCountShow">
			{{ count }}
		</div>
	</div>
</template>
<script>
import CardComponent from './CardComponent.vue'
import { savePationData } from '../../api/index'

export default {
	/* TODO:  #32 Implement a 2D dimencional array to place the card on the grid  */
	components: { CardComponent },
	data() {
		return {
			timeCountShow: false,
			count: 3,
			cards: [
				{
					name: "react",
					front: require("./img/cherry.png"),
				},
				{
					name: "ember",
					front: require("./img/banana.png"),
				},
				{
					name: "vue",
					front: require("./img/coconut.png"),
				},
				{
					name: "node",
					front: require("./img/grape.png"),
				},
				{
					name: "svelte",
					front: require("./img/mango.png"),
				},
				{
					name: "angular",
					front: require("./img/peach.png"),
				},
			],
			formData: {
				level: 1,
				count: 5
			},
			currentTrainResult: {
				errorNumber: 0,
				time: 0,
			},
			trainResultTotal: [],
			start: false,
			hasFlippedCard: false,
			lockBoard: false,
			firstCard: false,
			secondCard: false,
		}
	},
	mounted() {
	},
	computed: {
		timmerShow() {
			const time = parseInt(this.currentTrainResult.time / 1000) || 0
			const mSecond = this.currentTrainResult.time % 1000 || 0
			const minute = parseInt(time / 60)
			const second = time % 60 || 0
			return `${minute}:${second}:${mSecond}`
		}
	},
	methods: {
		submit() {
			setTimeout(() => {
				const cards = document.querySelectorAll('.memory-card')
				cards.forEach((card) => {
					const randomPos = Math.floor(Math.random() * cards.length)
					card.style.order = randomPos
				})
				cards.forEach((card) => card.addEventListener('click', this.flipCard))
			}, 100);
			this.timeCount()
			this.start = true
			this.timeCountShow = true
		},
		timerRuning() {
			const cards = document.querySelectorAll('.memory-card')
			cards.forEach((card) => card.addEventListener('click', this.flipCard))
			cards.forEach((card) => {
				card.classList.add('flip')
			})
			setTimeout(() => {
				cards.forEach((card) => {
					card.classList.remove('flip')
				})
			}, 1500);
			this.timmer = setInterval(() => {
				this.currentTrainResult.time += 100
			}, 100);
		},
		timeCount() {
			this.count = 3
			this.timeCountShow = true
			clearInterval(this.timmer)
			setTimeout(() => {
				clearInterval(this.timmer)
				this.timeCountShow = false
				this.timerRuning()
			}, 3000);

			this.timmer = setInterval(() => {
				this.count -= 1
			}, 1000);
		},
		flipCard(event) {
			if (this.lockBoard) {
				return
			}
			if (event.currentTarget === this.firstCard) {
				// Fixed Issue #38 : card remains flipped when card was double clicked both in React and Vue app
				return
			}

			event.currentTarget.classList.add('flip')

			if (!this.hasFlippedCard) {
				this.hasFlippedCard = true
				this.firstCard = event.currentTarget
				return
			}
			this.secondCard = event.currentTarget
			/* this.hasFlippedCard = false; */
			this.checkForMatch()
		},
		checkForMatch() {
			let isMatch = this.firstCard.dataset['framework'] === this.secondCard.dataset['framework']
			isMatch ? this.disableCards() : this.unflipCards()
			console.log('isMath', isMatch)
			if (!isMatch) {
				return
			}
			if (document.querySelectorAll('.memory-card').length != document.querySelectorAll('.flip').length) {
				console.log('asdfasdf this is memory-card not equal')
				return
			}

			this.trainResultTotal.push({
				pationId: this.$router.currentRoute.params.pationId,
				mode: 'memory',
				currentTime: +new Date(),
				level: this.formData.level,
				time: this.currentTrainResult.time / 1000,
				errorNumber: this.currentTrainResult.errorNumber
			})

			if(this.trainResultTotal.length >= this.formData.count) {
				this.endTotalTask()
			}

			this.restart()
		},

		async endTotalTask() {
			console.log('this is total task end')
			console.log(this.trainResultTotal)
			this.start = true
            const res = await savePationData(this.trainResultTotal)

		},
		restart() {
			clearInterval(this.timmer)
			setTimeout(() => {
				const cards = document.querySelectorAll('.memory-card')
				cards.forEach((card) => {
					const randomPos = Math.floor(Math.random() * cards.length)
					card.style.order = randomPos
					card.classList.remove('flip')
				})
				cards.forEach((card) => card.addEventListener('click', this.flipCard))
			}, 100);
			this.currentTrainResult = {
				time: '',
				errorNumber: ''
			}
			this.hasFlippedCard = false
			this.lockBoard = false
			this.firstCard = false
			this.secondCard = false
			this.timeCount()
		},
		disableCards() {
			this.firstCard.removeEventListener('click', this.flipCard)
			this.secondCard.removeEventListener('click', this.flipCard)
			this.resetBoard()
		},
		unflipCards() {
			this.lockBoard = true
			setTimeout(() => {
				this.firstCard.classList.remove('flip')
				this.secondCard.classList.remove('flip')
				this.resetBoard()
			}, 1500)
			this.currentTrainResult.errorNumber += 1
		},
		resetBoard() {
			this.hasFlippedCard = this.lockBoard = false
			this.firstCard = this.secondCard = false
		},
	},
}
</script>


<style>
.attention_memory_training {
	max-width: 800px;
	margin: 5px auto;
	background: white;
	padding: 30px;
	box-sizing: border-box;
}

.memory-game {
	width: 640px;
	height: 640px;
	margin: auto;
	display: flex;
	flex-wrap: wrap;
	perspective: 1000px;
}

.memory-card {
	width: calc(25% - 10px);
	height: calc(33.333% - 10px);
	margin: 5px;
	position: relative;
	box-shadow: 1px 1px 1px rgba(0, 0, 0, 0.3);
	transform: scale(1);
	transform-style: preserve-3d;
	transition: transform 0.5s;
}

.memory-card:active {
	transform: scale(0.97);
	transition: transform 0.2s;
}

.front-face,
.back-face {
	width: 100%;
	height: 100%;
	padding: 20px;
	position: absolute;
	border-radius: 5px;
	background-color: #527089;
	backface-visibility: hidden;
	box-sizing: border-box;
}

.front-face {
	transform: rotateY(180deg);
}

.memory-card.flip {
	transform: rotateY(180deg);
}

.attention_memory_training-count {
	position: fixed;
	z-index: 100;
	width: 100%;
	height: 100%;
	background: rgba(0, 0, 0, 0.2);
	text-align: center;
	top: 0;
	left: 0;
	color: red;
	line-height: 500px;
	font-size: 100px;
}
</style>