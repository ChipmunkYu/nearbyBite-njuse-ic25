<!-- 初始页面 -->
<template>
  <div>
    <h1>首页</h1>
    <router-link to="/login">登录</router-link>
    <br> </br>
    <router-link to="/register">注册</router-link>
  </div>


  <el-button @click="simulateError">模拟 500 错误</el-button>




</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const simulateError = () => {
  router.push({
    name: 'NotFound',
    params: { code: 500, message: '服务器错误，请稍后重试' }
  })
}
</script>
