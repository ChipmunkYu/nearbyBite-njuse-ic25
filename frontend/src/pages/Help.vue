<template>
  <BackFirstButton/>
  <div class="help-container">
    <!-- 背景装饰 -->
    <div class="background">
      <div class="floating-icon">❓</div>
      <div class="floating-icon">💡</div>
      <div class="floating-icon">📚</div>
      <div class="floating-icon">🔧</div>
      <div class="floating-icon">🤔</div>
      <div class="floating-icon">✨</div>
    </div>

    <!-- 主内容卡片 -->
    <div class="help-card">
      <!-- 页面标题 -->
      <div class="page-header">
        <div class="title-group">
          <span class="title-icon">❓</span>
          <h1>使用帮助中心</h1>
        </div>
        <p class="page-subtitle">为您解答常见问题，快速上手美食推荐系统</p>
        <div class="header-line"></div>
      </div>

      <!-- FAQ 区域 -->
      <div class="faq-section">
        <div class="section-header">
          <span class="section-icon">❔</span>
          <h2 class="section-title">常见问题解答</h2>
          <p class="section-subtitle">快速找到您需要的答案</p>
        </div>
        
        <el-collapse v-model="activeNames" accordion class="faq-collapse">
          <el-collapse-item name="1">
            <template #title>
              <div class="collapse-title">
                <span class="title-icon">🎲</span>
                <span>如何使用随机推荐功能？</span>
              </div>
            </template>
            <div class="collapse-content">
              <p>1. 进入「随机推荐」页面</p>
              <p>2. 设置预算范围（人均消费）</p>
              <p>3. 选择您感兴趣的美食类型</p>
              <p>4. 设置口味偏好（可选）</p>
              <p>5. 点击「随机推荐」按钮即可获得推荐</p>
              <div class="tip-box">
                <span class="tip-icon">💡</span>
                <span class="tip-text">推荐结果将自动保存到历史记录中</span>
              </div>
            </div>
          </el-collapse-item>

          <el-collapse-item name="2">
            <template #title>
              <div class="collapse-title">
                <span class="title-icon">📖</span>
                <span>历史记录是如何生成的？</span>
              </div>
            </template>
            <div class="collapse-content">
              <p>系统会自动记录您的推荐历史：</p>
              <ul class="content-list">
                <li>每次使用随机推荐功能并查看推荐结果时</li>
                <li>推荐结果弹窗显示时会自动保存记录</li>
                <li>记录包含餐馆名称、推荐时间等信息</li>
              </ul>
              <div class="feature-badge">
                <span class="badge-icon">🔄</span>
                <span class="badge-text">自动同步，无需手动操作</span>
              </div>
            </div>
          </el-collapse-item>

          <el-collapse-item name="3">
            <template #title>
              <div class="collapse-title">
                <span class="title-icon">📊</span>
                <span>为什么统计页面没有数据显示？</span>
              </div>
            </template>
            <div class="collapse-content">
              <p>统计数据基于历史记录生成：</p>
              <div class="warning-box">
                <span class="warning-icon">⚠️</span>
                <div class="warning-content">
                  <div class="warning-title">数据来源</div>
                  <div class="warning-text">如果您尚未使用过随机推荐功能，统计图表将显示为空</div>
                </div>
              </div>
              <p>开始使用随机推荐后，统计数据将自动生成并更新</p>
            </div>
          </el-collapse-item>

          <el-collapse-item name="4">
            <template #title>
              <div class="collapse-title">
                <span class="title-icon">🏪</span>
                <span>如何管理餐馆信息？</span>
              </div>
            </template>
            <div class="collapse-content">
              <p>您可以在「所有餐馆」页面进行以下操作：</p>
              <div class="feature-grid">
                <div class="feature-item">
                  <span class="item-icon">➕</span>
                  <div class="item-content">
                    <div class="item-title">新增餐馆</div>
                    <div class="item-desc">添加新的餐馆信息</div>
                  </div>
                </div>
                <div class="feature-item">
                  <span class="item-icon">✏️</span>
                  <div class="item-content">
                    <div class="item-title">编辑信息</div>
                    <div class="item-desc">修改现有餐馆信息</div>
                  </div>
                </div>
                <div class="feature-item">
                  <span class="item-icon">🗑️</span>
                  <div class="item-content">
                    <div class="item-title">删除餐馆</div>
                    <div class="item-desc">移除不需要的餐馆</div>
                  </div>
                </div>
              </div>
            </div>
          </el-collapse-item>

          <el-collapse-item name="5">
            <template #title>
              <div class="collapse-title">
                <span class="title-icon">🔐</span>
                <span>如何修改账号信息？</span>
              </div>
            </template>
            <div class="collapse-content">
              <p>在「个人设置」页面可以进行以下操作：</p>
              <ul class="content-list">
                <li>修改用户名（显示名称）</li>
                <li>更改登录密码</li>
                <li>查看您的唯一用户编号</li>
              </ul>
              <div class="tip-box success">
                <span class="tip-icon">✅</span>
                <span class="tip-text">用户名修改立即生效，密码修改后需要重新登录</span>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 功能说明 -->
      <div class="features-section">
        <div class="section-header">
          <span class="section-icon">✨</span>
          <h2 class="section-title">核心功能介绍</h2>
          <p class="section-subtitle">探索系统的强大功能</p>
        </div>
        
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🎲</div>
            <div class="feature-content">
              <h3 class="feature-title">智能推荐</h3>
              <p class="feature-desc">根据筛选条件智能抽取美食，解决选择困难症</p>
            </div>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <div class="feature-content">
              <h3 class="feature-title">历史记录</h3>
              <p class="feature-desc">自动保存浏览记录，方便回顾和查找</p>
            </div>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-content">
              <h3 class="feature-title">统计图表</h3>
              <p class="feature-desc">可视化分析您的饮食偏好和消费习惯</p>
            </div>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">🏪</div>
            <div class="feature-content">
              <h3 class="feature-title">餐馆管理</h3>
              <p class="feature-desc">完整的CRUD操作，轻松管理餐馆信息</p>
            </div>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">⚙️</div>
            <div class="feature-content">
              <h3 class="feature-title">个人设置</h3>
              <p class="feature-desc">自定义账号信息和安全设置</p>
            </div>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">💬</div>
            <div class="feature-content">
              <h3 class="feature-title">反馈系统</h3>
              <p class="feature-desc">随时向我们提出建议或报告问题</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 联系支持 -->
      <div class="contact-section">
        <div class="section-header">
          <span class="section-icon">📩</span>
          <h2 class="section-title">需要更多帮助？</h2>
          <p class="section-subtitle">我们随时为您提供支持</p>
        </div>
        
        <div class="contact-card">
          <div class="contact-content">
            <div class="contact-icon">💭</div>
            <div class="contact-info">
              <h3 class="contact-title">提交反馈</h3>
              <p class="contact-desc">如果您遇到问题或有改进建议，欢迎提交反馈</p>
            </div>
          </div>
          <el-button 
            type="primary" 
            @click="goToFeedback"
            class="contact-btn"
          >
            <span class="btn-icon">📤</span>
            <span class="btn-text">前往反馈页面</span>
          </el-button>
        </div>
        
        <div class="support-tips">
          <div class="tips-header">
            <span class="tips-icon">💡</span>
            <span>温馨提示</span>
          </div>
          <div class="tips-content">
            <p>• 我们会在24小时内回复您的反馈</p>
            <p>• 请尽量详细描述您遇到的问题</p>
            <p>• 感谢您帮助我们改进产品</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import BackFirstButton from '@/components/BackFirstButton.vue'

const router = useRouter();
const activeNames = ref(['1']);

const goToFeedback = () => {
  router.push("/feedback");
};
</script>

<style scoped>
.help-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #f6d365 100%);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  overflow: auto;
  position: relative;
  padding: 40px 20px;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.background {
  position: absolute;
  inset: 0;
}

.floating-icon {
  position: absolute;
  font-size: 42px;
  opacity: 0.2;
  animation: float 8s ease-in-out infinite;
}

.floating-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.floating-icon:nth-child(2) { top: 20%; right: 15%; animation-delay: 1.5s; }
.floating-icon:nth-child(3) { bottom: 25%; left: 15%; animation-delay: 3s; }
.floating-icon:nth-child(4) { bottom: 15%; right: 10%; animation-delay: 4.5s; }
.floating-icon:nth-child(5) { top: 40%; left: 85%; animation-delay: 6s; }
.floating-icon:nth-child(6) { bottom: 40%; right: 85%; animation-delay: 7.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-25px) rotate(15deg); }
}

.help-card {
  width: 1000px;
  max-width: 95%;
  padding: 48px 42px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(16px);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 2;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.title-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 12px;
}

.title-icon {
  font-size: 48px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.page-header h1 {
  font-size: 36px;
  font-weight: 800;
  color: #2c3e50;
  margin: 0;
  background: linear-gradient(135deg, #2c3e50, #4a6572);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.page-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
  letter-spacing: 0.5px;
}

.header-line {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b, #ff8e53);
  margin: 20px auto 0;
  border-radius: 2px;
}

/* FAQ 区域 */
.faq-section {
  margin-bottom: 50px;
}

.section-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #f0f0f0;
}

.section-icon {
  font-size: 28px;
  margin-right: 12px;
  vertical-align: middle;
}

.section-title {
  display: inline-block;
  font-size: 22px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 6px 0;
  vertical-align: middle;
}

.section-subtitle {
  font-size: 14px;
  color: #7f8c8d;
  margin: 0 0 0 40px;
}

/* 折叠面板 */
.faq-collapse {
  border-radius: 16px;
  overflow: hidden;
}

.faq-collapse :deep(.el-collapse-item__header) {
  background: #f8f9fa;
  border: none;
  padding: 20px 24px;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 1px solid #e9ecef;
  transition: all 0.3s;
}

.faq-collapse :deep(.el-collapse-item__header:hover) {
  background: #f1f3f4;
  color: #ff6b6b;
}

.faq-collapse :deep(.el-collapse-item__wrap) {
  border: none;
  background: white;
}

.faq-collapse :deep(.el-collapse-item__content) {
  padding: 24px;
  color: #495057;
  line-height: 1.6;
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.collapse-title .title-icon {
  font-size: 24px;
  animation: none;
}

.collapse-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

.collapse-content p {
  margin: 12px 0;
  font-size: 15px;
  color: #495057;
}

.collapse-content p:first-child {
  margin-top: 0;
}

.content-list {
  padding-left: 20px;
  margin: 16px 0;
}

.content-list li {
  margin-bottom: 8px;
  color: #495057;
  font-size: 15px;
}

.tip-box {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #e9f7fe, #d6f1ff);
  border-radius: 12px;
  border-left: 4px solid #3498db;
  margin-top: 20px;
}

.tip-box.success {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border-left-color: #28a745;
}

.tip-icon {
  font-size: 20px;
}

.tip-text {
  font-size: 14px;
  font-weight: 600;
  color: #2c3e50;
  flex: 1;
}

.feature-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  margin-top: 16px;
}

.badge-icon {
  font-size: 16px;
}

.warning-box {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px;
  background: linear-gradient(135deg, #fff3cd, #ffecb5);
  border-radius: 12px;
  border: 1px solid #ffeaa7;
  margin: 20px 0;
}

.warning-icon {
  font-size: 28px;
  flex-shrink: 0;
}

.warning-content {
  flex: 1;
}

.warning-title {
  font-size: 15px;
  font-weight: 700;
  color: #856404;
  margin-bottom: 4px;
}

.warning-text {
  font-size: 14px;
  color: #856404;
  line-height: 1.5;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 20px 0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: white;
  border-radius: 12px;
  border: 1px solid #e9ecef;
  transition: all 0.3s;
}

.feature-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: #3498db;
}

.item-icon {
  font-size: 24px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  border-radius: 50%;
  flex-shrink: 0;
}

.item-content {
  flex: 1;
}

.item-title {
  font-size: 14px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 4px;
}

.item-desc {
  font-size: 12px;
  color: #6c757d;
}

/* 功能说明 */
.features-section {
  margin-bottom: 50px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  background: white;
  border-radius: 20px;
  padding: 28px 24px;
  text-align: center;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  border-color: #3498db;
}

.feature-icon {
  font-size: 48px;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  border-radius: 50%;
  margin-bottom: 20px;
}

.feature-content {
  flex: 1;
}

.feature-title {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 12px;
}

.feature-desc {
  font-size: 14px;
  color: #6c757d;
  line-height: 1.6;
  margin: 0;
}

/* 联系支持 */
.contact-section {
  margin-bottom: 20px;
}

.contact-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 32px;
  background: linear-gradient(135deg, #f8f9fa, #f1f3f4);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  margin: 24px 0 32px;
}

.contact-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.contact-icon {
  font-size: 48px;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  border-radius: 50%;
  color: white;
}

.contact-info {
  flex: 1;
}

.contact-title {
  font-size: 22px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.contact-desc {
  font-size: 15px;
  color: #6c757d;
  margin: 0;
  line-height: 1.6;
}

.contact-btn {
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  border: none;
  font-size: 16px;
  font-weight: 700;
  padding: 0 32px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
}

.contact-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(255, 107, 107, 0.4);
}

.btn-icon {
  font-size: 20px;
}

.support-tips {
  background: linear-gradient(135deg, #fff3cd, #ffecb5);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid #ffeaa7;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
  font-weight: 700;
  color: #856404;
  margin-bottom: 16px;
}

.tips-icon {
  font-size: 20px;
}

.tips-content {
  color: #856404;
  font-size: 14px;
  line-height: 1.6;
}

.tips-content p {
  margin: 12px 0 0 0;
  padding-left: 8px;
}

.tips-content p:first-child {
  margin-top: 0;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .features-grid,
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .contact-card {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .contact-content {
    flex-direction: column;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .help-container {
    padding: 20px 10px;
  }
  
  .help-card {
    padding: 32px 24px;
    border-radius: 24px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .title-icon {
    font-size: 36px;
  }
  
  .features-grid,
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .section-title {
    font-size: 20px;
  }
  
  .section-subtitle {
    margin-left: 0;
    margin-top: 4px;
  }
  
  .faq-collapse :deep(.el-collapse-item__header) {
    padding: 16px 20px;
    font-size: 15px;
  }
  
  .feature-card {
    padding: 24px 20px;
  }
  
  .feature-icon {
    width: 64px;
    height: 64px;
    font-size: 36px;
  }
}
</style>