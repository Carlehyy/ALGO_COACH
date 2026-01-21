/**
 * 用户相关API请求
 */

import request from './request'

/**
 * 用户注册
 */
export function register(data) {
  return request({
    url: '/users/register',
    method: 'post',
    data
  })
}

/**
 * 用户登录
 */
export function login(data) {
  return request({
    url: '/users/login',
    method: 'post',
    data
  })
}

/**
 * 获取当前用户信息
 */
export function getCurrentUser() {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

/**
 * 更新用户信息
 */
export function updateUser(data) {
  return request({
    url: '/users/me',
    method: 'put',
    data
  })
}

/**
 * 修改密码
 */
export function changePassword(data) {
  return request({
    url: '/users/change-password',
    method: 'post',
    data
  })
}

/**
 * 获取积分余额
 */
export function getBalance() {
  return request({
    url: '/users/balance',
    method: 'get'
  })
}

/**
 * 刷新Token
 */
export function refreshToken() {
  return request({
    url: '/users/refresh',
    method: 'post'
  })
}
