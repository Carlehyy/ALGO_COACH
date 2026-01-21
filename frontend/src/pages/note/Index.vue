<template>
  <div class="note-list-page">
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        <h1>算法笔记</h1>
        <p class="subtitle">L1-L4分层学习，由浅入深掌握算法</p>
      </div>

      <!-- 搜索和筛选 -->
      <div class="filters">
        <div class="search-box">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索笔记..."
            @keyup.enter="handleSearch"
          />
          <button class="btn-search" @click="handleSearch">搜索</button>
        </div>
        <div class="category-filter">
          <button
            v-for="cat in categories"
            :key="cat.id"
            :class="['category-btn', { active: selectedCategory === cat.id }]"
            @click="selectCategory(cat.id)"
          >
            {{ cat.name }}
          </button>
        </div>
      </div>

      <!-- 笔记列表 -->
      <div v-if="loading" class="loading">加载中...</div>

      <div v-else class="notes-grid">
        <div
          v-for="note in notes"
          :key="note.id"
          class="note-card"
          @click="goToNote(note.id)"
        >
          <div class="note-header">
            <h3>{{ note.title }}</h3>
            <span class="difficulty" :class="'diff-' + note.difficulty">
              {{ '⭐'.repeat(note.difficulty || 1) }}
            </span>
          </div>
          <p class="note-summary">{{ note.summary || '暂无摘要' }}</p>
          <div class="note-meta">
            <span class="meta-tag">📚 {{ note.topic_name || '算法' }}</span>
            <span class="meta-tag">👁 {{ note.view_count || 0 }}</span>
            <span class="meta-tag">⏱ {{ note.estimated_hours || 1 }}h</span>
          </div>
          <div class="note-layers">
            <span class="layer-badge">L1</span>
            <span class="layer-badge">L2</span>
            <span class="layer-badge">L3</span>
            <span class="layer-badge">L4</span>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="pagination">
        <button
          :disabled="currentPage === 1"
          @click="goToPage(currentPage - 1)"
          class="page-btn"
        >
          上一页
        </button>
        <span class="page-info">第 {{ currentPage }} / {{ totalPages }} 页</span>
        <button
          :disabled="currentPage === totalPages"
          @click="goToPage(currentPage + 1)"
          class="page-btn"
        >
          下一页
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { getNotes, searchNotes } from '@/api/note'

const router = useRouter()

const notes = ref([])
const loading = ref(true)
const searchKeyword = ref('')
const selectedCategory = ref('all')
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

const categories = [
  { id: 'all', name: '全部' },
  { id: 'basic', name: '基础算法' },
  { id: 'data_structure', name: '数据结构' },
  { id: 'dp', name: '动态规划' },
  { id: 'graph', name: '图论' },
  { id: 'string', name: '字符串' },
  { id: 'math', name: '数学' }
]

const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

onMounted(() => {
  loadNotes()
})

async function loadNotes() {
  loading.value = true
  try {
    // TODO: 调用API
    // const data = await getNotes({
    //   page: currentPage.value,
    //   page_size: pageSize.value,
    //   topic_id: selectedCategory.value === 'all' ? undefined : selectedCategory.value
    // })
    // notes.value = data.items
    // total.value = data.total

    // 模拟数据
    await new Promise(resolve => setTimeout(resolve, 500))
    notes.value = [
      {
        id: '1',
        title: '二分查找详解',
        summary: '在有序数组中快速查找目标元素的经典算法',
        difficulty: 2,
        topic_name: '基础算法',
        view_count: 120,
        estimated_hours: 2
      },
      {
        id: '2',
        title: '动态规划入门',
        summary: '理解DP的核心思想：最优子结构和重叠子问题',
        difficulty: 4,
        topic_name: '动态规划',
        view_count: 85,
        estimated_hours: 4
      }
    ]
    total.value = 15
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  if (!searchKeyword.value.trim()) {
    loadNotes()
    return
  }

  loading.value = true
  try {
    const data = await searchNotes(searchKeyword.value)
    notes.value = data
  } catch (error) {
    console.error('搜索失败', error)
  } finally {
    loading.value = false
  }
}

function selectCategory(catId) {
  selectedCategory.value = catId
  currentPage.value = 1
  loadNotes()
}

function goToPage(page) {
  currentPage.value = page
  loadNotes()
}

function goToNote(noteId) {
  router.push(`/note/${noteId}`)
}
</script>

<style scoped>
.note-list-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

h1 {
  font-size: 36px;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  font-size: 18px;
  color: #666;
}

.filters {
  margin-bottom: 30px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.search-box input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.search-box input:focus {
  outline: none;
  border-color: #6366f1;
}

.btn-search {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  cursor: pointer;
  font-weight: 600;
}

.btn-search:hover {
  background: #4f46e5;
}

.category-filter {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.category-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.category-btn:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.category-btn.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #999;
  font-size: 16px;
}

.notes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.note-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.note-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.2);
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.note-header h3 {
  font-size: 18px;
  margin: 0;
  color: #333;
}

.difficulty {
  font-size: 14px;
}

.diff-1 { color: #10b981; }
.diff-2 { color: #22c55e; }
.diff-3 { color: #eab308; }
.diff-4 { color: #f97316; }
.diff-5 { color: #ef4444; }

.note-summary {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.note-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.meta-tag {
  font-size: 12px;
  color: #999;
  padding: 4px 10px;
  background: #f3f4f6;
  border-radius: 4px;
}

.note-layers {
  display: flex;
  gap: 6px;
}

.layer-badge {
  padding: 4px 10px;
  border-radius: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-size: 11px;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 40px;
}

.page-btn {
  padding: 10px 24px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #6366f1;
  color: #6366f1;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #666;
}
</style>
