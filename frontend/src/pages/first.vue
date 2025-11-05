<!-- 这部分我后期再调整一下，现在出一个大致的模板 -->
<template>
  <div class="dashboard-container">
    <div class="background">
      <div class="floating-food">🍕</div>
      <div class="floating-food">🍣</div>
      <div class="floating-food">🍔</div>
      <div class="floating-food">☕</div>
    </div>

    <div class="dashboard-layout">
      <!-- 左侧边栏 -->
      <aside class="sidebar">
        <div class="user-profile">
          <el-avatar :size="80" :src="userStore.user?.avatar" class="user-avatar">
            {{ userStore.user?.username?.charAt(0) }}
          </el-avatar>
          <h2 class="username">{{ userStore.user?.username }}</h2>
          <p class="user-level">美食探索者</p>
        </div>

        <nav class="side-nav">
          <div class="nav-item active">
            <div class="nav-icon">🏠</div>
            <span>首页</span>
          </div>
          <div class="nav-item" @click="goToRecommend">
            <div class="nav-icon">🎲</div>
            <span>随机推荐</span>
          </div>
          <div class="nav-item" @click="goToRestaurants">
            <div class="nav-icon">🏪</div>
            <span>所有餐馆</span>
          </div>
          <div class="nav-item" @click="goToHistory">
            <div class="nav-icon">📚</div>
            <span>历史记录</span>
          </div>
          <div class="nav-item" @click="goToFavorites">
            <div class="nav-icon">❤️</div>
            <span>我的收藏</span>
          </div>
        </nav>

        <div class="quick-stats-side">
          <h3>本周数据</h3>
          <div class="stat-side">
            <div class="stat-side-item">
              <span class="stat-side-label">推荐次数</span>
              <span class="stat-side-value">5</span>
            </div>
            <div class="stat-side-item">
              <span class="stat-side-label">尝试新菜</span>
              <span class="stat-side-value">3</span>
            </div>
            <div class="stat-side-item">
              <span class="stat-side-label">收藏</span>
              <span class="stat-side-value">2</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- 主内容区 -->
      <main class="main-content">
        <!-- 欢迎区域 -->
        <div class="welcome-section">
          <h1>{{ timeGreeting }}！<span class="highlight">{{ userStore.user?.username }}</span></h1>
          <p class="subtitle">今天想吃什么？让我们帮您决定吧！</p>
        </div>

        <!-- 主要功能卡片 -->
        <div class="main-features">
          <div class="feature-main-card" @click="goToRecommend">
            <div class="feature-content">
              <div class="feature-icon-large">🎲</div>
              <div class="feature-text">
                <h3>随机推荐今日美食</h3>
                <p>点击开始，系统将为您智能推荐适合今天的美食</p>
                <div class="feature-tags">
                  <span class="tag">智能算法</span>
                  <span class="tag">个性化</span>
                  <span class="tag">一键获取</span>
                </div>
              </div>
              <div class="action-button">
                <el-button type="primary" size="large">立即开始</el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 功能网格 -->
        <div class="features-grid">
          <div class="feature-card" @click="goToRestaurants">
            <div class="card-header">
              <div class="card-icon">🏪</div>
              <h4>所有餐馆</h4>
            </div>
            <p>浏览完整的餐厅列表，按分类、评分、距离筛选</p>
            <div class="card-meta">
              <span class="meta-item">156家餐厅</span>
              <span class="meta-item">12个分类</span>
            </div>
          </div>

          <div class="feature-card" @click="goToHistory">
            <div class="card-header">
              <div class="card-icon">📚</div>
              <h4>历史记录</h4>
            </div>
            <p>查看您过往的美食选择记录和评价</p>
            <div class="card-meta">
              <span class="meta-item">28条记录</span>
              <span class="meta-item">4.2分均分</span>
            </div>
          </div>

          <div class="feature-card" @click="goToFavorites">
            <div class="card-header">
              <div class="card-icon">❤️</div>
              <h4>我的收藏</h4>
            </div>
            <p>管理您喜欢的美食和餐厅收藏</p>
            <div class="card-meta">
              <span class="meta-item">15个收藏</span>
              <span class="meta-item">3个分类</span>
            </div>
          </div>

          <div class="feature-card" @click="goToSettings">
            <div class="card-header">
              <div class="card-icon">⚙️</div>
              <h4>个人设置</h4>
            </div>
            <p>个性化您的饮食偏好和账户设置</p>
            <div class="card-meta">
              <span class="meta-item">5个偏好</span>
              <span class="meta-item">3种忌口</span>
            </div>
          </div>
        </div>

        <!-- 今日推荐 -->
        <div class="today-section">
          <div class="section-header">
            <h2>今日热门推荐</h2>
            <span class="see-all">查看全部</span>
          </div>
          <div class="recommendations">
            <div class="recommend-card">
              <div class="food-emoji">🍜</div>
              <div class="food-info">
                <h5>兰州拉面</h5>
                <p>评分：4.8 · 距离：1.2km</p>
              </div>
            </div>
            <div class="recommend-card">
              <div class="food-emoji">🍣</div>
              <div class="food-info">
                <h5>日式寿司</h5>
                <p>评分：4.6 · 距离：0.8km</p>
              </div>
            </div>
            <div class="recommend-card">
              <div class="food-emoji">🥗</div>
              <div class="food-info">
                <h5>健康沙拉</h5>
                <p>评分：4.5 · 距离：1.5km</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <!-- 右侧边栏 -->
      <aside class="right-sidebar">
        <div class="stats-card">
          <h3>数据统计</h3>
          <div class="stats-content">
            <div class="stat-item-large">
              <div class="stat-number">{{ stats.recommendCount }}</div>
              <div class="stat-label">总推荐次数</div>
            </div>
            <div class="stat-item-large">
              <div class="stat-number">{{ stats.favoriteCount }}</div>
              <div class="stat-label">收藏美食</div>
            </div>
            <div class="stat-item-large">
              <div class="stat-number">{{ stats.daysUsed }}</div>
              <div class="stat-label">使用天数</div>
            </div>
          </div>
        </div>

        <div class="daily-tip-card">
          <div class="tip-header">
            <el-icon><InfoFilled /></el-icon>
            <span>今日小贴士</span>
          </div>
          <p class="tip-content">{{ dailyTip }}</p>
        </div>

        <div class="quick-actions-card">
          <h3>快捷操作</h3>
          <div class="quick-buttons">
            <el-button @click="giveFeedback" class="quick-btn">
              💬 反馈建议
            </el-button>
            <el-button @click="goToHelp" class="quick-btn">
              ❓ 使用帮助
            </el-button>
            <el-button @click="logout" class="quick-btn logout-btn">
              🚪 退出登录
            </el-button>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

const stats = ref({
  recommendCount: 0,
  favoriteCount: 0,
  daysUsed: 1
})

const dailyTips = [
  '尝试一些新的菜系，发现不一样的美味！',
  '均衡饮食，记得多吃蔬菜水果哦～',
  '今天可以尝试自己动手做一顿美食',
  '别忘了多喝水，保持身体水分平衡',
  '分享美食，快乐加倍！'
]

const dailyTip = ref('')

const timeGreeting = computed(() => {
  const hour = new Date().getHours()
  if (hour >= 5 && hour < 12) return '早上好'
  else if (hour >= 12 && hour < 14) return '中午好'
  else if (hour >= 14 && hour < 18) return '下午好'
  else return '晚上好'
})

// 各种跳转函数
const goToRecommend = () => router.push('/recommend')
const goToRestaurants = () => ElMessage.info('所有餐馆功能开发中...')
const goToHistory = () => ElMessage.info('历史记录功能开发中...')
const goToFavorites = () => ElMessage.info('收藏功能开发中...')
const goToSettings = () => ElMessage.info('设置功能开发中...')
const goToHelp = () => ElMessage.info('帮助文档开发中...')
const giveFeedback = () => ElMessage.info('感谢您的反馈！')

const logout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  } catch {}
}

onMounted(() => {
  dailyTip.value = dailyTips[Math.floor(Math.random() * dailyTips.length)]
  setTimeout(() => {
    stats.value = { recommendCount: 12, favoriteCount: 8, daysUsed: 7 }
  }, 500)
})
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #f6d365 100%);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  padding: 20px;
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 40px);
}

/* 左侧边栏样式 */
.sidebar {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px 20px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.user-profile {
  text-align: center;
  margin-bottom: 30px;
}

.user-avatar {
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  color: white;
  font-weight: bold;
  margin: 0 auto 15px;
}

.username {
  font-size: 18px;
  margin-bottom: 5px;
  color: #333;
}

.user-level {
  color: #ff6b6b;
  font-size: 14px;
  margin: 0;
}

.side-nav {
  margin-bottom: 30px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 8px;
}

.nav-item:hover {
  background: rgba(255, 107, 107, 0.1);
}

.nav-item.active {
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  color: white;
}

.nav-icon {
  font-size: 20px;
}

.quick-stats-side h3 {
  margin-bottom: 15px;
  color: #333;
  font-size: 16px;
}

.stat-side-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 107, 107, 0.1);
}

.stat-side-label {
  color: #666;
  font-size: 14px;
}

.stat-side-value {
  color: #ff6b6b;
  font-weight: bold;
}

/* 主内容区样式 */
.main-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.welcome-section h1 {
  font-size: 32px;
  margin-bottom: 8px;
  color: #333;
}

.highlight {
  color: #ff6b6b;
}

.subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
}

.feature-main-card {
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  color: white;
  padding: 30px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.feature-main-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
}

.feature-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.feature-icon-large {
  font-size: 60px;
}

.feature-text h3 {
  font-size: 24px;
  margin-bottom: 8px;
}

.feature-text p {
  opacity: 0.9;
  margin-bottom: 12px;
}

.feature-tags {
  display: flex;
  gap: 8px;
}

.tag {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  backdrop-filter: blur(10px);
}

.action-button {
  margin-left: auto;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.8);
  padding: 24px;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-3px);
  border-color: #ff6b6b;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.card-icon {
  font-size: 24px;
}

.feature-card h4 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.feature-card p {
  color: #666;
  margin-bottom: 15px;
  font-size: 14px;
}

.card-meta {
  display: flex;
  gap: 15px;
}

.meta-item {
  background: rgba(255, 107, 107, 0.1);
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  color: #ff6b6b;
}

.today-section {
  background: rgba(255, 255, 255, 0.8);
  padding: 24px;
  border-radius: 16px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  margin: 0;
  color: #333;
  font-size: 20px;
}

.see-all {
  color: #ff6b6b;
  cursor: pointer;
  font-size: 14px;
}

.recommendations {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.recommend-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid rgba(255, 107, 107, 0.1);
}

.food-emoji {
  font-size: 32px;
}

.food-info h5 {
  margin: 0 0 4px 0;
  color: #333;
}

.food-info p {
  margin: 0;
  color: #666;
  font-size: 12px;
}

/* 右侧边栏样式 */
.right-sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-card,
.daily-tip-card,
.quick-actions-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(12px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.stats-card h3,
.quick-actions-card h3 {
  margin-bottom: 20px;
  color: #333;
}

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stat-item-large {
  text-align: center;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #ff6b6b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}

.tip-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: #ff6b6b;
  font-weight: 500;
}

.tip-content {
  color: #666;
  font-size: 14px;
  margin: 0;
  line-height: 1.5;
}

.quick-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.quick-btn {
  width: 100%;
  justify-content: flex-start;
}

.logout-btn {
  color: #ff6b6b;
  border-color: #ff6b6b;
}

/* 背景动画 */
.background {
  position: fixed;
  inset: 0;
  z-index: -1;
}

.floating-food {
  position: absolute;
  font-size: 36px;
  opacity: 0.15;
  animation: float 6s ease-in-out infinite;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-15px) rotate(5deg); }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .dashboard-layout {
    grid-template-columns: 250px 1fr;
  }
  .right-sidebar {
    display: none;
  }
}

@media (max-width: 768px) {
  .dashboard-layout {
    grid-template-columns: 1fr;
  }
  .sidebar {
    display: none;
  }
  .features-grid {
    grid-template-columns: 1fr;
  }
  .feature-content {
    flex-direction: column;
    text-align: center;
  }
}
</style>