import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user' 


// 创建 axios 实例
const api = axios.create({
    // Flask 后端地址
  baseURL: 'http://127.0.0.1:5000', 
  timeout: 5000,
})

//具体的 API 调用可以在这里定义，后续补充,注意路径要和后端保持一致！！

export const register = (username, password) => {
  return api.post('api/auth/register', { username, password })
}

export const login = (identifier, password) => {
  return api.post('api/auth/login', { identifier, password })
}

api.interceptors.response.use(
  res => res,
  err => {
    const userStore = useUserStore()
    if(err.response && err.response.status === 401) {
      ElMessage.error('登录已过期，请重新登录～🍱')
      userStore.logout()
      router.push('/login')
      
    }
    return Promise.reject(err)
  }
)

export default api
