<template>
  <div class="resources-page">
    <!-- 上传区域 -->
    <div class="upload-section">
      <h3 class="section-title">📤 上传新资源</h3>
      <div class="upload-form">
        <div class="form-row">
          <div class="form-group">
            <label>资源类型</label>
            <select v-model="uploadForm.type" class="form-control">
              <option value="">请选择</option>
              <option value="pdf">PDF文档</option>
              <option value="video">视频</option>
              <option value="blog">博客文章</option>
              <option value="leetcode">LeetCode题解</option>
            </select>
          </div>
          <div class="form-group">
            <label>资源标题</label>
            <input v-model="uploadForm.title" type="text" class="form-control" placeholder="请输入标题">
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>原始URL（可选）</label>
            <input v-model="uploadForm.url" type="text" class="form-control" placeholder="https://...">
          </div>
          <div class="form-group">
            <label>上传文件（可选）</label>
            <input type="file" @change="handleFileChange" class="form-control" accept=".pdf,.mp4">
          </div>
        </div>

        <button @click="handleUpload" :disabled="isUploading" class="upload-btn">
          {{ isUploading ? '上传中...' : '📤 立即上传' }}
        </button>
      </div>
    </div>

    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-group">
          <label>类型</label>
          <select v-model="filters.type" @change="loadResources" class="form-control">
            <option value="">全部</option>
            <option value="pdf">PDF</option>
            <option value="video">视频</option>
            <option value="blog">博客</option>
            <option value="leetcode">LeetCode</option>
          </select>
        </div>
        <div class="filter-group">
          <label>处理状态</label>
          <select v-model="filters.process_status" @change="loadResources" class="form-control">
            <option value="">全部</option>
            <option value="pending">待处理</option>
            <option value="processing">处理中</option>
            <option value="completed">已完成</option>
            <option value="failed">失败</option>
          </select>
        </div>
        <div class="filter-group">
          <label>审核状态</label>
          <select v-model="filters.review_status" @change="loadResources" class="form-control">
            <option value="">全部</option>
            <option value="pending">待审核</option>
            <option value="approved">已通过</option>
            <option value="rejected">已拒绝</option>
          </select>
        </div>
      </div>
    </div>

    <!-- 资源列表 -->
    <div class="resources-list">
      <div class="list-header">
        <h3>资源列表 ({{ pagination.total }})</h3>
        <button @click="loadResources" class="refresh-btn">🔄 刷新</button>
      </div>

      <div v-if="resources.length === 0" class="empty-state">
        <div class="empty-icon">📭</div>
        <div class="empty-text">暂无资源数据</div>
      </div>

      <div v-else class="table-container">
        <table class="resources-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>类型</th>
              <th>标题</th>
              <th>处理状态</th>
              <th>审核状态</th>
              <th>上传者</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="resource in resources" :key="resource.id">
              <td>{{ resource.id }}</td>
              <td>
                <span :class="['type-badge', resource.type]">{{ getTypeLabel(resource.type) }}</span>
              </td>
              <td>
                <div class="resource-title">{{ resource.title }}</div>
              </td>
              <td>
                <span :class="['status-badge', resource.process_status]">
                  {{ getProcessStatusLabel(resource.process_status) }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', resource.review_status]">
                  {{ getReviewStatusLabel(resource.review_status) }}
                </span>
              </td>
              <td>{{ resource.uploader_id }}</td>
              <td>{{ formatDate(resource.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="handleView(resource)" class="action-btn view" title="查看">👁️</button>
                  <button @click="handleParse(resource)" class="action-btn parse" title="解析" :disabled="resource.process_status === 'processing'">⚙️</button>
                  <button @click="handleDelete(resource)" class="action-btn delete" title="删除">🗑️</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div v-if="pagination.total > 0" class="pagination">
        <button @click="prevPage" :disabled="pagination.page === 1" class="page-btn">上一页</button>
        <span class="page-info">第 {{ pagination.page }} 页，共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="pagination.page >= totalPages" class="page-btn">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminApi } from '@/api/modules/admin'

const resources = ref([])
const isUploading = ref(false)
const selectedFile = ref(null)

const uploadForm = ref({
  type: '',
  title: '',
  url: ''
})

const filters = ref({
  type: '',
  process_status: '',
  review_status: ''
})

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.page_size)
})

const loadResources = async () => {
  try {
    const data = await adminApi.getResources({
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      type: filters.value.type,
      process_status: filters.value.process_status,
      review_status: filters.value.review_status
    })
    resources.value = data.items
    pagination.value.total = data.total
  } catch (error) {
    console.error('Failed to load resources:', error)
  }
}

const handleFileChange = (e) => {
  selectedFile.value = e.target.files[0]
}

const handleUpload = async () => {
  if (!uploadForm.value.type || !uploadForm.value.title) {
    alert('请填写资源类型和标题')
    return
  }

  isUploading.value = true
  try {
    const formData = new FormData()
    formData.append('type', uploadForm.value.type)
    formData.append('title', uploadForm.value.title)
    if (uploadForm.value.url) {
      formData.append('url', uploadForm.value.url)
    }
    if (selectedFile.value) {
      formData.append('file', selectedFile.value)
    }

    // TODO: 实现上传API
    await adminApi.uploadResource(formData)

    alert('上传成功')
    uploadForm.value = { type: '', title: '', url: '' }
    selectedFile.value = null
    loadResources()
  } catch (error) {
    alert('上传失败: ' + error.message)
  } finally {
    isUploading.value = false
  }
}

const handleView = (resource) => {
  console.log('View resource:', resource)
}

const handleParse = async (resource) => {
  if (!confirm(`确定要重新解析资源"${resource.title}"吗？`)) return

  try {
    await adminApi.triggerParse(resource.id)
    alert('解析任务已触发')
    loadResources()
  } catch (error) {
    alert('触发失败: ' + error.message)
  }
}

const handleDelete = async (resource) => {
  if (!confirm(`确定要删除资源"${resource.title}"吗？此操作不可恢复。`)) return

  try {
    await adminApi.deleteResource(resource.id)
    alert('删除成功')
    loadResources()
  } catch (error) {
    alert('删除失败: ' + error.message)
  }
}

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    loadResources()
  }
}

const nextPage = () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++
    loadResources()
  }
}

const getTypeLabel = (type) => {
  const labels = {
    pdf: 'PDF',
    video: '视频',
    blog: '博客',
    leetcode: 'LeetCode'
  }
  return labels[type] || type
}

const getProcessStatusLabel = (status) => {
  const labels = {
    pending: '待处理',
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return labels[status] || status
}

const getReviewStatusLabel = (status) => {
  const labels = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return labels[status] || status
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadResources()
})
</script>

<style scoped>
.resources-page {
  max-width: 1400px;
  margin: 0 auto;
}

/* 上传区域 */
.upload-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px 0;
}

.upload-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.form-group label {
  font-size: 14px;
  font-weight: 500;
  color: #475569;
}

.form-control {
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: #60a5fa;
}

.upload-btn {
  padding: 12px 24px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  align-self: flex-start;
}

.upload-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 筛选区域 */
.filter-section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-size: 14px;
  color: #64748b;
}

/* 资源列表 */
.resources-list {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-header h3 {
  margin: 0;
  font-size: 18px;
  color: #1e293b;
}

.refresh-btn {
  padding: 8px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.refresh-btn:hover {
  background: #f8fafc;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #94a3b8;
}

/* 表格 */
.table-container {
  overflow-x: auto;
}

.resources-table {
  width: 100%;
  border-collapse: collapse;
}

.resources-table th {
  text-align: left;
  padding: 12px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  border-bottom: 2px solid #e2e8f0;
}

.resources-table td {
  padding: 12px;
  font-size: 14px;
  border-bottom: 1px solid #f1f5f9;
}

.type-badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.type-badge.pdf { background: #dbeafe; color: #1d4ed8; }
.type-badge.video { background: #fce7f3; color: #be185d; }
.type-badge.blog { background: #dcfce7; color: #15803d; }
.type-badge.leetcode { background: #fef3c7; color: #b45309; }

.status-badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.pending { background: #fef3c7; color: #b45309; }
.status-badge.processing { background: #dbeafe; color: #1d4ed8; }
.status-badge.completed, .status-badge.approved { background: #dcfce7; color: #15803d; }
.status-badge.failed, .status-badge.rejected { background: #fee2e2; color: #dc2626; }

.resource-title {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 6px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.page-btn {
  padding: 8px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #64748b;
}
</style>
