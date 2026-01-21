/**
 * AI教练相关API请求
 */

import request from './request'

/**
 * 创建会话
 */
export function createSession(data) {
  return request({
    url: '/coach/sessions',
    method: 'post',
    data
  })
}

/**
 * 获取会话列表
 */
export function getSessions() {
  return request({
    url: '/coach/sessions',
    method: 'get'
  })
}

/**
 * 获取会话详情
 */
export function getSession(id) {
  return request({
    url: `/coach/sessions/${id}`,
    method: 'get'
  })
}

/**
 * 获取历史消息
 */
export function getMessages(sessionId) {
  return request({
    url: `/coach/sessions/${sessionId}/messages`,
    method: 'get'
  })
}

/**
 * 发送消息
 */
export function sendMessage(data) {
  return request({
    url: '/coach/chat',
    method: 'post',
    data
  })
}

/**
 * 关闭会话
 */
export function closeSession(id) {
  return request({
    url: `/coach/sessions/${id}`,
    method: 'delete'
  })
}
