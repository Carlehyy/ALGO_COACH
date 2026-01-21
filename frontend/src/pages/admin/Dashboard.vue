<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon users">👥</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.users_count }}</div>
          <div class="stat-label">总用户数</div>
          <div class="stat-trend positive">+12% 本周</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon notes">📝</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.notes_count }}</div>
          <div class="stat-label">笔记总数</div>
          <div class="stat-trend positive">+8% 本周</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon resources">📚</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.resources_count }}</div>
          <div class="stat-label">资源总数</div>
          <div class="stat-trend positive">+5% 本周</div>
        </div>
      </div>

      <div class="stat-card warning">
        <div class="stat-icon pending">⏳</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.pending_reviews }}</div>
          <div class="stat-label">待审核</div>
          <div class="stat-trend">需要处理</div>
        </div>
      </div>
    </div>

    <!-- 收入统计 -->
    <div class="revenue-section">
      <h3 class="section-title">💰 收入统计</h3>
      <div class="revenue-grid">
        <div class="revenue-card">
          <div class="revenue-label">今日收入</div>
          <div class="revenue-value">¥{{ stats.today_revenue }}</div>
        </div>
        <div class="revenue-card">
          <div class="revenue-label">本周收入</div>
          <div class="revenue-value">¥{{ stats.week_revenue }}</div>
        </div>
        <div class="revenue-card">
          <div class="revenue-label">本月收入</div>
          <div class="revenue-value">¥{{ stats.month_revenue }}</div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <h3 class="section-title">⚡ 快捷操作</h3>
      <div class="actions-grid">
        <router-link to="/admin/resources" class="action-card">
          <span class="action-icon">📤</span>
          <span class="action-title">上传资源</span>
          <span class="action-desc">添加PDF、视频等学习资料</span>
        </router-link>

        <router-link to="/admin/proofreader" class="action-card">
          <span class="action-icon">✏️</span>
          <span class="action-title">PDF校对</span>
          <span class="action-desc">校对解析后的PDF内容</span>
        </router-link>

        <router-link to="/admin/notes/review" class="action-card">
          <span class="action-icon">✅</span>
          <span class="action-title">笔记审核</span>
          <span class="action-desc">审核待发布的笔记内容</span>
        </router-link>

        <router-link to="/admin/users" class="action-card">
          <span class="action-icon">👥</span>
          <span class="action-title">用户管理</span>
          <span class="action-desc">管理用户状态和权限</span>
        </router-link>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="recent-activity">
      <h3 class="section-title">📋 最近活动</h3>
      <div class="activity-list">
        <div class="activity-item" v-for="activity in recentActivities" :key="activity.id">
          <span class="activity-icon">{{ activity.icon }}</span>
          <div class="activity-content">
            <div class="activity-text">{{ activity.text }}</div>
            <div class="activity-time">{{ activity.time }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/modules/admin'

const stats = ref({
  users_count: 0,
  notes_count: 0,
  resources_count: 0,
  today_revenue: 0,
  week_revenue: 0,
  month_revenue: 0,
  pending_reviews: 0
})

const recentActivities = ref([
  { id: 1, icon: '👤', text: '新用户注册：user@example.com', time: '5分钟前' },
  { id: 2, icon: '📚', text: '新资源上传：算法导论.pdf', time: '15分钟前' },
  { id: 3, icon: '✅', text: '笔记已发布：二分查找', time: '1小时前' },
  { id: 4, icon: '💰', text: '订单完成：99积分套餐', time: '2小时前' },
])

const loadDashboard = async () => {
  try {
    const data = await adminApi.getDashboard()
    stats.value = data
  } catch (error) {
    console.error('Failed to load dashboard:', error)
  }
}

onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-card.warning {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.stat-icon.users {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
}

.stat-icon.notes {
  background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
}

.stat-icon.resources {
  background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%);
}

.stat-icon.pending {
  background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 12px;
  color: #64748b;
}

.stat-trend.positive {
  color: #10b981;
}

/* 收入统计 */
.revenue-section {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px 0;
}

.revenue-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.revenue-card {
  padding: 20px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 8px;
  text-align: center;
}

.revenue-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 8px;
}

.revenue-value {
  font-size: 28px;
  font-weight: 700;
  color: #10b981;
}

/* 快捷操作 */
.quick-actions {
  margin-bottom: 32px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
}

.action-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.action-icon {
  font-size: 40px;
}

.action-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.action-desc {
  font-size: 13px;
  color: #64748b;
}

/* 最近活动 */
.recent-activity {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  transition: background 0.2s;
}

.activity-item:hover {
  background: #f8fafc;
}

.activity-icon {
  font-size: 24px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 8px;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  color: #1e293b;
  margin-bottom: 2px;
}

.activity-time {
  font-size: 12px;
  color: #94a3b8;
}
</style>
