import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { auth: true }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('@/views/History.vue'),
    meta: { auth: true }
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: () => import('@/views/Detail.vue'),
    meta: { auth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // 直接从localStorage获取token，避免在路由守卫中使用Pinia store
  const token = localStorage.getItem('token')

  if (to.meta.auth && !token) {
    next('/login')
  } else if (to.meta.guest && token) {
    next('/')
  } else {
    next()
  }
})

export default router
