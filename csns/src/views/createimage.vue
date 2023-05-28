<template>
    <div class="create-image">
        <div class="black-block"></div>
    </div>
</template>
<script>
export default {
    
}
</script>
<style>
    .create-image {
        background-color: gray;
        position: fixed;
        z-index: 100;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }

    .black-block {
        width: 900px;
        height: 400px;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: black;
    }
</style>