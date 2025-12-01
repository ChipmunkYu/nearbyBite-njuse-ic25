<template>
  <div class="fun-homepage">
    <!-- 背景动画 -->
    <div class="background-animation">
      <div class="floating-text" v-for="(text, index) in floatingTexts" :key="index" :style="getTextStyle(index)">
        {{ text }}
      </div>
      <div class="floating-food" v-for="(food, index) in floatingFoods" :key="'food-' + index" 
           :style="getFoodStyle(index)">
        {{ food }}
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="main-content">
      <!-- 标题区域 -->
      <div class="title-section">
        <h1 class="main-title">
          <span class="title-word" v-for="(word, index) in titleWords" :key="index" 
                :style="{ animationDelay: `${index * 0.1}s` }">
            {{ word }}
          </span>
        </h1>
        <p class="subtitle">一个困扰全人类的世纪难题...</p>
      </div>

      <!-- 痛点展示区 -->
      <div class="pain-points">
        <div class="pain-card" v-for="(point, index) in painPoints" :key="index"
             :style="{ animationDelay: `${0.5 + index * 0.2}s` }">
          <div class="pain-emoji">{{ point.emoji }}</div>
          <h3>{{ point.title }}</h3>
          <p>{{ point.description }}</p>
        </div>
      </div>

      <!-- 解决方案CTA -->
      <div class="solution-section">
        <div class="solution-card">
          <div class="solution-icon">🎯</div>
          <h2>别再纠结了！</h2>
          <p class="solution-text">让我们用魔法（算法）帮你解决这个难题</p>
          
          <div class="cta-buttons">
            <button class="cta-primary" @click="showSolution">
              🎲 立即解决选择困难症
            </button>
            <button class="cta-secondary" @click="scrollToFeatures">
              ℹ️ 了解更多
            </button>
          </div>
        </div>
      </div>

      <!-- 功能特性（滚动后显示） -->
      <div class="features-section" ref="featuresSection">
        <h2>How it works?</h2>
        <div class="features-grid">
          <div class="feature-item" v-for="(feature, index) in features" :key="index">
            <div class="feature-step">{{ feature.step }}</div>
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>

        <!-- 最终行动号召 -->
        <div class="final-cta">
          <h2>Ready to end the struggle?</h2>
          <p>加入 thousands of 已经告别选择困难症的用户</p>
          <div class="final-buttons">
            <button class="final-btn primary" @click="goToRegister">
              🚀 立即开始美食之旅
            </button>
            <button class="final-btn secondary" @click="goToLogin">
              🔑 已有账号？直接登录
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部 -->
    <footer class="footer">
      <p>© 2025 What-to-eat-today · 告别选择困难，从今天开始</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const featuresSection = ref(null)

// 浮动文字内容
const floatingTexts = [
  '吃什么？', '好纠结...', '随便吧', '都行', '不知道', '选择困难', '头疼', '饿但不知道吃什么',
  '火锅？', '烤肉？', '日料？', '中餐？', '西餐？', '快餐？', '自己做？', '点外卖？'
]

// 浮动食物emoji
const floatingFoods = ['🍕', '🍣', '🍔', '🥗', '🍜', '🌮', '🍛', '🥘', '🍝', '🍲']

// 标题文字
const titleWords = ['选', '择', '困', '难', '症', '？', '我', '们', '懂', '！']

// 痛点列表
const painPoints = [
  {
    emoji: '😫',
    title: '菜单翻来覆去',
    description: '刷了半小时外卖APP，还是不知道点什么'
  },
  {
    emoji: '🤔',
    title: '朋友互相推诿',
    description: '"随便"、"都行"成了最让人头疼的答案'
  },
  {
    emoji: '⏰',
    title: '时间白白浪费',
    description: '每天花在决定吃什么上的时间累积起来很惊人'
  },
 /* {
    emoji: '😵',
    title: '决策疲劳',
    description: '工作已经够累了，不想再为吃饭做决定'
  }*/
]

// 功能特性
const features = [
  {
    step: '01',
    icon: '🎲',
    title: '一键随机',
    description: '点击按钮，系统智能推荐今日美食，告别纠结'
  },
  {
    step: '02',
    icon: '🏪',
    title: '海量选择',
    description: '覆盖周边所有餐厅，从快餐到高级料理应有尽有'
  },
  {
    step: '03',
    icon: '⭐',
    title: '个性化推荐',
    description: '基于您的口味偏好，推荐更合适的美食'
  }
  /*{
    step: '04',
    icon: '❤️',
    title: '收藏管理',
    description: '标记喜欢的餐厅，建立个人美食地图'
  }*/
]

// 获取浮动文字样式
const getTextStyle = (index) => {
  const left = Math.random() * 90 + 5
  const animationDelay = Math.random() * 10
  const duration = 15 + Math.random() * 10
  return {
    left: `${left}%`,
    animationDelay: `${animationDelay}s`,
    animationDuration: `${duration}s`
  }
}

// 获取浮动食物样式
const getFoodStyle = (index) => {
  const left = Math.random() * 85 + 5
  const animationDelay = Math.random() * 8
  const duration = 20 + Math.random() * 15
  const size = 24 + Math.random() * 24
  return {
    left: `${left}%`,
    animationDelay: `${animationDelay}s`,
    animationDuration: `${duration}s`,
    fontSize: `${size}px`
  }
}

// 显示解决方案
const showSolution = () => {
  // 可以添加一些动画效果
  scrollToFeatures()
}

// 滚动到特性区域
const scrollToFeatures = () => {
  featuresSection.value?.scrollIntoView({ behavior: 'smooth' })
}

// 跳转到注册
const goToRegister = () => {
  router.push('/register')
}

// 跳转到登录
const goToLogin = () => {
  router.push('/login')
}

// 鼠标移动效果
const handleMouseMove = (e) => {
  const cards = document.querySelectorAll('.pain-card')
  cards.forEach(card => {
    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    card.style.setProperty('--mouse-x', `${x}px`)
    card.style.setProperty('--mouse-y', `${y}px`)
  })
}

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
})
</script>

<style scoped>
.fun-homepage {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.background-animation {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.floating-text {
  position: absolute;
  color: rgba(255, 255, 255, 0.3);
  font-size: 18px;
  font-weight: bold;
  animation: floatUp 15s linear infinite;
  white-space: nowrap;
}

.floating-food {
  position: absolute;
  opacity: 0.4;
  animation: floatFood 20s linear infinite;
}

@keyframes floatUp {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.3;
  }
  90% {
    opacity: 0.3;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes floatFood {
  0% {
    transform: translateY(100vh) translateX(0px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.4;
  }
  90% {
    opacity: 0.4;
  }
  100% {
    transform: translateY(-100px) translateX(100px) rotate(360deg);
    opacity: 0;
  }
}

.main-content {
  position: relative;
  z-index: 2;
  padding: 80px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* 标题区域 */
.title-section {
  text-align: center;
  margin-bottom: 80px;
}

.main-title {
  font-size: 4rem;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}

.title-word {
  display: inline-block;
  animation: bounceIn 0.6s ease both;
}

.subtitle {
  font-size: 1.5rem;
  opacity: 0.8;
  animation: fadeInUp 1s ease 1s both;
}

@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 0.8;
    transform: translateY(0);
  }
}

/* 痛点展示 */
.pain-points {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 80px;
}

.pain-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 40px 30px;
  border-radius: 20px;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  animation: slideInUp 0.8s ease both;
  position: relative;
  overflow: hidden;
}

.pain-card::before {
  content: '';
  position: absolute;
  top: var(--mouse-y, 50%);
  left: var(--mouse-x, 50%);
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  opacity: 0;
  transition: opacity 0.3s;
}

.pain-card:hover::before {
  opacity: 1;
}

.pain-emoji {
  font-size: 3rem;
  margin-bottom: 20px;
}

.pain-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.pain-card p {
  opacity: 0.8;
  line-height: 1.6;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 解决方案 */
.solution-section {
  display: flex;
  justify-content: center;
  margin-bottom: 100px;
}

.solution-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(15px);
  padding: 60px 40px;
  border-radius: 30px;
  text-align: center;
  border: 2px solid rgba(255, 255, 255, 0.3);
  max-width: 600px;
  width: 100%;
}

.solution-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.solution-card h2 {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.solution-text {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 40px;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-primary, .cta-secondary, .final-btn {
  padding: 18px 32px;
  font-size: 1.1rem;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.cta-primary, .final-btn.primary {
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  color: white;
}

.cta-primary:hover, .final-btn.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 107, 107, 0.4);
}

.cta-secondary, .final-btn.secondary {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.5);
}

.cta-secondary:hover, .final-btn.secondary:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: translateY(-2px);
}

/* 功能特性 */
.features-section {
  padding: 100px 0;
}

.features-section h2 {
  text-align: center;
  font-size: 3rem;
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  margin-bottom: 80px;
}

.feature-item {
  text-align: center;
  padding: 40px 20px;
}

.feature-step {
  font-size: 0.9rem;
  opacity: 0.7;
  margin-bottom: 15px;
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-item h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.feature-item p {
  opacity: 0.8;
  line-height: 1.6;
}

/* 最终CTA */
.final-cta {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 60px 40px;
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.final-cta h2 {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.final-cta p {
  font-size: 1.2rem;
  opacity: 0.8;
  margin-bottom: 40px;
}

.final-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 底部 */
.footer {
  text-align: center;
  padding: 40px 20px;
  opacity: 0.7;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-title {
    font-size: 2.5rem;
  }
  
  .pain-points {
    grid-template-columns: 1fr;
  }
  
  .cta-buttons, .final-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .cta-primary, .cta-secondary, .final-btn {
    width: 100%;
    max-width: 300px;
  }
}
</style>