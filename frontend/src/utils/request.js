import axios from 'axios'
import { useUserStore } from '@/stores/user'
import router from '@/router'
import { ElMessage } from 'element-plus'
import { goErrorPage } from './errorPage'
import { showLoading, hideLoading } from './loading'


const request = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  timeout: 5000
})

// 请求拦截：自动加 token
request.interceptors.request.use(config => {
  showLoading()
  const store = useUserStore()
  if (store.token) {
    config.headers.Authorization = `Bearer ${store.token}`
  }
  return config
},
  error => {
    hideLoading()
    return Promise.reject(error)
  }
)

let isRefreshing = false
let subscribers = []

function onRefreshed(newToken) {
  subscribers.forEach(cb => cb(newToken))
  subscribers = []
}

// 响应拦截：检测 401 → 自动退出登录
request.interceptors.response.use(
   res => {
     hideLoading()
    return res
  },
  async err => {
    hideLoading()  
    const { response, config } = err
    const store = useUserStore()
    const code = response?.status || 500
    const msg = response?.data?.message || '服务器错误'

    
    ElMessage.error(msg)

    // token 过期
    if (code === 401) {
      if (!isRefreshing) {
        isRefreshing = true

        try {
          const newToken = await store.refreshTokenAction()
          isRefreshing = false
          onRefreshed(newToken)
        } catch {
          store.logout()
          router.push('/login')
          return Promise.reject(err)
        }
      }

      return new Promise(resolve => {
        subscribers.push(token => {
          config.headers.Authorization = `Bearer ${token}`
          resolve(request(config))
        })
      })
    }
    if ([404, 500].includes(code)) {
      goErrorPage(code, msg)
    }

    return Promise.reject(err)
  }
)

export default request
