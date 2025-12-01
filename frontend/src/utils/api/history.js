// src/utils/api/history.js
import request from './request.js'

// 创建历史记录
export const addHistory = (userId, restaurantName, restaurantId) => {
  return request.post(`/api/users/me/history`, {
    restaurant_id: restaurantId,
    restaurant_name: restaurantName,
    timestamp: new Date().toISOString(),
  })
}

// 获取用户历史记录
export const getHistory = (userId) => {
  return request.get(`/api/users/me/history`)
}

// 删除一条历史记录
export const deleteHistory = (recordId) => {
  return request.delete(`/api/users/me/history/${recordId}`)
}
