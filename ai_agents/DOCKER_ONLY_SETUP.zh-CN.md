# Docker 纯容器化安装指南

## 📌 核心信息

> **你的理解完全正确！** ✅
> 
> 使用 Docker 方式，你的本地电脑**只需要安装 Docker**，不需要安装：
> - ❌ Task（已在容器内）
> - ❌ tman（已在容器内）
> - ❌ Python 3.10（已在容器内）
> - ❌ Go 1.20+（已在容器内）
> - ❌ Node.js（已在容器内）
> - ❌ 任何其他开发工具
> 
> **所有工具都在 Docker 容器内预装好了！**

## 🎯 为什么选择 Docker 方式？

### Docker vs 本地安装对比

| 对比项 | Docker 方式 ✅ | 本地安装方式 |
|--------|----------------|--------------|
| **本地需要安装** | 只需要 Docker | Python、Go、Node.js、Task、tman 等 |
| **安装步骤** | 1 步 | 5+ 步 |
| **安装时间** | 5-10 分钟 | 30-60 分钟 |
| **适用系统** | Windows/Linux/macOS | Linux/macOS（Windows 需 WSL） |
| **环境隔离** | ✅ 完全隔离 | ❌ 可能冲突 |
| **依赖管理** | ✅ 自动 | ❌ 手动 |
| **问题排查** | ✅ 易排查 | ❌ 难排查 |
| **推荐指数** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### Docker 方式的优势

1. **零配置困难** 🎉
   - 不需要配置 Python 环境
   - 不需要解决依赖冲突
   - 不需要担心版本问题

2. **环境一致** 🔒
   - 所有人使用相同的环境
   - 避免"在我机器上能跑"的问题
   - 容易复现和排查问题

3. **快速开始** ⚡
   - 安装 Docker 后即可开始
   - 5 分钟内可以运行起来
   - 一键启动，开箱即用

4. **Windows 友好** 💻
   - 不需要 WSL
   - Docker Desktop 一键安装
   - 和 Linux/macOS 体验一致

## 🚀 快速开始（5 步）

### 第 1 步：安装 Docker

#### Windows

1. 访问 [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. 下载 Windows 版本（约 500 MB）
3. 双击安装文件，按提示安装
4. 重启电脑（如果需要）
5. 启动 Docker Desktop

#### macOS

```bash
# 方式 1：Homebrew
brew install --cask docker

# 方式 2：手动下载
# 访问 https://www.docker.com/products/docker-desktop
```

#### Linux (Ubuntu/Debian)

```bash
# 安装 Docker
sudo apt update
sudo apt install docker.io docker-compose

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户添加到 docker 组（避免 sudo）
sudo usermod -aG docker $USER
# 注销并重新登录
```

### 第 2 步：克隆项目

```bash
# 克隆仓库
git clone https://github.com/TEN-framework/ten-framework.git

# 进入 ai_agents 目录
cd ten-framework/ai_agents
```

### 第 3 步：配置 API 密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
# Windows: notepad .env
# macOS/Linux: nano .env 或 vim .env
```

需要填写的关键变量：
```bash
# RTC
AGORA_APP_ID=你的_Agora_App_ID
AGORA_APP_CERTIFICATE=你的_Agora_证书

# LLM
OPENAI_API_KEY=你的_OpenAI_密钥
# 或使用其他 LLM（Qwen、Gemini 等）

# STT
DEEPGRAM_API_KEY=你的_Deepgram_密钥

# TTS
ELEVENLABS_API_KEY=你的_ElevenLabs_密钥
```

💡 **提示**：如果还没有 API 密钥，查看 [FREE_TRIAL_GUIDE.zh-CN.md](./agents/examples/voice-assistant/FREE_TRIAL_GUIDE.zh-CN.md)

### 第 4 步：启动 Docker 容器

```bash
# 启动容器（后台运行）
docker compose up -d

# 查看容器状态
docker ps
```

你应该看到类似输出：
```
CONTAINER ID   IMAGE           COMMAND      STATUS         PORTS          NAMES
abc123def456   ten_agent_dev   "/bin/bash"  Up 10 seconds  0.0.0.0:8080   ten_agent_dev
```

### 第 5 步：在容器内运行项目

```bash
# 进入容器
docker exec -it ten_agent_dev bash

# 进入 voice-assistant 目录
cd agents/examples/voice-assistant

# 安装依赖（Task 和 tman 都在容器内可用）
task install

# 运行项目
task run
```

### 第 6 步：访问应用

打开浏览器，访问：
- **Web UI**: http://localhost:3000
- **API Server**: http://localhost:8080
- **TMAN Designer**: http://localhost:49483

## ❓ 常见问题

### 1. Task 真的不需要在本地安装吗？

**完全正确！** ✅

Docker 容器内已经预装了：
- Task: `/usr/local/bin/task`
- tman: `/usr/local/bin/tman`
- Python 3.10: `/usr/bin/python3.10`
- Go 1.20+: `/usr/local/go`
- Node.js: `/usr/bin/node`

你只需要：
1. 安装 Docker
2. 启动容器：`docker compose up -d`
3. 进入容器：`docker exec -it ten_agent_dev bash`
4. 运行命令：`task install`、`task run`

### 2. 我在 Windows 上需要安装 WSL 吗？

**不需要！** ✅

使用 Docker Desktop，Windows 用户不需要 WSL。Docker Desktop 会自动处理所有底层细节。

### 3. 代码在哪里？我如何编辑？

代码在**本地**，通过 Docker 卷映射到容器：

```yaml
# docker-compose.yaml
volumes:
  - ./:/app  # 本地目录映射到容器内 /app
```

你可以：
- ✅ 在本地用任何编辑器（VSCode、Sublime 等）编辑代码
- ✅ 容器内会实时看到变化
- ✅ 不需要重启容器

推荐工作流：
1. 在本地用 VSCode 编辑代码
2. 在容器内运行 `task run`
3. 浏览器查看效果
4. 保存代码，容器自动重载

### 4. 容器重启后数据会丢失吗？

**不会！** ✅

以下数据都保存在本地：
- 代码文件（通过卷映射）
- `.env` 配置（在本地）
- `property.json`（在本地）
- 日志文件（通过卷映射）

容器只提供运行环境，所有重要数据都在本地。

### 5. 如何停止和重启容器？

```bash
# 停止容器（保留所有数据）
docker compose down

# 重启容器
docker compose up -d

# 查看容器状态
docker ps

# 查看容器日志
docker logs ten_agent_dev

# 实时查看日志
docker logs -f ten_agent_dev
```

### 6. 容器占用多少磁盘空间？

- Docker 镜像：~1.5 GB
- 运行时容器：~500 MB
- Python 包缓存：~500 MB
- **总计**：约 2-3 GB

相比本地安装，占用略大但换来的是：
- 零配置困难
- 环境完全隔离
- 一键部署

### 7. 性能怎么样？

Docker 容器性能接近原生：
- **CPU**: 90-95% 原生性能
- **内存**: 95-98% 原生性能
- **磁盘 I/O**: 85-90% 原生性能

对于开发和测试，性能完全足够。

### 8. 可以同时运行多个项目吗？

可以，但需要修改端口避免冲突：

```yaml
# docker-compose.yaml
ports:
  - "8081:8080"   # API Server（改为 8081）
  - "3001:3000"   # Web UI（改为 3001）
  - "49484:49483" # TMAN Designer（改为 49484）
```

### 9. 如何更新代码？

```bash
# 在本地拉取最新代码
git pull

# 重启容器使更改生效
docker compose restart

# 如果需要重建镜像（依赖有变化）
docker compose down
docker compose build --no-cache
docker compose up -d
```

### 10. 遇到问题怎么办？

#### 方案 1：重启容器（解决 90% 的问题）

```bash
docker compose down
docker compose up -d
```

#### 方案 2：查看日志

```bash
# 查看容器日志
docker logs ten_agent_dev

# 实时查看日志
docker logs -f ten_agent_dev
```

#### 方案 3：重建容器

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

#### 方案 4：进入容器调试

```bash
# 进入容器
docker exec -it ten_agent_dev bash

# 检查工具是否可用
task --version
tman --version
python3 --version
go version
node --version
```

## 🛠️ Docker 命令速查

### 基础命令

```bash
# 启动容器（后台运行）
docker compose up -d

# 启动容器（前台运行，看日志）
docker compose up

# 停止容器
docker compose down

# 重启容器
docker compose restart

# 查看容器状态
docker ps

# 查看所有容器（包括停止的）
docker ps -a
```

### 进入容器

```bash
# 进入容器 bash
docker exec -it ten_agent_dev bash

# 在容器内执行单个命令
docker exec ten_agent_dev task --version

# 以 root 身份进入容器
docker exec -it -u root ten_agent_dev bash
```

### 日志查看

```bash
# 查看容器日志
docker logs ten_agent_dev

# 实时查看日志
docker logs -f ten_agent_dev

# 查看最近 100 行日志
docker logs --tail 100 ten_agent_dev
```

### 镜像管理

```bash
# 查看本地镜像
docker images

# 重建镜像
docker compose build --no-cache

# 删除旧镜像
docker image prune

# 查看镜像详情
docker inspect ten_agent_dev
```

### 资源清理

```bash
# 停止并删除容器
docker compose down

# 删除容器和卷
docker compose down -v

# 清理未使用的资源
docker system prune

# 清理所有未使用资源（包括镜像）
docker system prune -a
```

## 🔧 故障排查

### 问题 1：容器启动失败

**症状**：
```bash
docker compose up -d
Error response from daemon: driver failed programming external connectivity
```

**解决方案**：
1. 检查端口是否被占用：
   ```bash
   # Windows
   netstat -ano | findstr :8080
   
   # Linux/macOS
   lsof -i :8080
   ```

2. 修改端口或停止占用端口的程序

### 问题 2：容器运行但无法访问

**症状**：浏览器无法访问 http://localhost:3000

**解决方案**：
1. 检查容器是否真的在运行：
   ```bash
   docker ps
   ```

2. 检查容器内服务是否启动：
   ```bash
   docker exec -it ten_agent_dev bash
   ps aux | grep node
   ```

3. 查看容器日志：
   ```bash
   docker logs ten_agent_dev
   ```

### 问题 3：代码修改后不生效

**症状**：修改代码后，容器内没有更新

**解决方案**：
1. 检查卷映射是否正确：
   ```bash
   docker inspect ten_agent_dev | grep -A 10 Mounts
   ```

2. 重启容器：
   ```bash
   docker compose restart
   ```

### 问题 4：权限问题

**症状**：
```bash
permission denied while trying to connect to the Docker daemon socket
```

**解决方案**（Linux）：
```bash
# 将用户添加到 docker 组
sudo usermod -aG docker $USER

# 重新登录或运行
newgrp docker
```

### 问题 5：磁盘空间不足

**症状**：
```bash
no space left on device
```

**解决方案**：
```bash
# 清理未使用的资源
docker system prune -a

# 查看磁盘使用情况
docker system df
```

## 📚 相关文档

- [INSTALLATION_TROUBLESHOOTING.zh-CN.md](./INSTALLATION_TROUBLESHOOTING.zh-CN.md) - 安装故障排查
- [README_SECURITY.md](./README_SECURITY.md) - API 密钥安全指南
- [FREE_TRIAL_GUIDE.zh-CN.md](./agents/examples/voice-assistant/FREE_TRIAL_GUIDE.zh-CN.md) - 免费试用指南
- [VOICE_INTEGRATION_GUIDE.zh-CN.md](./agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md) - 集成指南

## 🎉 总结

**使用 Docker 方式，你的理解完全正确！**

> - ✅ 本地只需要安装 Docker
> - ✅ Task 不需要本地安装（在容器内）
> - ✅ tman 不需要本地安装（在容器内）
> - ✅ Python、Go、Node.js 都不需要本地安装
> - ✅ 所有开发工具都在容器内预装好了
> - ✅ 一条命令 `docker compose up -d` 启动
> - ✅ 进入容器后，所有命令都可以直接使用

**5 个步骤即可开始：**
1. 安装 Docker
2. 配置 `.env`
3. `docker compose up -d`
4. `docker exec -it ten_agent_dev bash`
5. `task install && task run`

享受开发！🚀
