<template>
  <div class="register-page">
    <div class="register-card">
      <h1>注册</h1>
      <form @submit.prevent="handleRegister">
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
          <label>昵称</label>
          <input
            v-model="form.nickname"
            type="text"
            placeholder="请输入昵称（可选）"
          />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入密码（6-50字符）"
            required
            minlength="6"
          />
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            required
          />
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="login-link">
        已有账号？<router-link to="/user/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { register } from '@/api/user'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  email: '',
  nickname: '',
  password: '',
  confirmPassword: ''
})

const loading = ref(false)
const errorMessage = ref('')

async function handleRegister() {
  // 表单验证
  if (!form.value.email) {
    errorMessage.value = '请输入邮箱'
    return
  }

  if (form.value.password.length < 6) {
    errorMessage.value = '密码长度不能少于6个字符'
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const data = await register({
      email: form.value.email,
      password: form.value.password,
      nickname: form.value.nickname || undefined
    })

    // 注册成功，自动登录
    userStore.setUser(data, data.access_token || 'temp-token')

    alert('注册成功！')
    router.push('/')
  } catch (error) {
    errorMessage.value = error.response?.data?.message || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
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

.error-message {
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 6px;
  background: #fee;
  color: #c33;
  font-size: 14px;
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

.login-link {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.login-link a {
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
