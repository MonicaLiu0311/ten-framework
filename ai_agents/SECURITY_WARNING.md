# ⚠️ SECURITY WARNING - API 密钥安全警告

## 🚨 重要安全通知

**您在问题描述中分享的 `.env` 文件包含真实的 API 密钥！**

### 发现的问题

以下密钥已暴露，需要立即采取行动：

1. **Agora Credentials**
   ```
   AGORA_APP_ID="7c0df0b964f942b995421df2f987c5ff"
   AGORA_APP_CERTIFICATE="eba4f5a450734aecbb007b001f567dbd"
   ```

2. **Qwen API Key**
   ```
   QWEN_API_KEY="sk-5dac8785e11111111111139a869"
   ```

3. **DeepSeek API Key**
   ```
   DEEPSEEK_API_KEY="sk-e15da98ff1111111111118a3d7404"
   ```

### 🔴 立即采取的行动

#### 1. 撤销所有暴露的密钥

**Agora (声网)**:
- 登录 [Agora Console](https://console.agora.io/)
- 进入项目设置
- 生成新的 App ID 和 App Certificate
- 删除或禁用旧的凭证

**Qwen (通义千问)**:
- 登录 [阿里云 DashScope](https://dashscope.aliyun.com/)
- 进入 API 密钥管理
- 删除暴露的密钥
- 生成新的 API 密钥

**DeepSeek**:
- 登录 [DeepSeek Platform](https://platform.deepseek.com/)
- 进入 API Keys 设置
- 删除暴露的密钥
- 生成新的 API 密钥

#### 2. 检查账单和使用情况

立即检查这些服务的使用情况和账单，确认是否有未授权的使用：
- Agora: 检查通话时长和流量
- Qwen: 检查 token 使用量
- DeepSeek: 检查 API 调用次数

如果发现异常使用，请联系服务商支持团队。

#### 3. 更新本地配置

在本地创建正确的 `.env` 文件：

```bash
cd /home/runner/work/ten-framework/ten-framework/ai_agents
cp .env.example .env
# 然后编辑 .env 文件，填入新的密钥
```

### ✅ 正确的做法

#### 1. .env 文件安全规则

**永远不要**：
- ❌ 将 `.env` 文件提交到 git
- ❌ 在 issue、PR、讨论中分享 `.env` 内容
- ❌ 将 API 密钥写在代码注释中
- ❌ 使用真实密钥作为示例
- ❌ 截图包含 API 密钥的界面
- ❌ 在日志中输出 API 密钥

**应该做**：
- ✅ 使用 `.env.example` 文件作为模板（只包含空值或占位符）
- ✅ 确保 `.env` 在 `.gitignore` 中
- ✅ 使用环境变量管理密钥
- ✅ 定期轮换 API 密钥
- ✅ 为不同环境使用不同的密钥（开发/测试/生产）
- ✅ 使用密钥管理服务（如 AWS Secrets Manager, Azure Key Vault）

#### 2. 检查 .gitignore

确认 `.gitignore` 包含以下内容：

```gitignore
# Environment variables
.env
.env.local
.env.*.local
*.env

# Except example files
!.env.example
```

#### 3. 检查 git 历史

如果您曾经提交过包含密钥的文件，需要从 git 历史中移除：

```bash
# 警告：这会重写 git 历史！
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch ai_agents/.env" \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送（需谨慎）
git push origin --force --all
git push origin --force --tags
```

### 🔐 最佳实践

#### 1. 使用环境变量

在生产环境，使用系统环境变量而不是 `.env` 文件：

```bash
# 在服务器上设置环境变量
export AGORA_APP_ID="your_app_id"
export OPENAI_API_KEY="your_openai_key"
```

#### 2. 使用密钥管理服务

**云服务商密钥管理**：
- AWS: AWS Secrets Manager
- Azure: Azure Key Vault
- Google Cloud: Secret Manager
- 阿里云: 密钥管理服务 KMS

**示例（AWS Secrets Manager）**：
```python
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# 使用
secrets = get_secret('ten-framework/api-keys')
agora_app_id = secrets['AGORA_APP_ID']
```

#### 3. 限制 API 密钥权限

- 为每个环境创建独立的 API 密钥
- 启用 IP 白名单限制
- 设置使用配额和限流
- 定期审计密钥使用情况

#### 4. 开发团队协作

**分享配置的正确方式**：

1. **使用 .env.example**：
   ```bash
   # .env.example
   AGORA_APP_ID=your_agora_app_id_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

2. **使用密钥管理平台**：
   - 1Password for Teams
   - LastPass Enterprise
   - HashiCorp Vault

3. **文档说明**：
   在 README 中说明如何获取和配置密钥，但不包含实际的密钥值。

### 📚 相关文档

- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP: API Security](https://owasp.org/www-project-api-security/)
- [12-Factor App: Config](https://12factor.net/config)

### 🔍 安全检查清单

在提交代码前，确认：

- [ ] `.env` 文件已在 `.gitignore` 中
- [ ] 所有 API 密钥使用环境变量
- [ ] `.env.example` 只包含占位符
- [ ] 代码中没有硬编码的密钥
- [ ] 日志输出已脱敏处理
- [ ] 已审查所有即将提交的文件
- [ ] 没有在 commit message 中包含敏感信息

### 🆘 需要帮助？

如果您不确定密钥是否已泄露或如何处理，请：

1. 立即撤销所有密钥（宁可过度反应，不可掉以轻心）
2. 联系您的安全团队或服务提供商
3. 查看服务商的安全事件响应指南

---

**记住**：一旦 API 密钥暴露在公开的地方（即使只是几秒钟），就应该被视为已泄露，必须立即撤销。

**这不是您的错**：很多开发者都犯过类似的错误。重要的是学习并采取预防措施。

---

**此文档创建于**：2026-02-04  
**文档版本**：1.0  
**最后更新**：2026-02-04
