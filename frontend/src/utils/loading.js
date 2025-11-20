import { ElLoading } from 'element-plus'
// 待丰富
let loadingInstance = null
let requestCount = 0  

export function showLoading(text = '加载中...') {
  requestCount++
  if (!loadingInstance) {
    loadingInstance = ElLoading.service({
      fullscreen: true,
      lock: true,
      text,
      background: 'rgba(0, 0, 0, 0.3)',
    })
  }
}

export function hideLoading() {
  requestCount--
  if (requestCount <= 0) {
    requestCount = 0
    if (loadingInstance) {
      loadingInstance.close()
      loadingInstance = null
    }
  }
}
