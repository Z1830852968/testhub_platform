<template>
  <div class="work-results">
    <div class="page-header">
      <h2>AI工作成果</h2>
      <p>查看系统自动探索生成的页面截图与功能分析</p>
    </div>

    <el-card class="box-card" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>功能清单 (探索任务: {{ runId || '所有' }})</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8" v-for="item in features" :key="item.id" style="margin-bottom: 20px;">
          <el-card :body-style="{ padding: '0px' }" shadow="hover">
            <img :src="item.screenshot_url" class="image" v-if="item.screenshot_url" @click="previewImage(item.screenshot_url)" />
            <div v-else class="image-placeholder">暂无截图</div>
            <div style="padding: 14px;">
              <span class="title">{{ item.name }}</span>

              <div class="bottom clearfix">
                <p class="desc">{{ item.description }}</p>
                <el-link type="primary" :href="item.url" target="_blank">{{ item.url }}</el-link>
                <div class="action-buttons" style="margin-top: 10px;">
                  <el-button type="success" size="small" @click="generateTestCase(item)">
                    <el-icon><MagicStick /></el-icon> 一键生成用例
                  </el-button>
                </div>
              </div>

            </div>
          </el-card>
        </el-col>
      </el-row>
      
      <el-empty v-if="fetchError" description="获取数据失败">
        <el-button type="primary" size="small" @click="loadFeatures">重试</el-button>
      </el-empty>
      <el-empty v-else-if="features.length === 0 && !loading" description="暂无探索成果" />
    </el-card>

    <el-dialog v-model="dialogVisible" width="80%">
      <img :src="dialogImageUrl" alt="Preview Image" style="width: 100%" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MagicStick } from '@element-plus/icons-vue'
import api from '@/utils/api'

const router = useRouter()


const route = useRoute()
const runId = ref(route.query.runId || '')
const features = ref([])
const loading = ref(false)
const fetchError = ref(false)
const dialogVisible = ref(false)
const dialogImageUrl = ref('')


const generateTestCase = (item) => {
  router.push({
    path: '/ai-intelligent-mode/requirement-analysis',
    query: {
      title: `探索发现功能: ${item.name}`,
      desc: `页面URL: ${item.url}\n\n功能描述: ${item.description}\n\n请针对此探索出的功能生成详尽的测试用例。`
    }
  })
}

const loadFeatures = async () => {
  loading.value = true
  fetchError.value = false
  try {
    const url = runId.value ? `/explorations/features/?run=${runId.value}` : '/explorations/features/'
    const res = await api.get(url)
    features.value = res.data.results || res.data
  } catch (err) {
    fetchError.value = true
    ElMessage.error('获取功能清单失败')
  } finally {
    loading.value = false
  }
}

const previewImage = (url) => {
  if (url.startsWith('/')) {
    dialogImageUrl.value = `http://localhost:8000${url}`
  } else {
    dialogImageUrl.value = url
  }
  dialogVisible.value = true
}

watch(() => route.query.runId, (newVal) => {
  runId.value = newVal || ''
  loadFeatures()
})

onMounted(() => {
  loadFeatures()
})
</script>

<style scoped>
.page-header {
  margin-bottom: 20px;
}
.page-header h2 {
  margin: 0 0 10px 0;
}
.page-header p {
  color: #666;
  margin: 0;
}
.card-header {
  font-weight: bold;
}
.image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}
.image-placeholder {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f5f7fa;
  color: #909399;
}
.title {
  font-weight: bold;
  font-size: 16px;
}
.bottom {
  margin-top: 13px;
  line-height: 1.5;
}
.desc {
  font-size: 13px;
  color: #999;
  margin-bottom: 10px;
}
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
</style>
