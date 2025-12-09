<template>
  <div class="detail-container">
    <!-- 顶部导航栏 -->
    <el-header class="detail-header">
      <div class="logo">摄影AI助手</div>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
        <el-menu-item index="1" @click="$router.push('/')">首页</el-menu-item>
        <el-menu-item index="2" @click="$router.push('/history')">历史记录</el-menu-item>
        <el-menu-item index="3" @click="handleLogout">退出登录</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="detail-main">
      <el-card class="detail-card" v-if="analysisResult">
        <template #header>
          <div class="card-header">
            <el-button type="primary" @click="$router.go(-1)">
              <el-icon><ArrowLeft /></el-icon> 返回
            </el-button>
            <span class="title">分析结果</span>
          </div>
        </template>

        <!-- 综合评分和雷达图 -->
        <div class="score-section">
          <div class="photo-preview">
            <el-image :src="previewImage" fit="cover" />
          </div>
          <div class="score-details">
            <div class="overall-score">
              <h3>综合评分</h3>
              <el-progress
                :percentage="analysisResult.overall_score"
                :color="scoreColor"
                :stroke-width="20"
                :show-text="true"
                text-inside
                :format="(value) => `${value}分`"
              />
            </div>
            <div class="radar-chart">
              <h3>四维度评分</h3>
              <ScoreRadar :scores="analysisResult.scores" />
            </div>
            <div class="model-info">
              <el-tag type="info">使用模型：{{ analysisResult.model_used }}</el-tag>
              <el-tag type="success">分析时间：{{ formatDate(analysisResult.created_at) }}</el-tag>
            </div>
          </div>
        </div>

        <!-- 优点 -->
        <div class="analysis-section">
          <h3 class="section-title"><el-icon class="success-icon"><Check /></el-icon> 优点</h3>
          <el-divider />
          <div class="custom-list">
            <div v-if="safeAnalysis.highlights.length === 0" class="empty-list">
              <el-empty description="暂无数据" />
            </div>
            <el-list-item v-for="(item, index) in safeAnalysis.highlights" :key="`highlight-${index}`" class="list-item">
              <el-icon><CircleCheck /></el-icon>
              <span class="list-content">{{ item }}</span>
            </el-list-item>
          </div>
        </div>

        <!-- 可改进 -->
        <div class="analysis-section">
          <h3 class="section-title"><el-icon class="warning-icon"><Warning /></el-icon> 可改进</h3>
          <el-divider />
          <div class="custom-list">
            <div v-if="safeAnalysis.improvements.length === 0" class="empty-list">
              <el-empty description="暂无数据" />
            </div>
            <el-list-item v-for="(item, index) in safeAnalysis.improvements" :key="`improvement-${index}`" class="list-item">
              <el-icon><Warning /></el-icon>
              <span class="list-content">{{ item }}</span>
            </el-list-item>
          </div>
        </div>

        <!-- 建议 -->
        <div class="analysis-section">
          <h3 class="section-title"><el-icon class="tips-icon"><HelpFilled /></el-icon> 建议</h3>
          <el-divider />
          <div class="custom-list">
            <div v-if="safeAnalysis.suggestions.length === 0" class="empty-list">
              <el-empty description="暂无数据" />
            </div>
            <el-list-item v-for="(item, index) in safeAnalysis.suggestions" :key="`suggestion-${index}`" class="list-item">
              <el-icon><HelpFilled /></el-icon>
              <span class="list-content">{{ item }}</span>
            </el-list-item>
          </div>
        </div>
      </el-card>

      <!-- 加载中状态 -->
      <el-card class="detail-card" v-else>
        <div class="loading-container">
          <el-skeleton :rows="10" animated />
        </div>
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ArrowLeft, Check, Warning, HelpFilled, CircleCheck } from '@element-plus/icons-vue'
import { getPhotoDetail } from '@/api/photo'
import { ElMessage } from 'element-plus'
import ScoreRadar from '@/components/ScoreRadar.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const activeIndex = ref('2')
const loading = ref(false)
const analysisResult = ref(null)
const previewImage = ref('')

// 根据评分获取对应的颜色
const scoreColor = computed(() => {
  if (!analysisResult.value) return ''
  const score = analysisResult.value.overall_score
  if (score >= 90) return '#67c23a'
  if (score >= 80) return '#e6a23c'
  if (score >= 70) return '#f56c6c'
  return '#909399'
})

// 确保分析数据格式正确
const safeAnalysis = computed(() => {
  if (!analysisResult.value || !analysisResult.value.analysis) {
    return {
      highlights: [],
      improvements: [],
      suggestions: []
    }
  }
  return {
    highlights: Array.isArray(analysisResult.value.analysis.highlights) ? analysisResult.value.analysis.highlights : [],
    improvements: Array.isArray(analysisResult.value.analysis.improvements) ? analysisResult.value.analysis.improvements : [],
    suggestions: Array.isArray(analysisResult.value.analysis.suggestions) ? analysisResult.value.analysis.suggestions : []
  }
})

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 获取分析详情
const fetchAnalysisDetail = async () => {
  const photoId = route.params.id
  try {
    loading.value = true
    const result = await getPhotoDetail(photoId)
    analysisResult.value = result
    // 使用后端返回的原图片，如果没有则使用缩略图，如果都没有则使用占位图
    previewImage.value = result.image_data || result.thumbnail || 'https://picsum.photos/400/300' // 占位图
  } catch (error) {
    ElMessage.error('获取分析结果失败')
    console.error('获取分析结果失败:', error)
  } finally {
    loading.value = false
  }
}

// 退出登录
const handleLogout = () => {
  userStore.logout()
  router.push('/login')
  ElMessage.success('已退出登录')
}

// 页面加载时获取数据
onMounted(() => {
  fetchAnalysisDetail()
})
</script>

<style scoped>
.detail-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.detail-header {
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

.detail-main {
  flex: 1;
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
  width: 100%;
}

.detail-card {
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

.title {
  margin-left: 20px;
}

.score-section {
  display: flex;
  gap: 20px;
  margin: 20px 0;
}

.photo-preview {
  width: 400px;
  height: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.score-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.overall-score h3,
.radar-chart h3 {
  margin-bottom: 10px;
  color: #303133;
}

.overall-score {
  text-align: center;
}

.radar-chart {
  flex: 1;
}

.model-info {
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.analysis-section {
  margin: 30px 0;
}

.section-title {
  color: #303133;
  display: flex;
  align-items: center;
  gap: 10px;
}

.success-icon {
  color: #67c23a;
  font-size: 20px;
}

.warning-icon {
  color: #e6a23c;
  font-size: 20px;
}

.tips-icon {
  color: #409eff;
  font-size: 20px;
}

.list-content {
  margin-left: 10px;
}

.custom-list {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.list-item {
  border-bottom: 1px solid #ebeef5;
  display: flex;
  align-items: center;
  padding: 12px 20px;
  transition: all 0.3s;
}

.list-item:last-child {
  border-bottom: none;
}

.list-item:hover {
  background-color: #f5f7fa;
}

.empty-list {
  padding: 20px;
  text-align: center;
  color: #909399;
}

.loading-container {
  padding: 20px;
}
</style>