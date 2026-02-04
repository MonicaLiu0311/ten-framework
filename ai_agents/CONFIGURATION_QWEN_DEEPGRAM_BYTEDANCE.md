# 配置说明 - Configuration Guide

## 服务配置 Service Configuration

本配置使用以下服务：
- **LLM**: Qwen (通义千问) - 使用 OpenAI 兼容 API
- **STT**: Deepgram - 语音转文字
- **TTS**: Bytedance (字节跳动) - 文字转语音
- **Tools**: Aliyun (阿里云) - 工具服务
- **DB**: 无 - 数据库未配置（不影响基本运行）

## 环境变量配置 (.env 文件)

请复制以下内容到 `ai_agents/.env` 文件：

```bash
# ------------------------------
# Log & Server & Worker
# ------------------------------

LOG_PATH=/tmp/ten_agent
LOG_STDOUT=true
GRAPH_DESIGNER_SERVER_PORT=49483
SERVER_PORT=8080
WORKERS_MAX=100
WORKER_QUIT_TIMEOUT_SECONDS=60

# ------------------------------
# Frontend
# ------------------------------

AGENT_SERVER_URL=http://localhost:8080
TEN_DEV_SERVER_URL=http://localhost:49483
NEXT_PUBLIC_EDIT_GRAPH_MODE=true

# ------------------------------
# RTC (实时通信)
# ------------------------------

# Agora App ID 和 Certificate
# 在 https://console.agora.io/ 获取
AGORA_APP_ID=your_agora_app_id_here
AGORA_APP_CERTIFICATE=your_agora_certificate_here

# ------------------------------
# LLM - Qwen (通义千问)
# ------------------------------

# Qwen API Key - 在 https://dashscope.aliyun.com/ 获取
QWEN_API_KEY=sk-your_qwen_api_key_here

# Qwen API Base URL (OpenAI 兼容接口)
QWEN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1

# Qwen 模型名称
QWEN_MODEL=qwen-max

# ------------------------------
# STT - Deepgram
# ------------------------------

# Deepgram API Key - 在 https://console.deepgram.com/ 获取
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# ------------------------------
# TTS - Bytedance (字节跳动)
# ------------------------------

# Bytedance TTS App ID 和 Token
# 在火山引擎控制台获取 https://console.volcengine.com/
BYTEDANCE_TTS_APPID=your_bytedance_appid_here
BYTEDANCE_TTS_TOKEN=your_bytedance_token_here

# ------------------------------
# Tools - Aliyun (阿里云)
# ------------------------------

# 阿里云文本嵌入服务 API Key
ALIYUN_TEXT_EMBEDDING_API_KEY=your_aliyun_embedding_key_here

# ------------------------------
# DB - 数据库 (可选)
# ------------------------------

# 注意：数据库配置是可选的
# 如果不配置，系统仍然可以正常运行基本的语音助手功能
# 只有需要持久化存储或向量搜索时才需要配置

# 如果需要配置 Aliyun AnalyticDB 向量存储，取消注释以下配置：
# ALIBABA_CLOUD_ACCESS_KEY_ID=your_access_key_id
# ALIBABA_CLOUD_ACCESS_KEY_SECRET=your_access_key_secret
# ALIYUN_ANALYTICDB_ACCOUNT=your_account
# ALIYUN_ANALYTICDB_ACCOUNT_PASSWORD=your_password
# ALIYUN_ANALYTICDB_INSTANCE_ID=your_instance_id
# ALIYUN_ANALYTICDB_INSTANCE_REGION=cn-shanghai
# ALIYUN_ANALYTICDB_NAMESPACE=your_namespace
# ALIYUN_ANALYTICDB_NAMESPACE_PASSWORD=your_namespace_password
```

## Property.json 配置

property.json 文件路径：`ai_agents/agents/examples/voice-assistant/tenapp/property.json`

关键配置修改：

### 1. LLM 配置 (Qwen)
```json
{
  "type": "extension",
  "name": "llm",
  "addon": "openai_llm2_python",
  "extension_group": "chatgpt",
  "property": {
    "base_url": "${env:QWEN_API_BASE}",
    "api_key": "${env:QWEN_API_KEY}",
    "model": "${env:QWEN_MODEL}",
    "max_tokens": 512,
    "frequency_penalty": 0.9,
    "prompt": "",
    "proxy_url": "",
    "greeting": "您好，我是智能语音助手，有什么可以帮您？",
    "max_memory_length": 10
  }
}
```

### 2. STT 配置 (Deepgram)
```json
{
  "type": "extension",
  "name": "stt",
  "addon": "deepgram_asr_python",
  "extension_group": "stt",
  "property": {
    "params": {
      "api_key": "${env:DEEPGRAM_API_KEY}",
      "language": "zh-CN",
      "model": "nova-3"
    }
  }
}
```

### 3. TTS 配置 (Bytedance)
```json
{
  "type": "extension",
  "name": "tts",
  "addon": "bytedance_tts_duplex",
  "extension_group": "tts",
  "property": {
    "dump": false,
    "dump_path": "./",
    "params": {
      "app_id": "${env:BYTEDANCE_TTS_APPID}",
      "token": "${env:BYTEDANCE_TTS_TOKEN}",
      "speaker": "zh_female_qingxin"
    }
  }
}
```

## Poetry/Pyproject.toml 配置

由于 TEN Framework 使用扩展系统，各个扩展有自己的 requirements.txt。
不需要单独的 poetry 配置，依赖会自动从各扩展的 requirements.txt 安装。

主要依赖会从以下位置安装：
- `ai_agents/agents/ten_packages/extension/deepgram_asr_python/requirements.txt`
- `ai_agents/agents/ten_packages/extension/bytedance_tts_duplex/requirements.txt`
- `ai_agents/agents/ten_packages/extension/openai_llm2_python/requirements.txt`

## 如何运行

1. **安装依赖**
   ```bash
   cd ai_agents
   task install
   ```

2. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，填入您的 API 密钥
   ```

3. **修改 property.json**
   按照上面的配置修改 `agents/examples/voice-assistant/tenapp/property.json`

4. **运行服务**
   ```bash
   task run
   ```

5. **访问应用**
   打开浏览器访问 http://localhost:3000

## 关于数据库配置

**数据库不是必需的！**

- ✅ **不配置数据库**：可以正常运行基本的语音助手功能
- ⚠️ **需要数据库的场景**：
  - 需要持久化对话历史
  - 需要向量搜索功能
  - 需要长期记忆功能

如果只是试用或开发测试，完全可以不配置数据库。

## API 密钥获取

### Qwen (通义千问)
1. 访问 https://dashscope.aliyun.com/
2. 注册/登录阿里云账号
3. 创建 API Key
4. 免费额度：100 万 tokens/月

### Deepgram
1. 访问 https://console.deepgram.com/
2. 注册账号
3. 创建 API Key
4. 新用户有 $200 免费额度

### Bytedance (火山引擎)
1. 访问 https://console.volcengine.com/
2. 注册账号
3. 开通语音合成服务
4. 获取 App ID 和 Token

### Agora (声网)
1. 访问 https://console.agora.io/
2. 注册账号
3. 创建项目
4. 获取 App ID 和 Certificate
5. 免费额度：每月 10,000 分钟

## 故障排查

### 问题 1：找不到扩展
确保 manifest.json 中包含了所有需要的扩展：
- `deepgram_asr_python`
- `bytedance_tts_duplex`
- `openai_llm2_python`

### 问题 2：API 密钥无效
- 检查 .env 文件中的密钥是否正确
- 确认密钥没有过期
- 检查是否有足够的配额

### 问题 3：连接失败
- 检查网络连接
- 确认防火墙设置
- 检查 API 服务是否可用

## 参考文档

- [配置文件修改指南](CONFIG_MODIFICATION_GUIDE.zh-CN.md)
- [API 密钥安全指南](API_KEYS_SECURITY_GUIDE.zh-CN.md)
- [集成指南](agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md)
