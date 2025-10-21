<template>
  <AuthLayout>
    <div class="logo-section">
      <div class="app-logo">🍽️</div>
      <h1>登录</h1>
      <p></p>
    </div>

    <el-form :model="form" :rules="rules" ref="loginFormRef">
      <el-form-item prop="username">
        <el-input v-model="form.username" placeholder="用户名/手机号" size="large">
          <template #prefix>
            <el-icon><User /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item prop="password">
        <el-input v-model="form.password" placeholder="密码" type="password" show-password size="large">
          <template #prefix>
            <el-icon><Lock /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-button type="primary" @click="submitForm" size="large" class="login-btn" :loading="loading">
        {{ loading ? '登录中...' : '开始发现美食之旅' }}
      </el-button>

      <div class="footer">
        <RouterLink to="/register" class="register-link">新用户？立即注册</RouterLink>
      </div>
    </el-form>
  </AuthLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import AuthLayout from '@/components/AuthLayout.vue'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}


// 提交登录表单，跳转页面，可更改
const submitForm = async () => {
  await loginFormRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await new Promise((r) => setTimeout(r, 800))
      ElMessage.success('欢迎回来！🍱')
      router.push('/first')
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.logo-section {
  text-align: center;
  margin-bottom: 36px;
}
.app-logo {
  font-size: 64px;
  margin-bottom: 12px;
  filter: drop-shadow(0 4px 8px rgba(255, 107, 107, 0.3));
}
h1 {
  color: #ff6b6b;
  font-size: 34px;
  margin-bottom: 8px;
  font-weight: 700;
}
p {
  color: #666;
  font-size: 16px;
}

.login-btn {
  width: 100%;
  height: 50px;
  margin-top: 10px;
  border-radius: 16px;
  font-size: 18px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
}
.footer {
  text-align: center;
  margin-top: 24px;
}
.register-link {
  color: #ff6b6b;
  font-weight: 600;
  font-size: 15px;
}
</style>
