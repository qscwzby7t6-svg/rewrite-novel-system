# NovelForge - 项目总结文档

## 项目概述

NovelForge是一款强大的AI小说仿写引擎，能够深度分析原版小说的宏观架构、章节结构、世界观、力量系统、人物性格，生成风格相似但内容原创的新小说。

## 功能特点

### ✅ 已实现的核心功能

#### 1. 深度分析模块
- **文本解析器**: 支持TXT格式小说，自动识别章节和内容
- **结构分析**: 宏观架构分析、章节结构分析、高潮点识别、伏笔提取
- **世界观分析**: 地理环境、社会结构、文化背景、势力关系提取
- **力量系统分析**: 等级识别、修炼方法提取、特殊能力分析
- **人物分析**: 性格提取、关系网络构建、成长弧线识别

#### 2. 智能仿写引擎
- **风格复刻**: 保持原作的写作风格和节奏
- **描述具体化**: 将抽象描述转化为具体动作和场景描写
- **战斗场景生成**: 详细的战斗描写
- **高潮控制**: 每10章设置小高潮
- **字数控制**: 严格控制章节字数偏差在±10%

#### 3. 去AI化处理
- **自然语言变化**: 打破AI写作的规律性
- **口语化表达**: 加入适当的口语和语气词
- **错误模拟**: 模拟人类写作中的小错误
- **节奏调整**: 调整语句节奏，避免过于流畅

#### 4. 相似度检测
- **多算法检测**: Jaccard相似度、余弦相似度、N-gram相似度
- **逐章验证**: 每个章节单独验证相似度
- **阈值控制**: 严格控制相似度低于10%
- **原创性报告**: 生成详细的相似度报告

#### 5. 多语言支持
- **中文** (简体/繁体): 主要支持语言
- **英文**: 第二支持语言
- **日文**: 第三支持语言
- **韩文**: 预留支持

#### 6. 国内主流大模型集成
- **DeepSeek**: 默认推荐模型
- **文心一言**: 百度出品
- **通义千问**: 阿里出品
- **Kimi**: 月之暗面
- **智谱AI**: GLM系列
- **OpenAI**: GPT系列（可选）

## 技术架构

### 后端技术栈
- **框架**: FastAPI (高性能异步API)
- **语言**: Python 3.11+
- **AI接口**: 统一的LLM抽象层
- **文本处理**: Jieba分词, NLTK
- **相似度计算**: Scikit-learn, NumPy

### 前端技术栈
- **框架**: React 18+
- **语言**: TypeScript
- **构建工具**: Vite
- **UI组件**: 自定义组件 + Framer Motion
- **状态管理**: React Query + Zustand
- **样式**: Tailwind CSS

### 部署架构
- **容器化**: Docker + Docker Compose
- **无状态服务**: 支持水平扩展
- **本地优先**: 支持本地运行

## 项目结构

```
novel-rewrite/
├── backend/
│   ├── api/                          # API接口
│   ├── core/
│   │   ├── parser/                   # 文本解析
│   │   │   └── text_parser.py
│   │   ├── analyzer/                 # 结构分析
│   │   │   ├── structure_analyzer.py
│   │   │   └── world_analyzer.py
│   │   │   └── character_analyzer.py
│   │   ├── engine/                   # 仿写引擎
│   │   ├── deai/                     # 去AI化
│   │   ├── similarity/               # 相似度检测
│   │   └── llm/                      # 大模型集成 (新增)
│   │       ├── base.py               # 基础抽象类
│   │       ├── providers.py          # 各LLM提供商实现
│   │       ├── factory.py            # 工厂类
│   │       └── service.py            # 服务层
│   ├── models/                       # 数据模型
│   ├── services/                     # 业务逻辑
│   └── main.py                       # 应用入口
├── frontend/
│   ├── src/
│   │   ├── components/               # 组件
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── UploadPage.tsx
│   │   │   ├── AnalysisPage.tsx
│   │   │   ├── RewritePage.tsx
│   │   │   ├── ResultPage.tsx
│   │   │   └── SettingsPage.tsx (更新)
│   │   ├── hooks/
│   │   │   └── useNovel.ts
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── tests/
│   └── unit/
│       ├── test_parser.py
│       └── test_llm.py (新增)
├── docker/
│   └── docker-compose.yml
├── PRD.md
└── README.md
```

## 新增的LLM模块详解

### 1. 统一抽象层

#### base.py
- `LLMProvider`: 枚举类型，包含所有支持的提供商
- `MessageRole`: 消息角色枚举
- `ChatMessage`: 聊天消息模型
- `LLMResponse`: LLM响应模型
- `LLMConfig`: LLM配置模型
- `BaseLLMProvider`: 抽象基类，定义统一接口

### 2. 各LLM提供商实现

#### providers.py
1. **DeepSeekProvider**: DeepSeek API封装
2. **WenxinProvider**: 文心一言API封装
3. **QianwenProvider**: 通义千问API封装
4. **KimiProvider**: Kimi API封装
5. **GLMProvider**: 智谱AI API封装
6. **OpenAIProvider**: OpenAI API封装

每个Provider支持:
- 同步聊天补全
- 流式聊天补全
- 自定义模型选择
- API密钥和Base URL配置

### 3. 工厂和管理

#### factory.py
- `LLMFactory`: 工厂类，创建Provider实例
- `LLMManager`: 管理器类，封装常用操作
  - `generate_text()`: 简单文本生成
  - `generate_with_context()`: 上下文生成
  - `stream_generate()`: 流式生成

### 4. 服务层

#### service.py
- `LLMRewriteService`: LLM仿写服务
  - `rewrite_chapter()`: 仿写章节
  - `generate_character_dialogue()`: 生成角色对话
  - `generate_battle_scene()`: 生成战斗场景
  - `expand_description()`: 描述具体化

### 5. API接口

新增的LLM管理接口:
- `GET /api/v1/llm/providers`: 获取提供商列表
- `GET /api/v1/llm/config`: 获取配置
- `POST /api/v1/llm/config`: 更新配置
- `POST /api/v1/llm/test`: 测试连接
- `POST /api/v1/llm/expand-description`: 描述扩写

## 前端更新

### SettingsPage.tsx
新增LLM管理功能:
- 提供商选择器（6种主流模型）
- API密钥配置区域
- 连接测试功能
- 模型参数调整
- 状态显示

## 配置说明

### 环境变量配置

```bash
# 默认提供商
DEFAULT_LLM_PROVIDER=deepseek

# DeepSeek
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 文心一言
WENXIN_API_KEY=...
WENXIN_MODEL=ERNIE-4.0-Turbo-8K

# 通义千问
QIANWEN_API_KEY=sk-...
QIANWEN_MODEL=qwen-turbo

# Kimi
KIMI_API_KEY=sk-...
KIMI_MODEL=moonshot-v1-8k

# 智谱AI
GLM_API_KEY=...
GLM_MODEL=glm-4-flash

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
```

### 模型参数配置

```python
LLM_TEMPERATURE=0.7         # 温度，控制随机性
LLM_MAX_TOKENS=2000         # 最大生成长度
LLM_TOP_P=1.0               # 核采样参数
LLM_TIMEOUT=60              # 请求超时时间
```

## 使用指南

### 快速开始

1. **安装依赖**
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

2. **配置LLM**
```bash
# 设置环境变量或在前端设置页面配置
export DEEPSEEK_API_KEY=your_api_key
```

3. **启动服务**
```bash
# 后端
cd backend && uvicorn main:app --reload

# 前端
cd frontend && npm run dev
```

4. **访问应用**
打开浏览器访问 http://localhost:3000

### LLM配置流程

1. 进入"设置"页面
2. 选择一个LLM提供商（推荐DeepSeek）
3. 输入对应的API Key
4. 点击"测试连接"验证
5. 调整模型参数（可选）
6. 保存配置

## 各LLM特点对比

| 提供商 | 推荐场景 | 价格 | 中文能力 | 速度 |
|--------|----------|------|----------|------|
| DeepSeek | 通用仿写 | 便宜 | 优秀 | 快 |
| 文心一言 | 中文创作 | 中等 | 极佳 | 中等 |
| 通义千问 | 场景描写 | 中等 | 优秀 | 快 |
| Kimi | 长文本 | 中等 | 良好 | 中等 |
| GLM | 对话生成 | 便宜 | 良好 | 快 |
| OpenAI | 通用 | 较贵 | 良好 | 快 |

## 测试说明

### 运行单元测试
```bash
cd tests/unit
pytest test_llm.py -v
```

### 运行集成测试
需要配置API密钥后运行
```bash
pytest test_llm.py -v -m integration
```

## 扩展开发

### 添加新的LLM提供商

1. 在 `backend/core/llm/providers.py` 中添加新类
2. 继承 `BaseLLMProvider`
3. 实现 `chat_completion()` 和 `stream_chat_completion()`
4. 在 `LLMFactory` 中注册新提供商
5. 更新前端提供商列表

### 自定义提示词

在 `LLMRewriteService` 中修改提示词构建方法
```python
def _build_system_prompt(self, world_settings):
    # 自定义系统提示词
    pass
```

## 注意事项

1. **API密钥安全**: 生产环境使用环境变量，不要硬编码
2. **费用控制**: 设置合理的token限制，监控API使用
3. **相似度验证**: 始终验证仿写结果的相似度
4. **防侵权**: 确保用户有原作的合法使用权

## 未来发展

- [ ] 支持更多格式（PDF, EPUB, DOCX）
- [ ] 批量处理多部小说
- [ ] 自定义风格模板
- [ ] 云端同步和协作
- [ ] 移动应用版本

---

**项目完成度**: ████████████ 100%

**最后更新**: 2026-05-16
