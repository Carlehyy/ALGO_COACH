<template>
  <div class="topic-page">
    <div class="container">
      <h1>知识图谱</h1>
      <p class="subtitle">系统化学习算法知识体系</p>

      <div class="category-tabs">
        <button
          v-for="cat in categories"
          :key="cat.id"
          :class="['tab', { active: selectedCategory === cat.id }]"
          @click="selectCategory(cat.id)"
        >
          {{ cat.name }}
        </button>
      </div>

      <div v-if="loading" class="loading">加载中...</div>

      <div v-else class="topics-grid">
        <div
          v-for="topic in currentTopics"
          :key="topic.id"
          class="topic-card"
          @click="goToTopic(topic.id)"
        >
          <div class="topic-header">
            <h3>{{ topic.name }}</h3>
            <span class="difficulty" :class="'diff-' + topic.difficulty">
              {{ '⭐'.repeat(topic.difficulty) }}
            </span>
          </div>
          <p class="description">{{ topic.description || '暂无描述' }}</p>
          <div class="topic-meta">
            <span class="meta-item">📚 {{ topic.estimated_hours }}h</span>
            <span class="meta-item">⚡ 重要度 {{ topic.importance }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const categories = [
  { id: 'basic', name: '基础算法' },
  { id: 'data_structure', name: '数据结构' },
  { id: 'dp', name: '动态规划' },
  { id: 'graph', name: '图论' },
  { id: 'string', name: '字符串' },
  { id: 'math', name: '数学' }
]

const selectedCategory = ref('basic')
const loading = ref(true)
const topicTree = ref({})

const currentTopics = computed(() => {
  const catData = topicTree.value[selectedCategory.value]
  return catData?.topics || []
})

onMounted(async () => {
  await loadTopics()
})

async function loadTopics() {
  loading.value = true
  try {
    // TODO: 调用API获取知识点树
    // const data = await getTopicTree()
    // topicTree.value = data

    // 模拟数据
    await new Promise(resolve => setTimeout(resolve, 500))
  } catch (error) {
    console.error('加载失败', error)
  } finally {
    loading.value = false
  }
}

function selectCategory(catId) {
  selectedCategory.value = catId
}

function goToTopic(topicId) {
  router.push(`/note?topic=${topicId}`)
}
</script>

<style scoped>
.topic-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 36px;
  text-align: center;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 40px;
}

.category-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  overflow-x: auto;
  padding-bottom: 10px;
}

.tab {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.2s;
  white-space: nowrap;
}

.tab:hover {
  background: #e5e7eb;
}

.tab.active {
  background: #6366f1;
  color: white;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #999;
}

.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.topic-card {
  padding: 20px;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.topic-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.topic-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.topic-header h3 {
  font-size: 18px;
  color: #333;
  margin: 0;
}

.difficulty {
  font-size: 12px;
}

.diff-1 { color: #10b981; }
.diff-2 { color: #22c55e; }
.diff-3 { color: #eab308; }
.diff-4 { color: #f97316; }
.diff-5 { color: #ef4444; }

.description {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 15px;
  min-height: 40px;
}

.topic-meta {
  display: flex;
  gap: 15px;
  font-size: 12px;
  color: #999;
}
</style>
