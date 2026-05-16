# GitHub 上传指南

## 方法一：使用 GitHub 网页（最简单）

### 1. 创建新仓库

1. 登录 GitHub：https://github.com/login
2. 点击右上角 **"+"** → **"New repository"**
3. 填写信息：
   - **Repository name**: `novel-rewrite`
   - **Description**: `AI 小说仿写引擎 - 深度分析原版小说风格，生成原创仿写作品`
   - **选择 Public**（或 Private）
   - **不要勾选** "Initialize this repository with a README"
4. 点击 **"Create repository"**

### 2. 上传文件

在新创建的仓库页面：

1. 点击 **"uploading an existing file"**
2. 将 `novel-rewrite` 文件夹中的所有文件拖拽到上传区域
3. 或者点击 **"choose your files"** 选择所有文件
4. 点击 **"Commit changes"**

### 3. 需要的文件清单

确保上传以下文件：

```
novel-rewrite/
├── backend/                    ✓ 全部上传
│   ├── api/                   ✓
│   ├── core/                 ✓
│   ├── models/               ✓
│   ├── main.py               ✓
│   ├── config.py             ✓
│   └── requirements.txt      ✓
├── frontend/                  ✓ 全部上传
│   ├── src/                  ✓
│   ├── package.json          ✓
│   └── vite.config.ts        ✓
├── tests/                     ✓ 全部上传
├── test_data/                 ✓ 全部上传
├── test_output/               ✓ 全部上传（可选）
├── docker/                     ✓ （如果有）
├── .env.example              ✓
├── .gitignore                ✓
├── deploy_windows.bat        ✓ 新增
├── deploy_termux.sh         ✓ 新增
├── deploy_linux.sh          ✓ 新增
├── DEPLOYMENT_GUIDE.md      ✓ 新增
├── README.md                 ✓
├── PRD.md                    ✓
└── TECHNICAL_ARCHITECTURE.md ✓
```

### 4. 不需要上传的文件

```
.git/              - Git 仓库数据
venv/             - Python 虚拟环境
node_modules/      - Node.js 依赖
.env               - 包含密钥
*.pyc              - 编译文件
__pycache__/      - Python 缓存
dist/             - 构建输出
.cache/           - 缓存文件
```

---

## 方法二：使用 Git 命令行

### 1. 在 GitHub 网页创建仓库

按照上面的步骤 1 创建仓库后，你会看到类似这样的页面：

```
...or push an existing repository from the command line

git remote add origin https://github.com/你的用户名/novel-rewrite.git
git branch -M main
git push -u origin main
```

### 2. 初始化本地 Git 仓库

```bash
# 进入项目目录
cd novel-rewrite

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: NovelForge AI小说仿写引擎
- 支持国内主流大模型（DeepSeek、文心一言、通义千问、Kimi、GLM）
- 完整的文本解析和风格分析
- 智能仿写和去AI化处理
- 相似度检测
- 多平台部署支持（Windows、Linux、Termux）
- 一键部署脚本"

# 添加远程仓库
git remote add origin https://github.com/你的用户名/novel-rewrite.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 3. 创建 .gitignore 文件

在项目根目录创建 `.gitignore`：

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
venv/
ENV/
env/
.venv/
*.egg-info/
dist/
build/

# Node.js
node_modules/
.npm
.yarn
.cache/
dist/
dist-ssr/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Misc
*.bak
```

---

## 方法三：使用 GitHub Desktop

### 1. 下载 GitHub Desktop

- 下载地址：https://desktop.github.com/

### 2. 添加仓库

1. 打开 GitHub Desktop
2. 点击 **"File"** → **"Add Local Repository"**
3. 选择 `novel-rewrite` 文件夹
4. 点击 **"Add Repository"**

### 3. 发布到 GitHub

1. 点击 **"Publish repository"**
2. 填写仓库名称和描述
3. 选择 Public 或 Private
4. 点击 **"Publish Repository"**

---

## 常用 Git 命令

### 基本操作

```bash
# 查看状态
git status

# 查看修改
git diff

# 添加文件
git add 文件名
git add .  # 添加所有文件

# 提交
git commit -m "提交信息"

# 推送到远程
git push

# 拉取更新
git pull

# 查看提交历史
git log
```

### 分支操作

```bash
# 创建新分支
git checkout -b feature/新功能

# 切换分支
git checkout main

# 合并分支
git merge feature/新功能

# 删除分支
git branch -d feature/新功能
```

### 撤销操作

```bash
# 撤销未提交的修改
git checkout -- 文件名

# 撤销已暂存的修改
git reset HEAD 文件名

# 撤销最近的提交
git revert HEAD
```

---

## 上传后配置

### 1. 添加仓库徽章

在 `README.md` 顶部添加：

```markdown
[![GitHub stars](https://img.shields.io/github/stars/你的用户名/novel-rewrite?style=social)](https://github.com/你的用户名/novel-rewrite/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/你的用户名/novel-rewrite?style=social)](https://github.com/你的用户名/novel-rewrite/network/members)
[![License](https://img.shields.io/github/license/你的用户名/novel-rewrite)](https://github.com/你的用户名/novel-rewrite/blob/main/LICENSE)
```

### 2. 添加 Topics

在 GitHub 仓库页面右侧，点击 **"About"** 下的 **Topics**，添加：

```
python
fastapi
react
typescript
novel
ai
deepseek
chatgpt
machine-learning
nlp
```

### 3. 设置仓库描述

在仓库页面，点击 ⚙️ **Settings**，设置：

- **Description**: `AI 小说仿写引擎 - 支持 DeepSeek、文心一言、通义千问、Kimi、GLM 等主流大模型`
- **Website**: 你的网站地址（如果有）
- **勾选** "Wikis"
- **勾选** "Issues"

### 4. 添加徽章和截图

在 `README.md` 添加：

```markdown
## Screenshots

![NovelForge 界面截图](screenshots/main.png)

## Demo

- 🌐 在线演示：https://your-demo-url.com
- 📖 API 文档：https://your-api-docs.com
```

---

## 同步更新到 GitHub

当你修改代码后：

```bash
# 1. 查看修改
git status

# 2. 添加修改
git add .

# 3. 提交
git commit -m "feat: 添加新功能

- 新增 xxx 功能
- 优化 xxx 性能
- 修复 xxx bug"

# 4. 推送到 GitHub
git push
```

---

## 常见问题

### Q: 推送被拒绝？

```bash
# 如果远程有更新，先拉取
git pull origin main --rebase

# 然后再推送
git push -u origin main
```

### Q: .env 文件太大？

```bash
# 确保 .env 在 .gitignore 中
echo ".env" >> .gitignore

# 撤销已添加的 .env
git rm --cached .env
```

### Q: 文件名编码问题？

```bash
# 设置 Git 使用 UTF-8
git config --global core.quotepath false
git config --global i18n.logOutputEncoding utf-8
```

### Q: 大文件上传失败？

GitHub 单个文件限制 100MB，大于 50MB 会警告。

```bash
# 使用 Git LFS
git lfs install
git lfs track "*.zip"
git add .gitattributes
```

---

## 快速检查清单

上传前确认：

- [ ] README.md 完整
- [ ] LICENSE 文件存在
- [ ] .gitignore 配置正确
- [ ] requirements.txt 包含所有依赖
- [ ] deploy_*.sh 脚本有执行权限
- [ ] 没有上传密钥或敏感信息

---

## 获取帮助

- GitHub 官方文档：https://docs.github.com/
- Git 教程：https://git-scm.com/book/zh/v2
- GitHub Skills：https://skills.github.com/

---

**祝上传顺利！🚀**
