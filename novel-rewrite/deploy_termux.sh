#!/bin/bash

# NovelForge Termux 一键部署脚本
# 适用于荣耀平板和其他 Android 设备

echo "============================================"
echo "  NovelForge Termux 一键部署脚本"
echo "  适用于荣耀平板 / Android 设备"
echo "  Version: 1.0.0"
echo "============================================"
echo ""

# 检查是否在 Termux 中运行
if [ ! -d "$PREFIX" ]; then
    echo "[错误] 此脚本必须在 Termux 中运行"
    echo "下载 Termux: https://f-droid.org/en/packages/com.termux/"
    exit 1
fi

# 显示系统信息
echo "[信息] 系统环境检查..."
echo "  设备: $(uname -m)"
echo "  系统: $(uname -s)"
echo "  Termux 版本: $($PREFIX/bin/sh --version 2>/dev/null || echo 'Unknown')"
echo ""

# 更新包列表
echo "[1/9] 更新系统包..."
pkg update -y && pkg upgrade -y
if [ $? -ne 0 ]; then
    echo "[警告] 包更新失败，尝试继续..."
fi

# 安装必要工具
echo "[2/9] 安装必要工具..."
pkg install git python nodejs -y
if [ $? -ne 0 ]; then
    echo "[错误] 工具安装失败"
    exit 1
fi

# 验证安装
echo "[3/9] 验证安装..."
python --version
node --version
npm --version
git --version
echo ""

# 设置存储权限
echo "[4/9] 配置存储权限..."
if [ ! -d "$HOME/storage" ]; then
    echo "请授予存储权限..."
    termux-setup-storage
    echo "如果授权成功，应该能看到 ~/storage 目录"
    ls -la ~/storage/ 2>/dev/null || echo "存储权限未授权，某些功能可能受限"
fi
echo ""

# 获取项目目录
echo "[5/9] 选择项目位置..."
echo "  1. 共享存储 (~/storage/shared) - 推荐，便于电脑访问"
echo "  2. Termux 主目录 (~/novel-rewrite)"
echo "  3. 下载目录 (~/storage/downloads)"
read -p "请选择 [1-3，默认1]: " choice
choice=${choice:-1}

case $choice in
    1)
        PROJECT_DIR="$HOME/storage/shared/novel-rewrite"
        ;;
    2)
        PROJECT_DIR="$HOME/novel-rewrite"
        ;;
    3)
        PROJECT_DIR="$HOME/storage/downloads/novel-rewrite"
        ;;
    *)
        PROJECT_DIR="$HOME/storage/shared/novel-rewrite"
        ;;
esac

# 克隆项目
echo "[6/9] 克隆项目到 $PROJECT_DIR..."
mkdir -p "$(dirname "$PROJECT_DIR")"

if [ -d "$PROJECT_DIR/.git" ]; then
    echo "项目已存在，更新中..."
    cd "$PROJECT_DIR"
    git pull
else
    echo "请输入你的 GitHub 仓库地址:"
    echo "格式: https://github.com/用户名/仓库名.git"
    read -p "直接回车使用默认: " REPO_URL
    REPO_URL=${REPO_URL:-https://github.com/你的用户名/novel-rewrite.git}
    
    git clone "$REPO_URL" "$PROJECT_DIR"
    if [ $? -ne 0 ]; then
        echo "[错误] 项目克隆失败"
        exit 1
    fi
fi

cd "$PROJECT_DIR"
echo "当前目录: $(pwd)"
echo ""

# 创建虚拟环境
echo "[7/9] 创建 Python 虚拟环境..."
python -m venv venv
if [ $? -ne 0 ]; then
    echo "[错误] 虚拟环境创建失败"
    exit 1
fi

# 激活虚拟环境
source venv/bin/activate

# 升级 pip
echo "[8/9] 安装后端依赖..."
pip install --upgrade pip
pip install -r backend/requirements.txt
if [ $? -ne 0 ]; then
    echo "[警告] 部分依赖安装失败，尝试使用镜像源..."
    pip install -r backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
fi

# 安装前端依赖
echo "[9/9] 安装前端依赖..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "[警告] npm 安装失败，尝试使用淘宝镜像..."
    npm config set registry https://registry.npmmirror.com
    npm install
fi
cd ..

# 配置环境变量
echo ""
echo "[配置] 环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "已创建 .env 配置文件"
    echo "请编辑 .env 文件配置你的 API 密钥:"
    echo "  nano $PROJECT_DIR/.env"
else
    echo ".env 文件已存在"
fi

# 创建启动脚本
echo ""
echo "[完成] 创建便捷启动脚本..."
cat > start.sh << 'STARTSCRIPT'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "启动 NovelForge..."
echo "后端地址: http://localhost:8000"
echo "前端地址: http://localhost:3000"
echo "API 文档: http://localhost:8000/docs"
echo ""
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
FRONTEND_PID=$!
cd frontend && npm run dev &
wait
STARTSCRIPT

chmod +x start.sh

echo ""
echo "============================================"
echo "  ✓ 部署完成！"
echo "============================================"
echo ""
echo "项目位置: $PROJECT_DIR"
echo ""
echo "启动命令:"
echo "  cd $PROJECT_DIR"
echo "  bash start.sh"
echo ""
echo "或者分步启动:"
echo "  1. source venv/bin/activate"
echo "  2. uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "前端启动 (新窗口):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "配置文件: $PROJECT_DIR/.env"
echo ""
read -p "是否立即启动？ (Y/N) [N]: " start_now
start_now=${start_now:-N}

if [[ "$start_now" == "Y" || "$start_now" == "y" ]]; then
    echo ""
    echo "启动 NovelForge..."
    bash start.sh
else
    echo ""
    echo "部署完成！运行 'bash start.sh' 启动服务"
fi
