# ReAgent 🧠

**AI Marketing System** — 面向现代营销的智能推荐与自动化平台，提供从客户画像分析到 ML 驱动营销活动编排的一体化方案。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](CHANGELOG.md)
[![Python](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)]()

---

## 📦 Modules

| Module | Description |
|---|---|
| **customer-profile** | 客户画像数据处理、Enrichment 引擎、CRUD 服务与 REST API |
| **recommendation-engine** | 协同过滤、基于内容、混合推荐引擎，支持模型版本化与 A/B 测试 |
| **marketing-automation** | 工作流编排引擎、活动模板管理、A/B 测试活动支持 |
| **analytics-dashboard** | 指标计算、报告生成、WebSocket 实时数据面板 |
| **api** | API 网关、JWT 认证、CORS、API Key 管理 |
| **shared** | 配置管理、缓存、错误处理、日志工具集 |

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

| Version | Date | Highlights |
|---|---|---|
| **v1.0.0** | 2024-06-20 | Production-ready: ML upgrade, compliance, automation enhancement |
| **v0.3.0** | 2024-05-25 | Dashboard, integration tests, performance optimization |
| **v0.2.0** | 2024-05-08 | Integration layer, auth, stability fixes |
| **v0.1.0** | 2024-04-08 | Initial foundation: profiles, recommendations, campaigns, analytics |

## 🧪 Testing

```bash
# Run all tests
bash scripts/test.sh

# Run specific module tests
python -m pytest customer-profile/test_*
```

## 📄 License

MIT
