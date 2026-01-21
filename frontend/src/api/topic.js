/**
 * 知识点相关API请求
 */

import request from './request'

/**
 * 获取知识点树
 */
export function getTopicTree() {
  return request({
    url: '/topics/',
    method: 'get'
  })
}

/**
 * 获取知识点详情
 */
export function getTopicDetail(id) {
  return request({
    url: `/topics/${id}`,
    method: 'get'
  })
}

/**
 * 获取分类列表
 */
export function getCategories() {
  return request({
    url: '/topics/categories',
    method: 'get'
  })
}

/**
 * 获取前置知识点
 */
export function getPrerequisites(id) {
  return request({
    url: `/topics/${id}/prerequisites`,
    method: 'get'
  })
}

/**
 * 获取相关知识点
 */
export function getRelated(id) {
  return request({
    url: `/topics/${id}/related`,
    method: 'get'
  })
}
