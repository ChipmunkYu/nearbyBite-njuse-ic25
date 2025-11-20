<template>
  <div class="back-btn" @click="goHome">
    <svg viewBox="0 0 24 24" width="22" height="22">
      <path d="M15 18l-6-6 6-6" stroke="#444" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
</template>

<script setup>
import router from '@/router'
const goHome = () => router.push('/')
</script>

<style scoped>
.back-btn {
  position: fixed;
  top: 20px;
  left: 20px;
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(6px);
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 0.25s ease;
  z-index: 9999;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.9);
  transform: translateX(-3px); /* 轻微滑动效果 */
}
</style>
