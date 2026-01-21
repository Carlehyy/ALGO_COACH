<template>
  <div class="recharge-page">
    <div class="container">
      <button class="btn-back" @click="goBack">← 返回</button>

      <h1>充值积分</h1>
      <p class="subtitle">选择适合您的套餐</p>

      <!-- 套餐选择 -->
      <div class="packages-grid">
        <div
          v-for="pkg in packages"
          :key="pkg.id"
          :class="['package-card', { selected: selectedPackage?.id === pkg.id }]"
          @click="selectPackage(pkg)"
        >
          <div class="package-name">{{ pkg.name }}</div>
          <div class="package-points">
            <span class="points-value">{{ pkg.total_points }}</span>
            <span class="points-unit">积分</span>
          </div>
          <div class="package-price">
            <span class="price-symbol">¥</span>
            <span class="price-value">{{ (pkg.price / 100).toFixed(2) }}</span>
          </div>
          <div v-if="pkg.bonus_points > 0" class="package-bonus">
            赠送 {{ pkg.bonus_points }} 积分
          </div>
          <div class="package-desc">{{ pkg.description || '' }}</div>
        </div>
      </div>

      <!-- 支付按钮 -->
      <div v-if="selectedPackage" class="payment-section">
        <button class="btn-pay" @click="handlePay" :disabled="paying">
          {{ paying ? '支付中...' : `支付 ¥${(selectedPackage.price / 100).toFixed(2)}` }}
        </button>
      </div>

      <!-- 支付结果弹窗 -->
      <div v-if="showResult" class="modal-overlay" @click="closeModal">
        <div class="modal" @click.stop>
          <div v-if="paySuccess" class="success-content">
            <div class="success-icon">✅</div>
            <h2>支付成功</h2>
            <p>您已获得 {{ selectedPackage?.total_points }} 积分</p>
            <button class="btn-modal" @click="goToBalance">查看余额</button>
          </div>
          <div v-else class="error-content">
            <div class="error-icon">❌</div>
            <h2>支付失败</h2>
            <p>{{ errorMessage }}</p>
            <button class="btn-modal" @click="closeModal">关闭</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getPackages, createOrder, payOrder } from '@/api/point'

const router = useRouter()
const route = useRoute()

const packages = ref([])
const selectedPackage = ref(null)
const paying = ref(false)
const showResult = ref(false)
const paySuccess = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  await loadPackages()
})

async function loadPackages() {
  try {
    // TODO: 调用API
    // packages.value = await getPackages()

    // 模拟数据
    packages.value = [
      { id: 1, name: '体验套餐', price: 100, points: 10, bonus_points: 0, total_points: 10, description: '适合新手体验' },
      { id: 2, name: '基础套餐', price: 9900, points: 100, bonus_points: 0, total_points: 100, description: '日常学习使用' },
      { id: 3, name: '标准套餐', price: 4900, points: 500, bonus_points: 50, total_points: 550, description: '最受欢迎' },
      { id: 4, name: '高级套餐', price: 9800, points: 1000, bonus_points: 200, total_points: 1200, description: '性价比最高' },
      { id: 5, name: '豪华套餐', price: 47500, points: 5000, bonus_points: 1000, total_points: 6000, description: '学习无忧' },
    ]
  } catch (error) {
    console.error('加载失败', error)
  }
}

function selectPackage(pkg) {
  selectedPackage.value = pkg
}

async function handlePay() {
  if (!selectedPackage.value) return

  paying.value = true
  try {
    // TODO: 调用API
    // const order = await createOrder(selectedPackage.value.id)
    // await payOrder(order.order_no)
    // paySuccess.value = true

    // 模拟支付
    await new Promise(resolve => setTimeout(resolve, 1500))
    paySuccess.value = Math.random() > 0.2 // 80%成功率
    errorMessage.value = paySuccess.value ? '' : '网络连接失败'
  } catch (error) {
    paySuccess.value = false
    errorMessage.value = error.message || '支付失败'
  } finally {
    paying.value = false
    showResult.value = true
  }
}

function closeModal() {
  showResult.value = false
}

function goToBalance() {
  router.push('/point')
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.recharge-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 20px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

.btn-back {
  padding: 10px 20px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 8px;
  background: rgba(255,255,255,0.1);
  color: white;
  cursor: pointer;
  margin-bottom: 30px;
}

h1 {
  font-size: 36px;
  text-align: center;
  color: white;
  margin-bottom: 10px;
}

.subtitle {
  text-align: center;
  color: rgba(255,255,255,0.8);
  margin-bottom: 40px;
}

.packages-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.package-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  border: 3px solid transparent;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.package-card:hover {
  transform: translateY(-8px);
}

.package-card.selected {
  border-color: #fbbf24;
  box-shadow: 0 8px 24px rgba(251, 191, 36, 0.4);
}

.package-name {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

.package-points {
  margin-bottom: 10px;
}

.points-value {
  font-size: 36px;
  font-weight: 700;
  color: #6366f1;
}

.points-unit {
  font-size: 16px;
  color: #666;
}

.package-price {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.price-symbol {
  font-size: 20px;
}

.package-bonus {
  font-size: 14px;
  color: #10b981;
  font-weight: 500;
  margin-bottom: 10px;
}

.package-desc {
  font-size: 14px;
  color: #999;
}

.payment-section {
  text-align: center;
}

.btn-pay {
  padding: 16px 60px;
  border: none;
  border-radius: 30px;
  background: #fbbf24;
  color: #78350f;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-pay:hover:not(:disabled) {
  background: #f59e0b;
  transform: scale(1.05);
}

.btn-pay:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.modal-overlay {
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
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 40px;
  max-width: 400px;
  text-align: center;
}

.success-icon, .error-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.modal h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

.modal p {
  color: #666;
  margin-bottom: 30px;
}

.btn-modal {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  cursor: pointer;
}
</style>
