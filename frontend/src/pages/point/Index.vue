<template>
  <div class="point-page">
    <div class="container">
      <h1>积分中心</h1>

      <!-- 余额卡片 -->
      <div class="balance-card">
        <div class="balance-info">
          <div class="balance-label">当前余额</div>
          <div class="balance-value">{{ balance.points || 0 }}</div>
          <div class="balance-unit">积分</div>
        </div>
        <div class="balance-stats">
          <div class="stat-item">
            <div class="stat-value">{{ balance.total_recharged || 0 }}</div>
            <div class="stat-label">累计充值</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ balance.total_consumed || 0 }}</div>
            <div class="stat-label">累计消费</div>
          </div>
        </div>
      </div>

      <!-- 充值套餐 -->
      <section class="packages-section">
        <h2>充值套餐</h2>
        <div class="packages-grid">
          <div
            v-for="pkg in packages"
            :key="pkg.id"
            class="package-card"
            @click="selectPackage(pkg)"
          >
            <div class="package-name">{{ pkg.name }}</div>
            <div class="package-points">
              <span class="points-value">{{ pkg.total_points }}</span>
              <span class="points-unit">积分</span>
            </div>
            <div class="package-price">
              <span class="price-value">¥{{ (pkg.price / 100).toFixed(2) }}</span>
            </div>
            <div v-if="pkg.bonus_points > 0" class="package-bonus">
              赠送 {{ pkg.bonus_points }} 积分
            </div>
          </div>
        </div>
      </section>

      <!-- 积分流水 -->
      <section class="logs-section">
        <h2>积分流水</h2>
        <div class="logs-table">
          <div class="table-header">
            <div>类型</div>
            <div>变动</div>
            <div>余额</div>
            <div>原因</div>
            <div>时间</div>
          </div>
          <div v-for="log in logs" :key="log.id" class="table-row">
            <div>
              <span :class="['type-badge', log.type]">
                {{ getTypeText(log.type) }}
              </span>
            </div>
            <div :class="log.amount > 0 ? 'amount-positive' : 'amount-negative'">
              {{ log.amount > 0 ? '+' : '' }}{{ log.amount }}
            </div>
            <div>{{ log.balance }}</div>
            <div>{{ log.reason || '-' }}</div>
            <div>{{ formatTime(log.created_at) }}</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const balance = ref({})
const packages = ref([])
const logs = ref([])

onMounted(async () => {
  await loadData()
})

async function loadData() {
  try {
    // TODO: 调用API获取数据
    // balance.value = await getBalance()
    // packages.value = await getPackages()
    // logs.value = await getLogs()

    // 模拟数据
    balance.value = { points: 100, total_recharged: 0, total_consumed: 0 }
    packages.value = [
      { id: 1, name: '基础套餐', price: 9900, points: 100, bonus_points: 0, total_points: 100 },
      { id: 2, name: '标准套餐', price: 4900, points: 500, bonus_points: 50, total_points: 550 },
      { id: 3, name: '高级套餐', price: 9800, points: 1000, bonus_points: 200, total_points: 1200 },
    ]
  } catch (error) {
    console.error('加载数据失败', error)
  }
}

function selectPackage(pkg) {
  router.push(`/point/recharge?package=${pkg.id}`)
}

function getTypeText(type) {
  const map = {
    recharge: '充值',
    consume: '消费',
    refund: '退款',
    gift: '赠送'
  }
  return map[type] || type
}

function formatTime(isoString) {
  if (!isoString) return '-'
  const date = new Date(isoString)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.point-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 40px 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

h1 {
  font-size: 32px;
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

section h2 {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.balance-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 30px;
  color: white;
  margin-bottom: 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.balance-info {
  text-align: center;
}

.balance-label {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 10px;
}

.balance-value {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 5px;
}

.balance-unit {
  font-size: 18px;
  opacity: 0.8;
}

.balance-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.8;
}

.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.package-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.package-card:hover {
  transform: translateY(-4px);
  border-color: #6366f1;
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
}

.package-name {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.package-points {
  margin-bottom: 10px;
}

.points-value {
  font-size: 32px;
  font-weight: 700;
  color: #6366f1;
}

.points-unit {
  font-size: 16px;
  color: #666;
}

.package-price {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.package-bonus {
  font-size: 14px;
  color: #10b981;
  font-weight: 500;
}

.logs-table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: grid;
  grid-template-columns: 100px 100px 100px 1fr 180px;
  gap: 15px;
  padding: 15px 20px;
  background: #f9fafb;
  font-weight: 600;
  color: #666;
  font-size: 14px;
}

.table-row {
  display: grid;
  grid-template-columns: 100px 100px 100px 1fr 180px;
  gap: 15px;
  padding: 15px 20px;
  border-top: 1px solid #f3f4f6;
  font-size: 14px;
  align-items: center;
}

.type-badge {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.type-badge.recharge {
  background: #d1fae5;
  color: #065f46;
}

.type-badge.consume {
  background: #fee2e2;
  color: #991b1b;
}

.amount-positive {
  color: #10b981;
  font-weight: 600;
}

.amount-negative {
  color: #ef4444;
  font-weight: 600;
}
</style>
