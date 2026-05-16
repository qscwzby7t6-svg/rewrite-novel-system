@echo off
chcp 65001 > nul
echo ==========================================
echo   NovelForge Windows 一键部署脚本
echo   Version: 1.0.0
echo ==========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 建议以管理员身份运行以获得最佳体验
    echo.
)

:: 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python 3.11+
    echo.
    echo 请先安装 Python:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载 Python 3.11 或更高版本
    echo 3. 安装时务必勾选 "Add Python to PATH"
    echo.
    echo 或者使用 winget 安装:
    echo winget install Python.Python.3.11
    echo.
    pause
    exit /b 1
)

:: 检查 Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git
    echo.
    echo 请先安装 Git:
    echo 1. 访问 https://git-scm.com/download/win
    echo 2. 下载并安装 Git for Windows
    echo.
    echo 或者使用 winget 安装:
    echo winget install Git.Git
    echo.
    pause
    exit /b 1
)

:: 检查 Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Node.js
    echo.
    echo 请先安装 Node.js:
    echo 1. 访问 https://nodejs.org/
    echo 2. 下载 LTS 版本
    echo.
    echo 或者使用 winget 安装:
    echo winget install OpenJS.NodeJS.LTS
    echo.
    pause
    exit /b 1
)

echo [√] 系统检查通过
echo.
echo ==========================================
echo.

set /p REPO_URL=请输入你的 GitHub 仓库地址（直接回车使用默认）:
if "%REPO_URL%"=="" set REPO_URL=https://github.com/你的用户名/novel-rewrite.git

:: 获取当前目录
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo [1/8] 清理旧环境（如果存在）...
if exist "venv" (
    echo   - 删除旧虚拟环境
    rmdir /s /q venv
)
if exist "backend\venv" (
    echo   - 删除旧后端虚拟环境
    rmdir /s /q backend\venv
)

echo [2/8] 克隆/更新项目...
if exist ".git" (
    echo   - 检测到已有 Git 仓库，更新中...
    git pull
) else (
    echo   - 克隆新项目...
    git clone %REPO_URL% .
)

echo [3/8] 创建 Python 虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo [错误] 虚拟环境创建失败
    pause
    exit /b 1
)

echo [4/8] 激活虚拟环境并升级 pip...
call venv\Scripts\activate
python -m pip install --upgrade pip

echo [5/8] 安装后端依赖...
pip install -r backend\requirements.txt
if %errorlevel% neq 0 (
    echo [警告] 部分依赖安装失败，尝试使用镜像源...
    pip install -r backend\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
)

echo [6/8] 安装前端依赖...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo [警告] npm 安装失败，尝试使用淘宝镜像...
    npm config set registry https://registry.npmmirror.com
    call npm install
)
cd ..

echo [7/8] 配置环境变量...
if not exist ".env" (
    copy .env.example .env
    echo   - 已创建 .env 配置文件
    echo   - 请编辑 .env 文件配置你的 API 密钥
) else (
    echo   - .env 文件已存在
)

echo [8/8] 创建启动脚本...
call :create_start_script

echo.
echo ==========================================
echo   ✓ 部署完成！
echo ==========================================
echo.
echo 后端启动命令:
echo   call venv\Scripts\activate
echo   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo 前端启动命令:
echo   cd frontend
echo   npm run dev
echo.
echo 或者直接运行 start.bat 启动
echo.
echo 配置文件位置: %PROJECT_DIR%.env
echo.
echo 是否立即启动？ (Y/N)
set /p START_NOW=
if /i "%START_NOW%"=="Y" goto start_now
goto end

:start_now
echo.
echo 启动 NovelForge...
echo.
start "NovelForge Backend" cmd /k "call venv\Scripts\activate && uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak > nul
start "NovelForge Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak > nul
start http://localhost:3000
goto end

:create_start_script
echo @echo off > start.bat
echo chcp 65001 ^> nul >> start.bat
echo echo ========================================== >> start.bat
echo echo   NovelForge 启动脚本 >> start.bat
echo echo ========================================== >> start.bat
echo. >> start.bat
echo :: 激活虚拟环境 >> start.bat
echo call venv\Scripts\activate >> start.bat
echo. >> start.bat
echo :: 启动后端（后台运行） >> start.bat
echo start "NovelForge Backend" cmd /k "uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000" >> start.bat
echo. >> start.bat
echo :: 等待2秒 >> start.bat
echo timeout /t 2 /nobreak ^> nul >> start.bat
echo. >> start.bat
echo :: 启动前端 >> start.bat
echo cd frontend >> start.bat
echo start "NovelForge Frontend" cmd /k "npm run dev" >> start.bat
echo. >> start.bat
echo echo. >> start.bat
echo echo ========================================== >> start.bat
echo echo   NovelForge 已启动！ >> start.bat
echo echo ========================================== >> start.bat
echo echo. >> start.bat
echo echo   前端地址: http://localhost:3000 >> start.bat
echo echo   后端地址: http://localhost:8000 >> start.bat
echo echo   API 文档: http://localhost:8000/docs >> start.bat
echo echo. >> start.bat
echo echo   按任意键打开浏览器... >> start.bat
echo pause ^> nul >> start.bat
echo. >> start.bat
echo start http://localhost:3000 >> start.bat
exit /b 0

:end
pause
