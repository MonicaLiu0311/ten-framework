# 使用 Qwen + Deepgram + Bytedance 配置说明

## 快速开始

本文档提供使用以下服务组合的完整配置方案：
- **LLM**: Qwen (通义千问)
- **STT**: Deepgram
- **TTS**: Bytedance (字节跳动/火山引擎)
- **Tools**: Aliyun (可选)
- **DB**: 不配置（可选）

## 配置文件清单

本配置包含以下文件：

1. **env_qwen_deepgram_bytedance.example** - 环境变量配置模板
2. **property_qwen_deepgram_bytedance.json** - TEN Framework 图配置
3. **CONFIGURATION_QWEN_DEEPGRAM_BYTEDANCE.md** - 详细配置文档

## 配置步骤

### 步骤 1: 复制环境变量文件

```bash
cd ai_agents
cp env_qwen_deepgram_bytedance.example .env
```

### 步骤 2: 获取 API 密钥

#### 2.1 Agora (必需)
1. 访问 https://console.agora.io/
2. 注册并登录
3. 创建项目，获取 App ID 和 App Certificate
4. 免费额度：每月 10,000 分钟

#### 2.2 Qwen - 通义千问 (必需)
1. 访问 https://dashscope.aliyun.com/
2. 使用阿里云账号登录
3. 创建 API Key
4. 免费额度：100 万 tokens/月

#### 2.3 Deepgram (必需)
1. 访问 https://console.deepgram.com/
2. 注册账号
3. 创建 API Key
4. 新用户免费额度：$200

#### 2.4 Bytedance - 火山引擎 (必需)
1. 访问 https://console.volcengine.com/
2. 注册账号
3. 开通"语音合成"服务
4. 在控制台获取 App ID 和 Token

#### 2.5 Aliyun Tools (可选)
如果需要使用阿里云工具服务（如文本嵌入）：
1. 访问阿里云控制台
2. 开通相应服务
3. 获取 API Key

### 步骤 3: 填写 .env 文件

编辑 `.env` 文件，填入获取的 API 密钥：

```bash
# Agora
AGORA_APP_ID=your_actual_app_id
AGORA_APP_CERTIFICATE=your_actual_certificate

# Qwen
QWEN_API_KEY=sk-your_actual_qwen_key
QWEN_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-max

# Deepgram
DEEPGRAM_API_KEY=your_actual_deepgram_key

# Bytedance
BYTEDANCE_TTS_APPID=your_actual_appid
BYTEDANCE_TTS_TOKEN=your_actual_token
```

### 步骤 4: 配置 property.json

复制示例配置到实际使用的位置：

```bash
cp property_qwen_deepgram_bytedance.json agents/examples/voice-assistant/tenapp/property.json
```

或者手动修改现有的 `agents/examples/voice-assistant/tenapp/property.json`：

#### 修改 LLM 节点 (使用 Qwen)
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
    "greeting": "您好，我是智能语音助手，有什么可以帮您？",
    "max_memory_length": 10
  }
}
```

#### 修改 STT 节点 (使用 Deepgram)
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

#### 修改 TTS 节点 (使用 Bytedance)
```json
{
  "type": "extension",
  "name": "tts",
  "addon": "bytedance_tts_duplex",
  "extension_group": "tts",
  "property": {
    "params": {
      "app_id": "${env:BYTEDANCE_TTS_APPID}",
      "token": "${env:BYTEDANCE_TTS_TOKEN}",
      "speaker": "zh_female_qingxin"
    }
  }
}
```

### 步骤 5: 确认扩展依赖

确保 `agents/examples/voice-assistant/tenapp/manifest.json` 包含以下扩展：

```json
{
  "dependencies": [
    {
      "path": "../../../ten_packages/extension/deepgram_asr_python"
    },
    {
      "path": "../../../ten_packages/extension/bytedance_tts_duplex"
    },
    {
      "path": "../../../ten_packages/extension/openai_llm2_python"
    }
  ]
}
```

### 步骤 6: 安装依赖

```bash
cd ai_agents
task install
```

### 步骤 7: 运行服务

```bash
task run
```

### 步骤 8: 访问应用

打开浏览器访问：http://localhost:3000

## 常见问题

### Q1: 为什么 Qwen 使用 openai_llm2_python 扩展？

A: Qwen (通义千问) 提供了 OpenAI 兼容的 API 接口，因此可以使用 `openai_llm2_python` 扩展。只需将 `base_url` 设置为 Qwen 的 API 地址即可。

### Q2: 需要配置数据库吗？

A: **不需要！** 数据库配置是可选的。不配置数据库也可以正常运行语音助手的基本功能。

数据库只在以下场景需要：
- 需要持久化对话历史
- 需要向量搜索功能
- 需要长期记忆功能

### Q3: 如何更改语言设置？

A: 在 property.json 的 STT 配置中修改 `language` 参数：
- 中文：`"language": "zh-CN"`
- 英文：`"language": "en-US"`

同时建议修改 LLM 的 greeting 消息为对应语言。

### Q4: Bytedance TTS 有哪些可用的说话人？

A: 常见说话人包括：
- `zh_female_qingxin` - 中文女声-清新（默认）
- `zh_male_chunhou` - 中文男声-淳厚
- `zh_female_wanxin` - 中文女声-婉馨
- `zh_male_shuaishuai` - 中文男声-帅帅

更多说话人请查看火山引擎官方文档。

### Q5: 如何选择 Qwen 模型？

A: Qwen 提供多个模型：

| 模型名称 | 特点 | 适用场景 |
|---------|------|---------|
| qwen-max | 最强性能 | 复杂对话，推荐 |
| qwen-plus | 平衡性能和速度 | 一般应用 |
| qwen-turbo | 更快速度 | 快速响应 |

在 .env 文件中设置 `QWEN_MODEL` 即可切换。

### Q6: 服务启动失败怎么办？

常见原因和解决方法：

1. **API 密钥错误**
   - 检查 .env 文件中的密钥是否正确
   - 确认密钥没有过期

2. **扩展未找到**
   - 检查 manifest.json 是否包含所需扩展
   - 运行 `task install` 重新安装依赖

3. **网络连接问题**
   - 确认可以访问对应的 API 服务
   - 检查防火墙设置

4. **端口被占用**
   - 修改 .env 中的 SERVER_PORT
   - 检查是否有其他服务占用 8080 端口

### Q7: 如何添加工具扩展？

如果需要添加工具（如天气查询等），在 property.json 中添加工具节点：

```json
{
  "type": "extension",
  "name": "weatherapi_tool_python",
  "addon": "weatherapi_tool_python",
  "extension_group": "default",
  "property": {
    "api_key": "${env:WEATHERAPI_API_KEY|}"
  }
}
```

并在 connections 中配置工具注册连接。

## 依赖说明

### 不需要 Poetry/pyproject.toml

TEN Framework 使用扩展系统，每个扩展有自己的 `requirements.txt`。
系统会自动从各扩展的 requirements.txt 安装依赖。

主要依赖来源：
- `agents/ten_packages/extension/deepgram_asr_python/requirements.txt`
- `agents/ten_packages/extension/bytedance_tts_duplex/requirements.txt`
- `agents/ten_packages/extension/openai_llm2_python/requirements.txt`

使用 `task install` 命令会自动处理所有依赖。

## 性能优化建议

1. **选择合适的模型**
   - 对于快速响应场景，使用 `qwen-turbo`
   - 对于复杂对话场景，使用 `qwen-max`

2. **调整 max_tokens**
   - 减少 max_tokens 可以加快响应速度
   - 默认值 512 适合大多数场景

3. **配置内存长度**
   - `max_memory_length` 控制上下文记忆条数
   - 增大值可以记住更多对话，但会增加 token 消耗

4. **STT 语言设置**
   - 正确设置 language 可以提高识别准确率
   - 如果主要是中文对话，使用 `zh-CN`

## 成本估算

基于免费额度的使用时间估算（轻度使用）：

| 服务 | 免费额度 | 预估可用时长 |
|------|---------|-------------|
| Agora | 10,000 分钟/月 | 约 166 小时 |
| Qwen | 100 万 tokens/月 | 约 1000-2000 次对话 |
| Deepgram | $200 额度 | 约 40-80 小时转录 |
| Bytedance | 根据具体套餐 | 查看火山引擎定价 |

**总结**：免费额度足够个人开发和测试使用数月。

## 进一步定制

### 更改 Greeting 消息

在 property.json 的 llm 和 main_control 节点中：

```json
"greeting": "欢迎使用智能助手，我可以帮您解答问题！"
```

### 调整对话参数

```json
{
  "frequency_penalty": 0.9,  // 词频惩罚，范围 -2.0 到 2.0
  "temperature": 0.7,        // 温度，控制随机性
  "top_p": 0.9               // 核采样
}
```

### 添加自定义工具

参考 `agents/ten_packages/extension/weatherapi_tool_python` 创建自己的工具扩展。

## 相关文档

- [详细配置说明](CONFIGURATION_QWEN_DEEPGRAM_BYTEDANCE.md)
- [配置文件修改指南](CONFIG_MODIFICATION_GUIDE.zh-CN.md)
- [API 密钥安全指南](API_KEYS_SECURITY_GUIDE.zh-CN.md)
- [集成指南](agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md)

## 技术支持

遇到问题？

1. 查看 [GitHub Issues](https://github.com/TEN-framework/ten-framework/issues)
2. 加入 Discord 社区
3. 查看官方文档

## 更新日志

- 2026-02-04: 创建初始配置文档
