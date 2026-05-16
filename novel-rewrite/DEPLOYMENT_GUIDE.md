# NovelForge - 快速开始指南

## 🎯 支持平台

- ✅ Windows 10/11
- ✅ macOS
- ✅ Linux
- ✅ 荣耀平板 (Termux)
- ✅ Android (Termux)
- ✅ iOS (iSH)

---

## 📦 Windows 部署方案

### 方案一：一键部署（推荐）

#### 准备工作

1. **安装 Git for Windows**
   - 下载地址：https://git-scm.com/download/win
   - 选择 64-bit Git For Windows Setup.exe
   - 安装时勾选 "Add to PATH"

2. **安装 Python**
   - 下载地址：https://www.python.org/downloads/
   - 选择 Python 3.11 或更高版本
   - **重要**：安装时勾选 "Add Python to PATH"
   - 建议使用自定义安装，选择 "Install for all users"

3. **安装 Node.js (前端开发需要)**
   - 下载地址：https://nodejs.org/
   - 选择 LTS 版本（推荐 20.x）
   - 自动添加到 PATH

#### 一键部署脚本

创建 `deploy_windows.bat` 文件：

```batch
@echo off
chcp 65001 > nul
echo ==========================================
echo   NovelForge Windows 一键部署脚本
echo ==========================================
echo.

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.11+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 检查 Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git，请先安装 Git
    echo 下载地址：https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/6] 克隆项目...
git clone https://github.com/你的用户名/novel-rewrite.git
cd novel-rewrite

echo [2/6] 创建虚拟环境...
python -m venv venv
call venv\Scripts\activate

echo [3/6] 安装后端依赖...
pip install -r backend\requirements.txt

echo [4/6] 安装前端依赖...
cd frontend
call npm install
cd ..

echo [5/6] 复制环境变量配置...
copy .env.example .env

echo [6/6] 完成！
echo.
echo ==========================================
echo   部署完成！请运行以下命令启动：
echo ==========================================
echo.
echo   激活虚拟环境: venv\Scripts\activate
echo   启动后端: uvicorn backend.main:app --reload
echo   启动前端: cd frontend ^&^& npm run dev
echo.
echo   或者运行: start.bat 启动完整应用
echo.
pause
```

#### 使用步骤

1. 下载 `deploy_windows.bat` 到桌面
2. 右键以管理员身份运行
3. 等待自动安装完成
4. 双击 `start.bat` 启动应用

---

### 方案二：手动部署（详细）

#### 1. 安装依赖

```powershell
# 使用管理员权限打开 PowerShell

# 安装 Python (如果未安装)
winget install Python.Python.3.11

# 安装 Git (如果未安装)
winget install Git.Git

# 安装 Node.js (如果未安装)
winget install OpenJS.NodeJS.LTS

# 重启终端使 PATH 生效
```

#### 2. 克隆项目

```powershell
# 打开 PowerShell 或 Git Bash

# 克隆项目
git clone https://github.com/你的用户名/novel-rewrite.git
cd novel-rewrite
```

#### 3. 创建虚拟环境

```powershell
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\activate

# 升级 pip
python -m pip install --upgrade pip
```

#### 4. 安装后端依赖

```powershell
# 安装所有依赖
pip install -r backend/requirements.txt
```

#### 5. 安装前端依赖

```powershell
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 返回项目根目录
cd ..
```

#### 6. 配置环境变量

```powershell
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件
notepad .env
```

在 `.env` 文件中添加：

```env
# DeepSeek API
DEEPSEEK_API_KEY=sk-your-api-key-here
DEFAULT_LLM_PROVIDER=deepseek

# 其他配置（可选）
FLASK_ENV=development
DEBUG=True
```

#### 7. 启动应用

```powershell
# 启动后端（在新终端窗口）
.\venv\Scripts\activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# 启动前端（在新终端窗口）
cd frontend
npm run dev
```

#### 8. 访问应用

打开浏览器访问：
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

---

### 启动脚本（start.bat）

创建 `start.bat` 在项目根目录：

```batch
@echo off
chcp 65001 > nul
echo ==========================================
echo   NovelForge 启动脚本
echo ==========================================

:: 激活虚拟环境
call venv\Scripts\activate

:: 启动后端（后台运行）
start "NovelForge Backend" cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

:: 等待2秒
timeout /t 2 /nobreak > nul

:: 启动前端
cd frontend
start "NovelForge Frontend" cmd /k "npm run dev"

echo.
echo ==========================================
echo   NovelForge 已启动！
echo ==========================================
echo.
echo   前端地址: http://localhost:3000
echo   后端地址: http://localhost:8000
echo   API 文档: http://localhost:8000/docs
echo.
echo   按任意键打开浏览器...
pause > nul

start http://localhost:3000
```

---

## 📱 荣耀平板 Termux 部署方案

### 准备工作

#### 1. 安装 Termux

**方法一：通过 F-Droid（推荐）**
- 下载 F-Droid：https://f-droid.org/
- 搜索 Termux 并安装

**方法二：通过 GitHub**
- 下载最新 APK：https://github.com/termux/termux-app/releases
- 选择 `termux-app-release.apkg`

#### 2. 基础设置

```bash
# 更新包列表
pkg update && pkg upgrade -y

# 安装基础工具
pkg install git python nodejs -y

# 检查安装
python --version
node --version
npm --version
git --version
```

#### 3. 配置存储权限

Termux 需要存储权限才能访问手机文件：

```bash
# 在 Termux 中授予存储权限
termux-setup-storage
```

这会在家目录创建 `~/storage/` 目录，包含：
- `~/storage/shared` - 共享存储
- `~/storage/downloads` - 下载目录

---

### 方案一：一键部署（推荐）

#### 创建部署脚本

```bash
# 在家目录创建脚本
cd ~
cat > deploy_novelforge.sh << 'EOF'
#!/bin/bash

echo "============================================"
echo "  NovelForge Termux 一键部署脚本"
echo "============================================"
echo ""

# 更新包
echo "[1/8] 更新系统包..."
pkg update -y && pkg upgrade -y

# 安装依赖
echo "[2/8] 安装必要工具..."
pkg install git python nodejs -y

# 克隆项目
echo "[3/8] 克隆项目..."
if [ -d "~/storage/shared/novel-rewrite" ]; then
    echo "项目已存在，更新中..."
    cd ~/storage/shared/novel-rewrite
    git pull
else
    cd ~/storage/shared
    git clone https://github.com/你的用户名/novel-rewrite.git
    cd novel-rewrite
fi

# 创建虚拟环境
echo "[4/8] 创建 Python 虚拟环境..."
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装后端依赖
echo "[5/8] 安装后端依赖..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# 安装前端依赖
echo "[6/8] 安装前端依赖..."
cd frontend
npm install
cd ..

# 配置环境变量
echo "[7/8] 配置环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "请编辑 .env 文件配置 API 密钥"
fi

echo "[8/8] 完成！"
echo ""
echo "============================================"
echo "  部署完成！"
echo "============================================"
echo ""
echo "启动命令："
echo "  1. source venv/bin/activate"
echo "  2. uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "前端启动（另一个窗口）："
echo "  cd frontend && npm run dev"
echo ""
EOF

# 设置执行权限
chmod +x deploy_novelforge.sh

echo "部署脚本已创建！"
echo "运行命令：bash ~/deploy_novelforge.sh"
```

#### 使用方法

```bash
# 1. 复制脚本到 Termux
# 2. 运行脚本
bash ~/deploy_novelforge.sh

# 3. 等待安装完成
# 4. 配置 API 密钥
nano .env
```

---

### 方案二：手动部署（详细）

#### 1. 安装必要工具

```bash
# 更新包列表
pkg update -y

# 升级所有包
pkg upgrade -y

# 安装必要工具
pkg install git python nodejs -y

# 可选：安装更多工具
pkg install vim nano wget curl -y
```

#### 2. 克隆项目

```bash
# 进入共享存储目录
cd ~/storage/shared

# 克隆项目（使用你的仓库地址）
git clone https://github.com/你的用户名/novel-rewrite.git

# 进入项目目录
cd novel-rewrite
```

#### 3. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
pip install --upgrade pip
```

#### 4. 安装后端依赖

```bash
# 安装所有依赖
pip install -r backend/requirements.txt
```

**注意**：如果遇到内存不足问题，可以：

```bash
# 分批安装
pip install fastapi uvicorn
pip install pydantic python-multipart
pip install jieba nltk
pip install httpx openai
# ... 其他依赖
```

#### 5. 安装前端依赖

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 等待安装完成
```

**注意**：Node.js 在 Termux 中可能需要额外配置：

```bash
# 如果 npm 安装失败，尝试
pkg install nodejs-lts

# 或者使用 yarn
pkg install yarn
yarn install
```

#### 6. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
nano .env
```

添加你的 API 密钥：

```env
# DeepSeek API（推荐）
DEEPSEEK_API_KEY=sk-your-api-key-here
DEFAULT_LLM_PROVIDER=deepseek

# 其他可选
FLASK_ENV=development
```

保存并退出：`Ctrl + X`，然后 `Y`，再按 `Enter`

#### 7. 启动应用

需要两个终端窗口：

**窗口 1 - 启动后端：**

```bash
# 激活虚拟环境
source ~/storage/shared/novel-rewrite/venv/bin/activate

# 进入项目目录
cd ~/storage/shared/novel-rewrite

# 启动后端
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**窗口 2 - 启动前端：**

```bash
# 进入前端目录
cd ~/storage/shared/novel-rewrite/frontend

# 启动前端
npm run dev
```

#### 8. 访问应用

在浏览器中打开：
- 前端：http://localhost:3000
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/docs

**注意**：
- 如果在电脑上访问，使用电脑的浏览器
- 如果在同一设备上访问，使用 `http://localhost:端口号`
- 如果从其他设备访问，使用 `http://设备IP:端口号`

---

### 启动脚本

创建便捷启动脚本：

```bash
cat > ~/storage/shared/novel-rewrite/start.sh << 'EOF'
#!/bin/bash

echo "启动 NovelForge..."

# 激活虚拟环境
source venv/bin/activate

# 启动后端
echo "启动后端服务..."
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo "启动前端服务..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "NovelForge 已启动！"
echo "前端：http://localhost:3000"
echo "后端：http://localhost:8000"
echo ""
echo "按 Ctrl+C 停止服务"

# 等待中断信号
wait
EOF

chmod +x ~/storage/shared/novel-rewrite/start.sh
```

使用方法：

```bash
cd ~/storage/shared/novel-rewrite
bash start.sh
```

---

## 🐧 Linux 一键部署

```bash
# 下载一键部署脚本
wget https://raw.githubusercontent.com/你的用户名/novel-rewrite/main/deploy_linux.sh

# 或者创建脚本
cat > deploy_linux.sh << 'EOF'
#!/bin/bash

echo "============================================"
echo "  NovelForge Linux 一键部署脚本"
echo "============================================"

# 检测系统
if [ -f /etc/debian_version ]; then
    PKG_MANAGER="apt-get"
elif [ -f /etc/redhat-release ]; then
    PKG_MANAGER="yum"
elif [ -f /etc/arch-release ]; then
    PKG_MANAGER="pacman"
else
    echo "未检测到支持的包管理器"
    exit 1
fi

# 安装系统依赖
echo "[1/6] 安装系统依赖..."
sudo $PKG_MANAGER update -y
sudo $PKG_MANAGER install git python3 python3-venv nodejs npm -y

# 克隆项目
echo "[2/6] 克隆项目..."
git clone https://github.com/你的用户名/novel-rewrite.git
cd novel-rewrite

# 创建虚拟环境
echo "[3/6] 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 安装后端依赖
echo "[4/6] 安装后端依赖..."
pip install -r backend/requirements.txt

# 安装前端依赖
echo "[5/6] 安装前端依赖..."
cd frontend
npm install
cd ..

# 配置
echo "[6/6] 配置环境变量..."
cp .env.example .env

echo ""
echo "============================================"
echo "  部署完成！"
echo "============================================"
echo ""
echo "启动命令："
echo "  source venv/bin/activate"
echo "  uvicorn backend.main:app --reload"
echo ""
EOF

chmod +x deploy_linux.sh
./deploy_linux.sh
```

---

## 📱 Docker 部署（所有平台）

### 1. 安装 Docker

**Windows:**
- 下载 Docker Desktop：https://www.docker.com/products/docker-desktop
- 安装并启动

**Linux:**
```bash
curl -fsSL https://get.docker.com | sh
sudo systemctl start docker
sudo systemctl enable docker
```

**Termux (Android):**
```bash
# Termux 中可以使用 proot-distro 运行 Debian
pkg install proot-distro
proot-distro install debian
proot-distro login debian
# 然后按照 Linux 部署方案操作
```

### 2. Docker 部署

```bash
# 进入项目目录
cd novel-rewrite

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
      - DEFAULT_LLM_PROVIDER=deepseek
    volumes:
      - ./backend:/app
    command: uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev
```

---

## 🔧 常见问题

### 1. Windows 问题

**Q: 提示 "不是内部或外部命令"**
```
A: 重启终端或手动添加到 PATH
```

**Q: Python 版本不对**
```
A: 下载并安装 Python 3.11+：https://www.python.org/downloads/
```

**Q: pip install 失败**
```
A: 使用管理员权限打开 PowerShell，并升级 pip：
   python -m pip install --upgrade pip
```

### 2. Termux 问题

**Q: npm install 失败，内存不足**
```
A: 1. 增加 Termux 内存分配
   2. 使用 swapfile：
      wget https://raw.githubusercontent.com/MFDGaming/rust-in-termux/master/swapfile.sh
      bash swapfile.sh
```

**Q: 无法访问手机存储**
```
A: 运行以下命令授予权限：
   termux-setup-storage
```

**Q: 端口被占用**
```
A: 更换端口：
   uvicorn backend.main:app --reload --port 8001
```

### 3. 通用问题

**Q: API 密钥无效**
```
A: 检查 .env 文件中的 API 密钥是否正确
   确保没有多余的空格或引号
```

**Q: 依赖安装失败**
```
A: 使用国内镜像源：
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**Q: 前端无法启动**
```
A: 删除 node_modules，重新安装：
   rm -rf frontend/node_modules
   cd frontend && npm install
```

---

## 🌐 环境变量配置

创建 `.env` 文件：

```env
# LLM 提供商配置
DEFAULT_LLM_PROVIDER=deepseek

# DeepSeek API
DEEPSEEK_API_KEY=sk-your-deepseek-api-key
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 文心一言（可选）
WENXIN_API_KEY=your-wenxin-api-key
WENXIN_MODEL=ERNIE-4.0-Turbo-8K

# 通义千问（可选）
QIANWEN_API_KEY=your-qianwen-api-key
QIANWEN_MODEL=qwen-turbo

# Kimi（可选）
KIMI_API_KEY=your-kimi-api-key
KIMI_MODEL=moonshot-v1-8k

# 智谱 GLM（可选）
GLM_API_KEY=your-glm-api-key
GLM_MODEL=glm-4-flash

# OpenAI（可选）
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_MODEL=gpt-4

# 服务器配置
HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_PORT=3000

# 开发环境
FLASK_ENV=development
DEBUG=True
LOG_LEVEL=INFO
```

---

## 🚀 性能优化

### Windows

```powershell
# 使用 PowerShell 设置
$env:PYTHONFAULTHANDLER = "1"
$env:PYTHONUNBUFFERED = "1"

# 提高优先级
Start-Process python -ArgumentList "uvicorn backend.main:app" -Verb RunAs
```

### Termux

```bash
# 使用 tmux 或 screen
pkg install tmux
tmux new -s novelforge

# 在 tmux 中运行
source venv/bin/activate
uvicorn backend.main:app --reload

# 分离 tmux：Ctrl+b, d
# 重新连接：tmux attach -t novelforge
```

---

## 📞 获取帮助

- **GitHub Issues**: https://github.com/你的用户名/novel-rewrite/issues
- **文档**: https://github.com/你的用户名/novel-rewrite/README.md
- **邮箱**: your-email@example.com

---

**祝你使用愉快！🎉**
