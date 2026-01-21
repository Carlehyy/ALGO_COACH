import request from '../request'

/**
 * 管理后台API
 */
export const adminApi = {
  /**
   * 获取Dashboard统计数据
   */
  getDashboard() {
    return request.get('/admin/dashboard')
  },

  /**
   * 资源管理
   */
  getResources(params) {
    return request.get('/admin/resources', { params })
  },

  /**
   * 更新资源状态
   */
  updateResourceStatus(resourceId, data) {
    return request.put(`/admin/resources/${resourceId}/status`, data)
  },

  /**
   * 删除资源
   */
  deleteResource(resourceId) {
    return request.delete(`/admin/resources/${resourceId}`)
  },

  /**
   * 重新触发解析
   */
  triggerParse(resourceId) {
    return request.post(`/admin/resources/${resourceId}/parse`)
  },

  /**
   * 笔记审核
   */
  getPendingNotes(params) {
    return request.get('/admin/notes/pending', { params })
  },

  /**
   * 发布笔记
   */
  publishNote(noteId) {
    return request.post(`/admin/notes/${noteId}/publish`)
  },

  /**
   * 退回笔记
   */
  rejectNote(noteId, reason) {
    return request.post(`/admin/notes/${noteId}/reject`, { reason })
  },

  /**
   * 触发笔记生成
   */
  generateNote(noteId) {
    return request.post(`/admin/notes/${noteId}/generate`)
  },

  /**
   * 用户管理
   */
  getUsers(params) {
    return request.get('/admin/users', { params })
  },

  /**
   * 更新用户状态
   */
  updateUserStatus(userId, status) {
    return request.put(`/admin/users/${userId}/status`, { status })
  }
}
