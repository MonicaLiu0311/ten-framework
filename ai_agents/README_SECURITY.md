# API 密钥安全文档

本目录包含有关 API 密钥安全的重要文档和工具。

## 📚 文档

### [SECURITY_WARNING.md](SECURITY_WARNING.md)
**紧急安全警告** - 如果您不小心泄露了 API 密钥，请立即阅读此文档。

包含：
- 发现的安全问题
- 立即采取的行动
- 撤销密钥的步骤
- 检查账单和使用情况

### [API_KEYS_SECURITY_GUIDE.zh-CN.md](API_KEYS_SECURITY_GUIDE.zh-CN.md)
**完整的 API 密钥安全最佳实践指南**

包含：
- 为什么 API 密钥安全很重要
- 如何安全存储 API 密钥
- 开发环境和生产环境配置
- 团队协作最佳实践
- 安全检查工具
- 应急响应流程

## 🛠️ 工具

### scripts/check-api-keys.sh
**Git pre-commit hook** - 在提交前检查是否有 API 密钥

使用方法：
```bash
# 手动运行
cd ai_agents
./scripts/check-api-keys.sh

# 设置为 git hook（推荐）
ln -sf ../../ai_agents/scripts/check-api-keys.sh .git/hooks/pre-commit
```

### scripts/scan-api-keys.py
**项目扫描器** - 扫描整个项目查找可能的 API 密钥

使用方法：
```bash
# 扫描当前目录
python3 ai_agents/scripts/scan-api-keys.py

# 扫描指定目录
python3 ai_agents/scripts/scan-api-keys.py /path/to/project
```

## ⚠️ 重要提醒

### 如果您看到此消息...

您可能在问题、PR 或讨论中分享了包含 API 密钥的 `.env` 文件内容。

**立即行动**：
1. 撤销所有暴露的 API 密钥
2. 生成新的密钥
3. 检查账单和使用情况
4. 阅读 [SECURITY_WARNING.md](SECURITY_WARNING.md) 了解详细步骤

### 正确的做法

✅ **应该分享**：
- `.env.example` 文件（只包含空值或占位符）
- 配置说明和文档
- 如何获取 API 密钥的指引

❌ **不应该分享**：
- `.env` 文件（包含真实密钥）
- 任何包含实际 API 密钥的内容
- 截图中显示的 API 密钥

## 🔐 快速检查清单

在分享任何内容之前，确认：

- [ ] 没有包含 `.env` 文件内容
- [ ] 所有 API 密钥已被移除或替换为占位符
- [ ] 截图中没有显示敏感信息
- [ ] 日志输出已脱敏
- [ ] 代码示例使用环境变量而非硬编码密钥

## 📖 相关资源

### 官方文档
- [GitHub: Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [OWASP: API Security](https://owasp.org/www-project-api-security/)
- [12-Factor App: Config](https://12factor.net/config)

### 服务商安全指南
- [Agora Security](https://docs.agora.io/en/video-calling/develop/authentication-workflow)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)

## 🆘 需要帮助？

如果您不确定如何处理 API 密钥泄露问题：

1. **不要恐慌** - 这是常见的错误，有标准的处理流程
2. **立即撤销密钥** - 宁可过度反应，不可掉以轻心
3. **阅读文档** - [SECURITY_WARNING.md](SECURITY_WARNING.md) 和 [API_KEYS_SECURITY_GUIDE.zh-CN.md](API_KEYS_SECURITY_GUIDE.zh-CN.md)
4. **联系团队** - 如果您在组织中工作，通知您的安全团队
5. **联系服务商** - 如果发现未授权使用，联系服务商支持

---

**记住**：API 密钥安全是每个开发者的责任。预防总是比事后补救更好。

**最后更新**：2026-02-04
