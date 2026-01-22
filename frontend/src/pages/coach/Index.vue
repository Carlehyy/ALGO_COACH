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
import { createSession as apiCreateSession, getSessions, getMessages, sendMessage as apiSendMessage } from '@/api/coach'

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
    const result = await getSessions()
    sessions.value = result.data || []
  } catch (error) {
    console.error('加载会话失败', error)
  }
}

async function createSession() {
  try {
    const result = await apiCreateSession({ title: '新对话' })
    const newSession = result.data
    sessions.value.unshift(newSession)
    selectSession(newSession.id)
  } catch (error) {
    console.error('创建会话失败', error)
    alert('创建会话失败: ' + (error.response?.data?.message || error.message || '未知错误'))
  }
}

function selectSession(sessionId) {
  currentSessionId.value = sessionId
  loadMessages()
}

async function loadMessages() {
  try {
    const result = await getMessages(currentSessionId.value)
    messages.value = result.data || []
    await scrollToBottom()
  } catch (error) {
    console.error('加载消息失败', error)
  }
}

async function sendMessage() {
  if (!userInput.value.trim() || streaming.value) return
  if (!currentSessionId.value) {
    alert('请先创建或选择一个会话')
    return
  }

  const message = userInput.value.trim()
  userInput.value = ''

  // 添加用户消息到界面
  messages.value.push({
    role: 'user',
    content: message,
    tokens: Math.ceil(message.length / 4),
    created_at: new Date().toISOString()
  })

  await scrollToBottom()

  // 调用API发送消息
  streaming.value = true
  try {
    const result = await apiSendMessage({
      session_id: currentSessionId.value,
      message: message
    })

    // 添加AI回复
    const aiResponse = result.data
    messages.value.push({
      role: 'assistant',
      content: aiResponse.content,
      tokens: aiResponse.tokens || 0,
      created_at: new Date().toISOString()
    })
  } catch (error) {
    console.error('发送消息失败', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，消息发送失败: ' + (error.response?.data?.message || error.message || '未知错误'),
      tokens: 0,
      created_at: new Date().toISOString()
    })
  } finally {
    streaming.value = false
    await scrollToBottom()
  }
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
