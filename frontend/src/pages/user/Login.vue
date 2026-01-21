<template>
  <div class="login-page">
    <div class="login-card">
      <h1>登录</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>邮箱</label>
          <input
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱"
            required
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="register-link">
        还没有账号？<router-link to="/user/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  email: '',
  password: ''
})

const loading = ref(false)

async function handleLogin() {
  loading.value = true
  try {
    // TODO: 调用登录API
    await new Promise(resolve => setTimeout(resolve, 1000))

    // 模拟登录成功
    userStore.setUser(
      { id: 1, email: form.value.email, nickname: 'Test User' },
      'mock-token'
    )

    router.push('/')
  } catch (error) {
    alert('登录失败: ' + error.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

input:focus {
  outline: none;
  border-color: #6366f1;
}

.btn {
  width: 100%;
  padding: 14px;
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

.register-link {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.register-link a {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
