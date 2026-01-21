<template>
  <div class="note-detail-page">
    <div class="container">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading">加载中...</div>

      <!-- 笔记内容 -->
      <div v-else-if="note" class="note-content">
        <!-- 头部 -->
        <div class="note-header">
          <button class="btn-back" @click="goBack">← 返回</button>
          <h1>{{ note.title }}</h1>
          <div class="note-meta">
            <span class="meta-item">📚 {{ note.topic_name || '算法' }}</span>
            <span class="meta-item">⭐ 难度 {{ note.difficulty || 1 }}</span>
            <span class="meta-item">👁 {{ note.view_count || 0 }} 次浏览</span>
            <span class="meta-item">⏱ {{ note.estimated_hours || 1 }}h</span>
          </div>
        </div>

        <!-- L1-L4 标签页 -->
        <div class="layers-tabs">
          <button
            v-for="layer in layers"
            :key="layer.key"
            :class="['tab', { active: activeLayer === layer.key }]"
            @click="switchLayer(layer.key)"
          >
            <span class="tab-icon">{{ layer.icon }}</span>
            <span class="tab-label">{{ layer.label }}</span>
            <span class="tab-desc">{{ layer.desc }}</span>
          </button>
        </div>

        <!-- 内容区域 -->
        <div class="content-area">
          <div v-if="activeLayer === 'l1'" class="content-section">
            <h2>🎯 直观引入</h2>
            <div class="markdown-content" v-html="renderMarkdown(note.content_l1 || defaultContent.l1)"></div>
          </div>

          <div v-if="activeLayer === 'l2'" class="content-section">
            <h2>📐 核心原理</h2>
            <div class="markdown-content" v-html="renderMarkdown(note.content_l2 || defaultContent.l2)"></div>
          </div>

          <div v-if="activeLayer === 'l3'" class="content-section">
            <h2>💻 代码实现</h2>
            <div class="markdown-content" v-html="renderMarkdown(note.content_l3 || defaultContent.l3)"></div>
          </div>

          <div v-if="activeLayer === 'l4'" class="content-section">
            <h2>🔥 实战分析</h2>
            <div class="markdown-content" v-html="renderMarkdown(note.content_l4 || defaultContent.l4)"></div>
          </div>
        </div>

        <!-- 来源引用 -->
        <div v-if="note.sources && note.sources.length" class="sources-section">
          <h3>📚 参考资料</h3>
          <ul class="sources-list">
            <li v-for="source in note.sources" :key="source.id">
              <a :href="source.url" target="_blank" rel="noopener">
                {{ source.title }}
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const note = ref(null)
const loading = ref(true)
const activeLayer = ref('l1')

const layers = [
  { key: 'l1', icon: '🎯', label: 'L1 直观引入', desc: '生活类比' },
  { key: 'l2', icon: '📐', label: 'L2 核心原理', desc: '严谨推导' },
  { key: 'l3', icon: '💻', label: 'L3 代码实现', desc: '实战代码' },
  { key: 'l4', icon: '🔥', label: 'L4 实战分析', desc: '举一反三' }
]

const defaultContent = {
  l1: `## 直观引入

想象你要在一本1000页的字典中找一个单词...

**线性查找**：从头翻到尾，平均要翻500页。

**二分查找**：先翻到中间，如果目标在右半部分，就只在右半部分找，每次都能排除一半！

这就像玩游戏时"猜数字"，聪明的玩家会用二分法，每次猜中间值，这样最多猜10次就能在0-1023中找到任何数字！`,
  l2: `## 核心原理

### 算法思想

二分查找基于**分治策略**，将问题规模不断缩小。

### 时间复杂度

- **最好情况**：O(1) - 目标恰好是中间元素
- **最坏情况**：O(log n) - 持续缩小到只剩1个元素
- **平均情况**：O(log n)

### 空间复杂度

O(1) - 只需要常数级别的额外空间`,
  l3: `## 代码实现

\`\`\`python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
\`\`\``,
  l4: `## 实战分析

### LeetCode 704. 二分查找

**示例**：
输入：nums = [-1,0,3,5,9,12], target = 9
输出：4

### 常见陷阱

- 整数溢出：计算 mid 时使用 left + (right - left) / 2
- 循环终止条件：while (left <= right)
- 边界更新：避免死循环`
}

onMounted(async () => {
  const noteId = route.params.id
  if (noteId) {
    await loadNote(noteId)
  } else {
    loading.value = false
  }
})

async function loadNote(noteId) {
  loading.value = true
  try {
    // TODO: 调用API
    await new Promise(resolve => setTimeout(resolve, 300))
    note.value = {
      id: noteId,
      title: '二分查找详解',
      content_l1: defaultContent.l1,
      content_l2: defaultContent.l2,
      content_l3: defaultContent.l3,
      content_l4: defaultContent.l4,
      topic_name: '基础算法',
      difficulty: 2,
      view_count: 120,
      estimated_hours: 2
    }
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    loading.value = false
  }
}

function switchLayer(layer) {
  activeLayer.value = layer
}

function goBack() {
  router.back()
}

function renderMarkdown(content) {
  if (!content) return ''
  content = content.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
  content = content.replace(/^### (.*$)/gm, '<h4>$1</h4>')
  content = content.replace(/^## (.*$)/gm, '<h3>$1</h3>')
  content = content.replace(/^# (.*$)/gm, '<h2>$1</h2>')
  content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  content = content.replace(/\n/g, '<br>')
  return content
}
</script>

<style scoped>
.note-detail-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 20px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
}

.note-header {
  background: white;
  padding: 30px;
  border-radius: 12px 12px 0 0;
}

.btn-back {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  margin-bottom: 20px;
}

.layers-tabs {
  background: white;
  padding: 0 30px;
  border-radius: 0 0 12px 12px;
  display: flex;
  gap: 10px;
}

.tab {
  flex: 1;
  padding: 20px;
  border: none;
  border-bottom: 3px solid transparent;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
}

.tab.active {
  border-bottom-color: #6366f1;
  color: #6366f1;
}

.content-area {
  background: white;
  padding: 40px;
  border-radius: 0 0 12px 12px;
  min-height: 400px;
}

.markdown-content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 20px;
  border-radius: 8px;
  overflow-x: auto;
}
</style>
