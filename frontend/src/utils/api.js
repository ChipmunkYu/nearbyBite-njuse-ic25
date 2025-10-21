import axios from 'axios'

// 创建 axios 实例
const api = axios.create({
    // Flask 默认端口，后续可改成相应的后端地址
  baseURL: 'http://localhost:5000', 
  timeout: 5000,
})

//具体的 API 调用可以在这里定义，后续补充

export default api
