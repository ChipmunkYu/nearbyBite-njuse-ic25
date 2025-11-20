// src/utils/api/auth.js
import request from './request'

export const register = (username, password) => {
  return request.post('api/auth/register', {
    username,
    password
  })
}

export const login = (identifier, password) => {
  return request.post('api/auth/login', {
    identifier,
    password
  })
}
