<!-- src/views/Register.vue -->
<template>
  <AuthLayout>
    <div class="logo-section">
      <div class="app-logo"></div>
      <h1>注册</h1>
      <br></br>
    </div>

    <el-form :model="form" :rules="rules" ref="registerFormRef">
      <el-form-item prop="username">
        <el-input v-model="form.username" placeholder="用户名" size="large" />
      </el-form-item>

      <el-form-item prop="password">
        <el-input v-model="form.password" placeholder="密码" type="password" show-password size="large" />
      </el-form-item>

      <el-form-item prop="confirmPassword">
        <el-input v-model="form.confirmPassword" placeholder="确认密码" type="password" show-password size="large" />
      </el-form-item>

        <br></br>
      <el-button type="primary" @click="submitForm" size="large" class="login-btn" :loading="loading">
        {{ loading ? '注册中...' : '立即注册' }}
      </el-button>

      <div class="footer">
        <br></br>
        <RouterLink to="/login" class="register-link">已有账号？返回登录</RouterLink>
      </div>
    </el-form>
  </AuthLayout>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import AuthLayout from '@/components/AuthLayout.vue'
import { register } from '@/utils/api'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
  confirmPassword: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min : 2, max: 15, message: '用户名长度应在2到15个字符之间', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '邮箱格式错误', trigger: ['blur', 'change'] }
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' },
             { min : 6, message: '密码长度不能少于6位', trigger: 'blur' }    
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== form.password) callback(new Error('两次密码不一致'))
        else callback()
      },
      trigger: 'blur'
    }
  ]
}

const submitForm = async () => {
  await registerFormRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await register(form.username, form.password)
      
      if (res.data.code === 200) {
        ElMessage.success('注册成功，欢迎加入！✨')
        router.push('/login')
      } else {
        ElMessage.error(res.data.message || '注册失败')
      }
    } catch (err) {
      console.error('注册错误:', err)
      if(err.response?.status == 400){
        const errorMsg = err.response?.data?.message || ''
        if (errorMsg.includes('用户') || errorMsg.includes('username') || errorMsg.includes('已存在')) {
          ElMessage.error('用户名已存在，请重新输入')
        }
        else{
          ElMessage.error(errorMsg || '请检查填写内容')
        }
      }else {
        ElMessage.error('注册失败，请稍后重试')
      }
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
  h1 {
  color: #ff6b6b;
  font-size: 34px;
  margin-bottom: 8px;
  font-weight: 700;
}
</style>