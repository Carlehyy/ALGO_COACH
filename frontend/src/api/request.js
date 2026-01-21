import axios from 'axios'

// 创建axios实例
const request = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const { data } = response

    // 统一响应格式: { code, message, data }
    if (data.code === 200) {
      return data.data
    } else {
      // 业务错误
      console.error('业务错误:', data.message)
      return Promise.reject(new Error(data.message || '请求失败'))
    }
  },
  error => {
    console.error('响应错误:', error)

    // 401 未授权，跳转登录
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/user/login'
    }

    return Promise.reject(error)
  }
)

export default request
