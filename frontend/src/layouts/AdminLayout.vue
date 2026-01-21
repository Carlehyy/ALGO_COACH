<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="logo">
        <h1>🎯 管理后台</h1>
        <p class="subtitle">ACM算法学习平台</p>
      </div>

      <nav class="nav-menu">
        <router-link to="/admin/dashboard" class="nav-item">
          <span class="icon">📊</span>
          <span>数据概览</span>
        </router-link>
        <router-link to="/admin/resources" class="nav-item">
          <span class="icon">📚</span>
          <span>资源管理</span>
        </router-link>
        <router-link to="/admin/proofreader" class="nav-item">
          <span class="icon">✏️</span>
          <span>PDF校对</span>
        </router-link>
        <router-link to="/admin/notes/review" class="nav-item">
          <span class="icon">📝</span>
          <span>笔记审核</span>
        </router-link>
        <router-link to="/admin/users" class="nav-item">
          <span class="icon">👥</span>
          <span>用户管理</span>
        </router-link>
        <router-link to="/" class="nav-item external">
          <span class="icon">🔙</span>
          <span>返回首页</span>
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <div class="admin-info">
          <div class="admin-avatar">{{ adminAvatar }}</div>
          <div class="admin-details">
            <div class="admin-name">{{ adminName }}</div>
            <div class="admin-role">管理员</div>
          </div>
        </div>
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-header">
        <div class="header-title">
          <h2>{{ pageTitle }}</h2>
        </div>
        <div class="header-actions">
          <button @click="refreshData" class="action-btn">
            <span>🔄</span> 刷新
          </button>
        </div>
      </header>

      <div class="content-wrapper">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { adminApi } from '@/api/modules/admin'

const route = useRoute()
const router = useRouter()

const pageTitle = computed(() => {
  const titles = {
    '/admin/dashboard': '数据概览',
    '/admin/resources': '资源管理',
    '/admin/proofreader': 'PDF校对',
    '/admin/notes/review': '笔记审核',
    '/admin/users': '用户管理'
  }
  return titles[route.path] || '管理后台'
})

const adminName = computed(() => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.nickname || '管理员'
})

const adminAvatar = computed(() => {
  return adminName.value.charAt(0).toUpperCase()
})

const handleLogout = () => {
  localStorage.clear()
  router.push('/login')
}

const refreshData = () => {
  window.location.reload()
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #f5f7fa;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
  color: #fff;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.logo {
  padding: 24px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo h1 {
  font-size: 22px;
  font-weight: 700;
  margin: 0;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 12px;
  color: #94a3b8;
  margin: 4px 0 0 0;
}

.nav-menu {
  flex: 1;
  padding: 16px 0;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 14px 20px;
  color: #cbd5e1;
  text-decoration: none;
  transition: all 0.2s;
  border-left: 3px solid transparent;
  margin: 2px 0;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.nav-item.router-link-active {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
  border-left-color: #60a5fa;
}

.nav-item.external {
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 16px;
}

.icon {
  font-size: 20px;
  margin-right: 12px;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.admin-info {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.admin-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 16px;
  margin-right: 12px;
}

.admin-details {
  flex: 1;
}

.admin-name {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.admin-role {
  font-size: 12px;
  color: #94a3b8;
}

.logout-btn {
  width: 100%;
  padding: 10px;
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.3);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.top-header {
  background: #fff;
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-title h2 {
  margin: 0;
  font-size: 20px;
  color: #1e293b;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 8px 16px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.content-wrapper {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -260px;
    top: 0;
    bottom: 0;
    z-index: 100;
    transition: left 0.3s;
  }

  .sidebar.open {
    left: 0;
  }

  .main-content {
    width: 100%;
  }
}
</style>
