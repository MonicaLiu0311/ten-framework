# Installation Troubleshooting Guide

## Issue: `task install` Task Does Not Exist

### Symptoms
```powershell
PS D:\code\ten-framework\ai_agents> task install
task: Task "install" does not exist
```

### Cause
There is no `install` task in the `ai_agents` directory. The `install` task only exists in specific example project directories.

### Solution
Navigate to a specific example directory before running the install command:

```powershell
cd agents/examples/voice-assistant
task install
```

---

## Issue: `tman: executable file not found in $PATH`

### Symptoms
```powershell
PS D:\code\ten-framework\ai_agents\agents\examples\voice-assistant> task install
task: [install-tenapp] tman install
"tman": executable file not found in $PATH
task: Failed to run task "install": task: Failed to run task "install-tenapp": exit status 127
```

### Cause
`tman` (TEN Manager) is the package manager for TEN Framework and must be installed first. It is a **required tool** for running TEN applications.

### Solution

#### Windows Users

**Method 1: Use WSL (Recommended)**

TEN Framework primarily supports Linux and macOS. Windows users should use WSL (Windows Subsystem for Linux):

1. **Install WSL**
   ```powershell
   # Run PowerShell as Administrator
   wsl --install
   # Restart your computer
   ```

2. **Enter WSL Environment**
   ```powershell
   wsl
   ```

3. **Install tman in WSL**
   ```bash
   # Ubuntu/Debian
   sudo add-apt-repository ppa:ten-framework/ten-framework
   sudo apt update
   sudo apt install tman
   
   # Or use installation script
   bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)
   ```

4. **Continue Development in WSL**
   ```bash
   cd /mnt/d/code/ten-framework/ai_agents/agents/examples/voice-assistant
   task install
   ```

**Method 2: Docker (Alternative)**

Run TEN Framework in a Docker container:

```powershell
# Navigate to project directory
cd D:\code\ten-framework\ai_agents

# Use Docker Compose
docker compose up -d

# Enter container
docker exec -it ten_agent_dev bash

# Install and run inside container
cd agents/examples/voice-assistant
task install
task run
```

#### Linux/macOS Users

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

**Universal Method (Installation Script):**

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)
```

Or, if you've already cloned the repository:

```bash
cd ten-framework
bash tools/tman/install_tman.sh
```

#### Verify Installation

```bash
tman --version
# Should display tman version information
```

---

## Complete Installation Steps (From Scratch)

### Prerequisites Check

Before starting, ensure the following software is installed:

1. **Python 3.10**
   ```bash
   python3 --version
   # Should display: Python 3.10.x
   ```
   
   If you don't have Python 3.10, use pyenv to install it:
   ```bash
   # Install pyenv
   curl https://pyenv.run | bash
   
   # Install Python 3.10
   pyenv install 3.10.14
   pyenv local 3.10.14
   ```

2. **Go 1.20+**
   ```bash
   go version
   # Should display: go version go1.20 or higher
   ```

3. **Node.js / npm**
   ```bash
   node --version
   npm --version
   ```

4. **Task** (Task runner)
   ```bash
   # Ubuntu/Debian
   sudo apt install task
   
   # macOS
   brew install go-task
   
   # Other systems: https://taskfile.dev/installation/
   ```

### Install TEN Framework

**Step 1: Install tman**

Refer to the "Solution" section above and install tman according to your operating system.

**Step 2: Clone Repository (if not already done)**

```bash
git clone https://github.com/TEN-framework/ten-framework.git
cd ten-framework
```

**Step 3: Configure Environment Variables**

```bash
cd ai_agents
cp .env.example .env
# Edit .env file and fill in your API keys
```

**Step 4: Navigate to Example Directory**

```bash
cd agents/examples/voice-assistant
```

**Step 5: Install Dependencies**

```bash
task install
```

This command will:
- Install TEN app dependencies (`tman install`)
- Install Python dependencies
- Install frontend dependencies
- Build API server

**Step 6: Run Application**

```bash
task run
```

**Step 7: Access Application**

- Frontend: http://localhost:3000
- API Server: http://localhost:8080
- TMAN Designer: http://localhost:49483

---

## FAQ

### Q: Why can't I run directly on Windows?

A: TEN Framework currently primarily supports Linux and macOS. Windows users need to use WSL or Docker. This is because TEN Framework depends on some Unix-specific features.

### Q: I've installed tman, but it still says it's not found?

A: Check the following:

1. **Verify tman is in PATH**
   ```bash
   which tman
   # Should display tman's path
   ```

2. **Reload shell configuration**
   ```bash
   # Bash
   source ~/.bashrc
   
   # Zsh
   source ~/.zshrc
   ```

3. **Check tman version**
   ```bash
   tman --version
   ```

### Q: What if I encounter permission errors during installation?

A: Some operations may require administrator privileges:

```bash
# Linux/macOS - use sudo
sudo apt install tman

# Or install to user directory (no sudo needed)
bash tools/tman/install_tman.sh
```

### Q: What if my Python version is wrong?

A: TEN Framework requires Python 3.10. Use pyenv to manage Python versions:

```bash
# Install pyenv
curl https://pyenv.run | bash

# Install Python 3.10
pyenv install 3.10.14
pyenv local 3.10.14

# Verify
python --version
```

### Q: Issues when running in Docker?

A: Ensure Docker service is running:

```bash
# Check Docker status
docker ps

# Start Docker Compose
cd ai_agents
docker compose up -d

# View logs
docker compose logs -f
```

### Q: task command not found?

A: You need to install Task runner first:

**Ubuntu/Debian:**
```bash
sudo apt install task
```

**macOS:**
```bash
brew install go-task
```

**Other systems:**
See https://taskfile.dev/installation/

### Q: Installation hangs or times out?

A: This might be a network issue. Try:

1. **Use a proxy**
   ```bash
   export HTTP_PROXY=http://your-proxy:port
   export HTTPS_PROXY=http://your-proxy:port
   ```

2. **Increase timeout**
   ```bash
   export TIMEOUT=300
   ```

3. **Use mirrors (for Chinese users)**
   ```bash
   # Python pip mirror
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   
   # npm mirror
   npm config set registry https://registry.npmmirror.com
   ```

---

## Diagnostic Script

Run this script to check your environment:

```bash
#!/bin/bash

echo "===== TEN Framework Environment Diagnostic ====="
echo ""

# Check Python
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
    if [[ $PYTHON_VERSION == *"3.10"* ]]; then
        echo "✅ Python version is correct"
    else
        echo "⚠️  Python version is not 3.10, recommend using Python 3.10"
    fi
else
    echo "❌ Python not installed"
fi
echo ""

# Check Go
echo "Checking Go..."
if command -v go &> /dev/null; then
    echo "✅ $(go version)"
else
    echo "❌ Go not installed"
fi
echo ""

# Check Node.js
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    echo "✅ Node $(node --version)"
else
    echo "❌ Node.js not installed"
fi
echo ""

# Check npm
echo "Checking npm..."
if command -v npm &> /dev/null; then
    echo "✅ npm $(npm --version)"
else
    echo "❌ npm not installed"
fi
echo ""

# Check Task
echo "Checking Task..."
if command -v task &> /dev/null; then
    echo "✅ $(task --version)"
else
    echo "❌ Task not installed"
fi
echo ""

# Check tman
echo "Checking tman..."
if command -v tman &> /dev/null; then
    echo "✅ $(tman --version)"
else
    echo "❌ tman not installed"
    echo "   Please run the following command to install:"
    echo "   bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)"
fi
echo ""

# Check OS
echo "Operating System Info:"
uname -a
echo ""

echo "===== Diagnostic Complete ====="
```

Save as `check_env.sh`, then run:

```bash
bash check_env.sh
```

---

## Get Help

If none of the above solutions work:

1. **View Detailed Documentation**
   - [Quick Start Guide](../../docs/getting-started/quick-start.md)
   - [Voice Assistant README](README.md)

2. **Search Known Issues**
   - [GitHub Issues](https://github.com/TEN-framework/ten-framework/issues)

3. **Ask Questions**
   - [Discord Community](https://discord.gg/VnPftUzAMJ)
   - [GitHub Discussions](https://github.com/TEN-framework/ten-framework/discussions)

4. **Create an Issue**
   Include the following information:
   - Operating system and version
   - Python/Go/Node.js versions
   - Complete error messages
   - Output of running `check_env.sh`

---

## Related Documentation

- [README.md](README.md) - Voice Assistant Documentation
- [Quick Start Guide](../../docs/getting-started/quick-start.md) - TEN Framework Quick Start
- [Configuration Modification Guide](CONFIG_MODIFICATION_GUIDE.zh-CN.md) - How to Modify Configuration
- [API Keys Security Guide](../../API_KEYS_SECURITY_GUIDE.zh-CN.md) - API Key Management
