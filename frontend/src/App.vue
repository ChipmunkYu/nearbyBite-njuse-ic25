<template>
  <div id="app">

    <router-view>
    
    </router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<!-- 解决顶部留白问题， 固定格式 -->
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
}

<style>
  #app {
  font-family: Arial, sans-serif;
  text-align: center;
  }
</style>