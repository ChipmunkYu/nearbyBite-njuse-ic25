<!-- 登录成功后的首页，用于页面跳转到其他页面 -->
<template>
  <div class="first-container">
    <div class="background">
      <div class="floating-food">🍕</div>
      <div class="floating-food">🍣</div>
      <div class="floating-food">🍔</div>
      <div class="floating-food">☕</div>
    </div>

    <div class="welcome-card">
      <h1>欢迎使用 <span class="highlight">What-to-eat-today!</span></h1>
      <p>您已成功登录。</p>

      <el-button type="primary" @click="goToRecommend" class="btn">
         去看看今天吃什么
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const goToRecommend = () => {
  router.push('/recommend')
}
</script>

<style scoped>
.first-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #f6d365 100%);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  position: relative;
  overflow: hidden;
  font-family: "Microsoft YaHei", sans-serif;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.background {
  position: absolute;
  inset: 0;
}

.floating-food {
  position: absolute;
  font-size: 36px;
  opacity: 0.25;
  animation: float 6s ease-in-out infinite;
}

.floating-food:nth-child(1) { top: 10%; left: 12%; animation-delay: 0s; }
.floating-food:nth-child(2) { top: 20%; right: 15%; animation-delay: 1.8s; }
.floating-food:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 3.2s; }
.floating-food:nth-child(4) { bottom: 10%; right: 8%; animation-delay: 4.6s; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

.welcome-card {
  text-align: center;
  background: rgba(255, 255, 255, 0.93);
  padding: 60px 120px;
  border-radius: 24px;
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
}

h1 {
  font-size: 32px;
  margin-bottom: 10px;
  color: #333;
}

.highlight {
  color: #ff6b6b;
  font-weight: 700;
}

p {
  color: #555;
  margin-bottom: 24px;
  font-size: 18px;
}

.btn {
  font-size: 18px;
  border-radius: 16px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
}
</style>
