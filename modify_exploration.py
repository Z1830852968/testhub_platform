import re

with open('frontend/src/views/ai-intelligent-mode/AISystemExploration.vue', 'r') as f:
    content = f.read()

form_html = """      <el-form :model="form" label-width="120px" ref="formRef">
        <el-form-item label="选择项目" prop="project" required>
          <el-select v-model="form.project" placeholder="请选择要探索的项目" style="width: 100%;">
            <el-option
              v-for="item in projects"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="基础URL" prop="base_url" required>
          <el-input v-model="form.base_url" placeholder="如: http://localhost:3000"></el-input>
        </el-form-item>

        <el-form-item label="认证类型" prop="auth_type">
          <el-radio-group v-model="form.auth_type">
            <el-radio label="none">无(免登录)</el-radio>
            <el-radio label="form">表单登录</el-radio>
          </el-radio-group>
        </el-form-item>

        <template v-if="form.auth_type === 'form'">
          <el-form-item label="登录账号" prop="auth_username">
            <el-input v-model="form.auth_username" placeholder="请输入探索账号"></el-input>
          </el-form-item>
          <el-form-item label="登录密码" prop="auth_password">
            <el-input type="password" v-model="form.auth_password" placeholder="请输入探索密码" show-password></el-input>
          </el-form-item>
        </template>

        <el-form-item label="最大探索步数" prop="max_steps">
          <el-input-number v-model="form.max_steps" :min="1" :max="50"></el-input-number>
        </el-form-item>"""

# Replace the original form part
# In original file it's probably just the project select.
# Let's see the original file content.
