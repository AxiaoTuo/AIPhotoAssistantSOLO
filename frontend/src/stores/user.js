import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMe } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  async function fetchUserInfo() {
    if (!token.value) return null
    try {
      const data = await getMe()
      userInfo.value = data
      return data
    } catch {
      logout()
      return null
    }
  }

  return {
    token,
    userInfo,
    setToken,
    logout,
    fetchUserInfo
  }
})
