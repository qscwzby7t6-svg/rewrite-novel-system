#!/bin/bash

# NovelForge Linux/macOS 一键部署脚本

echo "============================================"
echo "  NovelForge Linux/macOS 一键部署脚本"
echo "  Version: 1.0.0"
echo "============================================"
echo ""

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    PKG_MANAGER="brew"
    echo "[系统] 检测到 macOS"
else
    # 检测 Linux 发行版
    if [ -f /etc/debian_version ]; then
        PKG_MANAGER="apt-get"
        echo "[系统] 检测到 Debian/Ubuntu"
    elif [ -f /etc/redhat-release ]; then
        PKG_MANAGER="yum"
        echo "[系统] 检测到 RedHat/CentOS"
    elif [ -f /etc/arch-release ]; then
        PKG_MANAGER="pacman"
        echo "[系统] 检测到 Arch Linux"
    else
        echo "[系统] 尝试自动检测包管理器..."
        if command -v apt-get &> /dev/null; then
            PKG_MANAGER="apt-get"
        elif command -v yum &> /dev/null; then
            PKG_MANAGER="yum"
        elif command -v pacman &> /dev/null; then
            PKG_MANAGER="pacman"
        else
            echo "[错误] 未检测到支持的包管理器"
            exit 1
        fi
    fi
fi

# 检查必要命令
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "[错误] 未检测到 $1，请先安装"
        return 1
    fi
    echo "[✓] 检测到 $1: $($1 --version | head -n1)"
    return 0
}

echo "[1/8] 检查系统环境..."
check_command git || exit 1
check_command python3 || exit 1

# Python 版本检查
PYTHON_VERSION=$(python3 --version | grep -oP '\d+\.\d+' | cut -d. -f1)
if [ "$PYTHON_VERSION" -lt 3 ]; then
    echo "[错误] 需要 Python 3.11+"
    exit 1
fi
echo "[✓] Python 版本符合要求"

# 安装系统依赖
echo "[2/8] 安装系统依赖..."
if [ "$PKG_MANAGER" == "apt-get" ]; then
    sudo apt-get update
    sudo apt-get install -y python3-venv python3-pip nodejs npm
elif [ "$PKG_MANAGER" == "yum" ]; then
    sudo yum update
    sudo yum install -y python3 python3-pip python3-venv nodejs npm
elif [ "$PKG_MANAGER" == "pacman" ]; then
    sudo pacman -Sy
    sudo pacman -S --noconfirm python python-pip python-venv nodejs npm
elif [ "$PKG_MANAGER" == "brew" ]; then
    brew update
    brew install python node
fi

# 获取项目目录
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# Git 配置
echo "[3/8] 配置 Git..."
if [ ! -d ".git" ]; then
    echo "请输入你的 GitHub 仓库地址:"
    echo "格式: https://github.com/用户名/仓库名.git"
    read -p "直接回车使用当前目录作为新仓库: " REPO_URL
    
    if [ -n "$REPO_URL" ]; then
        git init
        git remote add origin "$REPO_URL"
    else
        git init
    fi
fi

# 创建虚拟环境
echo "[4/8] 创建 Python 虚拟环境..."
if [ -d "venv" ]; then
    echo "删除旧虚拟环境..."
    rm -rf venv
fi

python3 -m venv venv
source venv/bin/activate

# 升级 pip
echo "[5/8] 安装后端依赖..."
pip install --upgrade pip
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "[警告] 使用镜像源重试..."
    pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

# 安装前端依赖
echo "[6/8] 安装前端依赖..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "[警告] 使用淘宝镜像重试..."
    npm config set registry https://registry.npmmirror.com
    npm install
fi
cd ..

# 配置环境变量
echo "[7/8] 配置环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "已创建 .env 配置文件"
else
    echo ".env 文件已存在"
fi

# 创建启动脚本
echo "[8/8] 创建启动脚本..."
cat > start.sh << 'STARTSCRIPT'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "============================================"
echo "  NovelForge 启动中..."
echo "============================================"
echo ""
echo "后端地址: http://localhost:8000"
echo "前端地址: http://localhost:3000"
echo "API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
FRONTEND_PID=$!
cd frontend && npm run dev
STARTSCRIPT

chmod +x start.sh

cat > stop.sh << 'STOPSCRIPT'
#!/bin/bash
echo "停止 NovelForge 服务..."
pkill -f "uvicorn backend.main:app" || true
pkill -f "npm run dev" || true
echo "服务已停止"
STOPSCRIPT

chmod +x stop.sh

echo ""
echo "============================================"
echo "  ✓ 部署完成！"
echo "============================================"
echo ""
echo "项目目录: $PROJECT_DIR"
echo ""
echo "启动命令:"
echo "  bash start.sh"
echo ""
echo "停止命令:"
echo "  bash stop.sh"
echo ""
echo "配置文件: $PROJECT_DIR/.env"
echo ""
read -p "是否立即启动？ (Y/N) [N]: " start_now
start_now=${start_now:-N}

if [[ "$start_now" == "Y" || "$start_now" == "y" ]]; then
    echo ""
    bash start.sh
fi
