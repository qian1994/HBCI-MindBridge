<template>
  <div class="memory-card">
    <img class="front-face" draggable="false" :src="front" :alt="`${alt}`"/>
    <img class="back-face" draggable="false" :src="require(`./img/js-badge.svg`)" alt="memory-card"/>
  </div>
</template>
<script>
export default {
  name: 'CardComponent',
  props: {
    imgPwd: "",
    front: "",
    alt: "",
  }
}
</script>