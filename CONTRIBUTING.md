# 贡献指南 · ReAgent

欢迎参与到 ReAgent 的开发中来！本文档描述了项目的协作规范、代码标准与提交流程。

---

## 目录

1. [行为准则](#1-行为准则)
2. [开发环境搭建](#2-开发环境搭建)
3. [分支策略](#3-分支策略)
4. [开发流程](#4-开发流程)
5. [代码规范](#5-代码规范)
6. [提交信息规范](#6-提交信息规范)
7. [测试要求](#7-测试要求)
8. [Pull Request 流程](#8-pull-request-流程)

---

## 1. 行为准则

- 尊重每一位贡献者，鼓励开放、包容的协作氛围
- 代码审查聚焦于代码本身，而非个人
- 所有讨论保持专业与建设性

## 2. 开发环境搭建

```bash
# 克隆仓库
git clone <repo-url>
cd reagent

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install pytest pytest-cov flake8 black mypy

# 运行测试确认环境正常
bash scripts/test.sh
```

### 推荐工具

| 工具 | 用途 |
|---|---|
| VS Code + Python 扩展 | 集成开发环境 |
| Black | 代码格式化 |
| Flake8 | 代码风格检查 |
| mypy | 类型检查 |
| pytest | 单元/集成测试 |

## 3. 分支策略

采用 **Git Flow** 风格的分支策略：

```
main          ← 生产就绪版本
  └── develop ← 开发主线
       ├── feature/*  → 新功能分支（从 develop 拉出，合并回 develop）
       ├── fix/*      → 修复分支（从 develop 拉出，合并回 develop）
       └── release/*  → 发布分支（从 develop 拉出，合并到 main 和 develop）
```

### 分支命名

| 分支类型 | 命名规范 | 示例 |
|---|---|---|
| 功能分支 | `feature/<描述>` | `feature/customer-enrichment-v2` |
| 修复分支 | `fix/<描述>` | `fix/profile-matching-edge-case` |
| 发布分支 | `release/v<版本>` | `release/v1.1.0` |
| 热修复 | `hotfix/<描述>` | `hotfix/critical-auth-bypass` |

## 4. 开发流程

1. 从 `develop` 拉出功能/修复分支
2. 在分支上完成开发与自测
3. 提交 Pull Request 到 `develop`
4. 通过代码审查后合并
5. 定期从 `develop` 创建 `release/*` 分支进行发布准备

## 5. 代码规范

### Python

- **格式化:** 使用 [Black](https://black.readthedocs.io/) 自动格式化（行宽 100）
- **风格检查:** 通过 Flake8 检查（忽略 E501 行宽检查）
- **类型注解:** 所有函数必须包含类型注解
- **文档字符串:** 公共函数和类使用 Google 风格 docstring

```python
def enrich_profile(
    profile_id: str,
    source_data: dict[str, Any],
    options: EnrichOptions | None = None,
) -> EnrichedProfile:
    """基于原始数据丰富客户画像。

    Args:
        profile_id: 客户画像 ID
        source_data: 原始事件/行为数据
        options: 丰富选项（可选）

    Returns:
        丰富后的客户画像对象

    Raises:
        ProfileNotFoundError: 指定画像不存在
    """
```

### 模块结构

```
customer-profile/
├── __init__.py      # 模块导出
├── models.py        # 数据模型
├── service.py       # 业务逻辑
├── enricher.py      # 专门化处理
├── api.py           # REST API 层
└── test_*.py        # 测试文件
```

## 6. 提交信息规范

采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <简短描述>

[可选的详细描述]

[可选的关闭 Issue]
```

### 类型

| 类型 | 用途 | 示例 |
|---|---|---|
| `feat` | 新功能 | `feat(recommendation): add deep learning collaborative filter` |
| `fix` | 修复 | `fix(profile): handle empty enrichment data gracefully` |
| `refactor` | 重构 | `refactor(automation): extract node execution into pluggable handlers` |
| `perf` | 性能优化 | `perf(customer-profile): cache enrichment results to reduce latency` |
| `test` | 测试 | `test: add integration tests for all modules` |
| `docs` | 文档 | `docs: add API documentation for recommendation endpoints` |
| `chore` | 工程维护 | `chore: update dependencies to latest versions` |
| `style` | 代码风格 | `style: apply consistent code formatting across modules` |

### 示例

```
feat(automation): add A/B test campaign type

实现活动级别的 A/B 测试支持，允许营销人员为同一活动配置
不同版本（文案/渠道/触发条件），系统自动分流并收集效果数据。

Closes #42
```

## 7. 测试要求

### 覆盖标准

- 新功能必须包含对应的单元测试
- 修复 Bug 必须附带回归测试
- 核心业务逻辑覆盖率 ≥ 90%
- 整体项目覆盖率 ≥ 80%

### 测试分类

```bash
# 单元测试（覆盖单个函数/类）
pytest customer-profile/tests/

# 集成测试（覆盖模块间交互）
pytest tests/integration/

# 端到端测试（覆盖完整业务流程）
pytest tests/e2e/
```

### 测试命名

测试函数使用 `test_<被测试功能>_<场景>_<期望结果>` 格式：

```python
def test_recommend_empty_profile_returns_empty_list():
    """空画像调用推荐应返回空列表而非报错。"""
    result = engine.recommend("empty_profile", top_n=10)
    assert result == []
```

## 8. Pull Request 流程

### PR 创建

1. 确保分支已同步最新的 `develop`
2. 运行全部测试：`bash scripts/test.sh`
3. 创建 Pull Request 到 `develop`
4. 在 PR 描述中写明：

```
## 变更内容
简要描述本次变更做了什么

## 测试说明
- [x] 单元测试通过
- [x] 集成测试通过
- [x] 手动验证了边界场景 X

## 关联 Issue
Closes #42
```

### 代码审查

- 至少需要 1 名 reviewer 批准方可合并
- reviewer 关注：代码正确性、可维护性、测试覆盖、安全性
- 非紧急变更使用 "Squash and merge" 策略
- 紧急热修复使用 "Rebase and merge" 策略

---

> 本文档将持续更新。如有疑问请在项目中提 Issue 讨论。
