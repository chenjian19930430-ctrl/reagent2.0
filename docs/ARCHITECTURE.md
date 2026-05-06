# ReAgent v2.0 · 技术架构文档

> **版本**: 2.0.0
> **更新日期**: 2026-05-06
> **状态**: ✅ 已定稿
> **关联任务**: JJC-20260506-007-工部

---

## 1. 系统总体架构

### 1.1 模块分层图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         REST API Layer                              │
│          FastAPI · /api/v1/{ai,content,profile,automation}          │
│          SSE Streaming · OpenAPI (Swagger/ReDoc)                    │
└────────┬──────────────┬───────────────┬──────────────┬──────────────┘
         │              │               │              │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐    ┌────▼──────────┐
    │   AI    │    │ Content │    │ Profile │    │  Automation   │
    │ Model   │    │Generation│    │ Analysis│    │   Engine      │
    │ Adapter │    │ Pipeline│    │  Module │    │               │
    └────┬────┘    └────┬────┘    └────┬────┘    └────┬──────────┘
         │              │               │              │
    ┌────▼──────────────▼───────────────▼──────────────▼──────────┐
    │                   Shared Infrastructure                     │
    │    Config (pydantic-settings)  ·  Cache (Memory/Redis)      │
    │    Logging (Loguru)  ·  Errors (层次化异常)                 │
    └─────────────────────────────────────────────────────────────┘
```

### 1.2 模块职责

| 层级 | 模块 | 职责 |
|------|------|------|
| 路由层 | `reagent/api/` | FastAPI 路由定义，请求验证与响应序列化 |
| 业务层 | `reagent/ai/` | AI模型统一接入、多模型路由、生成编排 |
| 业务层 | `reagent/content/` | 内容生成管线（文案→Banner→落地页） |
| 业务层 | `reagent/profile/` | 用户画像分析、分群、行业模板 |
| 业务层 | `reagent/automation/` | 规则引擎、事件触发、动作执行 |
| 基础层 | `reagent/shared/` | 配置、缓存、日志、错误处理 |

---

## 2. 技术栈选型

### 2.1 核心栈

| 层级 | 选型 | 版本 | 选型理由 |
|------|------|------|----------|
| 后端框架 | FastAPI | 0.115+ | 异步原生、性能优异、自动 OpenAPI |
| 运行时 | Python | 3.11+ | 生态完善、AI/ML 支持 |
| 数据校验 | Pydantic | 2.5+ | 类型安全、序列化、Schema 生成 |
| 配置管理 | pydantic-settings | 2.1+ | 环境变量注入、类型校验 |
| HTTP 服务 | uvicorn | 0.30+ | ASGI 服务器、WebSocket 支持 |
| 日志 | Loguru | 0.7+ | 结构化日志、自动旋转 |

### 2.2 AI 模型接入

| 供应商 | SDK | 默认模型 | 能力 |
|--------|-----|----------|------|
| OpenAI | openai ≥ 1.50 | gpt-4o | 文本/代码/图像理解/工具调用 |
| Anthropic | anthropic ≥ 0.40 | claude-sonnet-4-20250514 | 文本/代码/工具调用 |
| Local/Ollama | openai (兼容端点) | qwen2.5:14b | 文本/代码（免费） |
| LiteLLM | litellm ≥ 1.40 | 按配置 | 多供应商聚合 |

### 2.3 内容生成

| 组件 | 技术选型 | 备注 |
|------|----------|------|
| 图片生成 | Pillow (PIL) | Phase 1 MVP，纯代码合成 |
| 视频拼接 | FFmpeg (subprocess) | Phase 1 MVP，后期替换 MiniMax |
| 模板渲染 | Jinja2 | 落地页 HTML 生成 |
| Markdown | markdown ≥ 3.5 | 文案 Markdown→HTML 转换 |

### 2.4 数据与存储

| 组件 | 选型 | 备注 |
|------|------|------|
| 数据库 | SQLite (Dev) / PostgreSQL (Prod) | ORM 待定（SQLAlchemy/Prisma） |
| 缓存 | MemoryCache (Dev) / Redis (Prod) | 统一 CacheBackend 接口 |
| 文件存储 | 本地文件系统 → OSS | 素材输出目录化 |

---

## 3. 核心模块设计

### 3.1 AI 模型适配层

#### 设计模式：策略模式 + 注册表模式

```
┌──────────────────────────────────────────┐
│           BaseAIAdapter (ABC)            │
│  ├── generate(request) → GenerationResult │
│  ├── generate_stream(request) → AsyncGen  │
│  └── get_model_info() → ModelInfo         │
└────────────┬──────────────┬──────────────┘
             │              │
    ┌────────▼──┐    ┌─────▼──────┐    ┌─────▼──────┐
    │OpenAI     │    │  Claude    │    │   Local    │
    │Adapter    │    │  Adapter   │    │  Adapter   │
    └───────────┘    └────────────┘    └────────────┘
             │              │               │
             └──────────────┼───────────────┘
                            ▼
                   ┌────────────────┐
                   │AIAdapterRegistry│
                   │  • resolve()    │
                   │  • generate()   │
                   │  • list_models()│
                   └────────────────┘
```

#### 模型路由规则

1. 精确匹配：`openai:gpt-4o` → 直接返回对应适配器
2. Provider 匹配：`openai:` 前缀 → 返回 OpenAI 系列的任意适配器
3. 默认降级：未命中时使用 `ai_default_provider` 配置
4. 兜底：获取第一个可用适配器

#### 核心数据结构

```python
class ModelRequest:
    provider: ModelProvider    # openai / anthropic / local
    model: str                # 模型标识
    messages: list[Message]   # 对话消息
    system_prompt: str        # 系统提示
    temperature: float        # 温度 (0-2)
    max_tokens: int           # 最大输出
    stream: bool              # 是否流式
    tools: list[dict]         # 工具调用

class ModelResponse:
    provider: ModelProvider
    model: str
    content: str              # 生成文本
    tool_calls: list[ToolCall]
    usage: dict               # token 用量
```

### 3.2 内容生成管线

#### 管线编排

```
用户请求 → ContentPipeline.run()
  │
  ├─ Stage 1: Copywriting （AI 模型生成文案）
  │   ├─ 多语调支持 (专业/友好/紧迫/高端/随意/幽默)
  │   ├─ SEO 关键词建议
  │   └─ JSON 结构化输出
  │
  ├─ Stage 2: Banner（PIL 合成图片）
  │   ├─ 多尺寸支持 (1080×1080 / 1200×628 / 720×1280)
  │   ├─ 渐变色背景 + 文字叠加
  │   └─ 品牌色自动适配
  │
  └─ Stage 3: Landing Page（Jinja2 HTML）
      ├─ 响应式设计
      ├─ Markdown → HTML 渲染
      └─ 品牌风格注入
```

#### 各阶段独立可调用

```python
# 仅文案
pipeline.generate_copy_only(request)

# 全管线
pipeline.generate_full(request)

# 自定义组合
copy = await copywriter.generate(request)
banner = await banner_generator.generate(banner_request)
html, path = await landing_gen.generate(copy)
```

### 3.3 用户画像分析模块

#### 双模式分析引擎

```
ProfileAnalyzer.analyze(request)
  │
  ├─ 规则模式 (快速分群)
  │   ├─ 基于 industry 模板
  │   ├─ 分段阈值判断
  │   └─ 流失风险计算
  │
  └─ AI 模式 (深度洞察，可选)
      ├─ 行为模式分析
      ├─ 人群特征提炼
      ├─ 下一步最佳行动建议
      └─ 自然语言画像描述
```

#### 行业模板库

| 模板 | 关键特征 | 默认分群 |
|------|----------|----------|
| 电商 | 客单价、品类偏好、复购率 | VIP/复购达人/新品探索者 |
| 教育 | 学习时长、完课率、付费意愿 | 学霸/试听/付费用户 |
| SaaS | 活跃功能、团队规模、NPS | Power用户/决策者 |
| 通用 | 活跃度、LTV、流失风险 | 高活跃/新用户/沉默 |

### 3.4 营销自动化引擎

#### 核心架构

```
┌──────────────────────────────────────────────────┐
│                  AutomationEngine                 │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────┐ │
│  │ RuleEvaluator │  │TriggerManager│  │ActionHandler│
│  └──────┬───────┘  └──────┬──────┘  └─────┬────┘ │
│         │                 │                │      │
│  ┌──────┴───────┐  ┌──────┴──────┐  ┌─────┴────┐ │
│  │ 条件评估引擎 │  │ 事件/定时   │  │ 动作执行器 │ │
│  │ - 12种运算符 │  │ 触发器      │  │ - 消息    │ │
│  │ - AND/OR逻辑 │  │ - CoolDown  │  │ - Webhook │ │
│  │ - 多数据源   │  │ - 审计      │  │ - 标签    │ │
│  └──────────────┘  └─────────────┘  └──────────┘ │
└──────────────────────────────────────────────────┘
```

#### 条件运算符（12种）

| 运算符 | 说明 | 示例 |
|--------|------|------|
| eq | 等于 | `plan == "premium"` |
| neq | 不等于 | `role != "viewer"` |
| gt | 大于 | `total_spent > 5000` |
| gte | 大于等于 | `purchase_count >= 10` |
| lt | 小于 | `churn_risk < 0.3` |
| lte | 小于等于 | `days_since_login <= 30` |
| contains | 包含 | `email contains "@corp.com"` |
| in | 在列表中 | `role in ["admin","owner"]` |
| not_in | 不在列表中 | `plan not_in ["free","trial"]` |
| matches | 正则匹配 | `phone matches "^1[3-9]"` |
| exists | 字段存在 | `wechat_id exists` |
| not_exists | 字段不存在 | `company not_exists` |

#### 动作队列

| 动作 | 配置说明 | 延迟支持 | 冷却支持 |
|------|----------|----------|----------|
| send_message | channel + template | ✅ | ✅ |
| update_segment | segment + operation | ✅ | ✅ |
| trigger_campaign | campaign_id | ✅ | ✅ |
| call_webhook | url + method | ✅ | ✅ |
| assign_tag | tags 数组 | ✅ | ✅ |
| update_profile | field + value | ✅ | ✅ |
| generate_content | AI生成配置 | ✅ | ✅ |

---

## 4. 数据流设计

### 4.1 AI 内容生成数据流

```
Client                  API                     Pipeline                AI Model
  │                     │                        │                       │
  │  POST /content/generate                      │                       │
  │ ──────────────────►│                        │                       │
  │                    │  ContentGenerationReq    │                       │
  │                    │ ─────────────────────►  │                       │
  │                    │                        │                       │
  │                    │  Stage 1: Copy          │                       │
  │                    │ ─────────────────────►  │                       │
  │                    │                        │  ModelRequest          │
  │                    │                        │ ─────────────────────►│
  │                    │                        │  GenerationResult     │
  │                    │                        │ ◄─────────────────────│
  │                    │  CopywritingResponse    │                       │
  │                    │ ◄───────────────────── │                       │
  │                    │                        │                       │
  │                    │  Stage 2: Banner        │                       │
  │                    │ ─────────────────────►  │                       │
  │                    │  BannerResponse         │                       │
  │                    │ ◄───────────────────── │                       │
  │                    │                        │                       │
  │                    │  Stage 3: Landing       │                       │
  │                    │ ─────────────────────►  │                       │
  │                    │  Landing HTML + File    │                       │
  │                    │ ◄───────────────────── │                       │
  │                    │                        │                       │
  │  ContentGenResp    │                        │                       │
  │ ◄──────────────────│                        │                       │
  │                    │                        │                       │
```

### 4.2 营销自动化事件流

```
外部系统/用户                    AutomationEngine                 RuleEvaluator
    │                              │                                │
    │  自动化事件 (POST /events/process)                              │
    │ ───────────────────────────► │                                │
    │                              │  resolve trigger               │
    │                              │ ───────────────────────────►   │
    │                              │                                │
    │                              │  evaluate conditions           │
    │                              │ ───────────────────────────►   │
    │                              │  bool: matched / not           │
    │                              │ ◄───────────────────────────   │
    │                              │                                │
    │  if matched:                                                  │
    │                              │  execute actions               │
    │                              │    │─ send_message             │
    │                              │    │─ update_segment           │
    │                              │    │─ call_webhook             │
    │                              │    │─ ...                      │
    │                              │                                │
    │                              │  record execution              │
    │                              │  update cooldown               │
    │                              │                                │
    │  matched_rules + results     │                                │
    │ ◄─────────────────────────── │                                │
    │                              │                                │
```

---

## 5. API 接口规范

### 5.1 通用约定

- **Base URL**: `/api/v1`
- **格式**: JSON (request/response)
- **流式**: Server-Sent Events (`text/event-stream`)
- **分页**: `?limit=N&offset=N`
- **错误**: 统一 `{error, message, detail}` 格式
- **认证**: JWT Bearer Token (Header: `Authorization: Bearer <token>`)

### 5.2 接口速览

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| AI | POST | `/api/v1/ai/generate` | AI 文本生成 |
| AI | GET | `/api/v1/ai/models` | 可用模型列表 |
| AI | POST | `/api/v1/ai/generate/stream` | SSE 流式生成 |
| Content | POST | `/api/v1/content/generate` | 端到端内容生成 |
| Content | POST | `/api/v1/content/copy` | 仅生成文案 |
| Content | POST | `/api/v1/content/full` | 全管线生成 |
| Profile | POST | `/api/v1/profile/analyze` | 分析用户画像 |
| Profile | GET | `/api/v1/profile/templates` | 行业模板列表 |
| Profile | GET | `/api/v1/profile/templates/{industry}` | 获取行业模板详情 |
| Automation | POST | `/api/v1/automation/rules` | 创建自动化规则 |
| Automation | GET | `/api/v1/automation/rules` | 规则列表 |
| Automation | GET | `/api/v1/automation/rules/{id}` | 规则详情 |
| Automation | PUT | `/api/v1/automation/rules/{id}` | 更新规则 |
| Automation | DELETE | `/api/v1/automation/rules/{id}` | 删除规则 |
| Automation | POST | `/api/v1/automation/campaigns` | 创建活动 |
| Automation | POST | `/api/v1/automation/campaigns/{id}/activate` | 激活活动 |
| Automation | POST | `/api/v1/automation/campaigns/{id}/pause` | 暂停活动 |
| Automation | POST | `/api/v1/automation/events/process` | 处理事件 |
| Automation | GET | `/api/v1/automation/executions` | 执行记录 |
| System | GET | `/api/v1/health` | 健康检查 |

---

## 6. Phase 1 开发重点

### 6.1 已完成

| 模块 | 状态 | 说明 |
|------|------|------|
| AI 模型适配层 | ✅ 完成 | OpenAI + Claude + Local 三适配器 |
| 文案撰写 | ✅ 完成 | 多语调、SEO、结构化输出 |
| Banner 生成 | ✅ MVP | PIL 合成，多尺寸+渐变色 |
| 落地页生成 | ✅ MVP | Jinja2 响应式 HTML |
| FFmpeg 媒体拼接 | ✅ MVP | 视频拼接+文字叠加 |
| 用户画像分析 | ✅ 完成 | 规则+AI 双模式 |
| 行业模板 | ✅ 完成 | 电商/教育/SaaS/通用 |
| 规则引擎 | ✅ 完成 | 12种运算符+AND/OR |
| 事件触发 | ✅ 完成 | 事件+定时触发+冷却 |
| 动作执行 | ✅ 完成 | 7种动作类型 |
| REST API | ✅ 完成 | 完整 v1 接口 |
| 单元测试 | ✅ 完成 | 43个测试全部通过 |

### 6.2 Phase 2 计划（待定）

| 模块 | 优先级 | 说明 |
|------|--------|------|
| 数据库持久化 | P0 | 从内存存储迁移到 PostgreSQL |
| WebSocket 支持 | P0 | 实时事件推送 |
| MiniMax 视频生成 | P1 | 替代 FFmpeg MVP |
| 推荐引擎 | P1 | 协同过滤+内容推荐 |
| 分析看板 | P1 | 实时指标与可视化 |
| A/B 测试框架 | P2 | 内容版本比较 |
| 多租户 | P2 | 企业级隔离 |
| 合规审计 | P2 | GDPR 审计日志 |

---

## 7. 回滚方案

### 7.1 代码回滚

```bash
# 方法一：切换到旧分支
git checkout main
git branch -D feature/architecture-redesign

# 方法二：revert 提交
git revert HEAD --no-edit

# 方法三：重置到旧版本
git reset --hard <last-stable-commit-hash>
```

### 7.2 数据结构回滚

- Phase 1 使用内存存储，无需数据迁移
- 如已启用 Redis，清空缓存：`redis-cli FLUSHDB`
- 后续 Phase 2 引入数据库后，需执行向下迁移脚本

### 7.3 服务回滚

```bash
# 停止新服务
kill $(lsof -ti:8000)

# 启动旧服务
bash scripts/run.sh  # 旧版本
```

---

> **文档维护**: 工部尚书 · JJC-20260506-007-工部
> **上次更新**: 2026-05-06 17:30 CST
