<template>
  <div class="system-exploration">
    <div class="page-header">
      <h2>系统自动探索</h2>
      <p>自动遍历系统功能，生成功能清单和截图</p>
    </div>

    <el-card class="box-card">
      <template #header>
        <div class="card-header">
          <span>新建探索任务</span>
        </div>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="所属项目" prop="project">
          <el-select v-model="form.project" placeholder="请选择项目" style="width: 100%">
            <el-option
              v-for="p in projects"
              :key="p.id"
              :label="p.name"
              :value="p.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="startExploration" :loading="loading">
            开始探索
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="box-card" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>探索任务记录</span>
        </div>
      </template>

      <el-table :data="runs" style="width: 100%" v-loading="tableLoading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.start_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="result_summary" label="结果摘要" show-overflow-tooltip />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button 
              type="danger" 
              link 
              v-if="row.status === 'running' || row.status === 'pending'"
              @click="stopExploration(row.id)">
              停止
            </el-button>
            <el-button 
              type="primary" 
              link 
              @click="$router.push({ name: 'AIWorkResults', query: { runId: row.id } })">
              查看结果
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'
import dayjs from 'dayjs'

const formRef = ref(null)
const form = ref({
  project: ''
})

const rules = {
  project: [{ required: true, message: '请选择项目', trigger: 'change' }]
}

const projects = ref([])
const runs = ref([])
const loading = ref(false)
const tableLoading = ref(false)
let timer = null

const getStatusType = (status) => {
  const map = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    stopped: 'danger'
  }
  return map[status] || 'info'
}

const getStatusLabel = (status) => {
  const map = {
    pending: '排队中',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
    stopped: '已停止'
  }
  return map[status] || status
}

const formatDate = (date) => {
  if (!date) return '-'
  return dayjs(date).format('YYYY-MM-DD HH:mm:ss')
}

const loadProjects = async () => {
  try {
    const res = await api.get('/projects/')
    projects.value = res.data.results || res.data
  } catch (err) {
    ElMessage.error('加载项目列表失败')
  }
}

const loadRuns = async () => {
  tableLoading.value = true
  try {
    const res = await api.get('/explorations/runs/')
    runs.value = res.data.results || res.data
  } catch (err) {
    console.error('加载探索记录失败', err)
  } finally {
    tableLoading.value = false
  }
}

const pollRuns = async () => {
  try {
    const res = await api.get('/explorations/runs/')
    runs.value = res.data.results || res.data
  } catch (err) {
    console.error('轮询失败', err)
  }
}

const startExploration = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        await api.post('/explorations/runs/', {
          project: form.value.project
        })
        ElMessage.success('探索任务已启动')
        loadRuns()
      } catch (err) {
        ElMessage.error('启动探索失败')
      } finally {
        loading.value = false
      }
    }
  })
}

const stopExploration = async (id) => {
  try {
    await ElMessageBox.confirm('确定要停止该探索任务吗？', '提示', {
      type: 'warning'
    })
    await api.post(`/explorations/runs/${id}/stop/`)
    ElMessage.success('已发送停止信号')
    pollRuns()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('停止失败')
    }
  }
}

onMounted(() => {
  loadProjects()
  loadRuns()
  timer = setInterval(pollRuns, 3000)
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
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
</style>
