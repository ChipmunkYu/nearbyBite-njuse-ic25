// src/utils/api/history.js
import request from '../request'

// 创建历史记录
export const addHistory = (userId, restaurantName) => {
  return request.post(`/users/${userId}/history`, {
    restaurant_name: restaurantName,
    timestamp: new Date().toISOString(),
  })
}

// 获取用户历史记录
export const getHistory = (userId) => {
  return request.get(`/users/${userId}/history`)
}

// 删除一条历史记录
export const deleteHistory = (recordId) => {
  return request.delete(`/history/${recordId}`)
}
