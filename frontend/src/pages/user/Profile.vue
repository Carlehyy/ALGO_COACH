<template>
  <div class="profile-page">
    <div class="container">
      <div class="profile-card">
        <div class="avatar-section">
          <img :src="user?.avatar || defaultAvatar" alt="头像" class="avatar" />
          <button class="btn-upload">更换头像</button>
        </div>

        <div class="info-section">
          <h2>个人信息</h2>
          <form @submit.prevent="handleUpdate">
            <div class="form-row">
              <label>邮箱</label>
              <input v-model="form.email" type="email" disabled />
            </div>
            <div class="form-row">
              <label>昵称</label>
              <input v-model="form.nickname" type="text" />
            </div>
            <div class="form-row">
              <label>LeetCode用户名</label>
              <input v-model="form.leetcode_username" type="text" />
            </div>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ loading ? '保存中...' : '保存' }}
            </button>
          </form>
        </div>

        <div class="points-section">
          <h2>积分信息</h2>
          <div class="points-cards">
            <div class="points-card">
              <div class="points-value">{{ balance.points || 0 }}</div>
              <div class="points-label">积分余额</div>
            </div>
            <div class="points-card">
              <div class="points-value">{{ balance.total_recharged || 0 }}</div>
              <div class="points-label">累计充值</div>
            </div>
            <div class="points-card">
              <div class="points-value">{{ balance.total_consumed || 0 }}</div>
              <div class="points-label">累计消费</div>
            </div>
          </div>
          <router-link to="/point" class="btn btn-recharge">
            充值积分
          </router-link>
        </div>

        <div class="ability-section">
          <h2>能力评分</h2>
          <div class="ability-score">
            <span class="score-value">{{ user?.ability_score || 0 }}</span>
            <span class="score-label">分</span>
          </div>
          <p class="ability-desc">基于您的学习进度和测试成绩评估</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { updateUser, getBalance } from '@/api/user'

const userStore = useUserStore()
const user = ref(userStore.user)

const form = ref({
  email: user.value?.email || '',
  nickname: user.value?.nickname || '',
  leetcode_username: user.value?.leetcode_username || ''
})

const balance = ref({
  points: 0,
  total_recharged: 0,
  total_consumed: 0
})

const loading = ref(false)
const defaultAvatar = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Ccircle cx="50" cy="50" r="50" fill="%23ddd"/%3E%3Ctext x="50" y="60" text-anchor="middle" fill="%23666" font-size="40"%3E%3F%3C/text%3E%3C/svg%3E'

onMounted(async () => {
  await loadBalance()
})

async function loadBalance() {
  try {
    balance.value = await getBalance()
  } catch (error) {
    console.error('获取积分信息失败', error)
  }
}

async function handleUpdate() {
  loading.value = true
  try {
    const updated = await updateUser({
      nickname: form.value.nickname,
      leetcode_username: form.value.leetcode_username
    })
    userStore.updateUser(updated)
    user.value = updated
    alert('保存成功')
  } catch (error) {
    alert('保存失败: ' + (error.response?.data?.message || error.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.avatar-section {
  text-align: center;
  margin-bottom: 40px;
}

.avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 15px;
}

.btn-upload {
  padding: 8px 20px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-upload:hover {
  border-color: #6366f1;
  color: #6366f1;
}

.info-section,
.points-section,
.ability-section {
  margin-bottom: 40px;
}

h2 {
  font-size: 20px;
  margin-bottom: 20px;
  color: #333;
}

.form-row {
  display: flex;
  margin-bottom: 15px;
  align-items: center;
}

.form-row label {
  width: 150px;
  font-weight: 500;
  color: #666;
}

.form-row input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.form-row input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.points-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.points-card {
  padding: 20px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.points-value {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 5px;
}

.points-label {
  font-size: 14px;
  opacity: 0.9;
}

.ability-score {
  text-align: center;
  font-size: 48px;
  font-weight: 700;
  color: #6366f1;
}

.score-label {
  font-size: 20px;
  color: #666;
  margin-left: 5px;
}

.ability-desc {
  text-align: center;
  color: #999;
  margin-top: 10px;
}

.btn {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #6366f1;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #4f46e5;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-recharge {
  display: block;
  width: 100%;
  text-align: center;
  background: #10b981;
  color: white;
  text-decoration: none;
}

.btn-recharge:hover {
  background: #059669;
}
</style>
