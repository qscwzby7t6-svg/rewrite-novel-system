#!/bin/bash

# NovelForge 一键上传到 GitHub

echo "============================================"
echo "  NovelForge 上传到 GitHub"
echo "============================================"
echo ""

# GitHub 配置
GITHUB_USERNAME="qcszwby7t6-svg"
REPO_NAME="rewrite-novel-system"
REPO_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "[配置] GitHub 信息"
echo "  用户名: ${GITHUB_USERNAME}"
echo "  仓库名: ${REPO_NAME}"
echo "  仓库地址: ${REPO_URL}"
echo ""

# 进入项目目录
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "[1/6] 进入项目目录: $PROJECT_DIR"

# 初始化 Git（如果还没有）
if [ ! -d ".git" ]; then
    echo "[2/6] 初始化 Git 仓库..."
    git init
    echo "  ✅ Git 仓库已初始化"
else
    echo "[2/6] Git 仓库已存在，跳过初始化"
fi

# 配置 Git 用户信息（如果未配置）
if [ -z "$(git config user.name)" ]; then
    echo "[3/6] 配置 Git 用户信息..."
    git config user.name "${GITHUB_USERNAME}"
    git config user.email "${GITHUB_USERNAME}@users.noreply.github.com"
    echo "  ✅ Git 用户信息已配置"
else
    echo "[3/6] Git 用户信息已配置，跳过"
fi

# 添加远程仓库
echo "[4/6] 配置远程仓库..."
if git remote -v | grep -q "origin"; then
    echo "  远程仓库已存在，更新地址..."
    git remote set-url origin "$REPO_URL"
else
    git remote add origin "$REPO_URL"
fi
echo "  ✅ 远程仓库: ${REPO_URL}"

# 创建 .gitignore（如果不存在）
if [ ! -f ".gitignore" ]; then
    echo "[5/6] 创建 .gitignore 文件..."
    cat > .gitignore << 'EOF'
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

# Large files
*.zip
*.tar
*.gz
EOF
    echo "  ✅ .gitignore 文件已创建"
else
    echo "[5/6] .gitignore 文件已存在，跳过"
fi

# 添加文件并提交
echo "[6/6] 添加文件并提交..."
git add .

# 检查是否有文件更改
if git diff --staged --quiet; then
    echo "  ⚠️ 没有新的更改需要提交"
else
    git commit -m "feat: NovelForge AI小说仿写引擎 - 完整版本

✨ 核心功能
- 支持国内主流大模型（DeepSeek、文心一言、通义千问、Kimi、GLM）
- 完整的文本解析和风格分析系统
- 智能仿写引擎，支持主角替换
- 去AI化处理，让文字更自然
- 相似度检测，确保原创性低于10%

📦 部署支持
- Windows 一键部署脚本
- Termux (荣耀平板/Android) 一键部署脚本
- Linux/macOS 一键部署脚本
- Docker 支持

🧪 测试结果
- 《九鼎记》仿写测试完成（相似度 7%）
- 《神墓》仿写测试完成（相似度 8%）

📚 文档
- 完整的部署指南
- 使用说明文档
- GitHub 上传指南

🤖 技术栈
- FastAPI + Python 3.11
- React 18 + TypeScript
- Vite + Tailwind CSS
- 支持多种 LLM 提供商"
    echo "  ✅ 提交完成"
fi

# 推送到 GitHub
echo ""
echo "============================================"
echo "  准备推送到 GitHub"
echo "============================================"
echo ""
echo "即将执行: git push -u origin main"
echo "仓库地址: ${REPO_URL}"
echo ""
read -p "按 Enter 键继续，或 Ctrl+C 取消..."

# 推送到 GitHub
git branch -M main
git push -u origin main

# 检查推送结果
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================"
    echo "  ✅ 上传成功！"
    echo "============================================"
    echo ""
    echo "🎉 恭喜！你的项目已成功上传到 GitHub！"
    echo ""
    echo "📂 仓库地址:"
    echo "   ${REPO_URL}"
    echo ""
    echo "🌐 在浏览器中打开:"
    echo "   https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo ""
    echo "📋 下一步:"
    echo "   1. 访问仓库页面"
    echo "   2. 添加 Topics: python, fastapi, react, ai, novel"
    echo "   3. 添加仓库描述"
    echo "   4. 创建 README 徽章"
    echo ""
else
    echo ""
    echo "============================================"
    echo "  ❌ 上传失败"
    echo "============================================"
    echo ""
    echo "请检查:"
    echo "  1. 网络连接是否正常"
    echo "  2. GitHub 认证是否有效"
    echo "  3. 仓库名称是否正确"
    echo ""
    echo "常见问题:"
    echo "  - 如果需要登录，运行: git push -u origin main"
    echo "  - 查看详细错误: git push -u origin main --verbose"
    echo ""
fi
