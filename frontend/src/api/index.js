import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
  baseURL: '/api',
  timeout: 60000
})

// 获取token的函数
const getToken = () => {
  return localStorage.getItem('token') || ''
}

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const message = error.response?.data?.detail || '请求失败'
    ElMessage.error(message)

    // 401 跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      window.location.href = '/login'
    }

    return Promise.reject(error)
  }
)

export default request
