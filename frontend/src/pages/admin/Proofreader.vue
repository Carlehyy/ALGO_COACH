<template>
  <div class="proofreader-page">
    <!-- 选择资源 -->
    <div class="resource-selector">
      <h3 class="section-title">📄 选择待校对的PDF</h3>
      <div class="selector-content">
        <select v-model="selectedResourceId" @change="loadResource" class="resource-select">
          <option value="">请选择一个已解析的PDF资源</option>
          <option v-for="resource in parsedResources" :key="resource.id" :value="resource.id">
            {{ resource.id }} - {{ resource.title }}
          </option>
        </select>
        <button @click="loadParsedResources" class="refresh-btn">🔄 刷新列表</button>
      </div>
    </div>

    <!-- 校对界面 -->
    <div v-if="currentResource" class="proofreader-container">
      <!-- 左侧：原始内容 -->
      <div class="panel original-panel">
        <div class="panel-header">
          <h4>📖 原始PDF内容</h4>
          <span class="panel-info">{{ currentResource.title }}</span>
        </div>
        <div class="panel-content">
          <div v-if="originalContent" class="content-viewer">
            <div v-html="renderMarkdown(originalContent)"></div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">📭</div>
            <div class="empty-text">暂无内容</div>
          </div>
        </div>
      </div>

      <!-- 中间：编辑区 -->
      <div class="panel editor-panel">
        <div class="panel-header">
          <h4>✏️ 校对编辑</h4>
          <div class="header-actions">
            <button @click="copyFromOriginal" class="action-btn secondary">📋 复制原文</button>
            <button @click="saveChanges" :disabled="isSaving" class="action-btn primary">
              {{ isSaving ? '保存中...' : '💾 保存修改' }}
            </button>
          </div>
        </div>
        <div class="panel-content">
          <div class="editor-toolbar">
            <button @click="insertFormat('**', '**')" class="toolbar-btn" title="粗体"><b>B</b></button>
            <button @click="insertFormat('*', '*')" class="toolbar-btn" title="斜体"><i>I</i></button>
            <button @click="insertFormat('```\n', '\n```')" class="toolbar-btn" title="代码块">&lt;/&gt;</button>
            <button @click="insertFormat('\n## ', '')" class="toolbar-btn" title="标题">H</button>
            <button @click="insertFormat('\n- ', '')" class="toolbar-btn" title="列表">•</button>
          </div>
          <textarea
            v-model="editedContent"
            class="content-editor"
            placeholder="在此编辑校对后的内容..."
            spellcheck="false"
          ></textarea>
          <div class="preview-area">
            <h5>预览</h5>
            <div v-html="renderMarkdown(editedContent)" class="markdown-preview"></div>
          </div>
        </div>
      </div>

      <!-- 右侧：AI建议 -->
      <div class="panel suggestions-panel">
        <div class="panel-header">
          <h4>🤖 AI优化建议</h4>
          <button @click="generateSuggestions" :disabled="isGenerating" class="action-btn">
            {{ isGenerating ? '生成中...' : '✨ 生成建议' }}
          </button>
        </div>
        <div class="panel-content">
          <div v-if="suggestions.length > 0" class="suggestions-list">
            <div v-for="(suggestion, index) in suggestions" :key="index" class="suggestion-item">
              <div class="suggestion-header">
                <span class="suggestion-type">{{ suggestion.type }}</span>
                <button @click="applySuggestion(index)" class="apply-btn">✅ 应用</button>
              </div>
              <div class="suggestion-content">{{ suggestion.text }}</div>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">💡</div>
            <div class="empty-text">点击"生成建议"获取AI优化</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 未选择资源时的提示 -->
    <div v-else class="no-selection">
      <div class="empty-icon">📄</div>
      <div class="empty-text">请先选择一个PDF资源进行校对</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/modules/admin'
import { marked } from 'marked'

const parsedResources = ref([])
const selectedResourceId = ref(null)
const currentResource = ref(null)
const originalContent = ref('')
const editedContent = ref('')
const suggestions = ref([])
const isSaving = ref(false)
const isGenerating = ref(false)

const loadParsedResources = async () => {
  try {
    const data = await adminApi.getResources({
      page: 1,
      page_size: 100,
      type: 'pdf',
      process_status: 'completed'
    })
    parsedResources.value = data.items
  } catch (error) {
    console.error('Failed to load parsed resources:', error)
  }
}

const loadResource = async () => {
  if (!selectedResourceId.value) {
    currentResource.value = null
    return
  }

  currentResource.value = parsedResources.value.find(r => r.id === selectedResourceId.value)

  // TODO: 加载解析后的内容
  originalContent.value = currentResource.value?.parse_result || ''
  editedContent.value = originalContent.value
}

const copyFromOriginal = () => {
  editedContent.value = originalContent.value
}

const saveChanges = async () => {
  isSaving.value = true
  try {
    // TODO: 调用保存API
    await adminApi.updateResourceStatus(currentResource.value.id, {
      parse_result: editedContent.value
    })
    alert('保存成功')
  } catch (error) {
    alert('保存失败: ' + error.message)
  } finally {
    isSaving.value = false
  }
}

const generateSuggestions = async () => {
  isGenerating.value = true
  try {
    // TODO: 调用AI生成建议
    suggestions.value = [
      {
        type: '格式优化',
        text: '建议将第三段调整为有序列表，提高可读性'
      },
      {
        type: '内容补充',
        text: '建议在"时间复杂度"部分添加具体示例'
      },
      {
        type: '术语规范',
        text: '建议统一使用"O(log n)"而非"O(logn)"'
      }
    ]
  } catch (error) {
    alert('生成失败: ' + error.message)
  } finally {
    isGenerating.value = false
  }
}

const applySuggestion = (index) => {
  const suggestion = suggestions.value[index]
  // TODO: 实现建议应用逻辑
  alert('已应用建议: ' + suggestion.type)
}

const insertFormat = (before, after) => {
  const textarea = document.querySelector('.content-editor')
  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const text = editedContent.value
  const selected = text.substring(start, end)

  const replacement = before + selected + after
  editedContent.value = text.substring(0, start) + replacement + text.substring(end)

  textarea.focus()
  textarea.setSelectionRange(start + before.length, start + before.length + selected.length)
}

const renderMarkdown = (content) => {
  if (!content) return ''
  try {
    return marked(content)
  } catch {
    return content
  }
}

onMounted(() => {
  loadParsedResources()
})
</script>

<style scoped>
.proofreader-page {
  max-width: 1800px;
  margin: 0 auto;
}

/* 资源选择器 */
.resource-selector {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px 0;
}

.selector-content {
  display: flex;
  gap: 12px;
  align-items: center;
}

.resource-select {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.refresh-btn {
  padding: 10px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  white-space: nowrap;
}

.refresh-btn:hover {
  background: #f8fafc;
}

/* 校对容器 */
.proofreader-container {
  display: grid;
  grid-template-columns: 1fr 1.5fr 1fr;
  gap: 20px;
  height: calc(100vh - 250px);
}

.panel {
  background: #fff;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.panel-header {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.panel-info {
  font-size: 12px;
  color: #64748b;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.action-btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #fff;
}

.action-btn.primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.action-btn.secondary {
  background: #f1f5f9;
  color: #475569;
}

.action-btn.secondary:hover {
  background: #e2e8f0;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

/* 原始内容面板 */
.content-viewer {
  font-size: 14px;
  line-height: 1.8;
  color: #334155;
}

.content-viewer :deep(h1),
.content-viewer :deep(h2),
.content-viewer :deep(h3) {
  margin-top: 20px;
  margin-bottom: 12px;
  color: #1e293b;
}

.content-viewer :deep(pre) {
  background: #f1f5f9;
  padding: 12px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
}

/* 编辑面板 */
.editor-toolbar {
  display: flex;
  gap: 6px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 16px;
}

.toolbar-btn {
  width: 32px;
  height: 32px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.toolbar-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.content-editor {
  width: 100%;
  min-height: 300px;
  padding: 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
}

.content-editor:focus {
  outline: none;
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}

.preview-area {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e2e8f0;
}

.preview-area h5 {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #64748b;
}

.markdown-preview {
  background: #f8fafc;
  padding: 16px;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.8;
}

/* 建议面板 */
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.suggestion-type {
  font-size: 13px;
  font-weight: 600;
  color: #3b82f6;
}

.apply-btn {
  padding: 6px 12px;
  background: #dcfce7;
  color: #15803d;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.apply-btn:hover {
  background: #bbf7d0;
}

.suggestion-content {
  padding: 12px;
  font-size: 13px;
  line-height: 1.6;
  color: #475569;
}

/* 空状态 */
.empty-state, .no-selection {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  color: #94a3b8;
}

/* 响应式 */
@media (max-width: 1200px) {
  .proofreader-container {
    grid-template-columns: 1fr;
    height: auto;
  }

  .panel {
    height: 600px;
  }
}
</style>
