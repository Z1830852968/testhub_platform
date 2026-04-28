# Tasks
- [ ] Task 1: 代码盘点与死链清理（前端）
  - [ ] SubTask 1.1: 扫描并移除路由与菜单中指向不存在组件的入口，确保无 404 import（以 `frontend/src/router/index.js` 为主）。
  - [ ] SubTask 1.2: 清理 `frontend/src/views/**` 中被移除模块的残留引用（包含但不限于 api-testing/ui-automation/app-automation 的路径引用）。
  - [ ] SubTask 1.3: 统一测试用例入口与跳转路径（例如 `/ai-intelligent-mode/testcases/**`），避免旧路径残留。

- [ ] Task 2: API 调用统一与容错（前端）
  - [ ] SubTask 2.1: 统一 AI 相关页面的 API client 引用为 `frontend/src/utils/api`（或现有统一封装），移除重复/分散封装。
  - [ ] SubTask 2.2: 为关键页面请求添加最小错误态 UI（空状态 + 重试），避免异常导致白屏。

- [ ] Task 3: 探索引擎高可用（后端）
  - [ ] SubTask 3.1: 将 ExplorationRun 明确作为配置载体（base_url/auth/max_steps 等），并在 API 层对必填字段进行校验与默认值处理。
  - [ ] SubTask 3.2: 探索任务启动前进行 AI 模型配置校验：无 explorer 模型时给出明确失败原因与修复指引。
  - [ ] SubTask 3.3: 增强探索任务异常处理：对 Playwright/网络/解析异常生成结构化错误摘要并持久化到 `result_summary`。

- [ ] Task 4: AI 配置前置检查（全链路）
  - [ ] SubTask 4.1: 前端在启动需求分析/系统探索/AI 测试执行前调用配置检查接口或复用现有检查逻辑，缺失时阻断启动并引导配置。
  - [ ] SubTask 4.2: 配置中心页面明确区分 writer/reviewer/explorer 角色配置，并在缺失角色时给出提示。

- [ ] Task 5: 最小验证与回归保障
  - [ ] SubTask 5.1: 增加后端 API 冒烟测试（探索创建、探索列表、功能点列表）。
  - [ ] SubTask 5.2: 增加前端构建检查（`npm run build`）与关键路由访问冒烟（可用脚本或现有测试框架）。

# Task Dependencies
- [Task 2] depends on [Task 1]（先清理死链再统一 API 调用，避免重复修复）
- [Task 4] depends on [Task 2] and [Task 3]（前后端都具备校验能力后再做统一前置检查）
- [Task 5] depends on [Task 1-4]（回归验证最后执行）
