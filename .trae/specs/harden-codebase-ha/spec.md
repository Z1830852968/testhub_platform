# 代码高可用与AI模块治理 Spec

## Why
当前前后端已完成多轮功能合并与重构，存在路由/页面/接口调用的历史遗留与重复实现风险，容易引发白屏、接口 404、任务执行失败等可用性问题。需要系统性清理冗余代码与不一致实现，并补齐关键的稳定性保障，使现有业务功能与 AI 能力在无额外手工“补配置/补脚本”的前提下可稳定运行、可定位问题、可持续演进。

## What Changes
- 清理前端路由、页面与 API 调用中的死链/重复/历史模块残留，统一以 AI 智能模式为主入口。
- 建立 AI 相关能力（需求分析/生成、系统探索、AI 测试执行/报告）的配置校验与运行前置检查，避免“未配置也可点击但必失败”的体验。
- 规范 AI 探索执行链路：配置驱动、可观测（日志/产物/错误摘要）、可终止、失败可解释。
- 增强关键页面的错误兜底：避免单个接口或动态导入失败导致整页白屏。
- 为核心链路补齐最小可行的自动化验证（后端 API 冒烟 + 前端构建/路由校验）。

## Impact
- Affected specs: AI 智能模式全链路高可用（项目/需求/探索/用例/执行/报告）
- Affected code:
  - 前端：`frontend/src/router/index.js`，`frontend/src/views/ai-intelligent-mode/**`，`frontend/src/views/requirement-analysis/**`，`frontend/src/utils/api*`
  - 后端：`apps/explorations/**`，`apps/requirement_analysis/**`，`apps/projects/**`，`apps/reports/**`

## ADDED Requirements
### Requirement: 运行前置检查（AI能力）
系统 SHALL 在用户启动 AI 相关任务（需求分析、系统探索、AI 测试执行）前进行配置校验，并给出明确可执行的修复指引。

#### Scenario: Success case
- **WHEN** 用户点击“开始探索/开始分析/开始执行”
- **THEN** 若缺少必需配置（如 AI 模型配置、探索入口 URL、认证信息等），界面明确提示缺失项并提供跳转到配置页的入口

### Requirement: AI 系统探索配置驱动
系统 SHALL 以“探索运行记录”保存并驱动探索行为，不允许依赖写死 URL/账号或仅对当前系统固定路径探索。

#### Scenario: Success case
- **WHEN** 用户为某项目提交探索配置（base_url、auth_type、max_steps 等）并启动探索
- **THEN** 后端探索任务按照该配置执行，并将结果（FeatureItem、Artifact、错误摘要）与该运行记录关联

### Requirement: 关键页面白屏防护
系统 SHALL 在前端关键页面发生接口异常/动态导入异常时，展示可恢复的错误态，而不是白屏。

#### Scenario: Success case
- **WHEN** 页面关键接口返回 404/500 或某路由组件动态导入失败
- **THEN** 展示“加载失败”错误态与“重试/返回”操作，并记录可用于排查的错误信息（不包含敏感信息）

## MODIFIED Requirements
### Requirement: 路由与模块一致性
现有功能的所有入口 SHALL 仅指向当前仍然存在且可构建的页面与组件，不允许保留已移除模块（API/UI/APP 自动化等）导致的隐式依赖。

#### Scenario: Success case
- **WHEN** 运行前端构建与路由依赖扫描
- **THEN** 不存在任何无法解析的 import/动态导入路径

## REMOVED Requirements
### Requirement: 旧测试模块残留
**Reason**: 旧模块已整合至 AI 智能模式，残留代码带来维护与稳定性风险。
**Migration**: 将仍需要的能力以共享组件/共享 API 调用方式归入 `ai-intelligent-mode` 目录与统一 API client；删除无引用代码与路由入口。
