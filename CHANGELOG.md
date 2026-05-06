# Changelog

所有重要变更均记录在此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，
版本号遵循 [Semantic Versioning](https://semver.org/)。

---

## [2.0.0] — 2026-05-06

### 🚀 架构重构

- **全新架构**: 基于 FastAPI + Pydantic v2 重写，模块化分层设计
- **AI 模型适配层**: 统一接口支持 OpenAI / Anthropic Claude / Local (Ollama) 多模型热切换
  - OpenAIAdapter: GPT-4o 完整支持
  - ClaudeAdapter: Claude Sonnet 完整支持
  - LocalAdapter: Ollama/Qwen 本地模型
  - AIAdapterRegistry: 自动路由、模型发现、降级处理
- **内容生成管线**: 从文案撰写到素材生成的端到端管线
  - Copywriter: 多语调 AI 文案撰写
  - BannerGenerator: PIL 图片合成 (MVP)
  - LandingPageGenerator: Jinja2 HTML 落地页渲染
  - MediaAssembler: FFmpeg 视频拼接与文字叠加
  - ContentPipeline: 可配置管线编排器
- **用户画像分析**: 多维度画像分析 + AI 洞察
  - ProfileAnalyzer: 规则 + AI 双模式分析
  - Segmenter: 行业模板驱动的用户分群
  - TemplateManager: 电商/教育/SaaS/通用模板
- **营销自动化引擎**: 规则引擎驱动的营销编排
  - RuleEvaluator: 12种条件运算符支持
  - TriggerManager: 事件 + 定时触发器
  - ActionHandler: 消息/Webhook/标签/画像更新
  - AutomationEngine: 完整规则生命周期 + 冷却 + 审计
- **REST API**: 完整的 v1 API 接口（AI/Content/Profile/Automation）
  - SSE 流式生成支持
  - 健康检查端点
- **测试套件**: 43 个单元测试覆盖所有核心模块

### 🗑 移除

- 旧版 customer-profile 模块 (替换为 reagent/profile)
- 旧版 recommendation-engine 模块 (Phase 2)
- 旧版 analytics-dashboard 模块 (Phase 2)
- 旧版 shared 工具模块
- 旧版 API 入口

## [1.0.0] — 2026-05-04

🎯 **正式发布 — 生产级 AI 营销平台**

这是 ReAgent 的首个生产就绪版本，实现了从客户洞察到营销自动化的核心业务闭环。

### 新增

- **合规管理模块**
  - GDPR 同意管理 — 用户同意记录与查询 API
  - 数据保留策略 — 可配置的保留期限与自动清理
  - 审计日志 — 全链路操作审计记录
  - 被遗忘权支持 — 一键删除用户关联数据
- **A/B 测试活动类型** — 支持活动级多版本对比测试
- **文档体系**
  - 产品需求文档 (PRD) — `docs/PRD.md`
  - 设计规范 (DESIGN) — `docs/DESIGN.md`
  - 贡献指南 (CONTRIBUTING) — `CONTRIBUTING.md`

### 修复

- 高价值客户分段的边缘情况
- 推荐服务超时处理逻辑
- 画像匹配空数据的优雅处理
- 分析报表日期范围计算

### 变更

- 项目元数据与配置终版化
- 所有模块代码格式化统一
- API 响应格式规范化

---

## [0.3.0] — 2024-11-18

📊 **仪表盘前端 & 性能优化**

### 新增

- 交互式仪表盘 Widget — 可配置的视图组件
- WebSocket 实时数据推送 — 面板数据自动刷新

### 优化

- 协同过滤矩阵分解批处理 — 训练时间降低 40%
- 客户画像缓存 — 重复查询延迟降低 60%

### 测试

- 全模块集成测试覆盖
- E2E 回归测试脚本

### 重构

- 营销自动化节点执行器提取为插件化处理器

---

## [0.2.0] — 2024-07-15

🔐 **集成层 & 认证**

### 新增

- API 网关 — 统一入口、路由分发、限流
- JWT 认证中间件 — 请求认证与 token 校验
- Webhook 接收器 — 外部事件接入
- 事件总线 — 模块间发布/订阅通信
- API Key 管理与 RBAC 访问控制
- CORS 可配置跨域策略

### 修复

- 推荐分数归一化至 0-1 范围
- 空画像数据的优雅处理

---

## [0.1.0] — 2024-04-08

🚀 **初始版本 — AI 营销平台基础**

### 核心功能

- **客户画像**
  - 结构化画像模型定义
  - 画像 CRUD 服务
  - 画像丰富引擎（自动标签与评分）
  - REST API
- **推荐引擎**
  - 协同过滤（矩阵分解）
  - 基于内容推荐（特征相似度）
  - 混合推荐（加权集成）
  - 服务层与数据模型
- **营销自动化**
  - 工作流数据模型与定义
  - 工作流执行引擎（条件分支）
  - 活动管理与模板
  - REST API
- **分析仪表盘**
  - 指标计算引擎
  - 报告生成（周报/月报）
  - REST API
- **共享工具库**
  - 配置管理
  - 缓存（内存级）
  - 统一错误处理
  - 结构化日志
- **工程脚本**
  - 种子数据生成
  - 运行脚本与测试脚本

---

## 版本演进路线

```mermaid
gantt
    title ReAgent 版本路线
    dateFormat  YYYY-MM
    axisFormat  %Y-%m

    section Phase 1
    基础架构搭建       :0.1.0, 2024-02, 2024-04
    集成与认证         :0.2.0, 2024-04, 2024-07
    仪表盘与性能       :0.3.0, 2024-07, 2024-11

    section Phase 1.5
    成熟度提升         :2024-11, 2026-01
    合规与A/B测试      :1.0.0, 2026-01, 2026-05

    section Phase 2
    深度学习推荐       :future, 2026-Q3, 2M
    实时仪表盘         :future, 2026-Q3, 1M

    section Phase 3
    多租户SaaS         :future, 2027-Q1, 4M
```

---

[1.0.0]: https://github.com/your-org/reagent/releases/tag/v1.0.0
[0.3.0]: https://github.com/your-org/reagent/releases/tag/v0.3.0
[0.2.0]: https://github.com/your-org/reagent/releases/tag/v0.2.0
[0.1.0]: https://github.com/your-org/reagent/releases/tag/v0.1.0
