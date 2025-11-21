import { defineStore } from 'pinia'
import router from '@/router'
import request from '@/utils/api/request'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || '',
    refreshToken: localStorage.getItem('refreshToken') || ''
  }),
  actions: {
    setUser(user, token, refreshToken) {
      this.user = user
      this.token = token
      this.refreshToken = refreshToken
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('token', token)
      localStorage.setItem('refreshToken', refreshToken)
    },

    async refreshTokenAction() {
      const res = await request.post('/refresh', {
      refresh_token: this.refreshToken
    })
      this.token = res.data.access_token
      localStorage.setItem('token', res.data.access_token)
      return res.data.access_token
   },

    logout() {
      this.user = null
      this.token = ''
      this.refreshToken = ''
      localStorage.removeItem('user')
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      router.push('/login')  
    }
  }
})