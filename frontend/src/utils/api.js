import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
    // Flask 后端地址
  baseURL: 'http://127.0.0.1:5000', 
  timeout: 5000,
})

//具体的 API 调用可以在这里定义，后续补充

export const register = (username, password) => {
  return api.post('auth/register', { username, password })
}

export const login = (identifier, password) => {
  return api.post('auth/login', { identifier, password })
}

export default api
