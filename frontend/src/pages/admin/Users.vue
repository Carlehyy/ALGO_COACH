<template>
  <div class="users-page">
    <!-- 筛选区域 -->
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-group">
          <label>用户状态</label>
          <select v-model="filters.status" @change="loadUsers" class="form-control">
            <option value="">全部</option>
            <option value="0">已禁用</option>
            <option value="1">正常</option>
          </select>
        </div>
        <div class="filter-group">
          <label>搜索</label>
          <input v-model="filters.search" type="text" class="form-control" placeholder="邮箱/昵称">
        </div>
        <button @click="handleSearch" class="search-btn">🔍 搜索</button>
        <button @click="resetFilters" class="reset-btn">🔄 重置</button>
      </div>
    </div>

    <!-- 用户列表 -->
    <div class="users-list">
      <div class="list-header">
        <h3>用户列表 ({{ pagination.total }})</h3>
        <button @click="loadUsers" class="refresh-btn">🔄 刷新</button>
      </div>

      <div v-if="users.length === 0" class="empty-state">
        <div class="empty-icon">👥</div>
        <div class="empty-text">暂无用户数据</div>
      </div>

      <div v-else class="table-container">
        <table class="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>邮箱</th>
              <th>昵称</th>
              <th>积分</th>
              <th>角色</th>
              <th>状态</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.nickname }}</td>
              <td>
                <span :class="['points-badge', user.points > 100 ? 'high' : 'normal']">
                  {{ user.points }} 积分
                </span>
              </td>
              <td>
                <span :class="['role-badge', user.role]">
                  {{ getRoleLabel(user.role) }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', user.status]">
                  {{ user.status === '1' ? '正常' : '已禁用' }}
                </span>
              </td>
              <td>{{ formatDate(user.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="viewUser(user)" class="action-btn view" title="查看详情">👁️</button>
                  <button
                    @click="toggleUserStatus(user)"
                    :class="['action-btn', user.status === '1' ? 'disable' : 'enable']"
                    :title="user.status === '1' ? '禁用' : '启用'"
                  >
                    {{ user.status === '1' ? '🔒' : '🔓' }}
                  </button>
                  <button @click="adjustPoints(user)" class="action-btn points" title="调整积分">💎</button>
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

    <!-- 用户详情弹窗 -->
    <div v-if="selectedUser" class="user-modal" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>用户详情</h3>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>

        <div class="modal-body">
          <div class="user-profile">
            <div class="avatar">{{ selectedUser.nickname?.charAt(0).toUpperCase() || 'U' }}</div>
            <div class="user-info">
              <div class="user-name">{{ selectedUser.nickname }}</div>
              <div class="user-email">{{ selectedUser.email }}</div>
            </div>
          </div>

          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label">用户ID</span>
              <span class="detail-value">{{ selectedUser.id }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">积分余额</span>
              <span class="detail-value points">{{ selectedUser.points }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">角色</span>
              <span :class="['detail-value', 'role', selectedUser.role]">
                {{ getRoleLabel(selectedUser.role) }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">状态</span>
              <span :class="['detail-value', 'status', selectedUser.status === '1' ? 'active' : 'inactive']">
                {{ selectedUser.status === '1' ? '正常' : '已禁用' }}
              </span>
            </div>
            <div class="detail-item">
              <span class="detail-label">注册时间</span>
              <span class="detail-value">{{ formatDate(selectedUser.created_at) }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">最后登录</span>
              <span class="detail-value">{{ formatDate(selectedUser.last_login_at) }}</span>
            </div>
          </div>

          <!-- 统计信息 -->
          <div class="stats-section">
            <h4>使用统计</h4>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ selectedUser.notes_count || 0 }}</div>
                <div class="stat-label">笔记数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ selectedUser.chats_count || 0 }}</div>
                <div class="stat-label">对话数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ selectedUser.orders_count || 0 }}</div>
                <div class="stat-label">订单数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">¥{{ selectedUser.total_spent || 0 }}</div>
                <div class="stat-label">累计消费</div>
              </div>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closeModal" class="footer-btn secondary">关闭</button>
          <button v-if="selectedUser.status === '1'" @click="toggleFromModal" class="footer-btn danger">🔒 禁用用户</button>
          <button v-else @click="toggleFromModal" class="footer-btn primary">🔓 启用用户</button>
        </div>
      </div>
    </div>

    <!-- 调整积分弹窗 -->
    <div v-if="pointsUser" class="points-modal" @click.self="closePointsModal">
      <div class="modal-content small">
        <div class="modal-header">
          <h3>调整积分</h3>
          <button @click="closePointsModal" class="close-btn">✕</button>
        </div>

        <div class="modal-body">
          <div class="user-summary">
            <span>{{ pointsUser.nickname }}</span>
            <span>当前积分: {{ pointsUser.points }}</span>
          </div>

          <div class="points-form">
            <div class="form-group">
              <label>操作类型</label>
              <select v-model="pointsForm.type" class="form-control">
                <option value="add">增加积分</option>
                <option value="subtract">扣除积分</option>
                <option value="set">设置积分</option>
              </select>
            </div>

            <div class="form-group">
              <label>积分数量</label>
              <input v-model.number="pointsForm.amount" type="number" min="0" class="form-control" placeholder="请输入积分数量">
            </div>

            <div class="form-group">
              <label>备注</label>
              <input v-model="pointsForm.reason" type="text" class="form-control" placeholder="请输入调整原因">
            </div>

            <div class="preview" v-if="pointsForm.amount">
              <span>调整后积分: </span>
              <strong>{{ calculateNewPoints }}</strong>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="closePointsModal" class="footer-btn secondary">取消</button>
          <button @click="confirmPointsAdjustment" class="footer-btn primary">确认调整</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { adminApi } from '@/api/modules/admin'

const users = ref([])
const selectedUser = ref(null)
const pointsUser = ref(null)

const filters = ref({
  status: '',
  search: ''
})

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

const pointsForm = ref({
  type: 'add',
  amount: null,
  reason: ''
})

const totalPages = computed(() => {
  return Math.ceil(pagination.value.total / pagination.value.page_size)
})

const calculateNewPoints = computed(() => {
  if (!pointsForm.value.amount) return pointsUser.value?.points || 0

  const current = pointsUser.value?.points || 0
  const amount = pointsForm.value.amount

  switch (pointsForm.value.type) {
    case 'add':
      return current + amount
    case 'subtract':
      return Math.max(0, current - amount)
    case 'set':
      return amount
    default:
      return current
  }
})

const loadUsers = async () => {
  try {
    const data = await adminApi.getUsers({
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      status: filters.value.status
    })
    users.value = data.items
    pagination.value.total = data.total
  } catch (error) {
    console.error('Failed to load users:', error)
  }
}

const handleSearch = () => {
  pagination.value.page = 1
  loadUsers()
}

const resetFilters = () => {
  filters.value = { status: '', search: '' }
  pagination.value.page = 1
  loadUsers()
}

const viewUser = (user) => {
  selectedUser.value = user
}

const closeModal = () => {
  selectedUser.value = null
}

const toggleUserStatus = async (user) => {
  const newStatus = user.status === '1' ? '0' : '1'
  const action = newStatus === '1' ? '启用' : '禁用'

  if (!confirm(`确定要${action}用户"${user.nickname}"吗？`)) return

  try {
    await adminApi.updateUserStatus(user.id, newStatus)
    alert(`${action}成功`)
    loadUsers()
  } catch (error) {
    alert(`${action}失败: ` + error.message)
  }
}

const toggleFromModal = async () => {
  await toggleUserStatus(selectedUser.value)
  closeModal()
}

const adjustPoints = (user) => {
  pointsUser.value = user
  pointsForm.value = {
    type: 'add',
    amount: null,
    reason: ''
  }
}

const closePointsModal = () => {
  pointsUser.value = null
}

const confirmPointsAdjustment = async () => {
  if (!pointsForm.value.amount || pointsForm.value.amount <= 0) {
    alert('请输入有效的积分数量')
    return
  }

  if (!pointsForm.value.reason) {
    alert('请输入调整原因')
    return
  }

  try {
    // TODO: 调用积分调整API
    alert('积分调整成功')
    closePointsModal()
    loadUsers()
  } catch (error) {
    alert('调整失败: ' + error.message)
  }
}

const getRoleLabel = (role) => {
  const labels = {
    user: '普通用户',
    admin: '管理员',
    vip: 'VIP用户'
  }
  return labels[role] || role
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

const prevPage = () => {
  if (pagination.value.page > 1) {
    pagination.value.page--
    loadUsers()
  }
}

const nextPage = () => {
  if (pagination.value.page < totalPages.value) {
    pagination.value.page++
    loadUsers()
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.users-page {
  max-width: 1400px;
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
}

.search-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
}

.reset-btn {
  padding: 10px 20px;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.reset-btn:hover {
  background: #e2e8f0;
}

/* 用户列表 */
.users-list {
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

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th {
  text-align: left;
  padding: 12px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  border-bottom: 2px solid #e2e8f0;
}

.users-table td {
  padding: 12px;
  font-size: 14px;
  border-bottom: 1px solid #f1f5f9;
}

.points-badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.points-badge.normal { background: #f1f5f9; color: #64748b; }
.points-badge.high { background: #fef3c7; color: #b45309; }

.role-badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.role-badge.user { background: #f1f5f9; color: #64748b; }
.role-badge.admin { background: #fee2e2; color: #dc2626; }
.role-badge.vip { background: #fef3c7; color: #b45309; }

.status-badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge[style*="active"] { background: #dcfce7; color: #15803d; }
.status-badge[style*="inactive"] { background: #fee2e2; color: #dc2626; }

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

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
.user-modal, .points-modal {
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
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-content.small {
  max-width: 450px;
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

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  border-radius: 12px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.user-name {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.user-email {
  font-size: 14px;
  color: #64748b;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
}

.detail-label {
  font-size: 12px;
  color: #64748b;
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
  color: #1e293b;
}

.detail-value.points {
  color: #f59e0b;
  font-size: 18px;
}

.detail-value.role.admin { color: #dc2626; }
.detail-value.role.vip { color: #f59e0b; }

.detail-value.status.active { color: #10b981; }
.detail-value.status.inactive { color: #ef4444; }

.stats-section {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

.stats-section h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #1e293b;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.stat-item {
  padding: 16px;
  background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #15803d;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
}

/* 积分调整 */
.user-summary {
  display: flex;
  justify-content: space-between;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 20px;
  font-size: 14px;
}

.points-form {
  display: flex;
  flex-direction: column;
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

.preview {
  padding: 12px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 8px;
  font-size: 14px;
  text-align: center;
}

.preview strong {
  font-size: 18px;
  color: #b45309;
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
}

.footer-btn.primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
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
