<template>
  <div class="empty-state">
    <img v-if="image" :src="image" alt="空状态" class="empty-image"/>
    <p class="empty-text">{{ text }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  text: { type: String, default: '暂无数据' },
  image: { type: String, default: '' }
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #999;
  font-size: 16px;
}
.empty-image {
  width: 120px;
  height: 120px;
  margin-bottom: 16px;
}
.empty-text {
  text-align: center;
}
</style>
