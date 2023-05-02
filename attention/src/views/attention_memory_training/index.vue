<template>
	<div class="attention_memory_training">
		<div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span> <span>总共： {{ 1 }}</span>
			<span>剩余：</span> <span>错误次数: {{ currentTrainResult.errorNumber
			}}</span>
		</div>
		<div class="attention_concentration-config" v-if="!start">
			<el-form :model="formData" ref="ruleForm" label-width="100px" class="demo-ruleForm">
				<el-form-item label="难度级别" prop="name">
					<el-input v-model="formData.level"></el-input>
				</el-form-item>
				<el-form-item label="次数" prop="count">
					<el-input v-model="formData.count"></el-input>
				</el-form-item>
				<el-form-item>
					<el-button size="large" @click="submit"> 开始 </el-button>
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
	</div>
</template>
<script>
import CardComponent from './CardComponent.vue'

export default {
	/* TODO:  #32 Implement a 2D dimencional array to place the card on the grid  */
	components: { CardComponent },
	data() {
		return {
			cards: [
				{
					name: "react",
					front: require("./img/react.svg"),
				},
				{
					name: "ember",
					front: require("./img/ember.svg"),
				},
				{
					name: "vue",
					front: require("./img/vue.svg"),
				},
				{
					name: "node",
					front: require("./img/node.svg"),
				},
				{
					name: "svelte",
					front: require("./img/svelte.svg"),
				},
				{
					name: "angular",
					front: require("./img/angular.svg"),
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
		const cards = document.querySelectorAll('.memory-card')

		cards.forEach((card) => {
			const randomPos = Math.floor(Math.random() * cards.length)
			card.style.order = randomPos
		})

		cards.forEach((card) => card.addEventListener('click', this.flipCard))
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
			this.start = true
			setTimeout(() => {
				const cards = document.querySelectorAll('.memory-card')
				cards.forEach((card) => {
					const randomPos = Math.floor(Math.random() * cards.length)
					card.style.order = randomPos
				})

				cards.forEach((card) => card.addEventListener('click', this.flipCard))
			}, 100);
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
</style>