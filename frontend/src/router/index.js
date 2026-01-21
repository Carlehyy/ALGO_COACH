import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../pages/Home.vue'),
      meta: { title: '首页' }
    },
    {
      path: '/user/login',
      name: 'login',
      component: () => import('../pages/user/Login.vue'),
      meta: { title: '登录' }
    },
    {
      path: '/user/register',
      name: 'register',
      component: () => import('../pages/user/Register.vue'),
      meta: { title: '注册' }
    },
    {
      path: '/user/profile',
      name: 'profile',
      component: () => import('../pages/user/Profile.vue'),
      meta: { title: '个人中心', requiresAuth: true }
    },
    {
      path: '/note',
      name: 'note-list',
      component: () => import('../pages/note/Index.vue'),
      meta: { title: '笔记列表' }
    },
    {
      path: '/note/:id',
      name: 'note-detail',
      component: () => import('../pages/note/Detail.vue'),
      meta: { title: '笔记详情' }
    },
    {
      path: '/topic',
      name: 'topic',
      component: () => import('../pages/topic/Index.vue'),
      meta: { title: '知识图谱' }
    },
    {
      path: '/coach',
      name: 'coach',
      component: () => import('../pages/coach/Index.vue'),
      meta: { title: 'AI教练', requiresAuth: true }
    },
    {
      path: '/point',
      name: 'point',
      component: () => import('../pages/point/Index.vue'),
      meta: { title: '积分中心' }
    },
    {
      path: '/admin',
      component: () => import('../layouts/AdminLayout.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          redirect: '/admin/dashboard'
        },
        {
          path: 'dashboard',
          name: 'admin-dashboard',
          component: () => import('../pages/admin/Dashboard.vue'),
          meta: { title: '数据概览' }
        },
        {
          path: 'resources',
          name: 'admin-resources',
          component: () => import('../pages/admin/Resources.vue'),
          meta: { title: '资源管理' }
        },
        {
          path: 'proofreader',
          name: 'admin-proofreader',
          component: () => import('../pages/admin/Proofreader.vue'),
          meta: { title: 'PDF校对' }
        },
        {
          path: 'notes/review',
          name: 'admin-note-review',
          component: () => import('../pages/admin/NoteReview.vue'),
          meta: { title: '笔记审核' }
        },
        {
          path: 'users',
          name: 'admin-users',
          component: () => import('../pages/admin/Users.vue'),
          meta: { title: '用户管理' }
        }
      ]
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - ACM算法学习平台` : 'ACM算法学习平台'

  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/user/login')
  } else if (to.meta.requiresAdmin) {
    // TODO: 检查用户是否为管理员
    next()
  } else {
    next()
  }
})

export default router
