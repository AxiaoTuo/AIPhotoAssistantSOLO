<template>
  <div class="history-container">
    <!-- 顶部导航栏 -->
    <el-header class="history-header">
      <div class="logo">摄影AI助手</div>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
        <el-menu-item index="1" @click="$router.push('/')">首页</el-menu-item>
        <el-menu-item index="2" @click="$router.push('/history')">历史记录</el-menu-item>
        <el-menu-item index="3" @click="handleLogout">退出登录</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="history-main">
      <el-card class="history-card">
        <template #header>
          <div class="card-header">
            <span class="title">我的历史记录</span>
          </div>
        </template>

        <!-- 历史记录列表 -->
        <div class="history-list" v-if="historyItems.length > 0">
          <el-row :gutter="10">
            <el-col :span="6" v-for="item in historyItems" :key="item.id">
              <el-card class="history-item" @click="viewDetail(item.id)">
                <template #header>
                  <div class="item-header">
                    <span class="item-title">{{ item.filename }}</span>
                    <el-tag :type="getScoreType(item.overall_score)">
                      {{ item.overall_score }}分
                    </el-tag>
                  </div>
                </template>
                <div class="item-content">
                  <el-image :src="item.thumbnail || placeholderImage" fit="cover" />
                  <div class="item-date">{{ formatDate(item.created_at) }}</div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <!-- 空状态 -->
        <div class="empty-state" v-else>
          <el-empty description="暂无历史记录">
            <el-button type="primary" @click="$router.push('/')">
              <el-icon><UploadFilled /></el-icon> 立即上传
            </el-button>
          </el-empty>
        </div>

        <!-- 分页 -->
        <div class="pagination" v-if="total > 0">
          <el-pagination
            layout="total, prev, pager, next"
            :total="total"
            :page-size="pageSize"
            v-model:current-page="currentPage"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { UploadFilled } from '@element-plus/icons-vue'
import { getHistory } from '@/api/photo'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const activeIndex = ref('2')
const loading = ref(false)
const historyItems = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const placeholderImage = ref('https://picsum.photos/200/150')

// 根据评分获取对应的标签类型
const getScoreType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'warning'
  if (score >= 70) return 'danger'
  return 'info'
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// 查看详情
const viewDetail = (photoId) => {
  router.push(`/detail/${photoId}`)
}

// 获取历史记录
const fetchHistory = async (page = 1, size = 12) => {
  try {
    loading.value = true
    const result = await getHistory(page, size)
    historyItems.value = result.items
    total.value = result.total
  } catch (error) {
    ElMessage.error('获取历史记录失败')
    console.error('获取历史记录失败:', error)
  } finally {
    loading.value = false
  }
}

// 分页变化
const handlePageChange = (page) => {
  currentPage.value = page
  fetchHistory(page, pageSize.value)
}

// 退出登录
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
  ElMessage.success('已退出登录')
}

// 页面加载时获取数据
onMounted(() => {
  fetchHistory(currentPage.value, pageSize.value)
})
</script>

<style scoped>
.history-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 20px;
}

.logo {
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
}

.history-main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.history-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.history-list {
  margin: 20px 0;
}

.history-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-title {
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px;
}

.item-content {
  text-align: center;
}

.item-content img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 10px;
}

.item-date {
  font-size: 12px;
  color: #909399;
}

.empty-state {
  padding: 50px 0;
  text-align: center;
}

.pagination {
  margin-top: 20px;
  text-align: center;
}
</style>