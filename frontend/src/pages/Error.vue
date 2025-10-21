<!-- 错误页面 -->
<template>
  <div class="error-container">
    <div class="error-background">
      <div class="floating-food">🍕</div>
      <div class="floating-food">🍣</div>
      <div class="floating-food">🍔</div>
      <div class="floating-food">☕</div>
    </div>
    <div class="error-card">
      <div class="error-icon">⚠️</div>
      <h1>{{ code }}</h1>
      <p>{{ message }}</p>
      <el-button type="primary" @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  code: { type: Number, default: 404 },
  message: { type: String, default: '抱歉，页面未找到' }
})

const router = useRouter()
const goHome = () => router.push('/')
</script>

<style scoped>
.error-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #f6d365 100%);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  overflow: hidden;
  position: relative;
}

@keyframes gradientShift {
  0%,100% { background-position:0% 50% }
  50% { background-position:100% 50% }
}

.error-background {
  position: absolute;
  inset: 0;
}

.floating-food {
  position: absolute;
  font-size: 36px;
  opacity: 0.25;
  animation: float 6s ease-in-out infinite;
}

.floating-food:nth-child(1) { top: 8%; left: 12%; animation-delay: 0s; }
.floating-food:nth-child(2) { top: 18%; right: 15%; animation-delay: 1.8s; }
.floating-food:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 3.2s; }
.floating-food:nth-child(4) { bottom: 10%; right: 8%; animation-delay: 4.6s; }

@keyframes float {
  0%,100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

.error-card {
  text-align: center;
  background: rgba(255,255,255,0.93);
  padding: 48px 200px;
  border-radius: 24px;
  backdrop-filter: blur(12px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  position: relative;
  z-index: 2;
}

.error-icon { font-size: 64px; margin-bottom: 16px; color: #ff6b6b; }
.error-card h1 { font-size: 48px; font-weight: 700; margin-bottom: 12px; color: #ff6b6b; }
.error-card p { font-size: 18px; color: #666; margin-bottom: 24px; }
</style>
