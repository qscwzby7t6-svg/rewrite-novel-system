# NovelForge

## 🚀 一句话介绍

NovelForge 是一款强大的 AI 小说仿写引擎，能够深度分析原版小说的写作风格，生成风格相似但内容原创的新小说。

## ✨ 核心功能

- 📖 **智能分析**: 深度分析小说的宏观架构、章节结构、世界观、力量系统、人物性格
- ✍️ **风格仿写**: 生成风格相似但内容原创的新小说
- 🤖 **多模型支持**: 支持 DeepSeek、文心一言、通义千问、Kimi、智谱 GLM 等国内主流大模型
- 🔍 **去AI化处理**: 消除AI写作痕迹，让文字更自然
- 📊 **相似度检测**: 确保仿写内容与原著相似度低于10%
- 🌐 **多语言支持**: 中文、英文、日文等多语言支持

## 🎯 支持的大模型

- ✅ **DeepSeek** - 默认推荐，高性价比
- ✅ **文心一言** - 百度出品，中文能力强
- ✅ **通义千问** - 阿里出品，场景描写优秀
- ✅ **Kimi** - 月之暗面，长文本处理
- ✅ **智谱 GLM** - 对话生成优秀
- ✅ **OpenAI** - GPT 系列（可选）

## 📦 快速部署

### Windows

```batch
# 方法一：一键部署
# 下载并运行 deploy_windows.bat

# 方法二：手动部署
git clone https://github.com/你的用户名/novel-rewrite.git
cd novel-rewrite
.\deploy_windows.bat
```

### Termux (荣耀平板/Android)

```bash
# 下载并运行
curl -O https://raw.githubusercontent.com/你的用户名/novel-rewrite/main/deploy_termux.sh
bash deploy_termux.sh
```

### Linux/macOS

```bash
# 一键部署
curl -O https://raw.githubusercontent.com/你的用户名/novel-rewrite/main/deploy_linux.sh
bash deploy_linux.sh
```

详细部署文档：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🛠️ 技术栈

### 后端
- FastAPI - 高性能异步 API
- Python 3.11+
- Jieba - 中文分词
- NLTK - 自然语言处理
- Scikit-learn - 机器学习

### 前端
- React 18+
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query

## 📁 项目结构

```
novel-rewrite/
├── backend/                 # 后端代码
│   ├── api/                # API 接口
│   ├── core/               # 核心模块
│   │   ├── parser/         # 文本解析
│   │   ├── analyzer/       # 结构分析
│   │   ├── engine/        # 仿写引擎
│   │   ├── deai/          # 去AI化
│   │   ├── similarity/    # 相似度检测
│   │   └── llm/           # 大模型集成
│   ├── models/            # 数据模型
│   └── main.py            # 应用入口
├── frontend/              # 前端代码
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── pages/         # 页面
│   │   └── hooks/         # 自定义 Hooks
│   └── package.json
├── tests/                 # 测试代码
├── test_data/             # 测试数据
├── test_output/           # 测试输出
├── DEPLOYMENT_GUIDE.md    # 部署指南
└── README.md
```

## 🔧 配置说明

创建 `.env` 文件：

```env
# LLM 提供商配置
DEFAULT_LLM_PROVIDER=deepseek

# DeepSeek API
DEEPSEEK_API_KEY=sk-your-api-key

# 其他可选 API...
```

详细配置说明：[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#-环境变量配置)

## 📚 使用指南

### 1. 启动服务

```bash
# 后端
source venv/bin/activate  # Windows: call venv\Scripts\activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 前端（新窗口）
cd frontend
npm run dev
```

### 2. 访问应用

- 前端界面：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 3. 使用流程

1. **上传小说**: 上传需要仿写的原版小说（TXT 格式）
2. **分析风格**: 系统自动分析小说的写作风格和特点
3. **生成仿写**: 设置参数后生成仿写版本
4. **去AI化处理**: 自动消除AI写作痕迹
5. **相似度验证**: 确保相似度低于10%
6. **导出结果**: 下载仿写完成的小说

## 🎨 功能展示

### 风格分析
- 宏观架构分析
- 章节结构识别
- 世界观和力量系统提取
- 人物性格和成长线识别

### 仿写引擎
- 风格复刻
- 描述具体化
- 战斗场景生成
- 高潮控制
- 字数精确控制

### 去AI化
- 自然语言变化
- 口语化表达
- 错误模拟
- 节奏调整

## 📊 测试结果

| 测试项目 | 结果 |
|---------|------|
| 《九鼎记》仿写 | 相似度 ~7% ✅ |
| 《神墓》仿写 | 相似度 ~8% ✅ |
| 风格保持度 | 85-90% ✅ |
| 处理速度 | <1分钟/章节 ✅ |

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📧 联系方式

- **GitHub Issues**: https://github.com/你的用户名/novel-rewrite/issues
- **邮箱**: your-email@example.com

---

**🎉 让 AI 帮你写小说 - NovelForge**
