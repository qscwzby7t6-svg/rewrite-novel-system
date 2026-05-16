# NovelForge - AI小说仿写引擎

## 项目简介

NovelForge 是一款智能小说仿写工具，能够深度分析原版小说的宏观架构、章节结构、世界观、力量系统、人物性格等要素，生成风格相似但内容原创的新小说。

## 核心特性

- ✅ **智能分析**: 深度解析小说结构、人物、世界观
- ✅ **风格复刻**: 1:1复刻原版小说的写作风格
- ✅ **去AI化**: 消除AI生成痕迹，自然流畅
- ✅ **相似度控制**: 确保相似度低于10%
- ✅ **多语言支持**: 中文、英文、日文等
- ✅ **章节控制**: 严格控制字数在±10%范围内

## 技术栈

- **后端**: Python 3.11+ / FastAPI
- **前端**: React 18+ / TypeScript
- **AI**: OpenAI GPT-4 / Claude API
- **文本处理**: NLTK / spaCy / jieba
- **数据库**: SQLite / PostgreSQL

## 快速开始

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/novel-forge.git
cd novel-forge

# 安装后端依赖
cd backend
pip install -r requirements.txt

# 安装前端依赖
cd ../frontend
npm install
```

### 运行服务

```bash
# 开发模式（同时运行前后端）
npm run dev

# 或分别运行
# 后端
cd backend && uvicorn main:app --reload --port 8000

# 前端
cd frontend && npm run dev
```

### 使用Docker运行

```bash
docker-compose up -d
```

## 项目结构

```
novel-forge/
├── backend/              # 后端服务
│   ├── api/             # API接口
│   ├── core/            # 核心引擎
│   │   ├── parser/      # 文本解析
│   │   ├── analyzer/    # 结构分析
│   │   ├── engine/      # 仿写引擎
│   │   ├── deai/        # 去AI化
│   │   └── similarity/  # 相似度检测
│   ├── models/          # 数据模型
│   ├── services/        # 业务服务
│   └── utils/           # 工具函数
├── frontend/            # 前端应用
│   ├── components/      # React组件
│   ├── pages/          # 页面
│   ├── hooks/          # 自定义hooks
│   └── utils/          # 工具函数
├── tests/              # 测试用例
├── docs/               # 文档
└── docker/             # Docker配置
```

## API文档

启动服务后访问: http://localhost:8000/docs

## 开发指南

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License
