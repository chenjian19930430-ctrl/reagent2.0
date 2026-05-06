# ReAgent 基础设计规范

> **版本:** v1.0 | **最后更新:** 2026-05-06  
> **适用阶段:** Phase 1 MVP

本文档定义了 ReAgent 的架构设计原则、API 规范、数据模型约定与 UI 设计指南。

---

## 目录

1. [架构设计原则](#1-架构设计原则)
2. [API 设计规范](#2-api-设计规范)
3. [数据模型约定](#3-数据模型约定)
4. [错误处理规范](#4-错误处理规范)
5. [日志与可观测性](#5-日志与可观测性)
6. [UI/UX 设计指南](#6-uiux-设计指南)

---

## 1. 架构设计原则

### 1.1 分层架构

```
┌──────────────────────────────────────────┐
│          API Layer (FastAPI)              │
│  路由 · 认证 · 请求/响应序列化            │
├──────────────────────────────────────────┤
│          Service Layer                    │
│  业务逻辑 · 编排 · 事件发布               │
├──────────────────────────────────────────┤
│          Engine Layer                     │
│  推荐算法 · 工作流引擎 · 指标计算         │
├──────────────────────────────────────────┤
│          Data Layer                       │
│  模型定义 · 存储抽象 · 缓存               │
└──────────────────────────────────────────┘
```

### 1.2 设计原则

| 原则 | 说明 |
|---|---|
| **单一职责** | 每个模块只关注一个业务领域 |
| **接口分离** | REST API 与服务层接口分离，API 层仅负责序列化与路由 |
| **依赖注入** | 服务层通过构造器注入配置与依赖，便于测试 |
| **事件驱动** | 模块间通过事件总线解耦通信 |
| **配置外部化** | 所有环境相关配置通过 environment / 配置文件注入 |

### 1.3 模块间通信

```
API 请求 → API Gateway → (auth) → 目标模块 API → Service → Engine/Data
                                                          ↓
                                                    事件总线 (Event Bus)
                                                          ↓
                                           marketing-automation → analytics
```

Phase 1 中模块间通过直接方法调用（同步），Phase 2 引入事件总线（异步）。

---

## 2. API 设计规范

### 2.1 通用规则

- **基础路径:** `/api/v1/{module}`
- **响应格式:** 统一的 JSON 封装
- **认证:** JWT Bearer Token（`Authorization: Bearer <token>`）
- **版本化:** 路径版本控制 (`/api/v1/`, `/api/v2/`)
- **幂等性:** POST 创建返回 201 + Location，PUT 全量更新，PATCH 部分更新

### 2.2 响应格式

**成功响应:**
```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-05-06T10:00:00Z"
  }
}
```

**列表响应:**
```json
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total": 150,
    "request_id": "req_abc123",
    "timestamp": "2026-05-06T10:00:00Z"
  }
}
```

### 2.3 端点命名

| 动作 | HTTP 方法 | 端点 | 响应码 |
|---|---|---|---|
| 列表 | GET | `/api/v1/profiles` | 200 |
| 查询单个 | GET | `/api/v1/profiles/{id}` | 200 / 404 |
| 创建 | POST | `/api/v1/profiles` | 201 |
| 全量更新 | PUT | `/api/v1/profiles/{id}` | 200 / 404 |
| 部分更新 | PATCH | `/api/v1/profiles/{id}` | 200 / 404 |
| 删除 | DELETE | `/api/v1/profiles/{id}` | 204 / 404 |

**当前已注册端点前缀:**

| 模块 | 前缀 | 说明 |
|---|---|---|
| 客户画像 | `/api/v1/profiles` | 客户画像 CRUD |
| 推荐引擎 | `/api/v1/recommendations` | 推荐查询 |
| 营销自动化 | `/api/v1/automation` | 工作流与活动管理 |
| 分析仪表盘 | `/api/v1/analytics` | 指标与报告 |

---

## 3. 数据模型约定

### 3.1 通用字段

所有数据库模型应包含以下基础字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | UUID / String | 全局唯一标识 |
| `created_at` | DateTime (UTC) | 创建时间 |
| `updated_at` | DateTime (UTC) | 最后更新时间 |

### 3.2 客户画像模型 (Profile)

```python
class CustomerProfile(BaseModel):
    id: str
    external_id: str | None          # 外部系统 ID
    name: str | None
    email: str | None
    traits: dict[str, Any]           # 基础属性（年龄、地区、职业等）
    tags: list[str]                  # 行为标签（高价值、活跃、流失倾向等）
    scores: dict[str, float]         # 预测评分（购买倾向、流失风险等）
    enrichment_version: str          # 丰富引擎版本
    created_at: datetime
    updated_at: datetime
```

### 3.3 推荐模型 (Recommendation)

```python
class RecommendationResult(BaseModel):
    customer_id: str
    items: list[RecommendedItem]
    strategy: str                    # 推荐策略名称
    version: str                     # 模型版本
    timestamp: datetime

class RecommendedItem(BaseModel):
    item_id: str
    score: float                     # 0-1 归一化分数
    reason: str | None               # 推荐理由
```

### 3.4 工作流模型 (Workflow)

```python
class WorkflowNode(BaseModel):
    id: str
    type: Literal["condition", "action", "timer", "split"]
    config: dict[str, Any]

class WorkflowEdge(BaseModel):
    source: str                      # 源节点 ID
    target: str                      # 目标节点 ID
    condition: str | None            # 条件表达式

class Workflow(BaseModel):
    id: str
    name: str
    description: str
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]
    enabled: bool
    created_at: datetime
    updated_at: datetime
```

---

## 4. 错误处理规范

### 4.1 统一错误响应

```json
{
  "error": {
    "code": "PROFILE_NOT_FOUND",
    "message": "客户画像不存在",
    "details": {
      "profile_id": "abc-123"
    },
    "request_id": "req_abc123"
  }
}
```

### 4.2 错误码体系

| 错误码 | HTTP 状态码 | 说明 |
|---|---|---|
| `UNAUTHORIZED` | 401 | 未认证或 token 过期 |
| `FORBIDDEN` | 403 | 无权限访问 |
| `NOT_FOUND` | 404 | 资源不存在 |
| `VALIDATION_ERROR` | 422 | 请求数据校验失败 |
| `RATE_LIMITED` | 429 | 请求频率超限 |
| `INTERNAL_ERROR` | 500 | 服务端内部错误 |
| `SERVICE_UNAVAILABLE` | 503 | 服务暂时不可用 |

### 4.3 异常类

```python
# Predefined exception hierarchy
class ReAgentError(Exception): ...
class NotFoundError(ReAgentError): ...
class ValidationError(ReAgentError): ...
class AuthError(ReAgentError): ...
class RateLimitError(ReAgentError): ...
```

---

## 5. 日志与可观测性

### 5.1 结构化日志格式

```json
{
  "timestamp": "2026-05-06T10:00:00.123Z",
  "level": "INFO",
  "logger": "reagent.customer-profile",
  "request_id": "req_abc123",
  "message": "Profile enrichment completed",
  "extra": {
    "profile_id": "p_123",
    "source_events": 15,
    "tags_added": 3,
    "duration_ms": 42
  }
}
```

### 5.2 日志级别

| 级别 | 使用场景 |
|---|---|
| `DEBUG` | 开发调试信息 |
| `INFO` | 业务流程关键节点 |
| `WARNING` | 非异常但需要注意的情况 |
| `ERROR` | 可恢复的错误（如超时重试后仍失败） |
| `CRITICAL` | 不可恢复的系统级故障 |

---

## 6. UI/UX 设计指南

> Phase 1 以 API 为主，前端仪表盘为辅助。以下指南适用于 Phase 2 的前端开发。

### 6.1 品牌色

| 用途 | 色值 |
|---|---|
| 主色 | `#8A2BE2` (紫罗兰) |
| 辅助色 | `#4169E1` (皇家蓝) |
| 成功 | `#2ECC71` |
| 警告 | `#F39C12` |
| 错误 | `#E74C3C` |
| 背景 | `#F8F9FA` |
| 文字 | `#2C3E50` |

### 6.2 排版

| 层级 | 字号 | 字重 | 用途 |
|---|---|---|---|
| H1 | 28px | Bold | 页面标题 |
| H2 | 22px | Semibold | 区域标题 |
| H3 | 18px | Semibold | 卡片标题 |
| Body | 14px | Regular | 正文 |
| Small | 12px | Regular | 辅助文字 |

### 6.3 间距

采用 4px 基准网格：4, 8, 12, 16, 20, 24, 32, 40, 48, 64px

### 6.4 通用文案规范

| 场景 | 中文 | English |
|---|---|---|
| 加载中 | 正在加载… | Loading… |
| 空状态 | 暂无数据 | No data |
| 保存成功 | 保存成功 | Saved |
| 操作失败 | 操作失败，请重试 | Action failed, please retry |
| 确认删除 | 确认删除？此操作不可撤销。 | Delete? This action cannot be undone. |
| 搜索占位 | 搜索客户、活动… | Search customers, campaigns… |

---

> 本文档由礼部维护，随产品演进持续更新。Phase 2 将补充事件总线规范、前端组件库文档与 OpenAPI 规范。
