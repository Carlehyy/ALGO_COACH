<template>
  <div class="note-review-page">
    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-group">
          <label>状态</label>
          <select v-model="filters.status" @change="loadNotes" class="form-control">
            <option value="">全部</option>
            <option value="1">待审核</option>
            <option value="2">已发布</option>
          </select>
        </div>
        <div class="filter-group">
          <label>知识点</label>
          <input v-model="filters.topic_id" type="text" class="form-control" placeholder="输入知识点ID">
        </div>
        <button @click="loadNotes" class="search-btn">🔍 搜索</button>
      </div>
    </div>

    <!-- 笔记列表 -->
    <div class="notes-list">
      <div class="list-header">
        <h3>待审核笔记 ({{ notes.length }})</h3>
        <div class="header-actions">
          <button @click="loadNotes" class="refresh-btn">🔄 刷新</button>
        </div>
      </div>

      <div v-if="notes.length === 0" class="empty-state">
        <div class="empty-icon">📝</div>
        <div class="empty-text">暂无待审核笔记</div>
      </div>

      <div v-else class="notes-grid">
        <div v-for="note in notes" :key="note.id" class="note-card">
          <div class="note-header">
            <span class="note-topic">{{ note.topic_id }}</span>
            <span :class="['note-status', note.status === 1 ? 'pending' : 'published']">
              {{ note.status === 1 ? '待审核' : '已发布' }}
            </span>
          </div>

          <div class="note-layers">
            <div class="layer-item" v-if="note.content_l1">
              <span class="layer-label">L1 直观引入</span>
              <div class="layer-preview">{{ getPreview(note.content_l1) }}</div>
            </div>
            <div class="layer-item" v-if="note.content_l2">
              <span class="layer-label">L2 核心原理</span>
              <div class="layer-preview">{{ getPreview(note.content_l2) }}</div>
            </div>
            <div class="layer-item" v-if="note.content_l3">
              <span class="layer-label">L3 代码实现</span>
              <div class="layer-preview">{{ getPreview(note.content_l3) }}</div>
            </div>
            <div class="layer-item" v-if="note.content_l4">
              <span class="layer-label">L4 实战分析</span>
              <div class="layer-preview">{{ getPreview(note.content_l4) }}</div>
            </div>
          </div>

          <div class="note-quality">
            <span class="quality-label">质量评分</span>
            <div class="quality-score">
              <span class="score">{{ note.quality_score || 0 }}</span>
              <span class="score-max">/100</span>
            </div>
          </div>

          <div class="note-actions">
            <button @click="viewNote(note)" class="action-btn view">👁️ 查看</button>
            <button @click="publishNote(note)" class="action-btn publish" v-if="note.status === 1">✅ 发布</button>
            <button @click="rejectNote(note)" class="action-btn reject" v-if="note.status === 1">❌ 退回</button>
            <button @click="generateNote(note)" class="action-btn generate">🔄 重新生成</button>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="pagination.total > 0" class="pagination">
        <button @click="prevPage" :disabled="pagination.page === 1" class="page-btn">上一页</button>
        <span class="page-info">第 {{ pagination.page }} 页，共 {{ totalPages }} 页</span>
        <button @click="nextPage" :disabled="pagination.page >= totalPages" class="page-btn">下一页</button>
      </div>
    </div>

    <!-- 笔记详情弹窗 -->
    <div v-if="selectedNote" class="note-modal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ selectedNote.topic_id }} - 笔记详情</h3>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <div class="modal-body">
          <div class="detail-tabs">
            <button
              v-for="layer in layers"
              :key="layer.key"
              :class="['tab-btn', { active: activeLayer === layer.key }]"
              @click="activeLayer = layer.key"
            >
              <span class="tab-icon">{{ layer.icon }}</span>
              {{ layer.label }}
            </button>
          </div>

          <div class="detail-content">
            <div v-if="activeLayer === 'l1'" class="layer-section">
              <h4>🎯 直观引入</h4>
              <div v-html="renderMarkdown(selectedNote.content_l1)" class="markdown-content"></div>
            </div>
            <div v-if="activeLayer === 'l2'" class="layer-section">
              <h4>🔬 核心原理</h4>
              <div v-html="renderMarkdown(selectedNote.content_l2)" class="markdown-content"></div>
            </div>
            <div v-if="activeLayer === 'l3'" class="layer-section">
              <h4>💻 代码实现</h4>
              <div v-html="renderMarkdown(selectedNote.content_l3)" class="markdown-content"></div>
            </div>
            <div v-if="activeLayer === 'l4'" class="layer-section">
              <h4>⚔️ 实战分析</h4>
              <div v-html="renderMarkdown(selectedNote.content_l4)" class="markdown-content"></div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="footer-btn secondary">关闭</button>
          <button v-if="selectedNote.status === 1" @click="publishFromModal" class="footer-btn primary">✅ 发布笔记</button>
          <button v-if="selectedNote.status === 1" @click="rejectFromModal" class="footer-btn danger">❌ 退回修改</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminApi } from '@/api/modules/admin'
import { marked } from 'marked'

const notes = ref([])
const selectedNote = ref(null)
const activeLayer = ref('l1')
const isProcessing = ref(false)

const filters = ref({
  status: '1',
  topic_id: ''
})

const pagination = ref({
  page: 1,
  page_size: 12,
  total: 0
})

const layers = [
  { key: 'l1', icon: '🎯', label: 'L1 直观引入' },
  { key: 'l2', icon: '🔬', label: 'L2 核心原理' },
  { key: 'l3', icon: '💻', label: 'L3 代码实现' },
  { key: 'l4', icon: '⚔️', label: 'L4 实战分析' }
]

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.page_size)
})

const loadNotes = async () => {
  try {
    const data = await adminApi.getPendingNotes({
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: filters.value.status,
      topic_id: filters.value.topic_id
    })
    notes.value = data.items
    pagination.value.total = data.total
  } catch (error) {
    console.error('Failed to load notes:', error)
  }
}

const viewNote = (note) => {
  selectedNote.value = note
  activeLayer.value = 'l1'
}

const closeModal = () => {
  selectedNote.value = null
}

const publishNote = async (note) => {
  if (!confirm(`确定要发布笔记"${note.topic_id}"吗？`)) return

  try {
    await adminApi.publishNote(note.id)
    alert('发布成功')
    loadNotes()
  } catch (error) {
    alert('发布失败: ' + error.message)
  }
}

const rejectNote = async (note) => {
  const reason = prompt('请输入退回原因：')
  if (!reason) return

  try {
    await adminApi.rejectNote(note.id, reason)
    alert('已退回')
    loadNotes()
  } catch (error) {
    alert('退回失败: ' + error.message)
  }
}

const generateNote = async (note) => {
  if (!confirm(`确定要重新生成笔记"${note.topic_id}"吗？`)) return

  isProcessing.value = true
  try {
    await adminApi.generateNote(note.id)
    alert('生成任务已触发，请稍后查看')
  } catch (error) {
    alert('触发失败: ' + error.message)
  } finally {
    isProcessing.value = false
  }
}

const publishFromModal = async () => {
  await publishNote(selectedNote.value)
  closeModal()
}

const rejectFromModal = async () => {
  await rejectNote(selectedNote.value)
  closeModal()
}

const getPreview = (content) => {
  if (!content) return '暂无内容'
  const text = content.replace(/[#*`>\-\[\]()]/g, '')
  return text.length > 100 ? text.substring(0, 100) + '...' : text
}

const renderMarkdown = (content) => {
  if (!content) return '<p class="no-content">暂无内容</p>'
  try {
    return marked(content)
  } catch {
    return content
  }
}

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    loadNotes()
  }
}

const nextPage = () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++
    loadNotes()
  }
}

onMounted(() => {
  loadNotes()
})
</script>

<style scoped>
.note-review-page {
  max-width: 1600px;
  margin: 0 auto;
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
  gap: 12px;
  align-items: center;
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

.form-control {
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.search-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
}

.search-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

/* 笔记列表 */
.notes-list {
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

/* 笔记卡片网格 */
.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.note-card {
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: all 0.2s;
}

.note-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.note-topic {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.note-status {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.note-status.pending {
  background: #fef3c7;
  color: #b45309;
}

.note-status.published {
  background: #dcfce7;
  color: #15803d;
}

.note-layers {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-item {
  padding: 8px 12px;
  background: #f8fafc;
  border-radius: 6px;
}

.layer-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  display: block;
  margin-bottom: 4px;
}

.layer-preview {
  font-size: 13px;
  color: #475569;
  line-height: 1.5;
}

.note-quality {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 8px;
}

.quality-label {
  font-size: 14px;
  color: #15803d;
  font-weight: 500;
}

.quality-score {
  font-size: 24px;
  font-weight: 700;
  color: #15803d;
}

.score-max {
  font-size: 14px;
  color: #64748b;
}

.note-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 8px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background: #fff;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-btn.view { border-color: #3b82f6; color: #3b82f6; }
.action-btn.publish { border-color: #10b981; color: #10b981; }
.action-btn.reject { border-color: #ef4444; color: #ef4444; }
.action-btn.generate { border-color: #f59e0b; color: #f59e0b; }

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.page-btn {
  padding: 8px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
}

.page-btn:hover:not(:disabled) {
  background: #f8fafc;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #64748b;
}

/* 弹窗 */
.note-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #1e293b;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f1f5f9;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  color: #64748b;
}

.close-btn:hover {
  background: #e2e8f0;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.detail-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.tab-btn {
  padding: 10px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: #f8fafc;
}

.tab-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #fff;
  border-color: transparent;
}

.tab-icon {
  font-size: 16px;
}

.layer-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.layer-section h4 {
  margin: 0 0 16px 0;
  font-size: 18px;
  color: #1e293b;
}

.markdown-content {
  font-size: 15px;
  line-height: 1.8;
  color: #334155;
}

.markdown-content :deep(pre) {
  background: #f1f5f9;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin-top: 24px;
  margin-bottom: 12px;
  color: #1e293b;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e2e8f0;
}

.footer-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.footer-btn.primary {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #fff;
}

.footer-btn.danger {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: #fff;
}

.footer-btn.secondary {
  background: #f1f5f9;
  color: #475569;
}
</style>
