# 语音助手

基于 TEN Framework 的实时语音对话助手，使用 Agora RTC、Deepgram STT、OpenAI LLM 和 ElevenLabs TTS 实现完整的语音交互功能。

[English](README.md) | 简体中文

> 💡 **没有 API 密钥？** 查看 [免费试用指南](FREE_TRIAL_GUIDE.zh-CN.md) 了解如何免费开始！
> 
> 📝 **使用替代服务？** 查看 [配置文件修改指南](CONFIG_MODIFICATION_GUIDE.zh-CN.md) 了解如何正确配置！

## 功能特性

- **实时语音交互**：完整的语音对话流程，包括 STT（语音转文字）→ LLM（大语言模型）→ TTS（文字转语音）
- **低延迟**：优化的语音处理管道，实现流畅的对话体验
- **模块化设计**：可轻松替换 STT、LLM、TTS 等模块
- **可视化配置**：通过 TMAN Designer 可视化编辑器配置语音代理

## 快速开始

### 前置条件

在开始之前，您需要准备以下服务的 API 密钥：

| 服务 | 用途 | 获取方式 |
|------|------|----------|
| **Agora** | 实时音视频通信 | [Agora 控制台](https://console.agora.io/) |
| **Deepgram** | 语音转文字（STT） | [Deepgram 控制台](https://console.deepgram.com/) |
| **OpenAI** | 大语言模型（LLM） | [OpenAI 平台](https://platform.openai.com/) |
| **ElevenLabs** | 文字转语音（TTS） | [ElevenLabs](https://elevenlabs.io/) |

### 安装步骤

#### 1. 配置环境变量

在项目根目录的 `.env` 文件中添加以下配置：

```bash
# Agora（音频流必需）
AGORA_APP_ID=你的_agora_app_id
AGORA_APP_CERTIFICATE=你的_agora_证书

# Deepgram（语音转文字必需）
DEEPGRAM_API_KEY=你的_deepgram_api_key

# OpenAI（大语言模型必需）
OPENAI_API_KEY=你的_openai_api_key
OPENAI_MODEL=gpt-4

# ElevenLabs（文字转语音必需）
ELEVENLABS_TTS_KEY=你的_elevenlabs_api_key

# 可选配置
OPENAI_PROXY_URL=你的_代理_url
WEATHERAPI_API_KEY=你的_天气_api_key
```

#### 2. 安装依赖

```bash
cd agents/examples/voice-assistant
task install
```

此命令将安装 Python 依赖和前端组件。

#### 3. 启动语音助手

```bash
task run
```

#### 4. 访问应用

启动成功后，您可以访问以下界面：

- **前端界面**：http://localhost:3000
- **API 服务器**：http://localhost:8080
- **TMAN Designer 可视化编辑器**：http://localhost:49483

## 接口说明

### WebSocket 接口

语音助手通过 WebSocket 提供实时通信接口：

**连接地址**：`ws://localhost:8080/ws`

**消息格式**：

```json
{
  "type": "audio|text|control",
  "data": "消息内容",
  "timestamp": 1234567890
}
```

### HTTP API 接口

#### 创建会话

```http
POST /api/session
Content-Type: application/json

{
  "user_id": "用户ID",
  "config": {
    "language": "zh-CN",
    "voice_id": "语音ID"
  }
}
```

**响应**：

```json
{
  "session_id": "会话ID",
  "channel": "频道名称",
  "token": "Agora Token"
}
```

#### 发送文本消息

```http
POST /api/session/{session_id}/message
Content-Type: application/json

{
  "text": "你好，请介绍一下自己"
}
```

**响应**：

```json
{
  "message_id": "消息ID",
  "response": "助手回复内容"
}
```

## 项目集成指南

### 适配检查清单

在将语音交互集成到您的项目之前，请确认以下内容：

- [ ] **网络要求**：项目需要支持 WebSocket 或 HTTP 长连接
- [ ] **音频支持**：前端能够采集和播放音频（浏览器需要支持 Web Audio API）
- [ ] **API 密钥**：已获取必要的第三方服务 API 密钥
- [ ] **服务器资源**：
  - CPU：至少 2 核
  - 内存：至少 4 GB
  - 网络：稳定的互联网连接

### 集成方式 1：使用 Docker 部署

**构建镜像**：

```bash
cd ai_agents
docker build -f agents/examples/voice-assistant/Dockerfile -t voice-assistant-app .
```

**运行容器**：

```bash
docker run --rm -it --env-file .env -p 8080:8080 -p 3000:3000 voice-assistant-app
```

### 集成方式 2：作为微服务集成

如果您有现有的智能体项目，可以将语音助手作为独立的微服务运行：

1. **部署后端服务**：

```bash
# 启动语音助手后端
cd agents/examples/voice-assistant
task run
```

2. **在您的前端调用 API**：

```javascript
// 创建会话
const response = await fetch('http://localhost:8080/api/session', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'your_user_id',
    config: { language: 'zh-CN' }
  })
});
const { session_id, channel, token } = await response.json();

// 连接 WebSocket
const ws = new WebSocket('ws://localhost:8080/ws');
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('收到消息:', message);
};
```

### 集成方式 3：嵌入到现有项目

如果您想将 TEN Framework 直接嵌入到现有项目中：

1. **安装 TEN 核心库**：

```bash
# Python 项目
pip install ten-framework

# Node.js 项目
npm install @ten-framework/core
```

2. **配置 TEN 图**：

创建 `property.json` 配置文件，定义语音处理流程：

```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "voice_assistant",
        "auto_start": true,
        "graph": {
          "nodes": [
            {
              "name": "agora_rtc",
              "addon": "agora_rtc",
              "property": {
                "app_id": "${env:AGORA_APP_ID}"
              }
            },
            {
              "name": "stt",
              "addon": "deepgram_asr_python"
            },
            {
              "name": "llm",
              "addon": "openai_llm2_python"
            },
            {
              "name": "tts",
              "addon": "elevenlabs_tts2_python"
            }
          ]
        }
      }
    ]
  }
}
```

3. **在代码中初始化**：

```python
from ten import TenEnv, Extension

class VoiceAssistant(Extension):
    def on_init(self, ten_env: TenEnv):
        # 初始化语音助手
        ten_env.log_info("语音助手初始化")
    
    def on_start(self, ten_env: TenEnv):
        # 启动语音助手
        ten_env.log_info("语音助手启动")
```

## 自定义配置

### 通过 TMAN Designer 可视化配置

1. 打开 [http://localhost:49483](http://localhost:49483)
2. 在可视化编辑器中找到 STT、LLM、TTS 扩展节点
3. 右键点击节点，选择"属性"
4. 填写对应的 API 密钥和配置参数
5. 点击"提交"保存更改
6. 访问 [http://localhost:3000](http://localhost:3000) 查看更新后的效果

### 修改配置文件

您也可以直接编辑 `tenapp/property.json` 文件来配置语音助手：

```json
{
  "name": "stt",
  "addon": "deepgram_asr_python",
  "property": {
    "params": {
      "api_key": "${env:DEEPGRAM_API_KEY}",
      "language": "zh-CN",
      "model": "nova-2"
    }
  }
}
```

### 支持的配置参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AGORA_APP_ID` | string | - | Agora App ID（必需） |
| `AGORA_APP_CERTIFICATE` | string | - | Agora App Certificate（可选） |
| `DEEPGRAM_API_KEY` | string | - | Deepgram API 密钥（必需） |
| `OPENAI_API_KEY` | string | - | OpenAI API 密钥（必需） |
| `OPENAI_MODEL` | string | gpt-4 | OpenAI 模型名称 |
| `OPENAI_PROXY_URL` | string | - | OpenAI API 代理地址（可选） |
| `ELEVENLABS_TTS_KEY` | string | - | ElevenLabs API 密钥（必需） |
| `WEATHERAPI_API_KEY` | string | - | 天气 API 密钥（可选） |

## 常见问题

### 1. 如何切换语言？

在 `property.json` 中修改 `language` 参数：

```json
{
  "name": "stt",
  "addon": "deepgram_asr_python",
  "property": {
    "params": {
      "language": "zh-CN"  // 中文：zh-CN，英文：en-US
    }
  }
}
```

### 2. 如何替换 STT/TTS 提供商？

TEN Framework 支持多种 STT 和 TTS 提供商。在 TMAN Designer 中：

1. 删除现有的 STT/TTS 节点
2. 从扩展库中添加新的提供商（如 Azure STT、Google TTS 等）
3. 配置相应的 API 密钥

支持的提供商包括：
- **STT**：Deepgram、Azure、OpenAI Whisper、阿里云等
- **TTS**：ElevenLabs、Azure、Google、阿里云等

### 3. 如何优化延迟？

- 使用更快的 STT 模型（如 Deepgram Nova 2）
- 选择地理位置更近的服务器
- 启用流式处理模式
- 调整音频缓冲区大小

### 4. 能否在移动端使用？

可以！TEN Framework 支持以下移动端集成方式：

- **WebRTC**：通过浏览器直接访问
- **React Native**：使用 Agora React Native SDK
- **原生应用**：使用 Agora iOS/Android SDK

## 进阶功能

### 添加记忆功能

参考 [voice-assistant-with-PowerMem](../voice-assistant-with-PowerMem/README.zh-CN.md) 示例，为语音助手添加长期记忆能力。

### 添加多模态支持

参考 [voice-assistant-video](../voice-assistant-video) 示例，添加视频和图像处理功能。

### 添加唇形同步

参考 [voice-assistant-live2d](../voice-assistant-live2d) 示例，为虚拟角色添加唇形同步动画。

## 相关资源

- [TEN Framework 文档](https://theten.ai/docs)
- [Agora RTC 文档](https://docs.agora.io/cn/rtc/overview/product-overview)
- [Deepgram API 文档](https://developers.deepgram.com/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [ElevenLabs API 文档](https://docs.elevenlabs.io/)

## 技术支持

- [GitHub Issues](https://github.com/TEN-framework/ten-framework/issues)
- [Discord 社区](https://discord.gg/VnPftUzAMJ)
- [微信交流群](https://github.com/TEN-framework/ten-agent/discussions/170)

## 许可证

本示例遵循 TEN Framework 的许可证。详见根目录 [LICENSE](../../../../LICENSE) 文件。
