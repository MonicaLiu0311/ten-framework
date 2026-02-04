# 无 API 密钥试用指南

如果您还没有获取所有必需的 API 密钥，本指南将帮助您了解如何获取免费试用账号，或使用替代服务来体验语音对话功能。

[English](FREE_TRIAL_GUIDE.md) | 简体中文

## 目录

- [快速了解：您需要哪些服务](#快速了解您需要哪些服务)
- [免费试用方案](#免费试用方案)
- [替代服务提供商](#替代服务提供商)
- [最小化配置方案](#最小化配置方案)
- [常见问题](#常见问题)

## 快速了解：您需要哪些服务

语音对话系统需要以下四类服务：

| 服务类型 | 用途 | 是否必需 |
|---------|------|---------|
| **RTC（实时通信）** | 音视频传输 | ✅ 必需 |
| **STT（语音转文字）** | 识别用户语音 | ✅ 必需 |
| **LLM（大语言模型）** | 理解和生成回复 | ✅ 必需 |
| **TTS（文字转语音）** | 将回复转为语音 | ✅ 必需 |

**好消息**：所有这些服务都提供免费试用或免费额度！

## 免费试用方案

### 1. Agora（实时通信）

**免费额度**：
- ✅ 每月 10,000 分钟免费
- ✅ 无需信用卡即可开始
- ✅ 永久免费额度

**注册步骤**：
1. 访问 [Agora 控制台](https://console.agora.io/)
2. 注册账号（支持邮箱、GitHub、Google 登录）
3. 创建项目
4. 获取 App ID（立即可用）
5. 如需要，可以启用 App Certificate（可选）

**获取时间**：< 5 分钟

**中国用户提示**：
- Agora 是中国公司声网的国际版
- 在中国可以正常访问和使用
- 也可以使用声网中国版：https://console.shengwang.cn/

### 2. OpenAI（大语言模型）

**免费额度**：
- ⚠️ 新用户曾有 $5 免费额度（政策可能变化）
- 💰 需要绑定支付方式
- 💡 费用：GPT-4o mini 约 $0.15/百万 tokens（非常便宜）

**注册步骤**：
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册账号
3. 绑定支付方式（信用卡或 PayPal）
4. 创建 API Key

**获取时间**：5-10 分钟

**中国用户提示**：
- ⚠️ 需要科学上网
- 💳 需要国际支付方式
- 如果无法注册，请看下面的替代方案

**替代方案（推荐给中国用户）**：

#### 2a. Gemini（Google）- 推荐 ⭐

**免费额度**：
- ✅ 每分钟 15 次免费请求
- ✅ 每天 1,500 次免费请求
- ✅ 永久免费（Gemini 1.5 Flash）
- ✅ 无需信用卡

**注册步骤**：
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 使用 Google 账号登录
3. 点击 "Get API Key"
4. 创建 API Key（立即可用）

**获取时间**：< 3 分钟

**配置方式**：
```bash
# 在 .env 文件中
GEMINI_API_KEY=你的_gemini_api_key

# 在 property.json 中，将 LLM 改为 gemini_llm2_python
```

**中国用户提示**：
- ⚠️ 需要科学上网访问
- ✅ 完全免费，额度充足
- ✅ 性能优秀，Gemini 1.5 Flash 速度快

#### 2b. 阿里云通义千问（Qwen）- 推荐 ⭐⭐

**免费额度**：
- ✅ 每月 100 万 tokens 免费（通义千问-Turbo）
- ✅ 新用户有额外试用额度
- ✅ 支持中文，效果好

**注册步骤**：
1. 访问 [阿里云 DashScope](https://dashscope.aliyun.com/)
2. 注册阿里云账号（支持手机号）
3. 开通 DashScope 服务
4. 创建 API Key

**获取时间**：5 分钟

**配置方式**：
```bash
# 在 .env 文件中
QWEN_API_KEY=你的_qwen_api_key

# 在 property.json 中，将 LLM addon 改为 qwen_llm
```

**中国用户提示**：
- ✅ 无需科学上网
- ✅ 国内访问速度快
- ✅ 中文能力强

#### 2c. DeepSeek - 最便宜 ⭐⭐⭐

**免费额度**：
- 💰 极低价格：$0.14/百万输入 tokens，$0.28/百万输出 tokens
- ✅ 新用户有免费试用额度
- ✅ API 兼容 OpenAI

**注册步骤**：
1. 访问 [DeepSeek Platform](https://platform.deepseek.com/)
2. 注册账号（支持手机号）
3. 充值少量金额（如 ¥10）
4. 创建 API Key

**获取时间**：5 分钟

**配置方式**：
```bash
# 在 .env 文件中
DEEPSEEK_API_KEY=你的_deepseek_api_key

# 在 property.json 中，使用 deepseek_llm
```

### 3. Deepgram（语音转文字）

**免费额度**：
- ✅ $200 免费额度
- ✅ 约等于 45,000 分钟转录时间
- ✅ 无需信用卡

**注册步骤**：
1. 访问 [Deepgram Console](https://console.deepgram.com/)
2. 注册账号（支持邮箱、GitHub、Google 登录）
3. 自动获得 $200 免费额度
4. 创建 API Key

**获取时间**：< 5 分钟

**中国用户提示**：
- ⚠️ 可能需要科学上网
- ✅ 免费额度非常充足

**替代方案（推荐给中国用户）**：

#### 3a. Azure STT - 推荐 ⭐

**免费额度**：
- ✅ 每月 5 小时免费（标准版）
- ✅ 支持中文识别
- 💳 需要绑定信用卡（但不会自动扣费）

**注册步骤**：
1. 访问 [Azure Portal](https://portal.azure.com/)
2. 注册 Microsoft 账号
3. 创建语音服务资源
4. 获取 API Key 和区域

**配置方式**：
```bash
# 在 .env 文件中
AZURE_ASR_API_KEY=你的_azure_key
AZURE_ASR_REGION=你的_区域

# 在 property.json 中，将 STT 改为 azure_asr_python
```

#### 3b. 阿里云语音识别 - 推荐 ⭐⭐

**免费额度**：
- ✅ 每月 2 小时免费
- ✅ 中文识别准确率高

**注册步骤**：
1. 访问 [阿里云智能语音](https://ai.aliyun.com/nls)
2. 开通服务
3. 创建 AccessKey

**配置方式**：
```bash
# 在 property.json 中，将 STT 改为 aliyun_asr
```

#### 3c. 腾讯云语音识别

**免费额度**：
- ✅ 每月 10 小时免费

**注册步骤**：
1. 访问 [腾讯云语音识别](https://cloud.tencent.com/product/asr)
2. 开通服务
3. 创建 API 密钥

**配置方式**：
```bash
# 在 property.json 中，将 STT 改为 tencent_asr_python
```

### 4. ElevenLabs（文字转语音）

**免费额度**：
- ✅ 每月 10,000 字符免费
- ✅ 约等于 10-15 分钟语音
- ✅ 无需信用卡

**注册步骤**：
1. 访问 [ElevenLabs](https://elevenlabs.io/)
2. 注册账号
3. 自动获得免费额度
4. 在设置中找到 API Key

**获取时间**：< 5 分钟

**中国用户提示**：
- ⚠️ 可能需要科学上网
- ✅ 语音质量非常好

**替代方案（推荐给中国用户）**：

#### 4a. Azure TTS - 推荐 ⭐

**免费额度**：
- ✅ 每月 500 万字符免费（神经语音）
- ✅ 支持中文语音
- 💳 需要绑定信用卡

**配置方式**：
```bash
# 在 .env 文件中
AZURE_TTS_KEY=你的_azure_key
AZURE_TTS_REGION=你的_区域

# 在 property.json 中，将 TTS 改为 azure_tts_python
```

#### 4b. 阿里云语音合成 - 推荐 ⭐⭐

**免费额度**：
- ✅ 每月 100 万字符免费
- ✅ 中文语音自然

**注册步骤**：
1. 访问 [阿里云智能语音](https://ai.aliyun.com/nls)
2. 开通语音合成服务

**配置方式**：
```bash
# 在 property.json 中，将 TTS 改为对应的阿里云 TTS 扩展
```

#### 4c. 腾讯云语音合成

**免费额度**：
- ✅ 每月 100 万字符免费

**配置方式**：
```bash
# 在 property.json 中，将 TTS 改为 tencent_tts_python
```

#### 4d. Google TTS

**免费额度**：
- ✅ 每月 400 万字符免费
- ✅ 支持多语言

**配置方式**：
```bash
# 在 property.json 中，将 TTS 改为 google_tts_python
```

## 替代服务提供商

TEN Framework 支持多种服务提供商，您可以根据自己的情况选择：

### STT（语音转文字）提供商

| 提供商 | 免费额度 | 中文支持 | 需要科学上网 | 推荐指数 |
|--------|---------|---------|-------------|---------|
| **Deepgram** | $200 额度 | ✅ | ⚠️ | ⭐⭐⭐ |
| **Azure** | 5 小时/月 | ✅ | ❌ | ⭐⭐⭐ |
| **阿里云** | 2 小时/月 | ✅ | ❌ | ⭐⭐⭐ |
| **腾讯云** | 10 小时/月 | ✅ | ❌ | ⭐⭐⭐ |
| **Google** | 60 分钟/月 | ✅ | ⚠️ | ⭐⭐ |
| **OpenAI Whisper** | 按用量付费 | ✅ | ⚠️ | ⭐⭐ |
| **AssemblyAI** | $50 额度 | ⚠️ | ⚠️ | ⭐⭐ |

### LLM（大语言模型）提供商

| 提供商 | 免费额度 | 中文支持 | 需要科学上网 | 推荐指数 |
|--------|---------|---------|-------------|---------|
| **Gemini** | 1500 次/天 | ✅ | ⚠️ | ⭐⭐⭐ |
| **阿里云通义千问** | 100 万 tokens/月 | ✅ | ❌ | ⭐⭐⭐ |
| **DeepSeek** | 极低价格 | ✅ | ❌ | ⭐⭐⭐ |
| **OpenAI** | 需付费 | ✅ | ⚠️ | ⭐⭐ |
| **Azure OpenAI** | 需付费 | ✅ | ❌ | ⭐⭐ |
| **AWS Bedrock** | 需付费 | ✅ | ❌ | ⭐⭐ |

### TTS（文字转语音）提供商

| 提供商 | 免费额度 | 中文支持 | 需要科学上网 | 推荐指数 |
|--------|---------|---------|-------------|---------|
| **Azure** | 500 万字符/月 | ✅ | ❌ | ⭐⭐⭐ |
| **Google** | 400 万字符/月 | ✅ | ⚠️ | ⭐⭐⭐ |
| **阿里云** | 100 万字符/月 | ✅ | ❌ | ⭐⭐⭐ |
| **腾讯云** | 100 万字符/月 | ✅ | ❌ | ⭐⭐⭐ |
| **ElevenLabs** | 10,000 字符/月 | ⚠️ | ⚠️ | ⭐⭐ |
| **OpenAI TTS** | 按用量付费 | ✅ | ⚠️ | ⭐⭐ |

## 最小化配置方案

### 方案 1：完全免费（中国用户推荐）⭐⭐⭐

**总成本**：¥0
**所需时间**：约 20 分钟

```bash
# .env 配置
AGORA_APP_ID=你的_agora_app_id          # 免费：10,000 分钟/月
GEMINI_API_KEY=你的_gemini_api_key      # 免费：1,500 次/天
AZURE_ASR_API_KEY=你的_azure_key        # 免费：5 小时/月
AZURE_ASR_REGION=你的_区域
AZURE_TTS_KEY=你的_azure_key            # 免费：500 万字符/月
AZURE_TTS_REGION=你的_区域
```

**特点**：
- ✅ 完全免费
- ✅ 额度充足（个人试用足够）
- ⚠️ Gemini 需要科学上网

### 方案 2：完全免费（无需科学上网）⭐⭐⭐

**总成本**：¥0
**所需时间**：约 20 分钟

```bash
# .env 配置
AGORA_APP_ID=你的_agora_app_id          # 免费：10,000 分钟/月
QWEN_API_KEY=你的_qwen_api_key          # 免费：100 万 tokens/月
AZURE_ASR_API_KEY=你的_azure_key        # 免费：5 小时/月
AZURE_ASR_REGION=你的_区域
AZURE_TTS_KEY=你的_azure_key            # 免费：500 万字符/月
AZURE_TTS_REGION=你的_区域
```

**特点**：
- ✅ 完全免费
- ✅ 无需科学上网
- ✅ 中文效果好
- ⚠️ Azure 需要绑定信用卡（不会扣费）

### 方案 3：国内方案（完全国产）⭐⭐

**总成本**：¥0-10
**所需时间**：约 25 分钟

```bash
# .env 配置
AGORA_APP_ID=你的_agora_app_id          # 免费：10,000 分钟/月
QWEN_API_KEY=你的_qwen_api_key          # 免费：100 万 tokens/月
# 阿里云 STT 和 TTS（配置在 property.json 中）
```

**特点**：
- ✅ 完全国产服务
- ✅ 无需科学上网
- ✅ 国内访问速度快
- ✅ 中文效果优秀

### 方案 4：最低成本（DeepSeek）⭐

**总成本**：约 ¥10-20（可用很久）
**所需时间**：约 25 分钟

```bash
# .env 配置
AGORA_APP_ID=你的_agora_app_id          # 免费：10,000 分钟/月
DEEPSEEK_API_KEY=你的_deepseek_api_key  # 极低价格
AZURE_ASR_API_KEY=你的_azure_key        # 免费：5 小时/月
AZURE_ASR_REGION=你的_区域
AZURE_TTS_KEY=你的_azure_key            # 免费：500 万字符/月
AZURE_TTS_REGION=你的_区域
```

**特点**：
- 💰 总成本极低（¥10 可以用很久）
- ✅ 无需科学上网
- ✅ DeepSeek 性能优秀

## 配置步骤

### 1. 选择您的方案

根据上述方案选择最适合您的配置。

### 2. 获取 API 密钥

按照上面的指引，依次注册并获取各服务的 API 密钥。

### 3. 配置 .env 文件

```bash
cd ai_agents
cp .env.example .env
# 编辑 .env 文件，填入您的 API 密钥
```

### 4. 修改 property.json（如果使用替代服务）

> 📝 **重要提示**：如果您使用了替代服务（不是默认的 Deepgram + OpenAI + ElevenLabs），**必须修改** `property.json` 配置文件。详细的技术说明和原理请参阅 [配置文件修改指南](CONFIG_MODIFICATION_GUIDE.zh-CN.md)。

如果您使用了替代服务（不是默认的 Deepgram + OpenAI + ElevenLabs），需要修改配置文件：

**位置**：`agents/examples/voice-assistant/tenapp/property.json`

**示例：使用 Gemini + Azure STT + Azure TTS**：

找到 STT 配置部分：
```json
{
  "name": "stt",
  "addon": "azure_asr_python",  // 改为 azure_asr_python
  "property": {
    "params": {
      "api_key": "${env:AZURE_ASR_API_KEY}",
      "region": "${env:AZURE_ASR_REGION}",
      "language": "zh-CN"
    }
  }
}
```

找到 LLM 配置部分：
```json
{
  "name": "llm",
  "addon": "gemini_llm2_python",  // 改为 gemini_llm2_python
  "property": {
    "api_key": "${env:GEMINI_API_KEY}",
    "model": "gemini-1.5-flash",
    "max_tokens": 512
  }
}
```

找到 TTS 配置部分：
```json
{
  "name": "tts",
  "addon": "azure_tts_python",  // 改为 azure_tts_python
  "property": {
    "params": {
      "key": "${env:AZURE_TTS_KEY}",
      "region": "${env:AZURE_TTS_REGION}",
      "voice_name": "zh-CN-XiaoxiaoNeural"
    }
  }
}
```

### 5. 启动服务

```bash
cd agents/examples/voice-assistant
task install
task run
```

### 6. 访问应用

打开浏览器访问：http://localhost:3000

## 常见问题

### 1. 我完全没有信用卡，能试用吗？

**可以！** 推荐使用方案 3（国内方案）：
- Agora：无需信用卡，每月 10,000 分钟免费
- 阿里云通义千问：无需信用卡，每月 100 万 tokens 免费
- 阿里云 STT/TTS：实名认证后即可使用免费额度

### 2. 我无法科学上网，怎么办？

推荐使用国内服务：
- **LLM**：阿里云通义千问、DeepSeek
- **STT**：阿里云、腾讯云
- **TTS**：阿里云、腾讯云
- **RTC**：Agora（中国公司，直接访问）

### 3. 各个服务的免费额度够用吗？

对于个人试用和学习：
- **完全够用** ✅
- Agora 10,000 分钟 = 166 小时通话
- Azure TTS 500 万字符 = 约 5-10 小时语音
- 通义千问 100 万 tokens = 数千次对话

对于小型项目：
- **基本够用** ✅
- 可以处理几百个用户的日常使用

对于生产环境：
- 需要付费，但成本不高
- 可以按实际使用量付费

### 4. 哪个方案最推荐？

**根据您的情况选择**：

如果您能科学上网：
- 推荐 **方案 1**（Gemini + Azure）
- 理由：完全免费，额度充足，性能好

如果您无法科学上网：
- 推荐 **方案 2** 或 **方案 3**
- 理由：完全使用国内服务，访问速度快

如果您愿意花费少量费用：
- 推荐 **方案 4**（DeepSeek）
- 理由：¥10-20 可以用很久，性能优秀

### 5. 如何验证 API 密钥是否正确？

启动服务后，查看日志输出：
```bash
# 在容器中查看日志
docker exec -it ten_agent_dev tail -f /tmp/ten_agent/log/app.log
```

如果看到连接错误，检查：
1. API 密钥是否正确复制（没有多余空格）
2. 环境变量是否正确设置
3. property.json 中的 addon 名称是否正确

### 6. 能否混合使用不同提供商？

**完全可以！** 这正是 TEN Framework 的优势。

例如：
- RTC: Agora
- STT: Deepgram（英文识别好）
- LLM: 通义千问（中文理解好）
- TTS: Azure（中文语音自然）

每个服务独立配置，可以自由组合。

### 7. 免费额度用完后怎么办？

**选项 1**：切换到其他提供商
- TEN Framework 支持多种提供商
- 只需修改配置文件即可切换

**选项 2**：付费使用
- 大多数服务的付费价格都不贵
- 可以按实际使用量付费

**选项 3**：等待下个月
- 大多数免费额度按月重置

### 8. 我是学生/教师，有教育优惠吗？

**有的！**

- **Azure**：学生可获得 $100 免费额度（12 个月）
  - 访问：https://azure.microsoft.com/zh-cn/free/students/
  
- **Google Cloud**：新用户 $300 免费额度（90 天）
  - 访问：https://cloud.google.com/free
  
- **AWS**：学生可获得 $50-100 AWS Educate 额度
  - 访问：https://aws.amazon.com/education/awseducate/

- **GitHub 学生包**：包含多种服务的优惠
  - 访问：https://education.github.com/pack

## 下一步

1. **选择方案**：根据您的情况选择最合适的方案
2. **获取密钥**：按照指引注册并获取 API 密钥
3. **配置服务**：修改 .env 和 property.json 文件
4. **启动测试**：运行服务并测试效果
5. **优化调整**：根据实际使用体验调整配置

## 获取帮助

如果在配置过程中遇到问题：

- **文档**：查看 [README.zh-CN.md](README.zh-CN.md)
- **集成指南**：查看 [VOICE_INTEGRATION_GUIDE.zh-CN.md](VOICE_INTEGRATION_GUIDE.zh-CN.md)
- **Discord**：https://discord.gg/VnPftUzAMJ
- **微信群**：https://github.com/TEN-framework/ten-agent/discussions/170
- **GitHub Issues**：https://github.com/TEN-framework/ten-framework/issues

---

**祝您试用愉快！** 🎉

如果您觉得 TEN Framework 有用，欢迎给我们 ⭐ Star：https://github.com/TEN-framework/ten-framework
