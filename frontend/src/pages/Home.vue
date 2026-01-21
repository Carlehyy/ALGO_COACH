<template>
  <div class="home">
    <h1>欢迎来到 ACM 算法学习平台</h1>
    <p>AI驱动的个性化算法学习平台</p>

    <div class="features">
      <div class="feature-card">
        <h3>📚 智能笔记</h3>
        <p>L1-L4分层学习，由浅入深掌握算法</p>
      </div>
      <div class="feature-card">
        <h3>🤖 AI教练</h3>
        <p>24/7在线答疑，个性化学习指导</p>
      </div>
      <div class="feature-card">
        <h3>🗺️ 知识图谱</h3>
        <p>系统化学习路径，清晰掌握知识体系</p>
      </div>
    </div>

    <div class="cta">
      <button @click="goToNotes" class="btn btn-primary">开始学习</button>
      <button @click="goToLogin" class="btn btn-secondary">立即登录</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goToNotes() {
  router.push('/note')
}

function goToLogin() {
  router.push('/user/login')
}
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
  text-align: center;
}

h1 {
  font-size: 48px;
  margin-bottom: 20px;
  color: #333;
}

p {
  font-size: 20px;
  color: #666;
  margin-bottom: 60px;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
  margin-bottom: 60px;
}

.feature-card {
  padding: 30px;
  border-radius: 12px;
  background: #f5f5f5;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  font-size: 24px;
  margin-bottom: 15px;
}

.feature-card p {
  font-size: 16px;
  margin: 0;
}

.cta {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn {
  padding: 15px 40px;
  border-radius: 8px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn-primary {
  background: #6366f1;
  color: white;
}

.btn-primary:hover {
  background: #4f46e5;
}

.btn-secondary {
  background: #e5e7eb;
  color: #333;
}

.btn-secondary:hover {
  background: #d1d5db;
}
</style>
