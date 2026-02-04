# API 密钥安全最佳实践

[English](API_KEYS_SECURITY_GUIDE.md) | 简体中文

## 目录

- [为什么 API 密钥安全很重要](#为什么-api-密钥安全很重要)
- [安全存储 API 密钥](#安全存储-api-密钥)
- [开发环境配置](#开发环境配置)
- [生产环境配置](#生产环境配置)
- [团队协作](#团队协作)
- [安全检查](#安全检查)
- [应急响应](#应急响应)

## 为什么 API 密钥安全很重要

API 密钥就像是您家的钥匙。如果泄露：

- 💰 **财务损失**：他人可能使用您的账户，产生费用
- 🔒 **数据泄露**：可能访问您的私有数据
- 🚫 **服务中断**：滥用可能导致账户被封禁
- ⚖️ **法律责任**：未经授权的使用可能导致法律问题

### 真实案例

- GitHub 上每天有数千个密钥被意外提交
- 一个泄露的 AWS 密钥可能在几小时内产生数万美元的账单
- 自动扫描机器人会在几分钟内发现并利用泄露的密钥

## 安全存储 API 密钥

### ❌ 永远不要做

```bash
# 错误：硬编码在代码中
openai_api_key = "sk-abc123def456..."

# 错误：提交到 git
git add .env
git commit -m "Add config"

# 错误：写在代码注释中
# My OpenAI key: sk-abc123def456...

# 错误：存储在公共位置
echo "OPENAI_API_KEY=sk-123" > /tmp/keys.txt
```

### ✅ 应该做

#### 1. 使用环境变量

```bash
# 在 shell 配置文件中（~/.bashrc, ~/.zshrc）
export OPENAI_API_KEY="your-key-here"

# 或在应用启动时
OPENAI_API_KEY="your-key" python app.py
```

#### 2. 使用 .env 文件（仅限本地开发）

**步骤**：

1. 创建 `.env.example` 作为模板：
   ```bash
   # .env.example
   AGORA_APP_ID=
   OPENAI_API_KEY=
   DEEPGRAM_API_KEY=
   ```

2. 将 `.env` 添加到 `.gitignore`：
   ```gitignore
   # .gitignore
   .env
   .env.local
   .env.*.local
   ```

3. 复制并填写您的密钥：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入真实密钥
   ```

4. 在代码中使用：
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   api_key = os.getenv('OPENAI_API_KEY')
   ```

#### 3. 使用密钥管理服务

**推荐的服务**：

| 服务 | 适用场景 | 价格 |
|------|---------|------|
| AWS Secrets Manager | AWS 云服务 | 按使用量计费 |
| Azure Key Vault | Azure 云服务 | 有免费额度 |
| Google Secret Manager | GCP 云服务 | 有免费额度 |
| HashiCorp Vault | 自托管/混合云 | 开源（企业版付费） |
| Doppler | 跨平台 | 有免费计划 |
| 1Password/LastPass | 团队协作 | 按用户订阅 |

**AWS Secrets Manager 示例**：

```python
import boto3
import json

def get_secret(secret_name, region_name="us-east-1"):
    """从 AWS Secrets Manager 获取密钥"""
    client = boto3.client('secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise

# 使用
secrets = get_secret('ten-framework/prod/api-keys')
openai_key = secrets['OPENAI_API_KEY']
```

**Azure Key Vault 示例**：

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret(vault_url, secret_name):
    """从 Azure Key Vault 获取密钥"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    secret = client.get_secret(secret_name)
    return secret.value

# 使用
vault_url = "https://myvault.vault.azure.net/"
openai_key = get_secret(vault_url, "openai-api-key")
```

## 开发环境配置

### 本地开发设置

1. **初始设置**：
   ```bash
   cd ten-framework/ai_agents
   cp .env.example .env
   ```

2. **编辑 .env 文件**：
   ```bash
   # 使用文本编辑器
   nano .env
   # 或
   code .env
   ```

3. **填入您的密钥**：
   ```bash
   AGORA_APP_ID=your_actual_app_id
   OPENAI_API_KEY=sk-your_actual_key
   ```

4. **验证**：
   ```bash
   # 检查 .env 是否在 .gitignore 中
   git check-ignore .env
   # 应该输出: .env
   
   # 确认 .env 未被追踪
   git status | grep .env
   # 不应该看到 .env 文件
   ```

### VS Code 配置

在 `.vscode/settings.json` 中隐藏敏感文件：

```json
{
  "files.exclude": {
    "**/.env": true
  },
  "search.exclude": {
    "**/.env": true
  }
}
```

### 脱敏日志输出

```python
import re
import logging

class SensitiveDataFilter(logging.Filter):
    """过滤日志中的敏感数据"""
    
    PATTERNS = [
        (r'sk-[a-zA-Z0-9]{32,}', 'sk-***REDACTED***'),  # OpenAI keys
        (r'Bearer [a-zA-Z0-9_\-\.]+', 'Bearer ***REDACTED***'),  # Bearer tokens
        (r'"api_key"\s*:\s*"[^"]+', '"api_key": "***REDACTED***'),  # API keys in JSON
    ]
    
    def filter(self, record):
        message = record.getMessage()
        for pattern, replacement in self.PATTERNS:
            message = re.sub(pattern, replacement, message)
        record.msg = message
        return True

# 使用
logger = logging.getLogger(__name__)
logger.addFilter(SensitiveDataFilter())
```

## 生产环境配置

### Docker 容器

**不推荐**（密钥硬编码）：
```dockerfile
# ❌ 错误示例
ENV OPENAI_API_KEY=sk-abc123
```

**推荐**（运行时注入）：
```dockerfile
# ✅ 正确示例
# Dockerfile 中不设置密钥
```

```bash
# 运行时传入
docker run -e OPENAI_API_KEY="$OPENAI_API_KEY" myapp

# 或使用 .env 文件（不提交到 git）
docker run --env-file .env myapp
```

### Kubernetes

使用 Secrets：

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: api-keys
type: Opaque
stringData:
  openai-api-key: "sk-your-key"
  agora-app-id: "your-app-id"
```

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ten-agent
spec:
  template:
    spec:
      containers:
      - name: agent
        image: ten-agent:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-api-key
        - name: AGORA_APP_ID
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: agora-app-id
```

### CI/CD 环境

**GitHub Actions**：

```yaml
# .github/workflows/test.yml
name: Test
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run tests
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          AGORA_APP_ID: ${{ secrets.AGORA_APP_ID }}
        run: |
          npm test
```

在 GitHub 仓库设置中添加 secrets：
1. Settings → Secrets and variables → Actions
2. New repository secret
3. 添加密钥名称和值

## 团队协作

### 分享配置的正确方式

#### 方法 1：文档说明

在 README.md 中：

```markdown
## 环境配置

1. 复制环境变量模板：
   \`\`\`bash
   cp .env.example .env
   \`\`\`

2. 填写以下 API 密钥：

   | 变量名 | 获取方式 | 必需 |
   |--------|---------|------|
   | AGORA_APP_ID | [Agora Console](https://console.agora.io/) | 是 |
   | OPENAI_API_KEY | [OpenAI Platform](https://platform.openai.com/) | 是 |
   | DEEPGRAM_API_KEY | [Deepgram Console](https://console.deepgram.com/) | 是 |

3. 启动应用：
   \`\`\`bash
   npm start
   \`\`\`
```

#### 方法 2：使用密钥管理平台

**1Password Secrets Automation**：

```bash
# 安装 1Password CLI
brew install 1password-cli

# 在 1Password 中存储密钥
op create item --category=password \
  --title="TEN Framework Keys" \
  --vault="Development" \
  OPENAI_API_KEY=sk-abc123

# 团队成员获取密钥
op read "op://Development/TEN Framework Keys/OPENAI_API_KEY"
```

**集成到脚本**：

```bash
#!/bin/bash
# start.sh

# 从 1Password 加载密钥
export OPENAI_API_KEY=$(op read "op://Development/TEN Framework Keys/OPENAI_API_KEY")
export AGORA_APP_ID=$(op read "op://Development/TEN Framework Keys/AGORA_APP_ID")

# 启动应用
npm start
```

#### 方法 3：环境隔离

为不同环境使用不同的密钥：

```bash
# .env.development（本地开发）
OPENAI_API_KEY=sk-dev-key-xxx
AGORA_APP_ID=dev-app-id

# .env.staging（测试环境）
OPENAI_API_KEY=sk-staging-key-xxx
AGORA_APP_ID=staging-app-id

# .env.production（生产环境）
# 这个文件永远不要提交！
```

## 安全检查

### 自动化检查工具

#### 1. git-secrets

防止提交密钥到 git：

```bash
# 安装
brew install git-secrets

# 在项目中设置
cd ten-framework
git secrets --install
git secrets --register-aws

# 添加自定义模式
git secrets --add 'sk-[a-zA-Z0-9]{32,}'  # OpenAI keys
git secrets --add '[A-Za-z0-9]{32}'      # Agora keys
```

#### 2. pre-commit hooks

`.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
  
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

安装和使用：

```bash
# 安装 pre-commit
pip install pre-commit

# 安装 hooks
pre-commit install

# 运行检查
pre-commit run --all-files
```

#### 3. Gitleaks

扫描 git 历史：

```bash
# 安装
brew install gitleaks

# 扫描当前代码
gitleaks detect --source . --verbose

# 扫描 git 历史
gitleaks detect --source . --log-opts="--all"
```

### 手动检查清单

提交前检查：

```bash
# 1. 检查暂存的文件
git diff --cached

# 2. 搜索潜在的密钥模式
git diff --cached | grep -E "(api[_-]?key|secret|token|password)"

# 3. 确认 .env 未被追踪
git status | grep -E "\.env$"

# 4. 检查将要提交的文件
git ls-files --cached | grep -E "\.env$"
```

### 代码审查检查点

在 code review 时注意：

- [ ] 没有硬编码的 API 密钥
- [ ] 环境变量使用正确
- [ ] 日志输出已脱敏
- [ ] 错误信息不包含敏感数据
- [ ] 测试代码使用 mock 数据
- [ ] 文档中没有真实密钥

## 应急响应

### 如果密钥已泄露

**立即行动清单**：

1. **停止恐慌，快速行动** ⏱️
   - 保持冷静
   - 按照清单逐项操作

2. **撤销密钥** 🔐
   ```bash
   # 记录泄露的密钥（不要写全）
   echo "Compromised key: sk-abc...xyz" >> security-incident.log
   echo "Date: $(date)" >> security-incident.log
   ```
   
   - 立即登录服务商控制台
   - 删除或禁用泄露的密钥
   - 生成新的密钥
   - 更新所有使用该密钥的地方

3. **检查使用情况** 📊
   - 查看 API 调用日志
   - 检查异常活动
   - 审查账单/费用
   - 记录可疑的使用模式

4. **从 Git 历史中移除** 🗑️
   
   **警告**：这会重写 Git 历史！
   
   ```bash
   # 使用 BFG Repo-Cleaner（推荐）
   brew install bfg
   
   # 创建备份
   git clone --mirror <repo-url> repo-backup
   
   # 清理密钥
   bfg --replace-text passwords.txt <repo-url>
   
   cd repo.git
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```
   
   或使用 git-filter-repo：
   
   ```bash
   # 安装
   pip install git-filter-repo
   
   # 移除包含密钥的文件
   git filter-repo --path .env --invert-paths
   
   # 强制推送
   git push origin --force --all
   ```

5. **通知团队** 📢
   - 告知所有团队成员
   - 说明情况和需要采取的行动
   - 更新团队文档

6. **审查安全措施** 🛡️
   - 检查其他可能泄露的地方
   - 更新 .gitignore
   - 安装密钥检测工具
   - 培训团队成员

7. **记录事件** 📝
   ```markdown
   # security-incident-2024-02-04.md
   
   ## 安全事件报告
   
   **日期**: 2024-02-04
   **发现者**: [姓名]
   **严重程度**: 高
   
   ### 事件描述
   - OpenAI API 密钥在 issue #123 中被意外公开
   
   ### 影响范围
   - 泄露时间：约 2 小时
   - 潜在访问者：公开仓库的任何人
   
   ### 采取的行动
   - [x] 撤销泄露的密钥
   - [x] 生成新密钥
   - [x] 检查使用情况（无异常）
   - [x] 从 Git 历史移除
   - [x] 通知团队
   
   ### 预防措施
   - [x] 安装 git-secrets
   - [x] 添加 pre-commit hooks
   - [x] 团队安全培训
   
   ### 经验教训
   - 需要在提交前双重检查
   - 应该使用密钥管理服务
   ```

### 服务商联系方式

如果发现未授权使用，联系服务商：

| 服务商 | 支持链接 | 应急联系 |
|--------|---------|---------|
| Agora | https://www.agora.io/en/support/ | support@agora.io |
| OpenAI | https://help.openai.com/ | - |
| Deepgram | https://deepgram.com/support | support@deepgram.com |
| Azure | https://azure.microsoft.com/support/ | - |
| AWS | https://aws.amazon.com/support/ | - |

## 其他资源

### 学习资源

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [The Twelve-Factor App: Config](https://12factor.net/config)
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

### 工具推荐

- **密钥检测**: Gitleaks, TruffleHog, detect-secrets
- **密钥管理**: 1Password, LastPass, HashiCorp Vault
- **CI/CD 集成**: GitHub Secrets, GitLab CI/CD Variables
- **监控**: Datadog, New Relic, Sentry

### 最佳实践总结

1. **永远不要硬编码密钥**
2. **使用 .env 文件（本地）+ .gitignore**
3. **使用密钥管理服务（生产）**
4. **定期轮换密钥**
5. **启用密钥检测工具**
6. **培训团队成员**
7. **建立应急响应流程**

---

**记住**：安全不是一次性的任务，而是持续的实践。

**问题？** 如有疑问，请查阅上述文档或联系您的安全团队。

---

**最后更新**：2026-02-04  
**文档版本**：1.0
