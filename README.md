# ReAgent · 重构智能ReAgent 🧠

**ReAgent（重构智能ReAgent）** 是新一代 AI 驱动的智能营销平台。

核心能力：
- **🤖 AI 内容生成** — 多模型文案撰写 + Banner/落地页素材生成
- **👤 用户画像分析** — 通用画像分析 + 行业模板 + AI 洞察
- **⚙️ 营销自动化** — 规则引擎驱动的营销编排

---

## 🏗 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                     REST API (FastAPI)                    │
│   /api/v1/ai · /api/v1/content · /api/v1/profile · ...   │
└────────┬──────────┬──────────┬──────────┬────────────────┘
         │          │          │          │
    ┌────▼────┐┌───▼────┐┌───▼────┐┌───▼──────────┐
    │   AI    ││ Content││Profile ││ Automation   │
    │ Adapter ││Pipeline││Analyzer││   Engine     │
    │  Layer  ││        ││        ││              │
    └────┬────┘└───┬────┘└───┬────┘└───┬──────────┘
         │         │         │         │
    ┌────▼─────────▼─────────▼─────────▼──────────┐
    │              Shared Infrastructure           │
    │    Config · Cache · Logging · Errors         │
    └──────────────────────────────────────────────┘
```

### AI 模型适配层（多模型切换）

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│  OpenAI     │  │  Anthropic  │  │   Local     │
│  Adapter    │  │  Claude     │  │   Ollama    │
│  (GPT-4o)   │  │  (Sonnet)   │  │   (Qwen)    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       └────────────────┼────────────────┘
                        ▼
              ┌─────────────────┐
              │  AI Registry    │
              │  (auto-routing) │
              └─────────────────┘
```

### 内容生成管线

```
文案请求 ──► AI Model ──► 文案输出
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Banner生成           Landing页生成
             (PIL/FFmpeg)         (Jinja2/HTML)
                    │                   │
                    └─────────┬─────────┘
                              ▼
                        素材输出
```

---

## 🚀 Quick Start

### 1. 环境准备

```bash
# Clone
cd /path/to/reagent

# 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 依赖
pip install -r requirements.txt

# 配置
cp .env.example .env
# 编辑 .env，填入 API Key
```

### 2. 启动服务

```bash
bash scripts/run.sh
# 或直接
python3 -m reagent.main
```

### 3. 验证

```bash
curl http://localhost:8000/api/v1/health
# → {"status":"ok","version":"2.0.0","service":"ReAgent"}
```

### 4. 运行测试

```bash
cd /path/to/reagent
python3 -m pytest tests/ -v
```

---

## 📡 API 概览

### AI 模型

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/ai/generate` | AI 文本生成 |
| GET | `/api/v1/ai/models` | 可用模型列表 |
| POST | `/api/v1/ai/generate/stream` | SSE 流式生成 |

### 内容生成

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/content/generate` | 端到端内容生成 |
| POST | `/api/v1/content/copy` | 仅生成文案 |
| POST | `/api/v1/content/full` | 全管线（文案+Banner+落地页） |

### 用户画像

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/profile/analyze` | 分析用户画像 |
| GET | `/api/v1/profile/templates` | 行业模板列表 |
| GET | `/api/v1/profile/templates/{industry}` | 获取行业模板 |

### 营销自动化

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/automation/rules` | 创建规则 |
| GET | `/api/v1/automation/rules` | 规则列表 |
| POST | `/api/v1/automation/campaigns` | 创建活动 |
| POST | `/api/v1/automation/events/process` | 处理事件 |
| GET | `/api/v1/automation/executions` | 执行记录 |

---

## 🧩 模块一览

### reagent/ai/ — AI 模型适配层
- `base.py` — 适配器接口抽象
- `registry.py` — 模型注册与路由
- `openai_adapter.py` — OpenAI/GPT-4o
- `claude_adapter.py` — Anthropic Claude
- `local_adapter.py` — Local/Ollama

### reagent/content/ — 内容生成管线
- `pipeline.py` — 管线编排器
- `copywriter.py` — AI 文案撰写
- `banner.py` — Banner 图片生成 (PIL)
- `landing.py` — 落地页 HTML 生成 (Jinja2)
- `media_gen.py` — FFmpeg 视频拼接

### reagent/profile/ — 用户画像分析
- `analyzer.py` — 画像分析引擎
- `segmenter.py` — 用户分群引擎
- `templates.py` — 行业模板管理

### reagent/automation/ — 营销自动化
- `engine.py` — 核心编排引擎
- `rules.py` — 规则条件评估
- `triggers.py` — 事件/定时触发器
- `actions.py` — 动作执行器

---

## 📋 Phase 1 开发状态

| 模块 | 状态 | 备注 |
|------|------|------|
| AI 模型适配层 | ✅ 完成 | OpenAI + Claude + Local |
| 文案撰写 | ✅ 完成 | 多语调支持 |
| Banner 生成 | ✅ MVP | PIL 图片合成 |
| 落地页生成 | ✅ MVP | Jinja2 HTML 渲染 |
| FFmpeg 媒体拼接 | ✅ MVP | 视频拼接 + 文字叠加 |
| 用户画像分析 | ✅ 完成 | AI洞察 + 规则分群 |
| 行业模板库 | ✅ 完成 | 电商/教育/SaaS/通用 |
| 规则引擎 | ✅ 完成 | CRUD + 条件评估 |
| 事件触发 | ✅ 完成 | 事件 + 定时触发 |
| 动作执行 | ✅ 完成 | 消息/Webhook/标签等 |
| API 接口 | ✅ 完成 | RESTful + 流式支持 |
| 单元测试 | ✅ 完成 | 80+ 测试用例 |

---

## 🛠 技术栈

| 层级 | 选型 |
|------|------|
| 后端框架 | Python FastAPI |
| API 模式 | REST + SSE Streaming |
| AI 接入 | OpenAI SDK / Anthropic SDK / LiteLLM |
| 数据校验 | Pydantic v2 |
| 配置管理 | pydantic-settings |
| 图片生成 | Pillow (PIL) |
| 模板渲染 | Jinja2 |
| 视频处理 | FFmpeg (subprocess) |
| 缓存 | MemoryCache / Redis |
| 日志 | Loguru |
| HTTP 客户端 | httpx |

---

## 📄 License

MIT
