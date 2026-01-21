<template>
  <div class="coach-page">
    <div class="coach-container">
      <!-- 左侧会话列表 -->
      <div class="session-list">
        <div class="session-header">
          <h2>对话历史</h2>
          <button class="btn-new" @click="createSession">+ 新对话</button>
        </div>
        <div class="sessions">
          <div
            v-for="session in sessions"
            :key="session.id"
            :class="['session-item', { active: currentSessionId === session.id }]"
            @click="selectSession(session.id)"
          >
            <div class="session-title">{{ session.title }}</div>
            <div class="session-time">{{ formatTime(session.updated_at) }}</div>
          </div>
        </div>
      </div>

      <!-- 右侧聊天窗口 -->
      <div class="chat-window">
        <div v-if="!currentSessionId" class="empty-state">
          <h2>🤖 AI教练</h2>
          <p>点击"新对话"开始学习</p>
        </div>

        <div v-else class="chat-content">
          <!-- 消息列表 -->
          <div class="messages" ref="messagesContainer">
            <div
              v-for="msg in messages"
              :key="msg.id"
              :class="['message', msg.role]"
            >
              <div class="message-content">
                <div class="message-text">{{ msg.content }}</div>
                <div class="message-meta">{{ msg.tokens }} tokens</div>
              </div>
            </div>
            <div v-if="streamingContent" class="message assistant streaming">
              <div class="message-content">
                <div class="message-text">{{ streamingContent }}</div>
                <div class="typing-indicator">正在输入...</div>
              </div>
            </div>
          </div>

          <!-- 输入框 -->
          <div class="input-area">
            <textarea
              v-model="userInput"
              placeholder="输入你的问题..."
              @keydown.enter.exact.prevent="sendMessage"
              rows="3"
            ></textarea>
            <button
              class="btn-send"
              @click="sendMessage"
              :disabled="!userInput.trim() || streaming"
            >
              {{ streaming ? '发送中...' : '发送' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const currentSessionId = ref(null)
const sessions = ref([])
const messages = ref([])
const userInput = ref('')
const streaming = ref(false)
const streamingContent = ref('')
const messagesContainer = ref(null)

onMounted(() => {
  loadSessions()
})

async function loadSessions() {
  try {
    // TODO: 调用API获取会话列表
    // const data = await getSessions()
    // sessions.value = data
  } catch (error) {
    console.error('加载会话失败', error)
  }
}

async function createSession() {
  try {
    // TODO: 调用API创建会话
    // const data = await createSession()
    // sessions.value.unshift(data)
    // selectSession(data.id)
  } catch (error) {
    console.error('创建会话失败', error)
  }
}

function selectSession(sessionId) {
  currentSessionId.value = sessionId
  loadMessages()
}

async function loadMessages() {
  try {
    // TODO: 调用API获取消息
    // const data = await getMessages(currentSessionId.value)
    // messages.value = data
    await scrollToBottom()
  } catch (error) {
    console.error('加载消息失败', error)
  }
}

async function sendMessage() {
  if (!userInput.value.trim() || streaming.value) return

  const message = userInput.value.trim()
  userInput.value = ''

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: message,
    tokens: message.length / 4,
    created_at: new Date().toISOString()
  })

  await scrollToBottom()

  // 模拟AI回复（非流式）
  streaming.value = true
  try {
    // TODO: 调用流式API
    await simulateAIResponse(message)
  } finally {
    streaming.value = false
    await scrollToBottom()
  }
}

async function simulateAIResponse(userMessage) {
  // 模拟AI回复
  const responses = [
    `关于"${userMessage}"这个问题，让我来帮你分析一下。\n\n这是一个很好的问题！建议从以下几个方面来理解：\n\n1. **基本概念**：首先需要理解核心概念\n2. **算法思路**：思考可能的解决方案\n3. **复杂度分析**：评估时间和空间复杂度\n\n你想深入了解哪部分呢？`,
    `理解这个算法需要多练习！\n\n**学习建议：**\n- 先掌握基础数据结构\n- 多做相关练习题\n- 总结常见解题模式\n\n需要我详细讲解这个知识点吗？`,
    `让我为你详细讲解一下。\n\n这个知识点是算法学习中的重点内容。建议你：\n\n1. 理解基本原理\n2. 手动实现代码\n3. 做几道练习题\n4. 总结常见的陷阱\n\n有什么具体问题吗？`
  ]

  const response = responses[Math.floor(Math.random() * responses.length)]

  // 模拟打字效果
  const words = response.split('')
  for (let char of words) {
    streamingContent.value += char
    await new Promise(resolve => setTimeout(resolve, 20))
  }

  messages.value.push({
    role: 'assistant',
    content: streamingContent.value,
    tokens: streamingContent.value.length / 4,
    created_at: new Date().toISOString()
  })

  streamingContent.value = ''
}

async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

function formatTime(isoString) {
  const date = new Date(isoString)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString()
}
</script>

<style scoped>
.coach-page {
  height: 100vh;
  display: flex;
  background: #f5f5f5;
}

.coach-container {
  display: flex;
  width: 100%;
  height: 100%;
}

.session-list {
  width: 300px;
  background: white;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.session-header {
  padding: 20px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.session-header h2 {
  font-size: 18px;
  margin: 0;
}

.btn-new {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #6366f1;
  color: white;
  cursor: pointer;
  font-size: 14px;
}

.btn-new:hover {
  background: #4f46e5;
}

.sessions {
  flex: 1;
  overflow-y: auto;
}

.session-item {
  padding: 15px 20px;
  cursor: pointer;
  border-bottom: 1px solid #f3f4f6;
  transition: background 0.2s;
}

.session-item:hover {
  background: #f9fafb;
}

.session-item.active {
  background: #eef2ff;
  border-left: 3px solid #6366f1;
}

.session-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 5px;
}

.session-time {
  font-size: 12px;
  color: #999;
}

.chat-window {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.empty-state h2 {
  font-size: 48px;
  margin-bottom: 10px;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.message {
  margin-bottom: 20px;
  display: flex;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  background: #6366f1;
  color: white;
  border-radius: 12px 12px 0 12px;
  padding: 12px 16px;
}

.message.assistant .message-content {
  background: #f3f4f6;
  border-radius: 12px 12px 12px 0;
  padding: 12px 16px;
}

.message-text {
  white-space: pre-wrap;
  line-height: 1.5;
  word-break: break-word;
}

.message-meta {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 5px;
}

.typing-indicator {
  color: #999;
  font-style: italic;
  font-size: 14px;
}

.input-area {
  padding: 20px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 10px;
}

.input-area textarea {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: none;
  font-family: inherit;
}

.input-area textarea:focus {
  outline: none;
  border-color: #6366f1;
}

.btn-send {
  padding: 12px 30px;
  border: none;
  border-radius: 8px;
  background: #6366f1;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.btn-send:hover:not(:disabled) {
  background: #4f46e5;
}

.btn-send:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
