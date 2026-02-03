---
title: 语音交互集成指南
_portal_target: getting-started/voice-interaction-integration.cn.md
---

# 语音交互集成指南

本指南将帮助您了解如何在现有的智能体项目中集成 TEN Framework 的语音交互功能，包括接口说明、兼容性要求和具体集成步骤。

## 目录

- [语音交互能力概述](#语音交互能力概述)
- [核心接口与 API](#核心接口与-api)
- [兼容性要求](#兼容性要求)
- [集成步骤](#集成步骤)
- [配置示例](#配置示例)
- [常见问题](#常见问题)

## 语音交互能力概述

TEN Framework 提供完整的实时语音对话能力，支持构建低延迟、高质量的语音 AI 助手。

### 主要功能特性

- **实时语音识别（ASR/STT）**：将用户语音实时转换为文本
- **文本转语音（TTS）**：将 AI 回复转换为自然语音输出
- **实时通信（RTC）**：支持低延迟的音视频流传输
- **语音活动检测（VAD）**：自动检测语音起止，优化交互体验
- **全双工对话**：支持对话轮次检测，实现自然的多轮对话
- **多语言支持**：支持中文、英文、日文等多种语言

### 支持的服务提供商

#### 语音识别（ASR/STT）提供商（40+）

| 提供商 | Extension 名称 | 支持语言 |
|--------|---------------|----------|
| Deepgram | `deepgram_asr_python` / `deepgram_ws_asr_python` | 多语言 |
| OpenAI Whisper | `openai_asr_python` | 多语言 |
| Azure Speech | `azure_asr_python` | 多语言 |
| Google Cloud | `google_asr_python` | 多语言 |
| AWS Transcribe | `aws_asr_python` | 多语言 |
| AssemblyAI | `assemblyai_asr_python` | 英语为主 |
| Speechmatics | `speechmatics_asr_python` | 多语言 |
| Soniox | `soniox_asr_python` | 英语 |
| Gladia | `gladia_asr_python` | 多语言 |
| Groq | `groq_asr_python` | 多语言 |
| 阿里云 | `aliyun_asr` / `aliyun_asr_bigmodel_python` | 中文为主 |
| 腾讯云 | `tencent_asr_python` | 中文为主 |
| 字节跳动 | `bytedance_asr` / `bytedance_llm_based_asr` | 中文为主 |
| 讯飞 | `xfyun_asr_python` / `xfyun_asr_bigmodel_python` | 中文为主 |
| Sarvam（印度） | `sarvam_asr_python` | 印度语言 |
| 其他 | `gradium_asr_python`, `elevenlabs_asr_python`, `ezai_asr` | - |

#### 语音合成（TTS）提供商（30+）

| 提供商 | Extension 名称 | 特点 |
|--------|---------------|------|
| ElevenLabs | `elevenlabs_tts2_python` | 高质量、自然情感 |
| OpenAI TTS | `openai_tts2_python` | 多语言、稳定 |
| Azure TTS | `azure_tts_python` | 企业级、多语言 |
| Google TTS | `google_tts_python` | 多语言支持 |
| AWS Polly | `polly_tts` | 多语言、SSML |
| Cartesia | `cartesia_tts` | 实时流式 |
| PlayHT | `playht_tts_python` | 高质量语音克隆 |
| Fish Audio | `fish_audio_tts_python` | 中文优化 |
| Minimax | `minimax_tts_websocket_python` | 中文、实时流式 |
| 腾讯云 | `tencent_tts_python` | 中文为主 |
| 阿里云 Cosy | `cosy_tts_python` | 中文情感语音 |
| 字节跳动 | `bytedance_tts_duplex` | 中文、实时 |
| 讯飞 Rime | `rime_tts` / `rime_http_tts` | 中文 |
| 其他 | `murf_tts_python`, `neuphonic_tts`, `nvidia_riva_tts_python`, `gemini_tts_python`, `stepfun_tts_python`, `qwen3_tts_python`, `humeai_tts_python`, `inworld_tts_python`, `dubverse_tts`, `gradium_tts_python`, `sarvam_http_tts`, `vibevoice_tts_websocket_python`, `groq_tts_python` | - |

#### 实时通信（RTC）

- **Agora RTC** (`agora_rtc`)：低延迟音视频传输，支持全球部署
- **WebSocket**：基于 WebSocket 的音频流传输

#### 其他增强功能

- **语音活动检测（VAD）**：`webrtc_vad_cpp`, `silero_vad_python`
- **对话轮次检测**：智能判断用户何时停止说话
- **说话人分离**：支持多人对话场景的说话人识别

## 核心接口与 API

### 语音交互架构

TEN Framework 采用**扩展图（Extension Graph）**架构，通过配置文件定义各个模块之间的数据流：

```
用户语音输入 → RTC/WebSocket → ASR → LLM → TTS → RTC/WebSocket → 用户语音输出
                                    ↓
                              工具调用（可选）
```

### 关键接口

#### 1. 音频帧接口（Audio Frame）

用于传输原始音频数据（PCM 格式）：

```json
{
  "audio_frame": [
    {
      "name": "pcm_frame",
      "dest": [{"extension": "stt"}]
    }
  ]
}
```

**音频格式规范**：
- 采样率：16000 Hz（推荐）
- 声道数：单声道（Mono）
- 位深度：16-bit PCM
- 字节序：Little Endian

#### 2. 数据接口（Data）

用于传输文本、JSON 等结构化数据：

```json
{
  "data": [
    {
      "name": "asr_result",
      "source": [{"extension": "stt"}]
    }
  ]
}
```

**ASR 结果数据格式**：
```json
{
  "text": "用户说的话",
  "is_final": true,
  "language": "zh-CN"
}
```

#### 3. 命令接口（Command）

用于控制流程和状态管理：

```json
{
  "cmd": [
    {
      "names": ["on_user_joined", "on_user_left"],
      "source": [{"extension": "agora_rtc"}]
    }
  ]
}
```

### HTTP API 接口

如果您使用 Agent Examples 中的 Web 服务，以下是关键的 HTTP API：

#### 启动对话会话

```bash
POST /api/v1/start
Content-Type: application/json

{
  "channel_name": "your_channel_name",
  "language": "zh-CN"
}
```

**响应**：
```json
{
  "channel_name": "your_channel_name",
  "token": "agora_rtc_token",
  "app_id": "agora_app_id"
}
```

#### 停止对话会话

```bash
POST /api/v1/stop
Content-Type: application/json

{
  "channel_name": "your_channel_name"
}
```

#### WebSocket 接口

用于基于 WebSocket 的语音流传输：

```javascript
// 连接 WebSocket
const ws = new WebSocket('ws://localhost:8080/ws');

// 发送音频数据（Base64 编码的 PCM）
ws.send(JSON.stringify({
  type: 'audio',
  data: base64AudioData
}));

// 接收语音回复
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  if (response.type === 'audio') {
    // 播放音频
  }
};
```

## 兼容性要求

### 技术栈兼容性

TEN Framework 是**语言无关**的框架，可以与以下技术栈集成：

✅ **编程语言支持**
- Python 3.10+
- JavaScript / TypeScript (Node.js)
- Go 1.20+
- C++ 17+

✅ **前端框架**
- React / Next.js（官方示例使用）
- Vue.js
- Angular
- 原生 JavaScript

✅ **后端框架**
- Express.js (Node.js)
- FastAPI (Python)
- Flask (Python)
- Go 原生 HTTP
- 任何支持 WebSocket 的框架

### 系统要求

**操作系统**：
- Linux (x64 / arm64)
- macOS (Intel / Apple Silicon)
- Windows（部分支持，推荐 WSL2）

**硬件要求**：
- CPU：2 核心以上
- 内存：4 GB 以上
- 网络：稳定的互联网连接（调用云服务 API）

### 项目集成兼容性检查

**您的项目适合集成语音交互，如果满足以下条件**：

✅ **场景匹配**
- 需要实时语音对话功能
- 需要将文本助手升级为语音助手
- 需要电话、客服、教育等语音交互场景

✅ **技术可行性**
- 项目可以部署音频处理服务（本地或云端）
- 能够访问语音服务提供商的 API（如 Deepgram、ElevenLabs 等）
- 有基本的音频采集和播放能力（麦克风、扬声器）

✅ **架构兼容**
- 可以通过 HTTP API 或 WebSocket 与外部服务通信
- 支持实时或准实时的音频流处理
- 能够处理异步事件（用户开始/停止说话）

**不适合的场景**：
- 纯文本对话（不需要语音）
- 离线环境且无法使用本地语音模型
- 设备无音频采集能力（如某些嵌入式设备）

## 集成步骤

### 方式一：在现有项目中添加 TEN Agent 作为独立服务

这是**推荐的方式**，适合已有成熟项目，希望快速添加语音交互能力。

#### 步骤 1：部署 TEN Agent 语音服务

```bash
# 克隆 TEN Framework 仓库
git clone https://github.com/TEN-framework/ten-framework.git
cd ten-framework/ai_agents

# 配置环境变量
cp .env.example .env
vim .env  # 填写 API Keys

# 选择并启动语音助手示例
cd agents/examples/voice-assistant
task install
task run
```

服务启动后会在以下端口监听：
- **API Server**: `http://localhost:8080`
- **Frontend UI**: `http://localhost:3000`

#### 步骤 2：从您的项目调用 TEN Agent API

在您的现有项目中，通过 HTTP API 调用语音服务：

**Python 示例**：
```python
import requests

# 启动语音会话
response = requests.post('http://localhost:8080/api/v1/start', json={
    'channel_name': 'my_channel',
    'language': 'zh-CN'
})
session_data = response.json()

print(f"Channel: {session_data['channel_name']}")
print(f"Token: {session_data['token']}")
```

**JavaScript 示例**：
```javascript
// 启动语音会话
const response = await fetch('http://localhost:8080/api/v1/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    channel_name: 'my_channel',
    language: 'zh-CN'
  })
});

const sessionData = await response.json();
console.log('Channel:', sessionData.channel_name);
```

#### 步骤 3：集成前端音频组件

如果使用 Agora RTC：

```javascript
import AgoraRTC from 'agora-rtc-sdk-ng';

// 初始化 Agora 客户端
const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

// 加入频道（使用从 API 获取的 token）
await client.join(
  sessionData.app_id,
  sessionData.channel_name,
  sessionData.token,
  null
);

// 创建并发布麦克风音轨
const microphoneTrack = await AgoraRTC.createMicrophoneAudioTrack();
await client.publish([microphoneTrack]);

// 监听远程音频（AI 的语音回复）
client.on('user-published', async (user, mediaType) => {
  if (mediaType === 'audio') {
    await client.subscribe(user, mediaType);
    user.audioTrack.play();
  }
});
```

如果使用 WebSocket（适合更灵活的场景）：

```javascript
// 连接到 WebSocket 服务
const ws = new WebSocket('ws://localhost:8080/ws');

// 发送音频（需要先采集麦克风并转换为 PCM）
function sendAudio(pcmData) {
  const base64Audio = btoa(String.fromCharCode(...new Uint8Array(pcmData)));
  ws.send(JSON.stringify({
    type: 'audio',
    data: base64Audio,
    sample_rate: 16000,
    channels: 1
  }));
}

// 接收并播放 AI 语音
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'audio') {
    // 解码 Base64 并播放音频
    const audioData = atob(message.data);
    playPCMAudio(audioData);
  } else if (message.type === 'transcript') {
    console.log('用户说:', message.text);
  }
};
```

### 方式二：在 TEN Framework 中创建定制化的语音助手

适合需要深度定制的场景，或者想要构建完全基于 TEN 的新应用。

#### 步骤 1：创建新的 TEN 应用

```bash
# 安装 TEN Manager
bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)

# 创建应用（基于现有模板）
cd ten-framework/ai_agents/agents/examples
cp -r voice-assistant my-custom-agent
cd my-custom-agent
```

#### 步骤 2：配置语音扩展

编辑 `tenapp/property.json`，选择您需要的 ASR 和 TTS 提供商：

```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "my_voice_assistant",
        "auto_start": true,
        "graph": {
          "nodes": [
            {
              "type": "extension",
              "name": "stt",
              "addon": "deepgram_asr_python",
              "property": {
                "params": {
                  "api_key": "${env:DEEPGRAM_API_KEY}",
                  "language": "zh-CN"
                }
              }
            },
            {
              "type": "extension",
              "name": "llm",
              "addon": "openai_llm2_python",
              "property": {
                "api_key": "${env:OPENAI_API_KEY}",
                "model": "gpt-4",
                "greeting": "您好，我是您的语音助手，有什么可以帮您？"
              }
            },
            {
              "type": "extension",
              "name": "tts",
              "addon": "elevenlabs_tts2_python",
              "property": {
                "params": {
                  "key": "${env:ELEVENLABS_TTS_KEY}",
                  "voice_id": "your_voice_id"
                }
              }
            }
          ]
        }
      }
    ]
  }
}
```

#### 步骤 3：添加自定义业务逻辑

创建自定义扩展来处理特定业务逻辑：

```bash
# 创建 Python 扩展
tman create extension my_business_logic --template default_extension_python

cd my_business_logic
```

编辑 `src/extension.py`：

```python
from ten import Extension, TenEnv, Cmd, Data

class MyBusinessLogicExtension(Extension):
    def on_start(self, ten_env: TenEnv) -> None:
        ten_env.log_info("业务逻辑扩展已启动")
        ten_env.on_start_done()

    def on_cmd(self, ten_env: TenEnv, cmd: Cmd) -> None:
        cmd_name = cmd.get_name()
        
        if cmd_name == "custom_command":
            # 处理自定义命令
            result = self.process_business_logic(cmd)
            ten_env.send_cmd(result)
        
        ten_env.on_cmd_done()

    def on_data(self, ten_env: TenEnv, data: Data) -> None:
        # 处理来自 ASR 的文本
        text = data.get_property_string("text")
        
        # 执行业务逻辑
        processed = self.analyze_user_intent(text)
        
        # 发送结果
        result_data = Data.create("processed_intent")
        result_data.set_property_string("intent", processed)
        ten_env.send_data(result_data)
        
        ten_env.on_data_done()
```

#### 步骤 4：构建和运行

```bash
task install
task run
```

### 方式三：使用 TEN Extension 作为 SDK 集成到现有代码

如果您想在现有的 Python/Node.js/Go 项目中直接使用 TEN 的语音能力，可以将 TEN Extension 作为库来使用。

#### 安装 TEN SDK

**Python**:
```bash
pip install ten-framework
```

**Node.js**:
```bash
npm install @ten-framework/ten-runtime
```

#### 在代码中使用

```python
from ten import App, TenEnv, Extension

# 创建应用
app = App()

# 添加语音扩展
app.add_extension("deepgram_asr_python")
app.add_extension("openai_llm2_python")
app.add_extension("elevenlabs_tts2_python")

# 启动应用
app.run()
```

## 配置示例

### 基础语音助手配置

**使用 Deepgram ASR + OpenAI LLM + ElevenLabs TTS**：

```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "basic_voice_assistant",
        "auto_start": true,
        "graph": {
          "nodes": [
            {
              "type": "extension",
              "name": "agora_rtc",
              "addon": "agora_rtc",
              "property": {
                "app_id": "${env:AGORA_APP_ID}",
                "channel": "voice_channel"
              }
            },
            {
              "type": "extension",
              "name": "stt",
              "addon": "deepgram_asr_python",
              "property": {
                "params": {
                  "api_key": "${env:DEEPGRAM_API_KEY}",
                  "language": "zh-CN",
                  "model": "nova-3"
                }
              }
            },
            {
              "type": "extension",
              "name": "llm",
              "addon": "openai_llm2_python",
              "property": {
                "api_key": "${env:OPENAI_API_KEY}",
                "model": "gpt-4",
                "greeting": "您好！"
              }
            },
            {
              "type": "extension",
              "name": "tts",
              "addon": "elevenlabs_tts2_python",
              "property": {
                "params": {
                  "key": "${env:ELEVENLABS_TTS_KEY}",
                  "model_id": "eleven_multilingual_v2",
                  "voice_id": "pNInz6obpgDQGcFmaJgB"
                }
              }
            }
          ],
          "connections": [
            {
              "extension": "agora_rtc",
              "audio_frame": [
                {
                  "name": "pcm_frame",
                  "dest": [{"extension": "stt"}]
                },
                {
                  "name": "pcm_frame",
                  "source": [{"extension": "tts"}]
                }
              ]
            },
            {
              "extension": "llm",
              "data": [
                {
                  "name": "asr_result",
                  "source": [{"extension": "stt"}]
                }
              ]
            }
          ]
        }
      }
    ]
  }
}
```

### 使用国内服务商的配置

**使用阿里云 ASR + 腾讯云 TTS**：

```json
{
  "nodes": [
    {
      "type": "extension",
      "name": "stt",
      "addon": "aliyun_asr_bigmodel_python",
      "property": {
        "params": {
          "app_key": "${env:ALIYUN_APP_KEY}",
          "access_key_id": "${env:ALIYUN_ACCESS_KEY_ID}",
          "access_key_secret": "${env:ALIYUN_ACCESS_KEY_SECRET}",
          "language": "zh-CN"
        }
      }
    },
    {
      "type": "extension",
      "name": "tts",
      "addon": "tencent_tts_python",
      "property": {
        "params": {
          "secret_id": "${env:TENCENT_SECRET_ID}",
          "secret_key": "${env:TENCENT_SECRET_KEY}",
          "voice_type": "101001"
        }
      }
    }
  ]
}
```

### 使用 Minimax 的流式 TTS

```json
{
  "type": "extension",
  "name": "tts",
  "addon": "minimax_tts_websocket_python",
  "property": {
    "params": {
      "api_key": "${env:MINIMAX_TTS_API_KEY}",
      "group_id": "${env:MINIMAX_TTS_GROUP_ID}",
      "model": "speech-02-turbo",
      "audio_setting": {
        "sample_rate": 16000,
        "format": "pcm"
      },
      "voice_setting": {
        "voice_id": "female-shaonv",
        "speed": 1.0,
        "vol": 1.0,
        "pitch": 0
      }
    }
  }
}
```

### 添加 VAD（语音活动检测）

```json
{
  "nodes": [
    {
      "type": "extension",
      "name": "vad",
      "addon": "webrtc_vad_cpp",
      "property": {
        "mode": 2,
        "sample_rate": 16000
      }
    }
  ],
  "connections": [
    {
      "extension": "vad",
      "audio_frame": [
        {
          "name": "pcm_frame",
          "source": [{"extension": "agora_rtc"}],
          "dest": [{"extension": "stt"}]
        }
      ]
    }
  ]
}
```

## 常见问题

### 1. 如何选择合适的 ASR 和 TTS 提供商？

**考虑因素**：

| 因素 | 推荐选择 |
|------|---------|
| **语言** | 中文：阿里云、腾讯云、讯飞；英文：Deepgram、OpenAI |
| **延迟** | 实时对话：Deepgram、Minimax；转录：可选任意 |
| **成本** | 高性价比：Deepgram、Azure；低成本：国内服务商 |
| **质量** | 自然度高：ElevenLabs、OpenAI、Fish Audio |
| **可定制性** | 需要声音克隆：ElevenLabs、PlayHT |

### 2. 我的项目已经有 LLM 集成，还能使用 TEN 的语音功能吗？

可以！有两种方式：

**方式 A**：只使用 ASR 和 TTS，文本交给您的 LLM 处理
- TEN Agent 提供 ASR → 文本
- 您的项目处理文本 → LLM → 回复文本
- TEN Agent 提供 文本 → TTS → 语音

**方式 B**：替换 TEN 中的 LLM 扩展
- 创建自定义扩展，调用您的 LLM API
- 保持 ASR 和 TTS 使用 TEN 的扩展

### 3. 支持哪些音频格式？

TEN Framework 内部使用 **PCM (16000Hz, 16-bit, Mono)** 格式。

如果您的音频是其他格式（如 MP3、WAV），需要先转换：

```python
from pydub import AudioSegment

# 转换为 PCM
audio = AudioSegment.from_file("input.mp3")
audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
pcm_data = audio.raw_data
```

### 4. 如何降低延迟？

**优化策略**：

1. **选择低延迟服务商**：
   - ASR：Deepgram WebSocket、Minimax
   - TTS：Cartesia、Minimax WebSocket

2. **使用流式处理**：
   ```json
   {
     "property": {
       "streaming": true
     }
   }
   ```

3. **启用 VAD**：减少静音传输
   ```json
   {
     "addon": "webrtc_vad_cpp"
   }
   ```

4. **优化网络**：
   - 使用最近的云服务区域
   - 增加带宽

### 5. 如何处理多语言对话？

**动态语言切换**：

```python
# 检测用户语言
detected_lang = detect_language(user_audio)

# 切换 ASR 语言
update_property_cmd = Cmd.create("update_property")
update_property_cmd.set_property_string("language", detected_lang)
ten_env.send_cmd(update_property_cmd, "stt")
```

**多语言配置示例**：

```json
{
  "nodes": [
    {
      "name": "stt",
      "property": {
        "params": {
          "language": "auto",  // 自动检测
          "enable_language_detection": true
        }
      }
    }
  ]
}
```

### 6. 如何在生产环境中部署？

参考主 README 中的 [Agent Examples Self-Hosting](../../README.md#agent-examples-self-hosting) 部分：

**使用 Docker**：
```bash
cd ai_agents
docker build -f agents/examples/voice-assistant/Dockerfile -t my-voice-agent .
docker run --env-file .env -p 8080:8080 -p 3000:3000 my-voice-agent
```

**使用云服务**：
- 后端：部署到 Fly.io、Render、AWS ECS、Google Cloud Run
- 前端：部署到 Vercel、Netlify

### 7. 如何监控和调试语音交互？

**日志配置**：

```json
{
  "ten": {
    "log": {
      "handlers": [
        {
          "matchers": [{"level": "debug"}],
          "formatter": {"type": "json"},
          "emitter": {
            "type": "file",
            "config": {"path": "logs/voice_agent.log"}
          }
        }
      ]
    }
  }
}
```

**使用 Grafana 监控**：

参考 [WebSocket 语音助手快速入门 - 配置监控](./websocket-voice-assistant-quick-start.cn.md#配置监控)

### 8. API Key 的费用是多少？

费用取决于您选择的服务商：

| 服务商 | ASR 定价 | TTS 定价 | 免费额度 |
|--------|---------|---------|---------|
| Deepgram | $0.0043/分钟 | - | $200 免费额度 |
| OpenAI | $0.006/分钟 | $15/百万字符 | 无免费额度 |
| ElevenLabs | - | $0.30/千字符 | 10k 字符/月 |
| Azure | $1/小时 | $16/百万字符 | 12 个月免费 |
| 阿里云 | ¥0.0003/秒 | ¥0.1/千字符 | 有免费额度 |

> 💡 **提示**：实际费用会因使用量、区域和套餐而异，请访问各服务商官网查看最新定价。

## 下一步

- **[快速开始](./quick-start.cn.md)** - 5 分钟运行第一个 TEN 应用
- **[WebSocket 语音助手快速入门](./websocket-voice-assistant-quick-start.cn.md)** - 构建完整的语音助手
- **[扩展开发指南](../development/how_to_develop_with_ext.cn.md)** - 开发自定义扩展
- **[示例项目](../../ai_agents/agents/examples/)** - 探索 12+ 个语音助手示例
- **[API 文档](../api/)** - 深入了解 TEN Framework API

## 获取帮助

- **GitHub Issues**: [https://github.com/TEN-framework/ten-framework/issues](https://github.com/TEN-framework/ten-framework/issues)
- **Discord 社区**: [加入 Discord](https://discord.gg/VnPftUzAMJ)
- **文档中心**: [https://theten.ai/cn/docs](https://theten.ai/cn/docs)
- **微信群**: [加入微信讨论组](https://github.com/TEN-framework/ten-agent/discussions/170)
