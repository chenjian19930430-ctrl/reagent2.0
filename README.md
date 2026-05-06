# ReAgent 🧠

**AI Marketing System** — 面向现代营销的智能推荐与自动化平台，提供从客户画像分析到 ML 驱动营销活动编排的一体化方案。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

---

## 📦 Modules

| Module | Description |
|---|---|
| **customer-profile/** | 客户画像数据处理、Enrichment 引擎、CRUD 服务与 REST API |
| **recommendation-engine/** | 协同过滤、基于内容、混合推荐引擎，支持模型版本化与 A/B 测试 |
| **marketing-automation/** | 工作流编排引擎、活动模板管理、A/B 测试活动支持 |
| **analytics-dashboard/** | 指标计算、报告生成、WebSocket 实时数据面板 |
| **api/** | API 网关、JWT 认证、CORS、API Key 管理 |
| **shared/** | 配置管理、缓存、错误处理、日志工具集 |
| **scripts/** | 运行脚本、测试脚本、种子数据生成 |

## 🚀 Quick Start

```bash
pip install -r requirements.txt
python -m api.main
```

### Prerequisites

- Python 3.10+
- pip

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
bash scripts/test.sh

# Seed sample data
python scripts/seed_data.py

# Start the server
bash scripts/run.sh
```

## 🏗 Architecture

```
                    ┌─────────────┐
                    │  API Gateway │
                    │  (auth/CORS) │
                    └──────┬──────┘
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
  ┌────────────┐  ┌──────────────┐  ┌──────────────┐
  │  Customer  │  │  Marketing   │  │  Analytics   │
  │  Profile   │  │  Automation  │  │  Dashboard   │
  └────────────┘  └──────────────┘  └──────────────┘
  ┌─────────────────────────────────────────────────┐
  │          Recommendation Engine                   │
  │  (collaborative + content-based + hybrid)        │
  └─────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────┐
  │         Shared Infrastructure                    │
  │  (config · cache · errors · logging · event bus) │
  └─────────────────────────────────────────────────┘
```

### Key Features

- **Hybrid Recommendations**: 协同过滤 + 基于内容 + 加权集成混合推荐
- **Deep Learning ML**: 深度学习协同过滤，支持模型版本管理和 A/B 测试
- **Compliance Ready**: GDPR 同意管理、数据保留与审计日志
- **Real-time Dashboard**: WebSocket 驱动的实时指标面板

## 📜 Version History

| Version | Date | Highlights | Tag |
|---|---|---|---|
| **v1.0.0** | 2026-05-04 | 🎯 正式发布 — 生产级 AI 营销平台，GDPR 合规模块 | `v1.0.0` |
| **v0.3.0** | 2024-11-18 | 📊 仪表盘 & 性能优化、WebSocket 实时刷新 | `v0.3.0` |
| **v0.2.0** | 2024-07-15 | 🔐 集成层 & 认证（JWT、API Key、RBAC） | `v0.2.0` |
| **v0.1.0** | 2024-04-08 | 🚀 初始版本 — 基础架构搭建 | `v0.1.0` |

完整变更日志见 [CHANGELOG.md](CHANGELOG.md)。

## 🧪 Testing

```bash
# Run all tests
bash scripts/test.sh

# Run specific module tests
python -m pytest customer-profile/test_*
```

## 📄 License

MIT
