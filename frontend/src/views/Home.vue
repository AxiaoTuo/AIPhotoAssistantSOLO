<template>
  <div class="home-container">
    <!-- 顶部导航栏 -->
    <el-header class="home-header">
      <div class="logo">摄影AI助手</div>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal">
        <el-menu-item index="1" @click="$router.push('/')">首页</el-menu-item>
        <el-menu-item index="2" @click="$router.push('/history')">历史记录</el-menu-item>
        <el-menu-item index="3" @click="handleLogout">退出登录</el-menu-item>
      </el-menu>
    </el-header>

    <!-- 主要内容区域 -->
    <el-main class="home-main">
      <el-card class="upload-card">
        <template #header>
          <div class="card-header">
            <span>上传图片进行AI分析</span>
          </div>
        </template>

        <!-- 图片上传区域 -->
        <div class="upload-area">
          <el-upload
            v-model:file-list="fileList"
            class="upload-demo"
            drag
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            :before-upload="beforeUpload"
            accept="image/*"
          >
            <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
            <div class="el-upload__text">点击或拖拽文件到此处上传</div>
            <template #tip>
              <div class="el-upload__tip">
                支持 JPG、PNG、WebP 格式，文件大小建议不超过 5MB
              </div>
            </template>
          </el-upload>
        </div>

        <!-- AI模型选择 -->
        <div class="model-selector">
          <el-form-item label="选择AI模型：">
            <el-select v-model="selectedModel" placeholder="请选择模型" size="large">
              <el-option label="DeepSeek" value="deepseek" />
              <el-option label="GPT-5-mini" value="openai" />
              <el-option label="Claude" value="claude" />
            </el-select>
          </el-form-item>
        </div>

        <!-- 分析按钮 -->
        <div class="action-buttons">
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleAnalyze"
            :disabled="fileList.length === 0"
          >
            开始分析
          </el-button>
        </div>
      </el-card>
    </el-main>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { UploadFilled } from '@element-plus/icons-vue'
import { analyzePhoto } from '@/api/photo'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const activeIndex = ref('1')
const loading = ref(false)
const fileList = ref([])
const selectedModel = ref('deepseek')
const uploadedFile = ref(null)

// 文件上传前的检查
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('请上传图片文件')
    return false
  }
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB')
    return false
  }
  return true
}

// 文件变化处理
const handleFileChange = (file) => {
  uploadedFile.value = file.raw
  fileList.value = [file]
}

// 开始分析
const handleAnalyze = async () => {
  if (!uploadedFile.value) {
    ElMessage.error('请先上传图片')
    return
  }

  try {
    loading.value = true
    const formData = new FormData()
    formData.append('file', uploadedFile.value)
    if (selectedModel.value) {
      formData.append('model', selectedModel.value)
    }

    const result = await analyzePhoto(formData)
    ElMessage.success('分析完成')
    // 跳转到结果详情页
    router.push(`/detail/${result.id}`)
  } catch (error) {
    ElMessage.error('分析失败，请稍后重试')
    console.error('分析失败:', error)
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
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.home-header {
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

.home-main {
  flex: 1;
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.upload-card {
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

.upload-area {
  margin: 20px 0;
}

.model-selector {
  margin: 20px 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}
</style>