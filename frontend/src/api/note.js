/**
 * 笔记相关API请求
 */

import request from './request'

/**
 * 获取笔记列表
 */
export function getNotes(params) {
  return request({
    url: '/notes/',
    method: 'get',
    params
  })
}

/**
 * 获取笔记详情
 */
export function getNoteDetail(id) {
  return request({
    url: `/notes/${id}`,
    method: 'get'
  })
}

/**
 * 根据知识点获取笔记
 */
export function getNotesByTopic(topicId) {
  return request({
    url: `/notes/topic/${topicId}`,
    method: 'get'
  })
}

/**
 * 搜索笔记
 */
export function searchNotes(keyword) {
  return request({
    url: '/notes/',
    method: 'get',
    params: { keyword }
  })
}
