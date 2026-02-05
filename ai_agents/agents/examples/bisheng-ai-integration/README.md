# Bisheng AI 语音集成示例 / Bisheng AI Voice Integration Example

[English](#english) | [中文](#chinese)

---

<a name="chinese"></a>
## 中文文档

### 概述

这是一个简化的TEN框架示例，专门用于集成**毕昇AI（Bisheng AI）**的助手或工作流功能。此示例**不使用**TEN内置的大模型，而是使用TEN的语音识别(STT)和语音合成(TTS)功能，中间通过HTTP调用您自己的毕昇AI服务。

**架构流程：**
```
用户语音 → TEN语音识别(STT) → 文本 → 毕昇AI处理(助手/工作流) → 文本 → TEN语音合成(TTS) → 音频输出
```

### 特点

- ✅ **仅使用语音功能**：只使用TEN的STT和TTS，不依赖TEN的LLM
- ✅ **集成毕昇AI**：通过HTTP API调用您的毕昇AI助手或工作流
- ✅ **WebSocket通信**：基于WebSocket的实时语音交互，支持base64音频编码
- ✅ **低延迟**：优化网络开销，适合Web应用
- ✅ **灵活配置**：支持助手模式和工作流模式

### 前置要求

#### 必需的环境变量

1. **Deepgram账户**（或其他STT服务）：从 [Deepgram Console](https://console.deepgram.com/) 获取
   - `DEEPGRAM_API_KEY` - 您的Deepgram API密钥（必需）

2. **ElevenLabs账户**（或其他TTS服务）：从 [ElevenLabs](https://elevenlabs.io/) 获取
   - `ELEVENLABS_TTS_KEY` - 您的ElevenLabs API密钥（必需）

3. **毕昇AI配置**：
   - `BISHENG_AI_URL` - 您的毕昇AI服务端点URL（必需）
   - `BISHENG_AI_API_KEY` - 毕昇AI的API密钥（可选，如果需要认证）
   - `BISHENG_AI_ASSISTANT_ID` - 助手ID（可选，使用助手模式时提供）
   - `BISHENG_AI_WORKFLOW_ID` - 工作流ID（可选，使用工作流模式时提供）

#### 可选的环境变量

- `STT_LANGUAGE` - 语音识别语言（默认: "zh-CN" 或 "en-US"）

### 安装和运行

#### 1. 配置环境变量

在 `.env` 文件中添加：

```bash
# Deepgram (语音识别必需)
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# ElevenLabs (语音合成必需)
ELEVENLABS_TTS_KEY=your_elevenlabs_api_key_here

# 毕昇AI配置 (必需)
BISHENG_AI_URL=https://your-bisheng-ai-domain.com/api/v1/chat
BISHENG_AI_API_KEY=your_bisheng_api_key_here  # 可选
BISHENG_AI_ASSISTANT_ID=your_assistant_id      # 可选，使用助手时提供
BISHENG_AI_WORKFLOW_ID=your_workflow_id        # 可选，使用工作流时提供
```

**注意：** 
- `BISHENG_AI_URL` 应该指向您的毕昇AI服务的聊天接口
- `BISHENG_AI_ASSISTANT_ID` 和 `BISHENG_AI_WORKFLOW_ID` 至少提供一个
- 如果两个都提供，系统会优先使用助手模式

#### 2. 测试配置（可选但推荐）

在运行服务前，建议先测试毕昇AI连接：

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
python3 test_connection.py
```

这个脚本会：
- 检查所有必需的环境变量
- 测试与毕昇AI服务的连接
- 验证响应格式是否正确

#### 3. 安装依赖

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
task install
```

这将安装Python依赖和前端组件。

#### 4. 运行语音助手

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
task run
```

#### 5. 访问应用

- **前端**: http://localhost:3000 （前端会自动生成8000-9000之间的随机WebSocket端口）
- **API服务器**: http://localhost:8080
- **TMAN设计器**: http://localhost:49483

### 毕昇AI API接口规范

示例期望毕昇AI的API接口遵循以下格式：

**请求格式：**
```json
{
  "input": "用户的语音识别文本",
  "session_id": "会话ID",
  "assistant_id": "助手ID（可选）",
  "workflow_id": "工作流ID（可选）"
}
```

**响应格式（支持以下任一字段）：**
```json
{
  "output": "AI的回复文本"
}
```

或者：
```json
{
  "response": "AI的回复文本"
}
```

或者：
```json
{
  "text": "AI的回复文本"
}
```

或者：
```json
{
  "answer": "AI的回复文本"
}
```

系统会自动检测这些常见的响应字段。

### WebSocket协议

#### 连接到WebSocket服务器

WebSocket服务器端口由前端客户端随机分配（8000-9000之间），并存储在浏览器的localStorage中。使用提供的前端时，端口会自动生成并显示在UI中。

**使用前端：**
前端自动生成随机端口，存储在localStorage中，并连接到它。端口显示在UI标识中。

**编程方式连接：**
```javascript
const port = localStorage.getItem('websocket_port') || 8765;
const ws = new WebSocket(`ws://localhost:${port}`);
```

#### 发送音频（客户端 → 服务器）

以JSON格式发送base64编码的PCM音频：

```javascript
// PCM音频格式: 16kHz, 单声道, 16位
const audioBase64 = btoa(String.fromCharCode(...pcmData));

ws.send(JSON.stringify({
  audio: audioBase64,
  metadata: {
    session_id: "optional-session-id"
  }
}));
```

**音频要求：**
- **格式**: 原始PCM（未压缩）
- **采样率**: 16000 Hz
- **声道**: 1（单声道）
- **位深度**: 16位（每样本2字节）
- **编码**: Base64

#### 接收消息（服务器 → 客户端）

服务器发送三种类型的消息：

**1. 音频消息（TTS输出）**
```javascript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'audio') {
    const pcmData = atob(message.audio);
    const sampleRate = message.metadata.sample_rate; // 16000
    playAudio(pcmData, sampleRate);
  }
};
```

**2. 数据消息（转录文本）**
```javascript
if (message.type === 'data' && message.name === 'text_data') {
  const text = message.data.text;
  const isFinal = message.data.is_final;
  const role = message.data.role; // 'user' 或 'assistant'
  console.log(`${role}: ${text}`);
}
```

**3. 错误消息**
```javascript
if (message.type === 'error') {
  console.error('服务器错误:', message.error);
}
```

### 配置

语音助手在 `tenapp/property.json` 中配置。图表包括：

- **websocket_server**: 从客户端接收音频并发送TTS音频
- **stt** (Deepgram ASR): 将语音转换为文本
- **main_control** (main_python): 编排对话流程，调用毕昇AI
- **tts** (ElevenLabs): 将文本转换为语音

关键配置部分：
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
              "name": "main_control",
              "addon": "main_python",
              "property": {
                "greeting": "您好！我已连接到毕昇AI语音服务。",
                "bisheng_ai_url": "${env:BISHENG_AI_URL}",
                "bisheng_ai_api_key": "${env:BISHENG_AI_API_KEY|}",
                "bisheng_ai_assistant_id": "${env:BISHENG_AI_ASSISTANT_ID|}",
                "bisheng_ai_workflow_id": "${env:BISHENG_AI_WORKFLOW_ID|}",
                "bisheng_ai_timeout": 30
              }
            }
          ]
        }
      }
    ]
  }
}
```

### 自定义

您可以轻松替换STT或TTS模块为其他提供商，使用TMAN设计器。

访问 http://localhost:49483 上的可视化设计器来自定义您的语音代理。详细使用说明，请参阅 [TMAN设计器文档](https://theten.ai/docs/ten_agent/customize_agent/tman-designer)。

### 使用Docker发布

**注意**：以下命令需要在Docker容器外执行。

#### 构建镜像

```bash
cd ai_agents
docker build -f agents/examples/bisheng-ai-integration/Dockerfile -t bisheng-voice-assistant .
```

#### 运行

```bash
docker run --rm -it --env-file .env -p 8080:8080 -p 3000:3000 -p 8765:8765 bisheng-voice-assistant
```

#### 访问

- 前端: http://localhost:3000
- API服务器: http://localhost:8080
- WebSocket服务器: 端口由前端随机分配（8000-9000）或在property.json中配置

### 故障排除

1. **连接毕昇AI失败**
   - 检查 `BISHENG_AI_URL` 是否正确
   - 确认毕昇AI服务正在运行
   - 验证API密钥是否有效

2. **语音识别不工作**
   - 检查 `DEEPGRAM_API_KEY` 是否有效
   - 确认音频格式正确（16kHz, 单声道, 16位PCM）

3. **语音合成不工作**
   - 检查 `ELEVENLABS_TTS_KEY` 是否有效
   - 确认网络连接正常

### 性能优化建议

1. **网络开销优化**：
   - 将毕昇AI服务部署在同一内网，减少延迟
   - 使用CDN加速前端资源加载
   - 开启gzip压缩减少数据传输

2. **服务开销优化**：
   - 使用WebSocket复用连接，避免频繁建立连接
   - 合理设置 `bisheng_ai_timeout` 参数
   - 考虑使用流式响应（如果毕昇AI支持）

---

<a name="english"></a>
## English Documentation

### Overview

This is a simplified TEN framework example specifically designed to integrate with **Bisheng AI** assistants or workflows. This example **does not use** TEN's built-in LLM. Instead, it uses TEN's speech recognition (STT) and text-to-speech (TTS) capabilities, calling your own Bisheng AI service via HTTP in between.

**Architecture Flow:**
```
User Voice → TEN Speech Recognition (STT) → Text → Bisheng AI Processing (Assistant/Workflow) → Text → TEN Text-to-Speech (TTS) → Audio Output
```

### Features

- ✅ **Voice Functions Only**: Uses only TEN's STT and TTS, without depending on TEN's LLM
- ✅ **Bisheng AI Integration**: Calls your Bisheng AI assistant or workflow via HTTP API
- ✅ **WebSocket Communication**: Real-time voice interaction based on WebSocket with base64 audio encoding
- ✅ **Low Latency**: Optimized for network overhead, suitable for web applications
- ✅ **Flexible Configuration**: Supports both assistant and workflow modes

### Prerequisites

#### Required Environment Variables

1. **Deepgram Account** (or other STT service): Get credentials from [Deepgram Console](https://console.deepgram.com/)
   - `DEEPGRAM_API_KEY` - Your Deepgram API key (required)

2. **ElevenLabs Account** (or other TTS service): Get credentials from [ElevenLabs](https://elevenlabs.io/)
   - `ELEVENLABS_TTS_KEY` - Your ElevenLabs API key (required)

3. **Bisheng AI Configuration**:
   - `BISHENG_AI_URL` - Your Bisheng AI service endpoint URL (required)
   - `BISHENG_AI_API_KEY` - Bisheng AI API key (optional, if authentication is needed)
   - `BISHENG_AI_ASSISTANT_ID` - Assistant ID (optional, provide when using assistant mode)
   - `BISHENG_AI_WORKFLOW_ID` - Workflow ID (optional, provide when using workflow mode)

#### Optional Environment Variables

- `STT_LANGUAGE` - Speech recognition language (default: "zh-CN" or "en-US")

### Installation and Running

#### 1. Configure Environment Variables

Add to your `.env` file:

```bash
# Deepgram (required for speech-to-text)
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# ElevenLabs (required for text-to-speech)
ELEVENLABS_TTS_KEY=your_elevenlabs_api_key_here

# Bisheng AI Configuration (required)
BISHENG_AI_URL=https://your-bisheng-ai-domain.com/api/v1/chat
BISHENG_AI_API_KEY=your_bisheng_api_key_here  # Optional
BISHENG_AI_ASSISTANT_ID=your_assistant_id      # Optional, provide when using assistant
BISHENG_AI_WORKFLOW_ID=your_workflow_id        # Optional, provide when using workflow
```

**Note:** 
- `BISHENG_AI_URL` should point to your Bisheng AI service's chat endpoint
- Provide at least one of `BISHENG_AI_ASSISTANT_ID` or `BISHENG_AI_WORKFLOW_ID`
- If both are provided, the system will prioritize assistant mode

#### 2. Test Configuration (Optional but Recommended)

Before running the service, it's recommended to test your Bisheng AI connection:

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
python3 test_connection.py
```

This script will:
- Check all required environment variables
- Test connection to Bisheng AI service
- Verify the response format is correct

#### 3. Install Dependencies

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
task install
```

This installs Python dependencies and frontend components.

#### 4. Run the Voice Assistant

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
task run
```

#### 5. Access the Application

- **Frontend**: http://localhost:3000 (The frontend will automatically generate a random WebSocket port between 8000-9000)
- **API Server**: http://localhost:8080
- **TMAN Designer**: http://localhost:49483

### Bisheng AI API Specification

The example expects Bisheng AI's API to follow this format:

**Request Format:**
```json
{
  "input": "User's speech recognition text",
  "session_id": "Session ID",
  "assistant_id": "Assistant ID (optional)",
  "workflow_id": "Workflow ID (optional)"
}
```

**Response Format (supports any of the following fields):**
```json
{
  "output": "AI response text"
}
```

Or:
```json
{
  "response": "AI response text"
}
```

Or:
```json
{
  "text": "AI response text"
}
```

Or:
```json
{
  "answer": "AI response text"
}
```

The system will automatically detect these common response fields.

### WebSocket Protocol

#### Connecting to the WebSocket Server

The WebSocket server port is randomly assigned by the frontend client (between 8000-9000) and stored in browser localStorage. When using the provided frontend, the port is automatically generated and displayed in the UI.

**Using the Frontend:**
The frontend automatically generates a random port, stores it in localStorage, and connects to it. The port is displayed in the UI badge.

**Connecting Programmatically:**
```javascript
const port = localStorage.getItem('websocket_port') || 8765;
const ws = new WebSocket(`ws://localhost:${port}`);
```

#### Sending Audio (Client → Server)

Send base64-encoded PCM audio in JSON format:

```javascript
// PCM audio format: 16kHz, mono, 16-bit
const audioBase64 = btoa(String.fromCharCode(...pcmData));

ws.send(JSON.stringify({
  audio: audioBase64,
  metadata: {
    session_id: "optional-session-id"
  }
}));
```

**Audio Requirements:**
- **Format**: Raw PCM (uncompressed)
- **Sample Rate**: 16000 Hz
- **Channels**: 1 (mono)
- **Bit Depth**: 16-bit (2 bytes per sample)
- **Encoding**: Base64

#### Receiving Messages (Server → Client)

The server sends three types of messages:

**1. Audio Messages (TTS Output)**
```javascript
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  
  if (message.type === 'audio') {
    const pcmData = atob(message.audio);
    const sampleRate = message.metadata.sample_rate; // 16000
    playAudio(pcmData, sampleRate);
  }
};
```

**2. Data Messages (Transcription Text)**
```javascript
if (message.type === 'data' && message.name === 'text_data') {
  const text = message.data.text;
  const isFinal = message.data.is_final;
  const role = message.data.role; // 'user' or 'assistant'
  console.log(`${role}: ${text}`);
}
```

**3. Error Messages**
```javascript
if (message.type === 'error') {
  console.error('Server error:', message.error);
}
```

### Configuration

The voice assistant is configured in `tenapp/property.json`. The graph includes:

- **websocket_server**: Receives audio from clients and sends TTS audio back
- **stt** (Deepgram ASR): Converts speech to text
- **main_control** (main_python): Orchestrates conversation flow, calls Bisheng AI
- **tts** (ElevenLabs): Converts text to speech

Key configuration sections:
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
              "name": "main_control",
              "addon": "main_python",
              "property": {
                "greeting": "Hello! I'm connected to Bisheng AI voice service.",
                "bisheng_ai_url": "${env:BISHENG_AI_URL}",
                "bisheng_ai_api_key": "${env:BISHENG_AI_API_KEY|}",
                "bisheng_ai_assistant_id": "${env:BISHENG_AI_ASSISTANT_ID|}",
                "bisheng_ai_workflow_id": "${env:BISHENG_AI_WORKFLOW_ID|}",
                "bisheng_ai_timeout": 30
              }
            }
          ]
        }
      }
    ]
  }
}
```

### Customization

You can easily replace STT or TTS modules with other providers using TMAN Designer.

Access the visual designer at http://localhost:49483 to customize your voice agent. For detailed usage instructions, see the [TMAN Designer documentation](https://theten.ai/docs/ten_agent/customize_agent/tman-designer).

### Release as Docker Image

**Note**: The following commands need to be executed outside of any Docker container.

#### Build Image

```bash
cd ai_agents
docker build -f agents/examples/bisheng-ai-integration/Dockerfile -t bisheng-voice-assistant .
```

#### Run

```bash
docker run --rm -it --env-file .env -p 8080:8080 -p 3000:3000 -p 8765:8765 bisheng-voice-assistant
```

#### Access

- Frontend: http://localhost:3000
- API Server: http://localhost:8080
- WebSocket Server: Port is randomly assigned by frontend (8000-9000) or configured in property.json

### Troubleshooting

1. **Failed to Connect to Bisheng AI**
   - Check if `BISHENG_AI_URL` is correct
   - Confirm Bisheng AI service is running
   - Verify API key is valid

2. **Speech Recognition Not Working**
   - Check if `DEEPGRAM_API_KEY` is valid
   - Confirm audio format is correct (16kHz, mono, 16-bit PCM)

3. **Text-to-Speech Not Working**
   - Check if `ELEVENLABS_TTS_KEY` is valid
   - Confirm network connection is normal

### Performance Optimization Tips

1. **Network Overhead Optimization**:
   - Deploy Bisheng AI service in the same internal network to reduce latency
   - Use CDN to accelerate frontend resource loading
   - Enable gzip compression to reduce data transfer

2. **Service Overhead Optimization**:
   - Use WebSocket connection reuse to avoid frequent connection establishment
   - Set `bisheng_ai_timeout` parameter reasonably
   - Consider using streaming responses (if Bisheng AI supports it)

## Learn More

- [Deepgram API Documentation](https://developers.deepgram.com/)
- [ElevenLabs API Documentation](https://docs.elevenlabs.io/)
- [TEN Framework Documentation](https://doc.theten.ai)
- [Bisheng AI Documentation](https://bisheng.dataelem.com/)
