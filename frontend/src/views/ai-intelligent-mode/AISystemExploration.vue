<template>
  <div class="system-exploration">
    <div class="page-header">
      <h2>系统自动探索</h2>
      <p>自动遍历系统功能，生成功能清单和截图</p>
    </div>

    <el-empty v-if="pageError" :description="pageErrorMessage">
      <el-button type="primary" @click="retryLoad">重试</el-button>
    </el-empty>

    <div v-else>
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

        <el-form-item label="探索入口 URL" prop="base_url">
          <el-input v-model="form.base_url" placeholder="如: http://localhost:3000"></el-input>
        </el-form-item>

        <el-form-item label="认证类型" prop="auth_type">
          <el-radio-group v-model="form.auth_type">
            <el-radio label="none">免登录</el-radio>
            <el-radio label="form">表单登录</el-radio>
          </el-radio-group>
        </el-form-item>

        <template v-if="form.auth_type === 'form'">
          <el-form-item label="登录账号" prop="auth_username">
            <el-input v-model="form.auth_username" placeholder="请输入系统账号"></el-input>
          </el-form-item>
          <el-form-item label="登录密码" prop="auth_password">
            <el-input type="password" v-model="form.auth_password" placeholder="请输入系统密码" show-password></el-input>
          </el-form-item>
        </template>

        <el-form-item label="最大探索步数" prop="max_steps">
          <el-input-number v-model="form.max_steps" :min="1" :max="50"></el-input-number>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="checkAndStartExploration" :loading="loading">
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
        <template #empty>
          <el-empty :description="tableError ? '加载失败' : '暂无数据'">
            <el-button v-if="tableError" type="primary" @click="loadRuns">重试</el-button>
          </el-empty>
        </template>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="base_url" label="目标 URL" min-width="150" show-overflow-tooltip />
        <el-table-column prop="max_steps" label="探索步数" width="100" />
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import api from '@/utils/api'
import dayjs from 'dayjs'

const router = useRouter()

const formRef = ref(null)
const form = ref({
  project: '',
  base_url: 'http://localhost:3000',
  auth_type: 'form',
  auth_username: 'admin',
  auth_password: 'admin123',
  max_steps: 10
})

const rules = {
  project: [{ required: true, message: '请选择项目', trigger: 'change' }],
  base_url: [{ required: true, message: '请输入入口 URL', trigger: 'blur' }]
}

const projects = ref([])
const runs = ref([])
const loading = ref(false)
const tableLoading = ref(false)
const pageError = ref(false)
const pageErrorMessage = ref('')
const tableError = ref(false)
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
    pageError.value = false
  } catch (err) {
    ElMessage.error('加载项目列表失败')
    pageError.value = true
    pageErrorMessage.value = '加载项目列表失败，请检查网络或稍后重试'
  }
}

const loadRuns = async () => {
  tableLoading.value = true
  tableError.value = false
  try {
    const res = await api.get('/explorations/runs/')
    runs.value = res.data.results || res.data
  } catch (err) {
    console.error('加载探索记录失败', err)
    tableError.value = true
    ElMessage.error('加载探索记录失败')
  } finally {
    tableLoading.value = false
  }
}

const retryLoad = () => {
  pageError.value = false
  loadProjects()
  loadRuns()
}

const pollRuns = async () => {
  // If there's a table error or page error, stop polling to avoid spam
  if (tableError.value || pageError.value) return
  try {
    const res = await api.get('/explorations/runs/')
    runs.value = res.data.results || res.data
  } catch (err) {
    console.error('轮询失败', err)
  }
}

const checkAndStartExploration = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await api.get('/requirement-analysis/config/check/')
        const configData = response.data
        if (!configData.explorer_model || !configData.explorer_model.configured || !configData.explorer_model.enabled) {
          ElMessageBox.confirm(
            '系统未配置 Explorer (AI网页探索专家) 角色模型，或模型未启用。请前往配置中心进行配置。',
            '缺少模型配置',
            {
              confirmButtonText: '去配置',
              cancelButtonText: '取消',
              type: 'warning',
            }
          ).then(() => {
            router.push('/configuration/ai-model')
          }).catch(() => {})
          return
        }
        
        await startExploration()
      } catch (error) {
        console.error('Check config error:', error)
        ElMessage.error('检查模型配置失败，请稍后重试')
      }
    }
  })
}

const startExploration = async () => {
  loading.value = true
  try {
    await api.post('/explorations/runs/', {
      project: form.value.project,
      base_url: form.value.base_url,
      auth_type: form.value.auth_type,
      auth_username: form.value.auth_username,
      auth_password: form.value.auth_password,
      max_steps: form.value.max_steps
    })
    ElMessage.success('探索任务已启动')
    loadRuns()
  } catch (err) {
    ElMessage.error('启动探索失败')
  } finally {
    loading.value = false
  }
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
