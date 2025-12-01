<template>
  <div class="feedback-container">

    <div class="background">
      <div class="floating-icon">💬</div>
      <div class="floating-icon">📧</div>
      <div class="floating-icon">✨</div>
    </div>

    <div class="feedback-card">
      <h1 class="title">💬 联系开发团队</h1>
      <p class="subtitle">如果你在使用过程中遇到问题，欢迎通过以下邮箱联系我们。</p>

      <div class="email-list">
        <div 
          v-for="(item, index) in emails" 
          :key="index" 
          class="email-item"
        >
          <div class="role-tag">{{ item.role }}</div>

          <div class="email-box">
            <span class="email-text">{{ item.address }}</span>
            <el-button type="primary" round class="copy-btn" @click="copy(item.address)">
              复制
            </el-button>
          </div>
        </div>
      </div>

      <p class="footer-tip">我们会尽快回复你，谢谢你的支持！💗</p>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";

const emails = ref([
  { role: "开发人员A", address: "1287513193@qq.com" },
  { role: "开发人员B", address: "backend@example.com" },
  { role: "开发人员C", address: "pm@example.com" },
  { role: "开发人员D", address: ""}
]);

function copy(text) {
  navigator.clipboard.writeText(text);
  ElMessage.success("已复制：" + text);
}
</script>

<style scoped>
/* --- 外层容器背景 --- */
.feedback-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #ffe3e3, #fff4e6, #e8f7ff);
  background-size: 300% 300%;
  animation: bgMove 8s ease infinite;
  position: relative;
  overflow: hidden;
  padding: 40px;
}

@keyframes bgMove {
  0% { background-position: 0% 50%; }
  100% { background-position: 100% 50%; }
}

/* --- 浮动背景图标 --- */
.background {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.floating-icon {
  position: absolute;
  font-size: 48px;
  opacity: 0.22;
  animation: float 6s ease-in-out infinite;
}

.floating-icon:nth-child(1) { top: 10%; left: 20%; }
.floating-icon:nth-child(2) { top: 50%; right: 18%; animation-delay: 2s; }
.floating-icon:nth-child(3) { bottom: 15%; left: 10%; animation-delay: 4s; }

@keyframes float {
  0%,100% { transform: translateY(0px); }
  50% { transform: translateY(-16px); }
}

/* --- 主卡片 --- */
.feedback-card {
  z-index: 2;
  background: white;
  padding: 50px 60px;
  width: 850px;
  max-width: 95%;
  border-radius: 28px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.10);
  text-align: center;
  position: relative;
}

/* 顶部亮条 */
.feedback-card::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 6px;
  background: linear-gradient(90deg, #ff6b6b, #ffa726, #ff6b6b);
  background-size: 200% 100%;
  animation: shine 4s linear infinite;
}

@keyframes shine {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* --- 标题 --- */
.title {
  font-size: 34px;
  font-weight: 800;
  color: #ff6b6b;
  margin-bottom: 12px;
}

.subtitle {
  font-size: 17px;
  color: #666;
  margin-bottom: 35px;
}

/* --- 邮箱列表 --- */
.email-list {
  display: flex;
  flex-direction: column;
  gap: 28px;
  margin-bottom: 25px;
}

.email-item {
  display: flex;
  align-items: center;
  gap: 20px;
}

/* 岗位标签 */
.role-tag {
  min-width: 140px;
  text-align: center;
  padding: 12px 18px;
  background: linear-gradient(135deg, #ffdede, #ffe8cc);
  border-radius: 16px;
  font-weight: 700;
  color: #d35454;
  font-size: 16px;
}

/* 邮箱显示区域 */
.email-box {
  flex: 1;
  background: #f9f9f9;
  padding: 16px 24px;
  border-radius: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.email-text {
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

/* 复制按钮 */
.copy-btn {
  padding: 10px 22px;
  font-size: 15px;
  border-radius: 20px;
}

/* 底部提示 */
.footer-tip {
  margin-top: 20px;
  font-size: 14px;
  color: #888;
}
</style>
