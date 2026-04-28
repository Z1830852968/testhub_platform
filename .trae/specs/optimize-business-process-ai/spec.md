# 业务流程与功能AI化系统优化 Spec

## Why
系统已成功移除了传统的接口、UI、APP自动化测试模块，并全面整合至“AI 智能模式”。但目前的业务流程（如需求分析、系统探索、用例生成、测试执行）之间仍然相对独立，缺乏深度串联和AI驱动的自动化流转。需要从业务流程的视角，将这些功能深度AI化，实现从需求到报告的无缝智能流转。

## What Changes
- 优化从“需求分析”到“用例生成”的连贯性，支持一键转化。
- 将“系统自动探索”的结果与“测试用例管理”打通，允许从探索结果直接生成测试用例。
- 增强 AI 执行过程中的实时反馈与交互体验。
- 在测试报告环节引入 AI 自动总结与缺陷分析能力。

## Impact
- Affected specs: AI 智能模式全流程体验 (Requirement -> Exploration -> Generation -> Execution -> Report).
- Affected code: `frontend/src/views/ai-intelligent-mode/*`, 后端 `explorations` 和 `requirement_analysis` 模块。

## ADDED Requirements
### Requirement: AI Auto-Exploration to Test Cases
系统应允许用户将“系统自动探索”得到的功能点直接转化为 AI 测试用例。
#### Scenario: Success case
- **WHEN** 用户在“AI工作成果”或探索详情中选中某个提取的功能点并点击“生成用例”
- **THEN** 系统自动跳转并带入上下文，生成对应的测试用例。

## MODIFIED Requirements
### Requirement: Seamless Requirement to Test Case Flow
现有的需求分析模块完成后，应直接提供明确的下一步操作。
#### Scenario: Success case
- **WHEN** 需求分析任务完成
- **THEN** 界面上显眼位置出现“基于此需求生成测试用例”按钮，点击后无缝衔接至用例生成流程。
