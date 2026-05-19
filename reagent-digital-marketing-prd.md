# ReAgent 数字营销平台 — 详细PRD

> 任务ID: JJC-20260519-001
> 基于: `reagent-upgrade-digital-marketing-platform.md` 方案升级
> 日期: 2026-05-19
> 状态: 草案（待确认碰碰卡硬件形态、自动直播路线、部署形态）

---

## 目录

1. [产品总览](#一产品总览)
2. [功能模块详细需求](#二功能模块详细需求)
3. [技术架构细化设计](#三技术架构细化设计)
4. [API接口设计](#四api接口设计)
5. [数据库模型扩展](#五数据库模型扩展)
6. [四阶段实施计划细化](#六四阶段实施计划细化)
7. [附录](#七附录)

---

## 一、产品总览

### 1.1 产品定位

**AI数字营销产业公共服务平台**——帮助中小企业实现线上+线下全渠道流量获取与转化的一站式平台。

### 1.2 目标用户画像

| 用户类型 | 典型场景 | 核心需求 |
|---------|---------|---------|
| 本地商户（餐饮/零售） | 线下门店引流 → 线上团购/打卡/加私域 | 碰碰卡、扫码互动、自动直播 |
| 营销团队/代运营 | 多账号内容创作+分发+获客 | 多平台发布、AI文案、线索管理 |
| 个人创业者 | 低成本获客+自动客服 | 短视频引擎、AI客服、AI文案 |
| 线下活动主办方 | 现场互动引流 | NFC打卡、Wi-Fi关注、扫码领券 |

### 1.3 核心差异优势

| 维度 | 竞品（小猫AI等） | ReAgent |
|------|---------------|---------|
| 线下引流 | ❌ 纯线上 | ✅ NFC碰碰卡+扫码互动+Wi-Fi引流 |
| 可观测性 | 黑盒操作 | ✅ 全链路可回溯、三省六部审核 |
| 部署方式 | 本地部署为主 | ✅ SaaS + 私有化可选 |
| 开源 | 闭源 | ✅ 开源社区版免费 |
| 多Agent制度 | 单Agent | ✅ 三省六部多Agent编排+审核 |

---

## 二、功能模块详细需求

### 2.1 SaaS管理端（Web后台）

#### 2.1.1 总控台（Dashboard）

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| DASH-01 | 营销链路全景图 | 横向链路展示：对标爆款→自动剪辑→智能发布→曝光追踪→自动互动→私信触达→留资转化→成交闭环；每个节点可点击查看详情、✅已完成/🔄处理中/⏳等待中状态标识 | P0 |
| DASH-02 | 一键启动全自动营销 | 核心入口按钮，选中渠道+目标后一键启动完整营销流 | P0 |
| DASH-03 | KPI总览卡片 | 今日曝光量、新增线索数、成交数、回复率，每5min自动刷新 | P0 |
| DASH-04 | 转化漏斗 | 曝光→点击→互动→留资→成交，每一步转化率+环比变化 | P1 |
| DASH-05 | 实时动态流 | 最新N条营销动作日志滚动展示（含Agent执行结果） | P1 |
| DASH-06 | 租户用量看板 | 套餐余量、API调用次数、存储用量 | P1（SaaS特有） |

#### 2.1.2 创作区

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| CREATE-01 | 短视频创作 | 输入文案/关键词 → AI自动生成短视频（含画面+配音+字幕），支持模板选择和自定义 | P0 |
| CREATE-02 | 数字人创作 | 上传真人视频素材/AI生成虚拟人 → 数字人口播视频生成，支持文案输入→自动配音+口型同步 | P0 |
| CREATE-03 | 短视频混剪 | 多素材混剪：选择多个视频+图片→AI自动选片段→合成+转场+配乐 | P1 |
| CREATE-04 | AI代写文案 | 输入产品/活动主题 → 自动生成多平台适配文案（抖音/小红书/快手/视频号/B站各风格），可一键复制或继续优化 | P0 |
| CREATE-05 | 内容日历 | 日历视图展示已排期/已发布内容，支持拖拽调整发布计划 | P1 |
| CREATE-06 | 素材库管理 | 视频/图片/音频/文案素材上传、分类、标签、搜索 | P1 |

#### 2.1.3 分发区

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| PUB-01 | 多平台一键发布 | 支持抖音、小红书、快手、视频号、B站的内容同步发布 | P0 |
| PUB-02 | 定时发布 | 设置发布时间，系统自动在指定时间发布到指定平台 | P0 |
| PUB-03 | AI搜索曝光 | 基于关键词自动生成各平台SEO内容+发布到搜索渠道 | P1 |
| PUB-04 | 发布历史查看 | 已发布内容记录、各平台状态、播放/互动数据汇总 | P0 |
| PUB-05 | 平台账号管理 | 多平台多账号绑定/授权管理，Cookie/Token刷新提醒 | P0 |

#### 2.1.4 触达区

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| REACH-01 | AI客服统一面板 | 抖音私信+微信客服+企微消息统一展示和管理 | P0 |
| REACH-02 | 自动回复规则 | 关键词触发自动回复、知识库FAQ、多轮对话策略配置 | P0 |
| REACH-03 | 私信自动触达 | 自动私信潜在客户（评论互动用户），配置话术+频次限制 | P0 |
| REACH-04 | 私域运营 | 自动加好友、定时群发、朋友圈互动、沉睡客户激活 | P1 |
| REACH-05 | 评论管理 | 多平台评论统一管理、AI自动回复/点赞/引导私信 | P1 |

#### 2.1.5 数据中心

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| DATA-01 | 数据总览看板 | 曝光量、播放量、互动量、线索数、成交数，支持时间维度筛选 | P0 |
| DATA-02 | 转化漏斗分析 | 从曝光到成交的每一步转化率，支持按渠道/平台/内容维度下钻 | P1 |
| DATA-03 | 线索管理 | 所有留资客户列表，含来源、评分、跟进状态 | P0 |
| DATA-04 | AI线索评分 | 基于行业匹配度+互动活跃度+预算匹配度的自动评分 | P0 |
| DATA-05 | 内容数据对比 | 不同内容的播放量/互动率/转化率对比，辅助创作决策 | P1 |

#### 2.1.6 碰碰卡管理

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| NFC-01 | 碰碰卡列表 | 所有已创建的碰碰卡卡片管理，含名称/NFC ID/关联商户/动作配置/状态 | P0 |
| NFC-02 | 碰碰卡创建 | 创建新碰碰卡，配置卡片名称、关联商户、配置碰触发后的动作 | P0 |
| NFC-03 | 动作配置编辑器 | 可视化配置碰触发后的动作序列（支持动作排序/启用/禁用） | P0 |
| NFC-04 | NFC数据写入工具 | 生成NFC NDEF数据写入指令，支持批量写入/批量打印 | P0 |
| NFC-05 | 碰碰记录查询 | NFC碰触数据统计：碰触次数、触达人数、动作触发成功/失败率 | P1 |
| NFC-06 | 硬件设备管理 | 绑定/解绑线下引流设备（平板/屏幕），查看设备在线状态 | P1 |

#### 2.1.7 直播管理

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| LIVE-01 | 直播列表 | 所有直播场次管理，含直播状态/在线人数/互动数据 | P0 |
| LIVE-02 | 创建直播 | 配置直播标题/封面/数字人形象/直播脚本/互动话术 | P0 |
| LIVE-03 | 直播编排 | 配置直播内容时间线：产品讲解顺序、互动环节、优惠活动 | P1 |
| LIVE-04 | 数字人管理 | 上传/管理数字人形象（真人克隆/虚拟人），支持多形象切换 | P0 |
| LIVE-05 | 自动互动配置 | 关键词自动回复、定时抽奖/优惠、评论区管理策略 | P1 |
| LIVE-06 | 直播数据看板 | 实时在线人数、观看人次、互动率、成交额 | P1 |

#### 2.1.8 开放平台/开发者中心

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| DEV-01 | API文档 | 基于OpenAPI的标准接口文档（自动生成） | P1 |
| DEV-02 | 应用管理 | 第三方应用注册、API Key管理、权限分配 | P1 |
| DEV-03 | SDK下载 | 主流语言SDK（Python/JavaScript/Java）下载 | P2 |
| DEV-04 | Webhook管理 | 事件回调配置（内容发布完成/新线索/NFC碰触等） | P2 |
| DEV-05 | 沙箱环境 | 独立的测试环境，供第三方开发者调试 | P2 |

#### 2.1.9 租户管理（SaaS特有）

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| SAAS-01 | 套餐管理 | 套餐定义（免费版/专业版/企业版）、功能权限配置 | P1 |
| SAAS-02 | 用量统计 | API调用次数、存储用量、NFC触发次数、直播时长等 | P1 |
| SAAS-03 | 账单管理 | 每月账单生成、支付记录、发票申请 | P2 |
| SAAS-04 | 成员管理 | 邀请/管理组织成员、角色分配（管理员/运营/客服） | P1 |

### 2.2 线下互动引流端

#### 2.2.1 硬件兼容方案

| 需求编号 | 说明 | 优先级 |
|---------|------|--------|
| HW-01 | 用户自备平板（iPad/安卓平板）+ 下载互动App或访问H5页面 | P0 |
| HW-02 | 支持外接NFC读写器（如ACR122U）实现碰触触发 | P0 |
| HW-03 | NFC标签贴纸方案：预写入数据的NFC标签贴在桌面/展架，用户手机碰触触发（贴纸成本约¥0.5-2/张） | P0 |
| HW-04 | 支持蓝牙信标方案（iBeacon/Eddystone）作为NFC的补充 | P1 |

#### 2.2.2 互动引流功能

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| OFFLINE-01 | 扫码互动 | 用户扫码进入互动页面 → 领券/抽奖/问卷调查 | P0 |
| OFFLINE-02 | 现场大屏互动 | 大屏展示互动内容（签到墙、抽奖转盘、实时数据） | P1 |
| OFFLINE-03 | 卡券发放系统 | 创建/发放电子优惠券，支持核销、有效期管理 | P1 |
| OFFLINE-04 | 引流效果统计 | 扫码人次、领券数、核销率、转化漏斗 | P1 |

### 2.3 碰碰卡系统（核心差异化功能）

#### 2.3.1 NFC碰触动作库

每个碰触可触发**一个或多个动作**（顺序执行或并行），动作库如下：

| 动作类型 | 动作ID | 详细说明 | 技术方案 |
|---------|--------|---------|---------|
| 多平台发布 | `action.publish` | 碰触触发 → 自动同步内容到已配置的多个平台 | 通过ReAgent发布引擎，需连接各平台账号 |
| 打卡收藏 | `action.checkin` | 碰触触发 → 跳转大众点评/抖音/高德/百度打卡收藏页面 | 通过Deep Link跳转各平台打卡页 |
| 加微信好友 | `action.add_wechat` | 碰触触发 → 展示商家微信二维码/企微二维码 | NFC写入微信二维码URL或企微链 |
| 团购直达 | `action.group_buy` | 碰触触发 → 直接跳转美团/大众/抖音团购页 | Deep Link / URL Scheme |
| 连Wi-Fi+关注 | `action.wifi_follow` | 碰触触发 → 自动连接Wi-Fi（需支持热点）+ 跳转关注页 | NFC NDEF Wi-Fi配置+微信关注链接 |
| 浏览店铺 | `action.view_shop` | 碰触触发 → 跳转商家店铺主页/商品详情页 | URL跳转 |
| 领取优惠券 | `action.coupon` | 碰触触发 → 自动领取电子优惠券 | 对接卡券系统 |
| 填写问卷 | `action.survey` | 碰触触发 → 打开满意度调查问卷 | 问卷链接 |

#### 2.3.2 NFC数据格式标准

```
NFC NDEF Record 格式:

Record 1: 类型标识
  - Type: "application/vnd.reagent.nfc"
  - Payload: {
      "v": "1.0",              // 协议版本
      "cid": "merchant_xxx",   // 商户ID
      "card_id": "card_xxx",   // 卡片ID
      "actions": [             // 动作列表
        "action.add_wechat",
        "action.checkin"
      ],
      "nonce": "random_str",   // 防重放
      "ts": 1716000000         // 写入时间戳
    }

Record 2: 回退URL（不支持NDEF的旧手机使用）
  - Type: "text/plain"
  - Payload: "https://reagent.ai/nfc/card_xxx"

Record 3: Wi-Fi配置（可选）
  - Type: "application/vnd.wfa.wsc" 或 Wi-Fi NDEF格式
  - Payload: WiFi SSID + 密码
```

#### 2.3.3 碰碰卡交互流程

```
用户手机碰触NFC标签
       │
       ▼
手机读取NDEF Record
       │
       ├── 是 → App自带NFC支持 → 解析动作 → 按序执行动作（加微信/打卡等）
       │
       ├── 是 → 非App用户 → 打开回退URL
       │                   │
       │                   ├── 已登录 → 展示碰碰卡配置的H5动作页
       │                   │            ├── 一键加微信好友（二维码）
       │                   │            ├── 一键打卡（逐平台跳转）
       │                   │            ├── 一键领券
       │                   │            └── 查看更多
       │                   │
       │                   └── 未登录 → 引导注册/登录
       │
       └── 否 → 无NFC手机/未开启 → 展示二维码引导扫码
                                            │
                                            ▼
                                     线上回退流程
```

#### 2.3.4 碰碰卡管理后台

| 功能 | 详细说明 | 优先级 |
|------|---------|--------|
| 卡片模板管理 | 预设多种行业模板（餐饮/零售/服务），一键应用 | P1 |
| 批量创建 | 支持批量生成NFC写入数据（CSV导入联系人+动作配置） | P0 |
| 批量写入引导 | 引导用户使用NFC写入器批量写入标签 | P0 |
| 动作优先级配置 | 设置动作执行顺序、用户选择或自动执行 | P1 |
| 频次限制 | 同一用户同一卡片碰触频次限制（防止刷单） | P1 |
| A/B测试 | 不同卡片配置的碰触转化率对比 | P2 |

### 2.4 自动直播模块

#### 2.4.1 数字人方案

| 选项 | 方案 | 说明 | 成本估算 | 优先 |
|-----|------|------|---------|------|
| A | LivePortrait开源 | 开源方案，基于表情驱动图像生成视频，可克隆真人形象 | 免费 + GPU成本 | ✅ 优先 |
| B | Duix-Avatar | 开源数字人交互框架，支持数字人对话 | 免费 + GPU成本 | ✅ 并行评估 |
| C | 商业数字人SDK | 采购商业数字人服务（如硅基智能/腾讯智影） | ¥1-3万/年 | 备选方案 |
| D | MiniMax数字人API | 通过mmx-cli集成MiniMax数字人能力 | API按量计费 | 备选方案 |

#### 2.4.2 直播编排

| 需求编号 | 功能 | 详细说明 | 优先级 |
|---------|------|---------|-------|
| AUTOLIVE-01 | 直播脚本生成 | AI根据选品/活动生成直播讲解脚本（含开场/产品介绍/互动环节/收尾） | P0 |
| AUTOLIVE-02 | 时间线编排 | 可视化编排直播内容时间线，支持拖拽调整 | P1 |
| AUTOLIVE-03 | 循环播放 | 脚本循环播放，7×24h不间断直播 | P0 |
| AUTOLIVE-04 | AI自动讲解 | 数字人按脚本自动讲解，语音合成+口型同步 | P0 |
| AUTOLIVE-05 | 评论区互动 | AI自动抓取评论→意图识别→数字人口播回复 | P1 |
| AUTOLIVE-06 | 自动上下架商品 | 按预设时间线自动调整直播间商品展示 | P1 |
| AUTOLIVE-07 | 直播推流 | 自动推流到目标平台（主要：抖音，后续扩展） | P0 |

#### 2.4.3 直播平台兼容性

| 平台 | 数字人直播支持 | 备注 |
|------|--------------|------|
| 抖音 | ✅ 支持（需申请数字人直播权限） | 抖音对AI数字人直播有内容标签要求 |
| 视频号 | ✅ 支持 | 目前管控相对宽松 |
| 快手 | ⏳ 调研中 | 政策变化快 |
| 小红书 | ⏳ 调研中 | 暂未开放数字人直播 |

### 2.5 AI Agent 集群详细设计

#### 2.5.1 Agent Master 编排器

在现有 `AgentOrchestrator` 基础上扩展：

```
AgentMaster（编排主控）
  ├── 三省六部式审核流
  │   ├── 中书省（分析需求/拆解任务）
  │   ├── 门下省（审核方案/合规检查）
  │   └── 尚书省（执行任务/结果上报）
  ├── 任务路由
  │   ├── 串行（前序Agent输出是后序输入）
  │   ├── 并行（多个Agent同时处理不同任务）
  │   └── 条件（根据结果选择分支）
  ├── 状态管理
  │   ├── 任务创建→分配→执行→审核→完成
  │   └── 异常处理：重试/降级/人工介入
  └── 全链路日志
      ├── 每一步的输入/输出/耗时
      └── 可回溯查看
```

#### 2.5.2 现有Agent升级

| Agent | 当前能力 | 升级方向 | 优先级 |
|-------|---------|---------|--------|
| `VideoScriptAgent` | 生成基础脚本 | 多平台适配（抖音15s/小红书图文/快手30s）、热门风格模板匹配 | P0 |
| `ContentGenerationAgent` | 基础文案生成 | 营销文案优化（AIDA模型、痛点-解决方案-行动号召）、各平台风格适配 | P0 |
| `LeadScoringAgent` | 基础评分 | 多维评分（RFM模型+互动行为+行业匹配度）、动态权重调整 | P1 |
| `SummaryAgent` | 文本摘要 | 推广内容摘要生成、SEO摘要优化 | P1 |
| `IntentClassifier` | 意图分类 | 扩展分类粒度、支持多轮对话上下文 | P1 |
| `CodingAgent` | 代码生成 | 保留现有，非核心 | P2 |

#### 2.5.3 新增Agent

| Agent | 功能 | 技术方案 | 优先级 |
|-------|------|---------|--------|
| **NfcRouterAgent** | NFC碰触后的动作路由、执行管理 | 解析NDEF→查动作配置→分派执行器 | P0 |
| **PublishAgent** | 多平台内容发布管理 | 抽象发布接口层，各平台适配器 | P0 |
| **CheckinAgent** | 打卡动作路由 | 按平台生成打卡跳转链接 | P0 |
| **WechatFriendAgent** | 加好友链路管理 | 生成微信二维码/企微链，监控添加情况 | P0 |
| **CouponAgent** | 卡券发放与核销 | 对接卡券系统，定时/触发发放 | P1 |
| **LiveStreamAgent** | 自动直播核心编排 | 数字人驱动+脚本讲解+直播交互 | P0 |
| **DigitalHumanAgent** | 数字人驱动 | 图片/视频→数字人表情+动作+口型 | P0 |
| **LiveReplyAgent** | 直播评论区自动回复 | 意图识别+生成回复+数字人口播 | P1 |
| **ContentCalendarAgent** | 内容日历管理 | 排期生成/提醒/自动发布调度 | P1 |
| **SeoAgent** | 搜索曝光内容生成 | 各平台SEO关键词+内容策略 | P1 |
| **AnalyticsAgent** | 数据分析与报告 | 多维度数据聚合+趋势分析+自动报告 | P1 |
| **PlatformAdapterAgent** | 平台适配层 | 各平台接口差异抽象化 | P0 |

#### 2.5.4 Agent交互流程（典型场景）

**场景：用户碰触碰碰卡**

```
NFC碰触
  │
  ▼
NfcRouterAgent 收到NDEF记录
  ├── 解析卡ID和动作列表
  ├── 记录碰触日志
  └── 分派动作 → PublishAgent（多平台发布）
                   │
                   ▼
              PlatformAdapterAgent（各平台适配）
                   │
                   ├── 抖音发布 → 返回结果
                   ├── 小红书发布 → 返回结果
                   ├── 快手发布 → 返回结果
                   └── 视频号发布 → 返回结果
                   │
                   ▼
              AnalyticsAgent 记录发布数据
              └── 返回NfcRouterAgent
                    │
                    ▼
              NfcRouterAgent 继续下一动作
                   ├── CheckinAgent（打卡动作）
                   │   └── 按平台生成跳转链接
                   ├── WechatFriendAgent（加好友）
                   │   └── 生成微信二维码
                   │
                   ▼
              汇总碰触结果（手机/设备显示）
```

**场景：自动直播启动**

```
用户点击"开始直播"
  │
  ▼
AgentMaster 编排
  ├── LiveStreamAgent
  │   ├── 读取直播配置（标题/封面/商品）
  │   ├── LiveScriptAgent → 生成直播脚本
  │   └── DigitalHumanAgent → 加载数字人形象
  │
  ├── 直播启动
  │   ├── 数字人开播（按脚本自动讲解）
  │   ├── LiveReplyAgent → 监控评论区
  │   │   └── 识别意图 → 生成回复 → 数字人口播
  │   └── 定时触发（商品上下架、优惠发放）
  │
  ├── AnalyticsAgent → 实时数据采集
  │
  └── 直播结束 → LiveSummaryAgent → 生成直播报告
```

### 2.6 硬件端（线下引流设备）交互设计

#### 2.6.1 NFC标签贴纸方案（默认方案）

| 要素 | 说明 |
|------|------|
| 硬件 | NFC标签贴纸（NTAG215/216），成本约¥0.5-2/张 |
| 写入 | 商家通过ReAgent管理后台生成NDEF数据 → 用NFC写入器（手机App）批量写入 |
| 放置 | 贴在桌面/收银台/展架/菜单上，顾客手机碰触触发 |
| 外壳选项 | 亚克力立牌/亚克力卡槽，¥2-5/个（客户可自行采购） |
| 维护 | 写入后无需供电，永久有效（NTAG约10万次擦写寿命） |

#### 2.6.2 互动终端方案（可选升级）

| 要素 | 说明 |
|------|------|
| 硬件 | 用户自备平板（iPad/安卓平板）或触摸屏 |
| 软件 | Flutter/React Native跨平台App或H5 Web App |
| 功能 | NFC读写 + 扫码 + 互动页面展示 + 数据同步 |
| 部署 | App Store/应用商店下载，或扫码即用H5版本 |
| 外设 | 可选外接NFC读写器（USB/蓝牙） |

#### 2.6.3 交互流程

```
顾客到店
   │
   ├── 看到桌面碰碰卡/展架
   │   └── 碰触NFC标签（或扫码）
   │
   ├── [首次] → 跳转落地页
   │   ├── 浏览商家信息（简介/商品/优惠）
   │   ├── 一键加微信好友 → 弹出微信/企微二维码 → 用户扫码添加
   │   ├── 一键打卡收藏 → 逐平台跳转打卡页面
   │   ├── 一键领券 → 自动发放优惠券至用户微信卡包
   │   ├── 团购直达 → 跳转美团/大众/抖音团购页
   │   └── 填写问卷 → 反馈收集
   │   └── 回退选项：未关注 → 引导关注公众号/视频号
   │
   ├── [多次] → 展示个性化内容
   │   ├── 上次领取的优惠券 → 提醒使用
   │   ├── 新人专享 → 分享给朋友可获额外优惠
   │   └── 会员价/积分查询
   │
   └── [离开后] → 线上触达延续
       ├── 微信好友 → 后续自动营销（朋友圈/群发）
       ├── 抖音/小红书关注 → 后续内容曝光
       └── 团购/券 → 引导到店核销
```

---

## 三、技术架构细化设计

### 3.1 总体架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                       客户端层                                      │
│  ┌─────────────┐  ┌──────────┐  ┌────────────┐  ┌──────────────┐ │
│  │ Vue 3       │  │ 手机H5   │  │ Flutter App│  │ 微信小程序   │ │
│  │ SaaS后台    │  │ 互动页面  │  │ 线下引流端  │  │ 终端用户     │ │
│  └──────┬──────┘  └─────┬────┘  └──────┬─────┘  └──────┬───────┘ │
└─────────┼───────────────┼──────────────┼───────────────┼──────────┘
          │               │              │               │
          ▼               ▼              ▼               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     API Gateway (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  反向代理: Nginx / Traefik                                   │  │
│  │  限流/鉴权/WAF/路由                                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│  ┌─────────┬─────────┬───────────┬──────────┬──────────────────┐  │
│  │ REST    │ WebSocket│ GraphQL  │ Webhook  │ NFC协议转换      │  │
│  │ API v1  │ 实时通信  │ 数据查询  │ 回调通知  │ NDEF ↔ HTTP      │  │
│  └─────────┴─────────┴───────────┴──────────┴──────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                        业务中台                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐ │
│  │ 内容运营 │ │ 自动直播 │ │ 线下引流 │ │ 碰碰卡  │ │ 开放平台    │ │
│  │ 模块     │ │ 模块     │ │ 模块     │ │ 系统    │ │ 模块        │ │
│  │          │ │          │ │          │ │         │ │             │ │
│  │内容管理   │ │数字人    │ │扫码互动  │ │NFC引擎  │ │API管理      │ │
│  │内容日历   │ │直播编排  │ │硬件管理  │ │动作路由  │ │SDK/文档     │ │
│  │AI文案     │ │直播互动  │ │渠道配置  │ │数据写入  │ │沙箱环境     │ │
│  │数据分析   │ │数据看板  │ │效果统计  │ │批量管理  │ │Webhook      │ │
│  └───────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────────┘ │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  租户/组织管理层： Organization → User → Role → Permission │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                      AI 引擎层 (扩展)                               │
│  ┌──────────────┐  ┌──────────┐  ┌────────────┐  ┌────────────┐  │
│  │ AgentMaster  │  │ LLM Client│  │ 数据Agent  │  │ 第三方AI   │  │
│  │ 编排器       │  │ DeepSeek  │  │ 分析Agent  │  │ LivePortrait│ │
│  ├──────────────┤  │ Gemini    │  │ 报告Agent  │  │ Duix       │  │
│  │ 三省六部审核  │  │ 备用LLM   │  │ 预测Agent  │  │ MiniMax    │  │
│  │ 任务路由     │  └──────────┘  └────────────┘  └────────────┘  │
│  │ Agent集群    │                                                  │
│  └──────────────┘                                                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Agent目录： 任务、记忆、工具、角色 四个能力维度               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                         数据层                                      │
│  ┌──────────┐ ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │PostgreSQL│ │ Redis  │ │Elastic   │ │ 对象存储  │ │Celery/Rabbit│ │
│  │业务数据   │ │缓存/   │ │search    │ │MinIO/S3  │ │MQ          │ │
│  │租户数据   │ │会话/   │ │ 搜索索引  │ │视频/素材  │ │任务队列    │ │
│  │NFC记录   │ │ 锁     │ │ 日志      │ │NFC数据   │ │定时任务    │ │
│  └──────────┘ └────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
┌─────────────────────────────────────────────────────────────────────┐
│                      基础设施层                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │Docker    │ │K8s/    │ │监控     │ │日志    │             │
│  │Compose   │ │Nomad    │ │Prometheus │ │Loki    │             │
│  │dev部署   │ │prod部署 │ │Grafana    │ │告警    │             │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.2 多租户架构设计

#### 3.2.1 数据隔离策略

```
方案: 共享数据库 + 行级租户隔离
理由: 平衡成本与隔离性；SaaS平台初级阶段够用，后期可升级为库级隔离

实现:
  1. 所有业务表增加 tenant_id 字段
  2. SQLAlchemy 中间件自动注入 tenant_id 过滤
  3. API鉴权后提取 JWT 中的 tenant_id
  4. Redis 缓存按 tenant_id 分 namespace
```

#### 3.2.2 租户模型

```
Organization
  ├── id: UUID (PK)
  ├── name: String
  ├── slug: String (唯一标识, 用于子域名/URL)
  ├── plan: Enum (free | pro | enterprise)
  ├── status: Enum (active | suspended | cancelled)
  ├── config: JSON (功能开关/配额)
  ├── created_at, updated_at
  │
  ├── User[] — 组织成员
  │   ├── id, username, email, password
  │   ├── role: Enum (admin | operator | cs | viewer)
  │   └── status
  │
  └── BillingInfo (账单信息)
      ├── payment_method
      └── current_period_end
```

#### 3.2.3 套餐定义

| 套餐 | 价格（预估） | 核心限制 |
|------|------------|---------|
| 免费版 | ¥0 | 1个账号、10条碰碰卡、5个视频/月、基础AI文案 |
| 专业版 | ¥198/月 | 5个账号、50条碰碰卡、100个视频/月、全部AI能力、自动直播 |
| 企业版 | ¥980/月 | 不限账号数、不限碰碰卡、不限视频、API接口、专属部署 |

### 3.3 NFC引擎架构

#### 3.3.1 整体架构

```
┌──────────────┐     NFC碰觸     ┌──────────────────┐
│ 用户手机端     │ ◄────—───────► │  NFC硬件          │
│ 原生NFC支持   │                 │  (标签/贴纸/终端) │
└──────────┬──────┘                 └────────┬─────────┘
       │                                  │
       │  Deep Link / HTTP                │ NDEF读取/MQTT
       ▼                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NFC 路由网关服务                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 1. NDEF解析层：解析NDEF Record → 提取商户ID/卡片ID/动作  │    │
│  │ 2. 卡片校验层：校验卡片有效性/频次限制                     │    │
│  │ 3. 动作路由层：按配置顺序分派动作到各执行器               │    │
│  │ 4. 日志记录层：记录碰触事件/动作执行结果到数据库          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    动作执行器集群                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │发布执行器 │ │打卡执行器 │ │加好友执行 │ │WiFi执行器│           │
│  │平台适配   │ │Deep Link  │ │生成二维码  │ │NDEF WiFi │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │团购执行器 │ │领券执行器 │ │问卷执行器 │ │分析执行器 │           │
│  │URL跳转    │ │API对接    │ │问卷连接   │ │数据统计   │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.3.2 NFC路由网关API

```
POST /api/v1/nfc/router  — 碰触发后的路由入口
  请求体: {
    "card_id": "card_xxx",
    "nonce": "random_str",
    "phone_model": "iPhone 15",
    "os_version": "iOS 18.0"
  }
  响应: {
    "actions": [
      {"type": "add_wechat", "url": "weixin://..."},
      {"type": "checkin", "platforms": ["dianping", "douyin", "gaode"]},
      {"type": "coupon", "coupon_id": "coupon_001"}
    ],
    "merchant_info": {"name": "xxx", "logo": "..."}
  }

GET /api/v1/nfc/cards — 碰碰卡列表
POST /api/v1/nfc/cards — 创建/更新碰碰卡配置
GET /api/v1/nfc/cards/:id/qr — 获取二维码回退链接
POST /api/v1/nfc/cards/:id/write-data — 生成NDEF写入数据（JSON格式，用于NFC写入器）
GET /api/v1/nfc/stats — 碰触统计（按日/周/月/卡片/商户维度）
```

#### 3.3.3 NFC批量管理

| 功能 | 说明 |
|------|------|
| 批量生成 | 选择商户+动作模板+数量 → 批量生成NDEF写入数据CSV |
| 批量写入 | 通过手机App（NFC写入工具）批量写入标签 |
| 批量打印 | 生成NFC标签二维码回退码+商户名称+使用说明的PDF模板 |
| 激活/停用 | 批量激活或停用一批碰碰卡 |

### 3.4 自动直播架构

#### 3.4.1 技术选型

```
┌──────────────────────────────────────────────────────────┐
│                    自动直播系统                            │
├──────────────────────────────────────────────────────────┤
│  LiveStreamAgent (直播主控)                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 直播编排器:                                         │  │
│  │  ├── 脚本管理：生成/加载/切换直播脚本              │  │
│  │  ├── 时间线引擎：按时间轴触发事件（讲解/互动/礼品）│  │
│  │  └── 状态机：开播→暖场→讲解→互动→促销→收尾        │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  DigitalHumanAgent (数字人驱动)                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 方案A: LivePortrait (开源，推荐优先评估)           │  │
│  │  ├── 输入: 静态肖像图 + 音频                      │  │
│  │  ├── 输出: 表情同步视频流                         │  │
│  │  └── GPU要求: RTX 3060+                           │  │
│  │                                                    │  │
│  │ 方案B: Duix-Avatar (开源数字人对话)                │  │
│  │  ├── 支持: 数字人+语音交互+表情动画               │  │
│  │  └── GPU要求: RTX 4060+                           │  │
│  │                                                    │  │
│  │ 方案C: MiniMax API (商业，无服务器成本)            │  │
│  │  └── API按量计费，无需GPU                          │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  LiveReplyAgent (互动回复)                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ 评论抓取 → 意图识别 → 回复生成 → 口播合成 → 回复发布 │  │
│  └────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────┤
│  推流模块                                               │
│  ┌────────────────────────────────────────────────────┐  │
│  │ FFmpeg + RTMP推流 → 各直播平台                     │  │
│  │ 抖音: rtmp://push.douyin.com/live/...              │  │
│  │ 视频号: 通过微信直播工具推流                       │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

#### 3.4.2 直播编排引擎

```json
// 直播配置示例
{
  "live_id": "live_001",
  "title": "新品特惠直播",
  "cover": "https://...",
  "stream_key": "rtmp://...",
  "schedule": [
    {"time": 0, "action": "open", "script": "开场白（AI生成）"},
    {"time": 30, "action": "present", "product_id": "prod_001", "duration": 120},
    {"time": 150, "action": "interact", "type": "qa", "faq_list": [...]},
    {"time": 300, "action": "promotion", "coupon_id": "coupon_001"},
    {"time": 600, "action": "loop", "from": 30}  // 循环播放
  ],
  "reply_rules": {
    "price_question": "回复价格信息",
    "product_question": "回复产品介绍",
    "complaint": "转接人工"
  }
}
```

### 3.5 平台适配层设计

#### 3.5.1 设计原则

```
平台适配层 = 抽象接口 + 各平台适配器 + 统一返回格式

核心接口:
  IPublishAdapter {
    publish(video: Video, params: PublishParams): PublishResult
    delete(video_id: string): boolean
    getStatus(video_id: string): PublishStatus
    getStats(video_id: string): VideoStats
  }

  ICheckinAdapter {
    getCheckinLink(platform: string, merchant_id: string): string
    getCheckinStatus(merchant_id: string): CheckinStats
  }

  ILiveStreamAdapter {
    startStream(stream_key: string, config: LiveConfig): LiveSession
    stopStream(session_id: string): boolean
    getCommentStream(session_id: string): AsyncIterator<Comment>
    sendReply(session_id: string, comment_id: string, reply: string): boolean
  }
```

#### 3.5.2 已确认平台覆盖

| 平台 | 发布 | 打卡 | 直播 | 加好友 | 团购 | 备注 |
|------|------|------|------|--------|------|------|
| 抖音 | ✅ | ✅ | ✅ | ❌ | ✅ | 抖音开放平台API |
| 小红书 | ✅ | ❌ | ⏳ | ❌ | ❌ | 蒲公英平台 |
| 快手 | ✅ | ✅ | ⏳ | ❌ | ✅ | 快手开放平台 |
| 视频号 | ✅ | ❌ | ✅ | ❌ | ❌ | 微信开放平台 |
| B站 | ✅ | ❌ | ❌ | ❌ | ❌ | 已有对接 |
| 大众点评 | ❌ | ✅ | ❌ | ❌ | ✅ | 需商户端操作 |
| 高德 | ❌ | ✅ | ❌ | ❌ | ❌ | 商家中心 |
| 百度地图 | ❌ | ✅ | ❌ | ❌ | ❌ | 百度商家中心 |

### 3.6 安全与合规设计

#### 3.6.1 API安全

| 措施 | 说明 |
|------|------|
| JWT认证 | 用户登录后签发JWT，含用户ID+租户ID+角色 |
| API限流 | 按租户维度限流（1000次/分钟专业版） |
| CORS | 只允许已注册域名跨域访问 |
| 参数校验 | Pydantic模型严格校验输入 |
| 敏感数据加密 | 平台账号Cookie/Token加密存储 |

#### 3.6.2 NFC安全

| 风险 | 措施 |
|------|------|
| NFC标签伪造 | 写入时签名(nonce+商户密钥)，服务器验证 |
| NFC标签数据篡改 | 标签内容加签名，有效期验证 |
| 频次攻击 | 同一用户同一卡片60秒内限1次 |
| 重放攻击 | nonce一次性，已使用的nonce服务端拒绝 |

#### 3.6.3 平台合规

| 平台 | 合规注意事项 |
|------|-------------|
| 抖音 | 数字人直播需申请「数字人主播」标签，第三方发布需遵循频次限制 |
| 微信 | NFC一键加好友需在微信开放平台注册应用，频次不可过高 |
| 各平台 | 第三方工具发布内容需遵守平台内容规范，避免触发反爬/封号 |

---

## 四、API接口设计

### 4.1 接口总览

共7大模块，约40+个API端点。前缀统一为 `/api/v1`。

| 模块 | 前缀 | 接口数量 | 说明 |
|------|------|---------|------|
| 认证 | `/auth` | 5 | 登录/注册/刷新/退出/重置密码 |
| 内容创作 | `/content` | 8 | 视频/文案/素材/日历 |
| 发布分发 | `/publish` | 6 | 发布/定时/平台账号/历史 |
| 客服触达 | `/reach` | 8 | 私信/评论/私域/自动回复 |
| 线索数据 | `/leads` | 6 | 线索/评分/分析报告 |
| NFC碰碰卡 | `/nfc` | 8 | 卡片管理/路由/写入/统计 |
| 直播 | `/live` | 8 | 直播/数字人/互动/推流 |

### 4.2 详细API定义

#### 4.2.1 认证模块 `/api/v1/auth`

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/auth/register` | 注册（同时创建租户组织） | ❌ |
| POST | `/auth/login` | 登录（返回JWT） | ❌ |
| POST | `/auth/refresh` | 刷新Token | ✅ |
| POST | `/auth/logout` | 退出登录 | ✅ |
| POST | `/auth/reset-password` | 重置密码 | ✅ |
| GET | `/auth/me` | 获取当前用户信息 | ✅ |

#### 4.2.2 内容创作 `/api/v1/content`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/content/scripts` | AI生成视频脚本 |
| POST | `/content/videos` | 创建视频（含AI自动生成） |
| GET | `/content/videos` | 视频列表 |
| GET | `/content/videos/{id}` | 视频详情 |
| PUT | `/content/videos/{id}` | 更新视频 |
| DELETE | `/content/videos/{id}` | 删除视频 |
| POST | `/content/videos/{id}/render` | 渲染视频（后台任务） |
| POST | `/content/copywriting` | AI代写文案（指定平台风格） |
| POST | `/content/mix` | 多素材混剪 |
| GET | `/content/calendar` | 内容日历查询 |
| POST | `/content/calendar` | 添加日历排期 |
| POST | `/content/materials` | 上传素材 |
| GET | `/content/materials` | 素材库列表 |

#### 4.2.3 发布分发 `/api/v1/publish`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/publish` | 一键发布多平台 |
| GET | `/publish` | 发布记录列表 |
| GET | `/publish/{id}` | 发布详情 |
| POST | `/publish/schedule` | 设置定时发布 |
| GET | `/publish/platforms` | 已绑定的平台账号列表 |
| POST | `/publish/platforms/{platform}/bind` | 绑定平台账号 |
| DELETE | `/publish/platforms/{platform}/unbind` | 解绑平台账号 |
| GET | `/publish/stats` | 发布数据统计 |

#### 4.2.4 客服触达 `/api/v1/reach`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/reach/messages` | 发送消息 |
| GET | `/reach/sessions` | 会话列表 |
| GET | `/reach/sessions/{id}` | 会话详情 |
| POST | `/reach/auto-reply/rules` | 创建自动回复规则 |
| GET | `/reach/auto-reply/rules` | 自动回复规则列表 |
| PUT | `/reach/auto-reply/rules/{id}` | 更新规则 |
| POST | `/reach/private-domain` | 设置私域运营任务 |
| GET | `/reach/comments` | 评论管理 |
| POST | `/reach/comments/{id}/reply` | AI自动回复评论 |

#### 4.2.5 线索与数据 `/api/v1/leads`

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/leads` | 线索列表（含筛选/排序/分页） |
| POST | `/leads` | 创建线索 |
| GET | `/leads/{id}` | 线索详情 |
| GET | `/leads/{id}/score` | AI线索评分详情 |
| POST | `/leads/{id}/assign` | 分配负责人 |
| PUT | `/leads/{id}/status` | 更新线索状态 |
| GET | `/leads/analytics` | 线索转化分析 |

#### 4.2.6 NFC碰碰卡 `/api/v1/nfc`

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/nfc/router` | NFC碰触路由入口（公开接口，需签名验证） | 🔑 |
| POST | `/nfc/cards` | 创建碰碰卡 | ✅ |
| GET | `/nfc/cards` | 碰碰卡列表 | ✅ |
| GET | `/nfc/cards/{id}` | 碰碰卡详情 | ✅ |
| PUT | `/nfc/cards/{id}` | 更新碰碰卡配置 | ✅ |
| DELETE | `/nfc/cards/{id}` | 删除碰碰卡 | ✅ |
| POST | `/nfc/cards/{id}/actions` | 更新动作配置 | ✅ |
| GET | `/nfc/cards/{id}/qr` | 获取回退二维码 | ✅ |
| POST | `/nfc/cards/batch` | 批量生成碰碰卡 | ✅ |
| GET | `/nfc/stats` | 碰触统计 | ✅ |
| POST | `/nfc/stats/track` | 碰触事件上报（公开接口） | 🔑 |

#### 4.2.7 直播 `/api/v1/live`

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/live` | 创建直播配置 |
| GET | `/live` | 直播列表 |
| GET | `/live/{id}` | 直播详情 |
| PUT | `/live/{id}` | 更新直播配置 |
| POST | `/live/{id}/start` | 开始直播 |
| POST | `/live/{id}/stop` | 停止直播 |
| POST | `/live/{id}/script` | AI生成/更新直播脚本 |
| POST | `/live/{id}/interact` | 手动触发直播互动 |
| GET | `/live/{id}/stats` | 直播数据 |
| POST | `/live/digital-humans` | 上传/创建数字人形象 |
| GET | `/live/digital-humans` | 数字人形象列表 |

### 4.3 Webhook事件定义

| 事件类型 | 触发时机 | Payload |
|---------|---------|--------|
| `content.published` | 内容发布完成 | `{content_id, platform, status, url}` |
| `lead.created` | 新线索产生 | `{lead_id, source, score}` |
| `nfc.tapped` | NFC碰触事件 | `{card_id, merchant_id, actions_triggered}` |
| `live.started` | 直播开始 | `{live_id, platform, stream_url}` |
| `live.interaction` | 直播互动 | `{live_id, user, type, content}` |
| `subscription.expired` | 套餐即将到期 | `{org_id, plan, expire_date}` |

### 4.4 通用API规范

```
统一响应格式:
  {
    "code": 200,       // 业务状态码
    "message": "success",
    "data": {},        // 实际数据
    "meta": {          // 分页信息（可选）
      "page": 1,
      "page_size": 20,
      "total": 100
    }
  }

分页参数:
  ?page=1&page_size=20  (默认 page=1, page_size=20, max 100)

错误响应:
  {
    "code": 40001,     // 业务错误码
    "message": "参数错误",
    "details": {}
  }

认证方式:
  Authorization: Bearer <JWT_TOKEN>
```

---

## 五、数据库模型扩展

### 5.1 现有模型升级

#### User表 (扩展)

```sql
ALTER TABLE users ADD COLUMN tenant_id VARCHAR(36) NOT NULL;
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'viewer';  -- admin|operator|cs|viewer
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users ADD COLUMN avatar VARCHAR(500);
```

#### Video表 (扩展)

```sql
ALTER TABLE videos ADD COLUMN tenant_id VARCHAR(36) NOT NULL;
ALTER TABLE videos ADD COLUMN platform_status JSONB;     -- 各平台发布状态
ALTER TABLE videos ADD COLUMN render_status VARCHAR(20);  -- rendering|ready|failed
ALTER TABLE videos ADD COLUMN ai_generated BOOLEAN DEFAULT false;
ALTER TABLE videos ADD COLUMN source_material_ids JSONB;  -- 用于混剪的素材ID列表
ALTER TABLE videos ADD COLUMN schedule_at TIMESTAMP;       -- 定时发布时间
ALTER TABLE videos ADD COLUMN published_at TIMESTAMP;
ALTER TABLE videos ADD COLUMN duration INTEGER;            -- 视频时长(秒)
```

#### Lead表 (扩展)

```sql
ALTER TABLE leads ADD COLUMN tenant_id VARCHAR(36) NOT NULL;
ALTER TABLE leads ADD COLUMN platform VARCHAR(20);    -- 来源平台
ALTER TABLE leads ADD COLUMN wechat_id VARCHAR(100);
ALTER TABLE leads ADD COLUMN tags JSONB;
ALTER TABLE leads ADD COLUMN last_contacted_at TIMESTAMP;
ALTER TABLE leads ADD COLUMN conversion_stage VARCHAR(20);  -- aware|interested|considering|purchased|lost
```

### 5.2 新增模型

#### 🌐 Organization（租户组织）

```sql
CREATE TABLE organizations (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(20) DEFAULT 'free',        -- free|pro|enterprise
    status VARCHAR(20) DEFAULT 'active',    -- active|suspended|cancelled
    config JSONB DEFAULT '{}',
    api_calls_monthly INTEGER DEFAULT 0,
    storage_bytes BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 📇 NfcCards（碰碰卡）

```sql
CREATE TABLE nfc_cards (
    id VARCHAR(36) PRIMARY KEY,
    tenant_id VARCHAR(36) NOT NULL REFERENCES organizations(id),
    name VARCHAR(200) NOT NULL,
    label VARCHAR(50),                -- NFC标签唯一标识/序列号
    status VARCHAR(20) DEFAULT 'active', -- active|inactive|expired
    actions JSONB NOT NULL,           -- [{"type": "publish", "config": {...}}, ...]
    merchant_info JSONB,              -- {name, logo, description, address}
    extra_config JSONB DEFAULT '{}',  -- {wifi_ssid, coupon_template, welcome_message}
    touch_count INTEGER DEFAULT 0,    -- 累计碰触次数
    unique_users INTEGER DEFAULT 0,   -- 唯一用户数
    activated_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_nfc_cards_tenant ON nfc_cards(tenant_id);
CREATE INDEX idx_nfc_cards_label ON nfc_cards(label);
```

#### 📊 NfcTouchLogs（碰触日志）

```sql
CREATE TABLE nfc_touch_logs (
    id BIGSERIAL PRIMARY KEY,
    card_id VARCHAR(36) NOT NULL REFERENCES nfc_cards(id),
    tenant_id VARCHAR(36) NOT NULL,
    device_id VARCHAR(100),           -- 用户设备标识
    nonce VARCHAR(64) UNIQUE,         -- 防重放
    ip_address VARCHAR(45),
    user_agent TEXT,
    actions_triggered JSONB,         -- [{type: "publish", status: "success"}, ...]
    action_results JSONB,           -- 各动作详细结果
    duration_ms INTEGER,             -- 处理耗时
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_touch_logs_card ON nfc_touch_logs(card_id, created_at);
CREATE INDEX idx_touch_logs_tenant ON nfc_touch_logs(tenant_id, created_at);
```

#### 🎥 LiveStreams（直播配置）

```sql
CREATE TABLE live_streams (
    id VARCHAR(36) PRIMARY KEY,
    tenant_id VARCHAR(36) NOT NULL REFERENCES organizations(id),
    title VARCHAR(200) NOT NULL,
    cover_url VARCHAR(500),
    digital_human_id VARCHAR(36),     -- 关联的数字人形象
    platform VARCHAR(20) DEFAULT 'douyin',
    stream_key VARCHAR(500),          -- 推流地址
    schedule JSONB NOT NULL,          -- 直播编排时间线
    reply_rules JSONB DEFAULT '{}',   -- 自动互动规则
    status VARCHAR(20) DEFAULT 'draft',  -- draft|scheduled|live|ended|stopped
    started_at TIMESTAMP,
    ended_at TIMESTAMP,
    total_viewers INTEGER DEFAULT 0,
    peak_viewers INTEGER DEFAULT 0,
    interaction_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_live_tenant ON live_streams(tenant_id);
```

#### 🧑 DigitalHumans（数字人形象）

```sql
CREATE TABLE digital_humans (
    id VARCHAR(36) PRIMARY KEY,
    tenant_id VARCHAR(36) NOT NULL REFERENCES organizations(id),
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20),                 -- clone(真人克隆)|virtual(虚拟人)|avatar(2D头像)
    source_url VARCHAR(500),          -- 原始素材URL（照片/视频）
    thumbnail_url VARCHAR(500),       -- 封面图
    voice_profile VARCHAR(100),       -- 语音模型配置
    status VARCHAR(20) DEFAULT 'processing',  -- processing|ready|failed
    config JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 📝 ContentSchedules（内容日历排期）

```sql
CREATE TABLE content_schedules (
    id VARCHAR(36) PRIMARY KEY,
    tenant_id VARCHAR(36) NOT NULL REFERENCES organizations(id),
    content_type VARCHAR(20),         -- video|article|post|live
    source_id VARCHAR(36),            -- 关联的具体内容ID
    platforms JSONB NOT NULL,         -- ["douyin", "kuaishou"]
    scheduled_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',  -- pending|publishing|published|failed
    auto_generate BOOLEAN DEFAULT false,   -- AI自动生成内容
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_schedule_tenant ON content_schedules(tenant_id, scheduled_at);
```

#### 📋 PlatformAccounts（平台账号绑定）

```sql
CREATE TABLE platform_accounts (
    id VARCHAR(36) PRIMARY KEY,
    tenant_id VARCHAR(36) NOT NULL REFERENCES organizations(id),
    platform VARCHAR(20) NOT NULL,   -- douyin|kuaishou|xiaohongshu|shipinhao
    nickname VARCHAR(100),
    avatar_url VARCHAR(500),
    credentials JSONB NOT NULL,     -- 加密存储的Cookie/Token
    is_active BOOLEAN DEFAULT true,
    last_sync_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_account_tenant ON platform_accounts(tenant_id);
```

#### 📦 Materials（素材库）

```sql
CREATE TABLE materials (
    id VARCHAR(36) PRIMARY KEY,
    tenant_id VARCHAR(36) NOT NULL REFERENCES organizations(id),
    type VARCHAR(20),                -- video|image|audio|text
    name VARCHAR(200),
    url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    size_bytes BIGINT,
    duration INTEGER,                 -- 视频/音频时长(秒)
    tags JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_materials_tenant ON materials(tenant_id, type);
```

### 5.3 数据库关系图（简化）

```
Organizations
  │
  ├── Users (用户/成员)
  ├── NfcCards (碰碰卡配置)
  │   └── NfcTouchLogs (碰触事件日志)
  ├── LiveStreams (直播配置)
  ├── DigitalHumans (数字人形象)
  ├── ContentSchedules (内容日历排期)
  ├── PlatformAccounts (平台账号绑定)
  ├── Materials (素材库)
  ├── Videos (短视频)
  ├── Leads (线索)
  └── Sessions (客服会话)
```

---

## 六、四阶段实施计划细化

### Phase 1：基础升级 (第1-4周)

**目标：完成公共服务平台基底搭建 + NFC协议定义 + AI文案升级**

| 周次 | 工部(后端) | 兵部(AI) | 礼部(前端) | 产出物 |
|------|-----------|---------|-----------|--------|
| W1 | 多租户架构改造 | NFC协议标准定义 | Dashboard MVP | 租户模型+API认证改造；NFC NDEF格式规范文档 |
| W2 | 数据库模型扩展 + 数据迁移 | AI文案Agent升级 | 总控台链路图 | 新增表结构+迁移脚本；content_agent多平台适配 |
| W3 | NFC引擎基础API | 发布引擎平台对接 | 总控台完整版 | NFC路由器+卡片管理API；抖音/小红书/快手/视频号发布对接 |
| W4 | 平台账号管理模块 | SEO搜索Agent初版 | 创作区UI | 账号绑定+安全存储；AI搜索曝光基础功能 |

**里程碑验收标准：**
- ✅ 多租户登录/注册流程可用
- ✅ 碰碰卡CRUD + NFC NDEF数据生成可用
- ✅ AI文案支持多平台风格
- ✅ 至少3个平台的发布接口可用

### Phase 2：核心模块 (第5-10周)

**目标：碰碰卡全功能上线 + SaaS管理端核心功能**

| 周次 | 工部(后端) | 兵部(AI) | 礼部(前端) | 产出物 |
|------|-----------|---------|-----------|--------|
| W5 | NFC路由网关 + 动作执行器 | 碰碰卡动作Agent集群 | 碰碰卡管理页面 | NFC全流程（碰触→路由→执行→记录） |
| W6 | 打卡执行器 + 加好友执行器 + Wi-Fi执行器 | CheckinAgent + WechatFriendAgent | 动作配置编辑器 | NFC完整动作库 |
| W7 | 团购执行器 + 领券执行器 | 碰碰卡批量管理 | 碰碰统计页面 | NFC所有动作可用；批量生成/写入功能 |
| W8 | 客服会话统一管理API | 多平台客服Agent | 客服统一面板 | 抖音+微信+企微客服统一会话 |
| W9 | 私域运营模块API | 私域运营Agent | 私域运营页面 | 自动加好友+群发+朋友圈互动 |
| W10 | 联调测试+性能优化 | Agent编排流优化 | 系统联调UI | Phase 2完整功能验证 |

**里程碑验收标准：**
- ✅ 碰碰卡全部6种动作可用
- ✅ 碰碰卡批量管理流程可用（创建→写入→摆卡→触达→统计）
- ✅ 多平台AI客服统一面板
- ✅ 私域运营（加好友+群发+朋友圈）基础功能

### Phase 3：自动直播 + 开放平台 (第11-16周)

| 周次 | 工部(后端) | 兵部(AI) | 礼部(前端) | 产出物 |
|------|-----------|---------|-----------|--------|
| W11 | 直播API基础模块 | 数字人技术选型与接入评估 | LivePortrait/Duix集成原型 | 数字人技术评估报告+原型 |
| W12 | 推流模块+直播状态管理 | LiveStreamAgent编排器 | 直播创建页面 | 自动直播MVP（可推流播放） |
| W13 | 直播互动回复API | LiveReplyAgent | 直播控制台 | AI自动回复评论区 |
| W14 | 开放平台API Gateway | AnalyticsAgent升级 | 开发者中心页面 | 开放API + SDK + 文档 |
| W15 | 内容日历API | ContentCalendarAgent | 内容日历页面 | 内容日历完整功能 |
| W16 | System联调+性能压测 | 全Agent链路优化 | 前端完善 | Phase 3完整功能 |

**里程碑验收标准：**
- ✅ 自动直播可用（数字人推流+脚本播放+互动回复）
- ✅ 开放平台可用（API文档+SDK+沙箱）
- ✅ 内容日历可用
- ✅ 数据看板完整（含转化漏斗）

### Phase 4：生态运营 (第17周起持续)

| 事项 | 说明 | 预估时长 |
|------|------|---------|
| 公共服务平台正式上线 | 官网 + 套餐定价 + 用户注册流程 | 1周 |
| 硬件合作生态 | 与NFC设备厂商合作，标准化碰碰卡 | 持续 |
| 渠道商/服务商体系 | 开放代理商入驻流程 | 2周 |
| 开源社区版发布 | GitHub公开仓库+社区版功能包 | 1周 |
| 插件市场 | 第三方开发者可开发/上架扩展 | 3周 |
| 持续迭代 | 根据用户反馈优化功能 | 持续 |

### 6.1 团队分工建议

| 三省六部/团队 | 对应职责 | 核心任务 |
|-------------|---------|---------|
| 中书省 | PRD细化/需求管理 | 需求文档维护、验收标准制定 |
| 工部（后端） | 多租户、NFC引擎、API | 数据库、API、NFC路由、直播推流 |
| 兵部（AI） | Agent集群、数字人 | 各Agent实现、LLM集成、数字人方案 |
| 礼部（前端） | 管理后台、互动页面 | Vue 3管理端、H5互动页、App原型 |
| 户部 | 硬件采购、定价策略 | NFC标签采购评估、套餐定价 |
| 尚书省 | 项目管理、交付跟踪 | 进度把控、风险预警、跨部协调 |

### 6.2 风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 各平台接口变更/限制 | 高 | 高 | 适配层抽象+每平台独立模块，变更时只改适配器 |
| 数字人技术路线不成熟 | 中 | 高 | 开源+商业双方案并行，先MVP再优化 |
| NFC硬件供应不稳定 | 中 | 中 | 支持多种硬件形态（贴纸/终端/扫二维码回退） |
| 抖音AI数字人政策收紧 | 中 | 高 | 提前关注政策，准备视频号等替代方案 |
| SaaS多租户数据安全 | 低 | 高 | 行级隔离+数据加密+定期安全审计 |
| 团队人力不足 | 中 | 中 | 明确优先级，砍P2功能保P0 |

---

## 七、附录

### A. 参考文档

| 文档 | 路径 |
|------|------|
| ReAgent README | `edict/projects/reagent/README.md` |
| ReAgent 方案升级文档 | `edict/projects/reagent/reagent-upgrade-digital-marketing-platform.md` |
| ReAgent 优化方案 | `edict/projects/reagent/reagent-optimization-plan.md` |
| 现有API文档 | `edict/projects/reagent/docs/api.md` |
| 现有架构文档 | `edict/projects/reagent/docs/architecture.md` |
| 原型图（8页HTML） | `edict/projects/reagent/prototypes/` |

### B. 术语表

| 术语 | 说明 |
|------|------|
| NFC | Near Field Communication，近场通信 |
| NDEF | NFC Data Exchange Format，NFC数据交换格式 |
| Agent Master | AI Agent编排主控器，管理所有Agent的生命周期 |
| 碰碰卡 | 内置NFC标签的营销卡片/贴纸，碰触触发自动化营销动作 |
| 动作执行器 | 执行NFC碰触后具体动作的微服务 |
| Deep Link | 深度链接，直接跳转到APP内特定页面 |
| 数字人 | AI驱动的虚拟主播形象 |
| 直播编排 | 直播内容时间线的可视化配置 |
| 平台适配层 | 抽象各平台API差异的中间层 |
| 多租户 | 单个实例服务多个组织的架构模式 |

### C. 现有AI Agent文件路径（参考）

| Agent | 路径 | 说明 |
|-------|------|------|
| BaseAgent | `ai/agents/base.py` | Agent基类，定义process/validate接口 |
| VideoScriptAgent | `ai/agents/video_agent.py` | 视频脚本生成（需升级多平台适配） |
| ContentGenerationAgent | `ai/agents/content_agent.py` | 文案生成（需升级营销文案能力） |
| IntentClassifier | `ai/agents/cs_agent.py` | 意图分类（需扩展抖音客服识别） |
| LeadScoringAgent | `ai/agents/lead_agent.py` | 线索评分（需扩展多维评分） |
| SummaryAgent | `ai/agents/base.py` | 摘要Agent |
| CodingAgent | `ai/agents/coding_agent.py` | 编程助手 |
| AgentOrchestrator | `ai/orchestrator.py` | 编排器（需升级为三省六部审核流） |

---

**文档版本: v1.0**
**最后更新: 2026-05-19**
**状态: 草案 — 待确认碰碰卡硬件形态、自动直播路线、部署形态后定稿**