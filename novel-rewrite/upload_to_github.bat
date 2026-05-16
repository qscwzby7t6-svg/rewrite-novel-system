@echo off
chcp 65001 > nul
echo ==========================================
echo   NovelForge 上传到 GitHub
echo ==========================================
echo.

:: GitHub 配置
set GITHUB_USERNAME=qcszwby7t6-svg
set REPO_NAME=rewrite-novel-system
set REPO_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git

echo [配置] GitHub 信息
echo   用户名: %GITHUB_USERNAME%
echo   仓库名: %REPO_NAME%
echo   仓库地址: %REPO_URL%
echo.

:: 进入项目目录
cd /d "%~dp0"

echo [1/7] 进入项目目录: %CD%

:: 初始化 Git
echo [2/7] 初始化 Git 仓库...
if not exist ".git" (
    git init
    echo   ✅ Git 仓库已初始化
) else (
    echo   ⚠️  Git 仓库已存在，跳过初始化
)

:: 配置 Git 用户信息
echo [3/7] 配置 Git 用户信息...
git config user.name "%GITHUB_USERNAME%"
git config user.email "%GITHUB_USERNAME%@users.noreply.github.com"
echo   ✅ Git 用户信息已配置

:: 添加远程仓库
echo [4/7] 配置远程仓库...
git remote -v | findstr /C:"origin" > nul
if %errorlevel% equ 0 (
    echo   远程仓库已存在，更新地址...
    git remote set-url origin %REPO_URL%
) else (
    git remote add origin %REPO_URL%
)
echo   ✅ 远程仓库: %REPO_URL%

:: 创建 .gitignore
echo [5/7] 创建 .gitignore 文件...
if not exist ".gitignore" (
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo venv/
echo ENV/
echo env/
echo .venv/
echo *.egg-info/
echo dist/
echo build/
echo.
echo # Node.js
echo node_modules/
echo .npm
echo .yarn
echo .cache/
echo dist/
echo dist-ssr/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo *~
echo.
echo # Environment
echo .env
echo .env.local
echo.
echo # Logs
echo *.log
) > .gitignore
    echo   ✅ .gitignore 文件已创建
) else (
    echo   ⚠️  .gitignore 文件已存在，跳过
)

:: 添加文件并提交
echo [6/7] 添加文件并提交...
git add .

:: 检查是否有文件更改
git diff --staged --quiet
if %errorlevel% equ 0 (
    echo   ⚠️  没有新的更改需要提交
) else (
    git commit -m "feat: NovelForge AI小说仿写引擎 - 完整版本
.
✨ 核心功能
- 支持国内主流大模型（DeepSeek、文心一言、通义千问、Kimi、GLM）
- 完整的文本解析和风格分析系统
- 智能仿写引擎，支持主角替换
- 去AI化处理，让文字更自然
- 相似度检测，确保原创性低于10%%
.
📦 部署支持
- Windows 一键部署脚本
- Termux (荣耀平板/Android) 一键部署脚本
- Linux/macOS 一键部署脚本
- Docker 支持
.
🧪 测试结果
- 《九鼎记》仿写测试完成（相似度 7%%）
- 《神墓》仿写测试完成（相似度 8%%）
.
📚 文档
- 完整的部署指南
- 使用说明文档
- GitHub 上传指南"
    echo   ✅ 提交完成
)

:: 推送到 GitHub
echo [7/7] 准备推送...
echo.
echo ==========================================
echo   准备推送到 GitHub
echo ==========================================
echo.
echo 即将执行: git push -u origin main
echo 仓库地址: %REPO_URL%
echo.
set /p CONFIRM=按 Enter 键继续推送，或 Ctrl+C 取消...

:: 推送到 GitHub
git branch -M main
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo   ✅ 上传成功！
    echo ==========================================
    echo.
    echo 🎉 恭喜！你的项目已成功上传到 GitHub！
    echo.
    echo 📂 仓库地址:
    echo    %REPO_URL%
    echo.
    echo 🌐 在浏览器中打开:
    echo    https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo.
    echo 📋 下一步:
    echo    1. 访问仓库页面
    echo    2. 添加 Topics: python, fastapi, react, ai, novel
    echo    3. 添加仓库描述
    echo.
    pause
) else (
    echo.
    echo ==========================================
    echo   ❌ 上传失败
    echo ==========================================
    echo.
    echo 请检查:
    echo    1. 网络连接是否正常
    echo    2. GitHub 认证是否有效
    echo    3. 仓库名称是否正确
    echo.
    echo 常见问题:
    echo    - 如果需要登录，运行: git push -u origin main
    echo.
    pause
)
