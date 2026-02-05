# Docker-Only Setup Guide

## 📌 Core Information

> **Your understanding is absolutely correct!** ✅
> 
> With the Docker approach, your local machine **only needs Docker installed**. You don't need:
> - ❌ Task (already in container)
> - ❌ tman (already in container)
> - ❌ Python 3.10 (already in container)
> - ❌ Go 1.20+ (already in container)
> - ❌ Node.js (already in container)
> - ❌ Any other development tools
> 
> **All tools are pre-installed in the Docker container!**

## 🎯 Why Choose Docker?

### Docker vs Local Installation Comparison

| Aspect | Docker Approach ✅ | Local Installation |
|--------|-------------------|-------------------|
| **Local Requirements** | Docker only | Python, Go, Node.js, Task, tman, etc. |
| **Installation Steps** | 1 step | 5+ steps |
| **Time to Install** | 5-10 minutes | 30-60 minutes |
| **Supported OS** | Windows/Linux/macOS | Linux/macOS (WSL for Windows) |
| **Environment Isolation** | ✅ Fully isolated | ❌ Potential conflicts |
| **Dependency Management** | ✅ Automatic | ❌ Manual |
| **Troubleshooting** | ✅ Easy | ❌ Difficult |
| **Recommendation** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

### Docker Advantages

1. **Zero Configuration Hassle** 🎉
   - No Python environment setup needed
   - No dependency conflicts
   - No version issues

2. **Consistent Environment** 🔒
   - Everyone uses the same environment
   - Avoids "works on my machine" problems
   - Easy to reproduce and troubleshoot

3. **Quick Start** ⚡
   - Start developing after installing Docker
   - Up and running in 5 minutes
   - One command to start

4. **Windows Friendly** 💻
   - No WSL needed
   - Docker Desktop one-click install
   - Same experience as Linux/macOS

## 🚀 Quick Start (5 Steps)

### Step 1: Install Docker

#### Windows

1. Visit [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Download Windows version (~500 MB)
3. Double-click installer and follow prompts
4. Restart computer if needed
5. Launch Docker Desktop

#### macOS

```bash
# Method 1: Homebrew
brew install --cask docker

# Method 2: Manual download
# Visit https://www.docker.com/products/docker-desktop
```

#### Linux (Ubuntu/Debian)

```bash
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group (avoid sudo)
sudo usermod -aG docker $USER
# Log out and log back in
```

### Step 2: Clone Project

```bash
# Clone repository
git clone https://github.com/TEN-framework/ten-framework.git

# Enter ai_agents directory
cd ten-framework/ai_agents
```

### Step 3: Configure API Keys

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
# Windows: notepad .env
# macOS/Linux: nano .env or vim .env
```

Required variables:
```bash
# RTC
AGORA_APP_ID=your_agora_app_id
AGORA_APP_CERTIFICATE=your_agora_certificate

# LLM
OPENAI_API_KEY=your_openai_key
# Or use other LLM (Qwen, Gemini, etc.)

# STT
DEEPGRAM_API_KEY=your_deepgram_key

# TTS
ELEVENLABS_API_KEY=your_elevenlabs_key
```

💡 **Tip**: If you don't have API keys yet, see [FREE_TRIAL_GUIDE.md](./agents/examples/voice-assistant/FREE_TRIAL_GUIDE.md)

### Step 4: Start Docker Container

```bash
# Start container (background)
docker compose up -d

# Check container status
docker ps
```

You should see output like:
```
CONTAINER ID   IMAGE           COMMAND      STATUS         PORTS          NAMES
abc123def456   ten_agent_dev   "/bin/bash"  Up 10 seconds  0.0.0.0:8080   ten_agent_dev
```

### Step 5: Run Project in Container

```bash
# Enter container
docker exec -it ten_agent_dev bash

# Navigate to voice-assistant directory
cd agents/examples/voice-assistant

# Install dependencies (Task and tman are available in container)
task install

# Run project
task run
```

### Step 6: Access Application

Open your browser and visit:
- **Web UI**: http://localhost:3000
- **API Server**: http://localhost:8080
- **TMAN Designer**: http://localhost:49483

## ❓ FAQ

### 1. Do I really not need to install Task locally?

**Absolutely correct!** ✅

The Docker container has pre-installed:
- Task: `/usr/local/bin/task`
- tman: `/usr/local/bin/tman`
- Python 3.10: `/usr/bin/python3.10`
- Go 1.20+: `/usr/local/go`
- Node.js: `/usr/bin/node`

You only need to:
1. Install Docker
2. Start container: `docker compose up -d`
3. Enter container: `docker exec -it ten_agent_dev bash`
4. Run commands: `task install`, `task run`

### 2. Do I need WSL on Windows?

**No!** ✅

With Docker Desktop, Windows users don't need WSL. Docker Desktop handles all the underlying details automatically.

### 3. Where is my code? How do I edit it?

Code is on your **local machine**, mapped to container via Docker volumes:

```yaml
# docker-compose.yaml
volumes:
  - ./:/app  # Local directory mapped to /app in container
```

You can:
- ✅ Edit code locally with any editor (VSCode, Sublime, etc.)
- ✅ Changes are reflected in container in real-time
- ✅ No need to restart container

Recommended workflow:
1. Edit code in VSCode locally
2. Run `task run` in container
3. View results in browser
4. Save code, container auto-reloads

### 4. Will data be lost after container restart?

**No!** ✅

The following data is saved locally:
- Code files (via volume mapping)
- `.env` configuration (local)
- `property.json` (local)
- Log files (via volume mapping)

Container only provides runtime environment; all important data is local.

### 5. How to stop and restart container?

```bash
# Stop container (keep all data)
docker compose down

# Restart container
docker compose up -d

# Check container status
docker ps

# View container logs
docker logs ten_agent_dev

# Follow logs in real-time
docker logs -f ten_agent_dev
```

### 6. How much disk space does it use?

- Docker image: ~1.5 GB
- Running container: ~500 MB
- Python package cache: ~500 MB
- **Total**: ~2-3 GB

Slightly larger than local installation, but you get:
- Zero configuration hassle
- Complete environment isolation
- One-click deployment

### 7. What's the performance like?

Docker container performance is close to native:
- **CPU**: 90-95% of native
- **Memory**: 95-98% of native
- **Disk I/O**: 85-90% of native

Perfect for development and testing.

### 8. Can I run multiple projects simultaneously?

Yes, but you need to change ports to avoid conflicts:

```yaml
# docker-compose.yaml
ports:
  - "8081:8080"   # API Server (changed to 8081)
  - "3001:3000"   # Web UI (changed to 3001)
  - "49484:49483" # TMAN Designer (changed to 49484)
```

### 9. How to update code?

```bash
# Pull latest code locally
git pull

# Restart container to apply changes
docker compose restart

# If dependencies changed, rebuild image
docker compose down
docker compose build --no-cache
docker compose up -d
```

### 10. What if I encounter problems?

#### Solution 1: Restart container (solves 90% of issues)

```bash
docker compose down
docker compose up -d
```

#### Solution 2: Check logs

```bash
# View container logs
docker logs ten_agent_dev

# Follow logs in real-time
docker logs -f ten_agent_dev
```

#### Solution 3: Rebuild container

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

#### Solution 4: Debug inside container

```bash
# Enter container
docker exec -it ten_agent_dev bash

# Check if tools are available
task --version
tman --version
python3 --version
go version
node --version
```

## 🛠️ Docker Command Reference

### Basic Commands

```bash
# Start container (background)
docker compose up -d

# Start container (foreground, see logs)
docker compose up

# Stop container
docker compose down

# Restart container
docker compose restart

# Check container status
docker ps

# Check all containers (including stopped)
docker ps -a
```

### Enter Container

```bash
# Enter container bash
docker exec -it ten_agent_dev bash

# Execute single command in container
docker exec ten_agent_dev task --version

# Enter container as root
docker exec -it -u root ten_agent_dev bash
```

### View Logs

```bash
# View container logs
docker logs ten_agent_dev

# Follow logs in real-time
docker logs -f ten_agent_dev

# View last 100 lines
docker logs --tail 100 ten_agent_dev
```

### Image Management

```bash
# List local images
docker images

# Rebuild image
docker compose build --no-cache

# Remove old images
docker image prune

# Inspect image
docker inspect ten_agent_dev
```

### Cleanup

```bash
# Stop and remove container
docker compose down

# Remove container and volumes
docker compose down -v

# Clean unused resources
docker system prune

# Clean all unused resources (including images)
docker system prune -a
```

## 🔧 Troubleshooting

### Issue 1: Container fails to start

**Symptom**:
```bash
docker compose up -d
Error response from daemon: driver failed programming external connectivity
```

**Solution**:
1. Check if ports are in use:
   ```bash
   # Windows
   netstat -ano | findstr :8080
   
   # Linux/macOS
   lsof -i :8080
   ```

2. Change ports or stop conflicting programs

### Issue 2: Container runs but can't access

**Symptom**: Browser can't access http://localhost:3000

**Solution**:
1. Check if container is really running:
   ```bash
   docker ps
   ```

2. Check if service started in container:
   ```bash
   docker exec -it ten_agent_dev bash
   ps aux | grep node
   ```

3. View container logs:
   ```bash
   docker logs ten_agent_dev
   ```

### Issue 3: Code changes don't take effect

**Symptom**: Modified code doesn't update in container

**Solution**:
1. Check volume mapping:
   ```bash
   docker inspect ten_agent_dev | grep -A 10 Mounts
   ```

2. Restart container:
   ```bash
   docker compose restart
   ```

### Issue 4: Permission issues

**Symptom**:
```bash
permission denied while trying to connect to the Docker daemon socket
```

**Solution** (Linux):
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Re-login or run
newgrp docker
```

### Issue 5: Disk space insufficient

**Symptom**:
```bash
no space left on device
```

**Solution**:
```bash
# Clean unused resources
docker system prune -a

# Check disk usage
docker system df
```

## 📚 Related Documentation

- [INSTALLATION_TROUBLESHOOTING.md](./INSTALLATION_TROUBLESHOOTING.md) - Installation troubleshooting
- [README_SECURITY.md](./README_SECURITY.md) - API keys security guide
- [FREE_TRIAL_GUIDE.md](./agents/examples/voice-assistant/FREE_TRIAL_GUIDE.md) - Free trial guide
- [VOICE_INTEGRATION_GUIDE.md](./agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.md) - Integration guide

## 🎉 Summary

**With Docker approach, your understanding is completely correct!**

> - ✅ Only Docker needed locally
> - ✅ Task doesn't need local installation (in container)
> - ✅ tman doesn't need local installation (in container)
> - ✅ Python, Go, Node.js not needed locally
> - ✅ All dev tools pre-installed in container
> - ✅ One command `docker compose up -d` to start
> - ✅ All commands work directly after entering container

**5 steps to start:**
1. Install Docker
2. Configure `.env`
3. `docker compose up -d`
4. `docker exec -it ten_agent_dev bash`
5. `task install && task run`

Happy coding! 🚀
