# TEN Framework 文档索引

本文档提供了 TEN Framework AI Agents 的完整文档导航。

## 📚 文档分类

### 🚀 快速开始

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [voice-assistant/README.zh-CN.md](agents/examples/voice-assistant/README.zh-CN.md) | 语音助手快速开始指南 | 所有用户 |
| [DOCKER_ONLY_SETUP.zh-CN.md](DOCKER_ONLY_SETUP.zh-CN.md) | Docker 纯容器化安装（推荐） | Windows/Linux/macOS 用户 |
| [FREE_TRIAL_GUIDE.zh-CN.md](agents/examples/voice-assistant/FREE_TRIAL_GUIDE.zh-CN.md) | 免费试用指南（无需付费 API） | 想免费试用的用户 |

### 🔧 配置和集成

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [VOICE_INTEGRATION_GUIDE.zh-CN.md](agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md) | 语音功能集成指南 | 要集成到项目的开发者 |
| [CONFIG_MODIFICATION_GUIDE.zh-CN.md](agents/examples/voice-assistant/CONFIG_MODIFICATION_GUIDE.zh-CN.md) | 配置文件修改详解 | 需要使用替代服务的用户 |
| [INTEGRATION_QA.zh-CN.md](INTEGRATION_QA.zh-CN.md) | 集成常见问题解答 | 有具体集成问题的开发者 |

### 📦 特定配置方案

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [README_QWEN_DEEPGRAM_BYTEDANCE.md](README_QWEN_DEEPGRAM_BYTEDANCE.md) | Qwen + Deepgram + Bytedance 配置 | 使用这些服务的用户 |
| [CONFIGURATION_QWEN_DEEPGRAM_BYTEDANCE.md](CONFIGURATION_QWEN_DEEPGRAM_BYTEDANCE.md) | Qwen 配置详细技术说明 | 需要详细配置信息的用户 |
| [env_qwen_deepgram_bytedance.example](env_qwen_deepgram_bytedance.example) | 环境变量配置模板 | 所有用户 |
| [property_qwen_deepgram_bytedance.json](property_qwen_deepgram_bytedance.json) | 图配置示例文件 | 所有用户 |

### 🛠️ 故障排查

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [INSTALLATION_TROUBLESHOOTING.zh-CN.md](INSTALLATION_TROUBLESHOOTING.zh-CN.md) | 安装问题故障排查 | 遇到安装问题的用户 |

### 🔐 安全

| 文档 | 说明 | 适合人群 |
|------|------|---------|
| [API_KEYS_SECURITY_GUIDE.zh-CN.md](API_KEYS_SECURITY_GUIDE.zh-CN.md) | API 密钥安全指南 | 所有用户（必读） |
| [SECURITY_WARNING.md](SECURITY_WARNING.md) | 安全警告（如果密钥泄露） | 密钥可能泄露的用户 |
| [README_SECURITY.md](README_SECURITY.md) | 安全文档索引 | 所有用户 |

---

## 🎯 按场景查找文档

### 场景 1：我是新用户，想快速试用

1. 阅读 [DOCKER_ONLY_SETUP.zh-CN.md](DOCKER_ONLY_SETUP.zh-CN.md)
2. 如果没有 API 密钥，查看 [FREE_TRIAL_GUIDE.zh-CN.md](agents/examples/voice-assistant/FREE_TRIAL_GUIDE.zh-CN.md)
3. 按照 [voice-assistant/README.zh-CN.md](agents/examples/voice-assistant/README.zh-CN.md) 开始使用

### 场景 2：我想集成到我的项目

1. 阅读 [VOICE_INTEGRATION_GUIDE.zh-CN.md](agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md) 了解集成方式
2. 阅读 [INTEGRATION_QA.zh-CN.md](INTEGRATION_QA.zh-CN.md) 了解具体实现
3. 选择合适的集成方式并实施

### 场景 3：我想使用特定的服务提供商

1. 阅读 [CONFIG_MODIFICATION_GUIDE.zh-CN.md](agents/examples/voice-assistant/CONFIG_MODIFICATION_GUIDE.zh-CN.md) 了解配置原理
2. 查看 [FREE_TRIAL_GUIDE.zh-CN.md](agents/examples/voice-assistant/FREE_TRIAL_GUIDE.zh-CN.md) 获取免费 API 密钥
3. 参考相应的配置示例（如 [README_QWEN_DEEPGRAM_BYTEDANCE.md](README_QWEN_DEEPGRAM_BYTEDANCE.md)）

### 场景 4：遇到安装问题

1. 阅读 [INSTALLATION_TROUBLESHOOTING.zh-CN.md](INSTALLATION_TROUBLESHOOTING.zh-CN.md)
2. 考虑使用 Docker 方式：[DOCKER_ONLY_SETUP.zh-CN.md](DOCKER_ONLY_SETUP.zh-CN.md)

### 场景 5：API 密钥泄露或安全问题

1. **立即**阅读 [SECURITY_WARNING.md](SECURITY_WARNING.md)
2. 按照指引撤销密钥
3. 学习 [API_KEYS_SECURITY_GUIDE.zh-CN.md](API_KEYS_SECURITY_GUIDE.zh-CN.md) 防止再次发生

---

## 📖 完整文档列表

### 根目录（ai_agents/）

- ✅ [README_DOCS_INDEX.zh-CN.md](README_DOCS_INDEX.zh-CN.md) - 本文档
- ✅ [DOCKER_ONLY_SETUP.zh-CN.md](DOCKER_ONLY_SETUP.zh-CN.md) - Docker 安装指南
- ✅ [INSTALLATION_TROUBLESHOOTING.zh-CN.md](INSTALLATION_TROUBLESHOOTING.zh-CN.md) - 安装故障排查
- ✅ [INTEGRATION_QA.zh-CN.md](INTEGRATION_QA.zh-CN.md) - 集成问答
- ✅ [README_QWEN_DEEPGRAM_BYTEDANCE.md](README_QWEN_DEEPGRAM_BYTEDANCE.md) - Qwen 配置指南
- ✅ [CONFIGURATION_QWEN_DEEPGRAM_BYTEDANCE.md](CONFIGURATION_QWEN_DEEPGRAM_BYTEDANCE.md) - Qwen 配置详解
- ✅ [API_KEYS_SECURITY_GUIDE.zh-CN.md](API_KEYS_SECURITY_GUIDE.zh-CN.md) - API 密钥安全
- ✅ [SECURITY_WARNING.md](SECURITY_WARNING.md) - 安全警告
- ✅ [README_SECURITY.md](README_SECURITY.md) - 安全文档索引

### voice-assistant 目录（agents/examples/voice-assistant/）

- ✅ [README.zh-CN.md](agents/examples/voice-assistant/README.zh-CN.md) - 语音助手 README
- ✅ [VOICE_INTEGRATION_GUIDE.zh-CN.md](agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md) - 集成指南
- ✅ [CONFIG_MODIFICATION_GUIDE.zh-CN.md](agents/examples/voice-assistant/CONFIG_MODIFICATION_GUIDE.zh-CN.md) - 配置修改指南
- ✅ [FREE_TRIAL_GUIDE.zh-CN.md](agents/examples/voice-assistant/FREE_TRIAL_GUIDE.zh-CN.md) - 免费试用指南

### 配置文件示例

- ✅ [env_qwen_deepgram_bytedance.example](env_qwen_deepgram_bytedance.example) - 环境变量模板
- ✅ [property_qwen_deepgram_bytedance.json](property_qwen_deepgram_bytedance.json) - 图配置示例

### 工具脚本

- ✅ [scripts/check-api-keys.sh](scripts/check-api-keys.sh) - API 密钥检查脚本
- ✅ [scripts/scan-api-keys.py](scripts/scan-api-keys.py) - 项目安全扫描

---

## 🌐 英文文档

大多数文档都有对应的英文版本，文件名将 `.zh-CN.md` 替换为 `.md` 即可。

例如：
- `DOCKER_ONLY_SETUP.zh-CN.md` → `DOCKER_ONLY_SETUP.md`
- `FREE_TRIAL_GUIDE.zh-CN.md` → `FREE_TRIAL_GUIDE.md`

---

## 📊 文档统计

- **总文档数**：20+ 份
- **总字数**：约 150,000 字
- **代码示例**：50+ 个
- **覆盖主题**：安装、配置、集成、安全、故障排查

---

## 🤝 获取帮助

如果文档没有回答你的问题：

1. **GitHub Issues**: https://github.com/TEN-framework/ten-framework/issues
2. **Discord**: https://discord.gg/VnPftUzAMJ
3. **官方网站**: https://theten.ai

---

## 📝 文档贡献

如果你发现文档有错误或可以改进的地方，欢迎：

1. 提交 Issue
2. 提交 Pull Request
3. 在 Discord 反馈

---

**最后更新**: 2026-02-05
