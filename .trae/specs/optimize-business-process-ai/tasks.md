# Tasks
- [x] Task 1: 优化“需求分析”到“用例生成”的流转
  - [x] SubTask 1.1: 在需求分析结果页（或提取的功能点列表）添加“一键生成测试用例”按钮。
  - [x] SubTask 1.2: 实现跳转逻辑，将需求上下文通过路由参数或 Store 自动传递给用例生成模块。
- [x] Task 2: 打通“系统自动探索”与“测试用例”
  - [x] SubTask 2.1: 在“AI工作成果”或探索结果详情列表中，为每个提取的功能点添加“生成用例”快捷操作。
  - [x] SubTask 2.2: 编写对接逻辑，将选中的功能点数据带入到用例创建表单（或直接触发后台 AI 自动生成用例）。
- [x] Task 3: 优化 AI 测试执行与报告的流转
  - [x] SubTask 3.1: 在 AI 测试执行完成后，提供直接查看或生成 AI 总结报告的显眼入口。
  - [x] SubTask 3.2: 优化测试报告页面，增加高亮的“AI 总结与建议”区域。

# Task Dependencies
- [Task 2] depends on [Task 1] (两者共享上下文传递和自动填充逻辑)
- [Task 3] can be executed in parallel with [Task 1] and [Task 2].