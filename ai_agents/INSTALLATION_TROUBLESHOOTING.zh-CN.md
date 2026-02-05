# 安装故障排查指南

## 问题：`task install` 任务不存在

### 症状
```powershell
PS D:\code\ten-framework\ai_agents> task install
task: Task "install" does not exist
```

### 原因
在 `ai_agents` 目录下没有 `install` 任务。`install` 任务只存在于具体的示例项目目录中。

### 解决方案
进入具体的示例目录后再运行安装命令：

```powershell
cd agents/examples/voice-assistant
task install
```

---

## 问题：`tman: executable file not found in $PATH`

### 症状
```powershell
PS D:\code\ten-framework\ai_agents\agents\examples\voice-assistant> task install
task: [install-tenapp] tman install
"tman": executable file not found in $PATH
task: Failed to run task "install": task: Failed to run task "install-tenapp": exit status 127
```

### 原因
`tman` (TEN Manager) 是 TEN Framework 的包管理器，需要先安装才能使用。这是运行 TEN 应用的**必需工具**。

### 解决方案

#### Windows 用户

**方式 1：使用 WSL (推荐)**

TEN Framework 目前主要支持 Linux 和 macOS。Windows 用户建议使用 WSL (Windows Subsystem for Linux)：

1. **安装 WSL**
   ```powershell
   # 以管理员身份运行 PowerShell
   wsl --install
   # 重启计算机
   ```

2. **进入 WSL 环境**
   ```powershell
   wsl
   ```

3. **在 WSL 中安装 tman**
   ```bash
   # Ubuntu/Debian
   sudo add-apt-repository ppa:ten-framework/ten-framework
   sudo apt update
   sudo apt install tman
   
   # 或使用安装脚本
   bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)
   ```

4. **在 WSL 中继续开发**
   ```bash
   cd /mnt/d/code/ten-framework/ai_agents/agents/examples/voice-assistant
   task install
   ```

**方式 2：Docker (备选方案)**

使用 Docker 容器运行 TEN Framework：

```powershell
# 进入项目目录
cd D:\code\ten-framework\ai_agents

# 使用 Docker Compose
docker compose up -d

# 进入容器
docker exec -it ten_agent_dev bash

# 在容器内安装和运行
cd agents/examples/voice-assistant
task install
task run
```

#### Linux/macOS 用户

**Ubuntu/Debian:**

```bash
sudo add-apt-repository ppa:ten-framework/ten-framework
sudo apt update
sudo apt install tman
```

**macOS:**

```bash
brew install TEN-framework/ten-framework/tman
```

**通用方式 (安装脚本):**

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)
```

或者，如果已经克隆了仓库：

```bash
cd ten-framework
bash tools/tman/install_tman.sh
```

#### 验证安装

```bash
tman --version
# 应显示 tman 版本信息
```

---

## 完整的安装步骤（从零开始）

### 前提条件检查

在开始之前，确保已安装以下软件：

1. **Python 3.10**
   ```bash
   python3 --version
   # 应显示: Python 3.10.x
   ```
   
   如果没有 Python 3.10，使用 pyenv 安装：
   ```bash
   # 安装 pyenv
   curl https://pyenv.run | bash
   
   # 安装 Python 3.10
   pyenv install 3.10.14
   pyenv local 3.10.14
   ```

2. **Go 1.20+**
   ```bash
   go version
   # 应显示: go version go1.20 或更高版本
   ```

3. **Node.js / npm**
   ```bash
   node --version
   npm --version
   ```

4. **Task** (任务运行器)
   ```bash
   # Ubuntu/Debian
   sudo apt install task
   
   # macOS
   brew install go-task
   
   # 其他系统：https://taskfile.dev/installation/
   ```

### 安装 TEN Framework

**步骤 1: 安装 tman**

参考上面的"解决方案"部分，根据你的操作系统安装 tman。

**步骤 2: 克隆仓库（如果还没有）**

```bash
git clone https://github.com/TEN-framework/ten-framework.git
cd ten-framework
```

**步骤 3: 配置环境变量**

```bash
cd ai_agents
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥
```

**步骤 4: 进入示例目录**

```bash
cd agents/examples/voice-assistant
```

**步骤 5: 安装依赖**

```bash
task install
```

这个命令会：
- 安装 TEN app 依赖 (`tman install`)
- 安装 Python 依赖
- 安装前端依赖
- 编译 API 服务器

**步骤 6: 运行应用**

```bash
task run
```

**步骤 7: 访问应用**

- 前端: http://localhost:3000
- API 服务器: http://localhost:8080
- TMAN Designer: http://localhost:49483

---

## 常见问题

### Q: 为什么 Windows 不能直接运行？

A: TEN Framework 目前主要支持 Linux 和 macOS。Windows 用户需要使用 WSL 或 Docker。这是因为 TEN Framework 依赖于一些 Unix 特定的功能。

### Q: 我已经安装了 tman，但还是提示找不到？

A: 检查以下几点：

1. **验证 tman 是否在 PATH 中**
   ```bash
   which tman
   # 应显示 tman 的路径
   ```

2. **重新加载 shell 配置**
   ```bash
   # Bash
   source ~/.bashrc
   
   # Zsh
   source ~/.zshrc
   ```

3. **检查 tman 版本**
   ```bash
   tman --version
   ```

### Q: 安装过程中遇到权限错误怎么办？

A: 某些操作可能需要管理员权限：

```bash
# Linux/macOS - 使用 sudo
sudo apt install tman

# 或者安装到用户目录（不需要 sudo）
bash tools/tman/install_tman.sh
```

### Q: Python 版本不对怎么办？

A: TEN Framework 需要 Python 3.10。使用 pyenv 管理 Python 版本：

```bash
# 安装 pyenv
curl https://pyenv.run | bash

# 安装 Python 3.10
pyenv install 3.10.14
pyenv local 3.10.14

# 验证
python --version
```

### Q: 在 Docker 中运行时遇到问题？

A: 确保 Docker 服务正在运行：

```bash
# 检查 Docker 状态
docker ps

# 启动 Docker Compose
cd ai_agents
docker compose up -d

# 查看日志
docker compose logs -f
```

### Q: task 命令找不到？

A: 需要先安装 Task 任务运行器：

**Ubuntu/Debian:**
```bash
sudo apt install task
```

**macOS:**
```bash
brew install go-task
```

**其他系统:**
参考 https://taskfile.dev/installation/

### Q: 安装依赖时卡住或超时？

A: 可能是网络问题。尝试：

1. **使用代理**
   ```bash
   export HTTP_PROXY=http://your-proxy:port
   export HTTPS_PROXY=http://your-proxy:port
   ```

2. **增加超时时间**
   ```bash
   export TIMEOUT=300
   ```

3. **使用国内镜像（中国用户）**
   ```bash
   # Python pip 镜像
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   
   # npm 镜像
   npm config set registry https://registry.npmmirror.com
   ```

---

## 诊断脚本

运行此脚本检查你的环境：

```bash
#!/bin/bash

echo "===== TEN Framework 环境诊断 ====="
echo ""

# 检查 Python
echo "检查 Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
    if [[ $PYTHON_VERSION == *"3.10"* ]]; then
        echo "✅ Python 版本正确"
    else
        echo "⚠️  Python 版本不是 3.10，建议使用 Python 3.10"
    fi
else
    echo "❌ Python 未安装"
fi
echo ""

# 检查 Go
echo "检查 Go..."
if command -v go &> /dev/null; then
    echo "✅ $(go version)"
else
    echo "❌ Go 未安装"
fi
echo ""

# 检查 Node.js
echo "检查 Node.js..."
if command -v node &> /dev/null; then
    echo "✅ Node $(node --version)"
else
    echo "❌ Node.js 未安装"
fi
echo ""

# 检查 npm
echo "检查 npm..."
if command -v npm &> /dev/null; then
    echo "✅ npm $(npm --version)"
else
    echo "❌ npm 未安装"
fi
echo ""

# 检查 Task
echo "检查 Task..."
if command -v task &> /dev/null; then
    echo "✅ $(task --version)"
else
    echo "❌ Task 未安装"
fi
echo ""

# 检查 tman
echo "检查 tman..."
if command -v tman &> /dev/null; then
    echo "✅ $(tman --version)"
else
    echo "❌ tman 未安装"
    echo "   请运行以下命令安装："
    echo "   bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)"
fi
echo ""

# 检查操作系统
echo "操作系统信息："
uname -a
echo ""

echo "===== 诊断完成 ====="
```

保存为 `check_env.sh`，然后运行：

```bash
bash check_env.sh
```

---

## 获取帮助

如果以上方法都无法解决你的问题：

1. **查看详细文档**
   - [快速开始指南](../../docs/getting-started/quick-start.cn.md)
   - [Voice Assistant README](README.zh-CN.md)

2. **搜索已知问题**
   - [GitHub Issues](https://github.com/TEN-framework/ten-framework/issues)

3. **提问**
   - [Discord 社区](https://discord.gg/VnPftUzAMJ)
   - [GitHub Discussions](https://github.com/TEN-framework/ten-framework/discussions)

4. **创建 Issue**
   提供以下信息：
   - 操作系统和版本
   - Python/Go/Node.js 版本
   - 完整的错误信息
   - 运行 `check_env.sh` 的输出

---

## 相关文档

- [README.zh-CN.md](README.zh-CN.md) - Voice Assistant 中文文档
- [快速开始指南](../../docs/getting-started/quick-start.cn.md) - TEN Framework 快速开始
- [配置修改指南](CONFIG_MODIFICATION_GUIDE.zh-CN.md) - 如何修改配置
- [API 密钥安全指南](../../API_KEYS_SECURITY_GUIDE.zh-CN.md) - API 密钥管理
