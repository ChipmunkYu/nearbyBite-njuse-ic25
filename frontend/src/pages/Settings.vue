<template>
  <BackFirstButton/>
  <div class="settings-container">
    <!-- 背景装饰 -->
    <div class="background">
      <div class="floating-icon">⚙️</div>
      <div class="floating-icon">🔧</div>
      <div class="floating-icon">👤</div>
      <div class="floating-icon">🔒</div>
      <div class="floating-icon">📝</div>
      <div class="floating-icon">🛡️</div>
    </div>

    <!-- 主内容卡片 -->
    <div class="settings-card">
      <!-- 页面标题 -->
      <div class="page-header">
        <div class="title-group">
          <span class="title-icon">⚙️</span>
          <h1>个人设置</h1>
        </div>
        <p class="page-subtitle">管理您的账号信息与安全</p>
        <div class="header-line"></div>
      </div>

      <!-- 主要内容区域 -->
      <div class="main-content">
        <!-- 左侧：账号信息 -->
        <div class="left-panel">
          <div class="panel-card info-card">
            <div class="panel-header">
              <div class="panel-icon">👤</div>
              <div class="panel-title-group">
                <h2 class="panel-title">账号信息</h2>
                <p class="panel-subtitle">管理您的基本账号设置</p>
              </div>
            </div>

            <div class="panel-body">
              <!-- 用户编号 -->
              <div class="info-section">
                <div class="info-label">
                  <span class="label-icon">🆔</span>
                  <span class="label-text">用户编号</span>
                </div>
                <div class="info-content">
                  <div class="id-display-box">
                    <div class="id-value">{{ userForm.user_id || '加载中...' }}</div>
                    <div class="id-badge">不可编辑</div>
                  </div>
                </div>
              </div>

              <!-- 用户名 -->
              <div class="info-section">
                <div class="info-label">
                  <span class="label-icon">📝</span>
                  <span class="label-text">用户名</span>
                </div>
                <div class="info-content">
                  <el-form
                    :model="userForm"
                    :rules="rules"
                    ref="userFormRef"
                    class="username-form"
                  >
                    <el-form-item prop="username" class="no-margin">
                      <el-input 
                        v-model="userForm.username" 
                        placeholder="输入新的用户名（2-20个字符）"
                        class="username-input"
                        :prefix-icon="User"
                        size="large"
                      >
                        <template #suffix>
                          <span class="char-counter">{{ userForm.username.length }}/20</span>
                        </template>
                      </el-input>
                    </el-form-item>
                  </el-form>
                  <div class="username-tips">
                    <span class="tip-item">✓ 显示名称</span>
                    <span class="tip-item">✓ 可随时修改</span>
                  </div>
                </div>
              </div>

              <!-- 保存按钮 -->
              <div class="action-section">
                <el-button 
                  type="primary" 
                  @click="updateUserInfo"
                  class="save-btn"
                  :icon="Check"
                  size="large"
                >
                  <span class="btn-text">保存账号信息</span>
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：安全设置 -->
        <div class="right-panel">
          <div class="panel-card security-card">
            <div class="panel-header">
              <div class="panel-icon">🔒</div>
              <div class="panel-title-group">
                <h2 class="panel-title">安全设置</h2>
                <p class="panel-subtitle">保护您的账号安全</p>
              </div>
            </div>

            <div class="panel-body">
              <div class="security-section">
                <div class="section-title">
                  <span class="title-icon">🔄</span>
                  <span class="title-text">修改密码</span>
                </div>
                
                <el-form
                  :model="pwdForm"
                  :rules="pwdRules"
                  ref="pwdFormRef"
                  class="password-form"
                >
                  <!-- 当前密码 -->
                  <div class="form-row">
                    <div class="form-label">
                      <span class="label-icon">🔐</span>
                      <span>当前密码</span>
                    </div>
                    <div class="form-input">
                      <el-form-item prop="oldPwd" class="no-margin">
                        <el-input 
                          type="password" 
                          v-model="pwdForm.oldPwd"
                          placeholder="请输入当前使用的密码"
                          class="password-input"
                          :prefix-icon="Lock"
                          size="large"
                          show-password
                        />
                      </el-form-item>
                    </div>
                  </div>

                  <!-- 新密码 -->
                  <div class="form-row">
                    <div class="form-label">
                      <span class="label-icon">🔑</span>
                      <span>新密码</span>
                    </div>
                    <div class="form-input">
                      <el-form-item prop="newPwd" class="no-margin">
                        <el-input 
                          type="password" 
                          v-model="pwdForm.newPwd"
                          placeholder="请输入6位以上的新密码"
                          class="password-input"
                          :prefix-icon="Key"
                          size="large"
                          show-password
                        />
                      </el-form-item>
                    </div>
                  </div>

                  <!-- 确认密码 -->
                  <div class="form-row">
                    <div class="form-label">
                      <span class="label-icon">✅</span>
                      <span>确认密码</span>
                    </div>
                    <div class="form-input">
                      <el-form-item prop="confirmPwd" class="no-margin">
                        <el-input 
                          type="password" 
                          v-model="pwdForm.confirmPwd"
                          placeholder="请再次输入新密码进行确认"
                          class="password-input"
                          :prefix-icon="Check"
                          size="large"
                          show-password
                        />
                      </el-form-item>
                    </div>
                  </div>

                  <!-- 密码修改按钮 -->
                  <div class="action-section">
                    <el-button 
                      type="danger" 
                      @click="changePassword"
                      class="change-password-btn"
                      :icon="Refresh"
                      size="large"
                    >
                      <span class="btn-text">更新登录密码</span>
                    </el-button>
                  </div>
                </el-form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock, Key, Check, Refresh } from '@element-plus/icons-vue'
import request from '@/utils/api/request'
import BackFirstButton from '@/components/BackFirstButton.vue'


// 表单数据

const userForm = ref({
  user_id: '',     
  username: ''   
})

const pwdForm = ref({
  oldPwd: '',
  newPwd: '',
  confirmPwd: ''
})


// 校验规则

const rules = {
  username: [
    { required: true, message: '用户名不能为空', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ]
}

const pwdRules = {
  oldPwd: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  newPwd: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
  ],
  confirmPwd: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== pwdForm.value.newPwd) {
          callback(new Error('两次输入的密码不一致'))
        } else callback()
      },
      trigger: 'blur'
    }
  ]
}

const userFormRef = ref()
const pwdFormRef = ref()

// 加载用户信息 

async function loadUserInfo() {
  try {
    const res = await request.get('/api/users/me')

    if (res.data.code !== 200) {
      ElMessage.error(res.data.message)
      return
    }

    userForm.value.user_id = res.data.data.user_id
    userForm.value.username = res.data.data.username

  } catch (err) {
    ElMessage.error('无法加载用户信息')
  }
}


// 修改用户名 /api/users/me (PUT)

async function updateUserInfo() {
  userFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      const res = await request.put('/api/users/me', {
        username: userForm.value.username
      })

      if (res.data.code === 200) {
        ElMessage.success('用户名更新成功！')
      } else {
        ElMessage.error(res.data.message)
      }
    } catch (err) {
      ElMessage.error('更新失败')
    }
  })
}


// 修改密码 /api/users/me/password (POST)

async function changePassword() {
  pwdFormRef.value.validate(async (valid) => {
    if (!valid) return

    try {
      const res = await request.post('/api/users/me/password', {
        oldPwd: pwdForm.value.oldPwd,
        newPwd: pwdForm.value.newPwd
      })

      if (res.data.code === 200) {
        ElMessage.success('密码修改成功！')

        // 清空输入框
        pwdForm.value.oldPwd = ''
        pwdForm.value.newPwd = ''
        pwdForm.value.confirmPwd = ''
        
        // 可选：密码修改后强制重新登录
        setTimeout(() => {
          ElMessage.info('请使用新密码重新登录')
          localStorage.removeItem('access_token')
          localStorage.removeItem('token')
          router.push('/login')
        }, 1500)
      } else {
        ElMessage.error(res.data.message)
      }
    } catch (err) {
      ElMessage.error('密码修改失败')
    }
  })
}

// 页面初始化执行
loadUserInfo()
</script>

<style scoped>
.settings-container {
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

.settings-card {
  width: 1200px;
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

/* 主要内容区域 */
.main-content {
  display: flex;
  gap: 30px;
}

.left-panel,
.right-panel {
  flex: 1;
  min-width: 0;
}

/* 面板卡片 */
.panel-card {
  background: #f8f9fa;
  border-radius: 20px;
  overflow: hidden;
  height: 100%;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.panel-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
}

.panel-header {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  padding: 28px 32px;
  color: white;
  display: flex;
  align-items: center;
  gap: 20px;
  position: relative;
  overflow: hidden;
}

.panel-header::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s;
}

.panel-card:hover .panel-header::after {
  transform: translateX(100%);
}

.security-card .panel-header {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
}

.panel-icon {
  font-size: 40px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  flex-shrink: 0;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.panel-title-group {
  flex: 1;
}

.panel-title {
  font-size: 24px;
  font-weight: 800;
  margin: 0 0 6px 0;
  color: white;
}

.panel-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
  color: rgba(255, 255, 255, 0.9);
}

.panel-body {
  padding: 32px;
}

/* 信息区域 */
.info-section {
  margin-bottom: 32px;
}

.info-section:last-child {
  margin-bottom: 0;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.label-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  border-radius: 50%;
}

.label-text {
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
}

.info-content {
  padding-left: 52px;
}

/* 用户编号显示 */
.id-display-box {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 12px;
}

.id-value {
  font-family: 'Courier New', 'Menlo', 'Monaco', monospace;
  font-size: 24px;
  font-weight: 800;
  color: #2c3e50;
  letter-spacing: 2px;
  padding: 14px 24px;
  background: white;
  border-radius: 14px;
  border: 2px dashed #dee2e6;
  flex: 1;
  text-align: center;
  box-shadow: inset 0 4px 12px rgba(0, 0, 0, 0.05);
}

.id-badge {
  background: linear-gradient(135deg, #ff6b6b, #ee5a52);
  color: white;
  padding: 8px 20px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
}

.info-description {
  font-size: 14px;
  color: #6c757d;
  line-height: 1.6;
  background: white;
  padding: 16px 20px;
  border-radius: 12px;
  border-left: 4px solid #3498db;
}

/* 用户名表单 */
.username-form {
  margin: 0;
}

.no-margin {
  margin-bottom: 0 !important;
}

.username-input :deep(.el-input__wrapper) {
  border-radius: 14px;
  border: 2px solid #e9ecef;
  padding: 12px 20px;
  transition: all 0.3s;
  background: white;
}

.username-input:hover :deep(.el-input__wrapper) {
  border-color: #3498db;
  box-shadow: 0 0 0 4px rgba(52, 152, 219, 0.1);
  transform: translateY(-2px);
}

.char-counter {
  font-size: 14px;
  color: #adb5bd;
  font-weight: 600;
}

.username-tips {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  flex-wrap: wrap;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #6c757d;
  background: white;
  padding: 8px 16px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
  font-weight: 500;
}

.tip-item:before {
  content: '✓';
  color: #28a745;
  font-weight: bold;
}

/* 安全设置区域 */
.security-section {
  margin-bottom: 20px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 28px;
}

.title-icon {
  font-size: 28px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  border-radius: 50%;
}

.title-text {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
}

.form-row {
  display: flex;
  align-items: flex-start;
  margin-bottom: 28px;
  gap: 24px;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-label {
  width: 120px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 700;
  color: #2c3e50;
  padding-top: 10px;
  flex-shrink: 0;
}

.form-input {
  flex: 1;
}

.password-input :deep(.el-input__wrapper) {
  border-radius: 14px;
  border: 2px solid #e9ecef;
  padding: 12px 20px;
  transition: all 0.3s;
  background: white;
}

.password-input:hover :deep(.el-input__wrapper) {
  border-color: #e74c3c;
  box-shadow: 0 0 0 4px rgba(231, 76, 60, 0.1);
  transform: translateY(-2px);
}



/* 按钮样式 */
.action-section {
  margin-top: 40px;
}

.save-btn {
  width: 100%;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  border: none;
  font-size: 16px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.save-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(52, 152, 219, 0.4);
}

.change-password-btn {
  width: 100%;
  height: 56px;
  border-radius: 16px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  border: none;
  font-size: 16px;
  font-weight: 700;
  color: white;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.change-password-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(231, 76, 60, 0.4);
}

.btn-text {
  margin-left: 8px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .settings-card {
    width: 95%;
  }
}

@media (max-width: 992px) {
  .main-content {
    flex-direction: column;
  }
  
  .panel-card {
    margin-bottom: 24px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
  
  .form-label {
    width: 100%;
    padding-top: 0;
  }
  
  .info-content {
    padding-left: 0;
  }
  
  .id-display-box {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }
  
  .id-badge {
    align-self: flex-start;
  }
}

@media (max-width: 768px) {
  .settings-container {
    padding: 20px 10px;
  }
  
  .settings-card {
    padding: 32px 24px;
    border-radius: 24px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .title-icon {
    font-size: 36px;
  }
  
  .panel-header {
    padding: 24px;
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }
  
  .panel-icon {
    width: 56px;
    height: 56px;
    font-size: 32px;
  }
  
  .id-value {
    font-size: 20px;
    padding: 12px 16px;
  }
  
  .username-tips {
    flex-direction: column;
    gap: 10px;
  }
  
  .tip-item {
    width: 100%;
    justify-content: center;
  }
}
</style>