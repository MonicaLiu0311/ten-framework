---
title: Voice Interaction Integration Guide
_portal_target: getting-started/voice-interaction-integration.md
---

# Voice Interaction Integration Guide

This guide will help you understand how to integrate TEN Framework's voice interaction capabilities into your existing agent projects, including interface documentation, compatibility requirements, and step-by-step integration instructions.

## Table of Contents

- [Voice Interaction Overview](#voice-interaction-overview)
- [Core Interfaces & APIs](#core-interfaces--apis)
- [Compatibility Requirements](#compatibility-requirements)
- [Integration Steps](#integration-steps)
- [Configuration Examples](#configuration-examples)
- [FAQ](#faq)

## Voice Interaction Overview

TEN Framework provides complete real-time voice conversation capabilities, supporting the construction of low-latency, high-quality voice AI assistants.

### Key Features

- **Real-time Speech Recognition (ASR/STT)**: Convert user speech to text in real-time
- **Text-to-Speech (TTS)**: Convert AI responses to natural voice output
- **Real-time Communication (RTC)**: Support for low-latency audio/video streaming
- **Voice Activity Detection (VAD)**: Automatically detect speech start/stop for better UX
- **Full-duplex Conversation**: Support turn detection for natural multi-turn dialogue
- **Multi-language Support**: Support for Chinese, English, Japanese, and more

### Supported Service Providers

#### Speech Recognition (ASR/STT) Providers (40+)

| Provider | Extension Name | Supported Languages |
|----------|---------------|---------------------|
| Deepgram | `deepgram_asr_python` / `deepgram_ws_asr_python` | Multi-language |
| OpenAI Whisper | `openai_asr_python` | Multi-language |
| Azure Speech | `azure_asr_python` | Multi-language |
| Google Cloud | `google_asr_python` | Multi-language |
| AWS Transcribe | `aws_asr_python` | Multi-language |
| AssemblyAI | `assemblyai_asr_python` | English-focused |
| Speechmatics | `speechmatics_asr_python` | Multi-language |
| Soniox | `soniox_asr_python` | English |
| Gladia | `gladia_asr_python` | Multi-language |
| Groq | `groq_asr_python` | Multi-language |
| Alibaba Cloud | `aliyun_asr` / `aliyun_asr_bigmodel_python` | Chinese-focused |
| Tencent Cloud | `tencent_asr_python` | Chinese-focused |
| ByteDance | `bytedance_asr` / `bytedance_llm_based_asr` | Chinese-focused |
| iFlytek | `xfyun_asr_python` / `xfyun_asr_bigmodel_python` | Chinese-focused |
| Sarvam (India) | `sarvam_asr_python` | Indian languages |
| Others | `gradium_asr_python`, `elevenlabs_asr_python`, `ezai_asr` | - |

#### Text-to-Speech (TTS) Providers (30+)

| Provider | Extension Name | Features |
|----------|---------------|----------|
| ElevenLabs | `elevenlabs_tts2_python` | High quality, natural emotion |
| OpenAI TTS | `openai_tts2_python` | Multi-language, stable |
| Azure TTS | `azure_tts_python` | Enterprise-grade, multi-language |
| Google TTS | `google_tts_python` | Multi-language support |
| AWS Polly | `polly_tts` | Multi-language, SSML |
| Cartesia | `cartesia_tts` | Real-time streaming |
| PlayHT | `playht_tts_python` | High-quality voice cloning |
| Fish Audio | `fish_audio_tts_python` | Chinese-optimized |
| Minimax | `minimax_tts_websocket_python` | Chinese, real-time streaming |
| Tencent Cloud | `tencent_tts_python` | Chinese-focused |
| Alibaba Cosy | `cosy_tts_python` | Chinese emotional voice |
| ByteDance | `bytedance_tts_duplex` | Chinese, real-time |
| iFlytek Rime | `rime_tts` / `rime_http_tts` | Chinese |
| Others | `murf_tts_python`, `neuphonic_tts`, `nvidia_riva_tts_python`, `gemini_tts_python`, `stepfun_tts_python`, `qwen3_tts_python`, `humeai_tts_python`, `inworld_tts_python`, `dubverse_tts`, `gradium_tts_python`, `sarvam_http_tts`, `vibevoice_tts_websocket_python`, `groq_tts_python` | - |

#### Real-time Communication (RTC)

- **Agora RTC** (`agora_rtc`): Low-latency audio/video transmission with global deployment
- **WebSocket**: WebSocket-based audio streaming

#### Additional Enhancement Features

- **Voice Activity Detection (VAD)**: `webrtc_vad_cpp`, `silero_vad_python`
- **Turn Detection**: Intelligently determine when users stop speaking
- **Speaker Diarization**: Support speaker identification in multi-person conversation scenarios

## Core Interfaces & APIs

### Voice Interaction Architecture

TEN Framework adopts an **Extension Graph** architecture, defining data flow between modules through configuration files:

```
User Voice Input → RTC/WebSocket → ASR → LLM → TTS → RTC/WebSocket → User Voice Output
                                           ↓
                                    Tool Calling (Optional)
```

### Key Interfaces

#### 1. Audio Frame Interface

Used to transmit raw audio data (PCM format):

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

**Audio Format Specification**:
- Sample Rate: 16000 Hz (recommended)
- Channels: Mono
- Bit Depth: 16-bit PCM
- Byte Order: Little Endian

#### 2. Data Interface

Used to transmit text, JSON, and other structured data:

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

**ASR Result Data Format**:
```json
{
  "text": "what the user said",
  "is_final": true,
  "language": "en-US"
}
```

#### 3. Command Interface

Used for flow control and state management:

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

### HTTP API Interface

If you're using the Web service from Agent Examples, here are the key HTTP APIs:

#### Start Conversation Session

```bash
POST /api/v1/start
Content-Type: application/json

{
  "channel_name": "your_channel_name",
  "language": "en-US"
}
```

**Response**:
```json
{
  "channel_name": "your_channel_name",
  "token": "agora_rtc_token",
  "app_id": "agora_app_id"
}
```

#### Stop Conversation Session

```bash
POST /api/v1/stop
Content-Type: application/json

{
  "channel_name": "your_channel_name"
}
```

#### WebSocket Interface

For WebSocket-based voice streaming:

```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8080/ws');

// Send audio data (Base64-encoded PCM)
ws.send(JSON.stringify({
  type: 'audio',
  data: base64AudioData
}));

// Receive voice response
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  if (response.type === 'audio') {
    // Play audio
  }
};
```

## Compatibility Requirements

### Technology Stack Compatibility

TEN Framework is **language-agnostic** and can be integrated with the following technology stacks:

✅ **Programming Language Support**
- Python 3.10+
- JavaScript / TypeScript (Node.js)
- Go 1.20+
- C++ 17+

✅ **Frontend Frameworks**
- React / Next.js (official examples use)
- Vue.js
- Angular
- Vanilla JavaScript

✅ **Backend Frameworks**
- Express.js (Node.js)
- FastAPI (Python)
- Flask (Python)
- Go native HTTP
- Any framework supporting WebSocket

### System Requirements

**Operating Systems**:
- Linux (x64 / arm64)
- macOS (Intel / Apple Silicon)
- Windows (partial support, WSL2 recommended)

**Hardware Requirements**:
- CPU: 2+ cores
- Memory: 4+ GB
- Network: Stable internet connection (for cloud service APIs)

### Project Integration Compatibility Check

**Your project is suitable for voice interaction integration if it meets the following conditions**:

✅ **Scenario Match**
- Needs real-time voice conversation features
- Needs to upgrade text assistant to voice assistant
- Needs voice interaction scenarios like phone, customer service, education

✅ **Technical Feasibility**
- Can deploy audio processing services (local or cloud)
- Can access voice service provider APIs (e.g., Deepgram, ElevenLabs)
- Has basic audio capture and playback capabilities (microphone, speakers)

✅ **Architecture Compatibility**
- Can communicate with external services via HTTP API or WebSocket
- Supports real-time or near real-time audio stream processing
- Can handle asynchronous events (user starts/stops speaking)

**Unsuitable Scenarios**:
- Pure text dialogue (no voice needed)
- Offline environment without local speech models
- Devices without audio capture capability (some embedded devices)

## Integration Steps

### Method 1: Add TEN Agent as Standalone Service to Existing Project

This is the **recommended approach**, suitable for existing mature projects that want to quickly add voice interaction capabilities.

#### Step 1: Deploy TEN Agent Voice Service

```bash
# Clone TEN Framework repository
git clone https://github.com/TEN-framework/ten-framework.git
cd ten-framework/ai_agents

# Configure environment variables
cp .env.example .env
vim .env  # Fill in API Keys

# Choose and start voice assistant example
cd agents/examples/voice-assistant
task install
task run
```

After the service starts, it will listen on the following ports:
- **API Server**: `http://localhost:8080`
- **Frontend UI**: `http://localhost:3000`

#### Step 2: Call TEN Agent API from Your Project

Call the voice service from your existing project via HTTP API:

**Python Example**:
```python
import requests

# Start voice session
response = requests.post('http://localhost:8080/api/v1/start', json={
    'channel_name': 'my_channel',
    'language': 'en-US'
})
session_data = response.json()

print(f"Channel: {session_data['channel_name']}")
print(f"Token: {session_data['token']}")
```

**JavaScript Example**:
```javascript
// Start voice session
const response = await fetch('http://localhost:8080/api/v1/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    channel_name: 'my_channel',
    language: 'en-US'
  })
});

const sessionData = await response.json();
console.log('Channel:', sessionData.channel_name);
```

#### Step 3: Integrate Frontend Audio Components

If using Agora RTC:

```javascript
import AgoraRTC from 'agora-rtc-sdk-ng';

// Initialize Agora client
const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

// Join channel (using token from API)
await client.join(
  sessionData.app_id,
  sessionData.channel_name,
  sessionData.token,
  null
);

// Create and publish microphone track
const microphoneTrack = await AgoraRTC.createMicrophoneAudioTrack();
await client.publish([microphoneTrack]);

// Listen for remote audio (AI voice response)
client.on('user-published', async (user, mediaType) => {
  if (mediaType === 'audio') {
    await client.subscribe(user, mediaType);
    user.audioTrack.play();
  }
});
```

If using WebSocket (more flexible):

```javascript
// Connect to WebSocket service
const ws = new WebSocket('ws://localhost:8080/ws');

// Send audio (capture microphone and convert to PCM first)
function sendAudio(pcmData) {
  const base64Audio = btoa(String.fromCharCode(...new Uint8Array(pcmData)));
  ws.send(JSON.stringify({
    type: 'audio',
    data: base64Audio,
    sample_rate: 16000,
    channels: 1
  }));
}

// Receive and play AI voice
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'audio') {
    // Decode Base64 and play audio
    const audioData = atob(message.data);
    playPCMAudio(audioData);
  } else if (message.type === 'transcript') {
    console.log('User said:', message.text);
  }
};
```

### Method 2: Create Customized Voice Assistant in TEN Framework

Suitable for deep customization scenarios or building completely new TEN-based applications.

#### Step 1: Create New TEN Application

```bash
# Install TEN Manager
bash <(curl -fsSL https://raw.githubusercontent.com/TEN-framework/ten-framework/main/tools/tman/install_tman.sh)

# Create application (based on existing template)
cd ten-framework/ai_agents/agents/examples
cp -r voice-assistant my-custom-agent
cd my-custom-agent
```

#### Step 2: Configure Voice Extensions

Edit `tenapp/property.json`, choose your preferred ASR and TTS providers:

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
                  "language": "en-US"
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
                "greeting": "Hello, I'm your voice assistant. How can I help you?"
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

#### Step 3: Add Custom Business Logic

Create custom extensions to handle specific business logic:

```bash
# Create Python extension
tman create extension my_business_logic --template default_extension_python

cd my_business_logic
```

Edit `src/extension.py`:

```python
from ten import Extension, TenEnv, Cmd, Data

class MyBusinessLogicExtension(Extension):
    def on_start(self, ten_env: TenEnv) -> None:
        ten_env.log_info("Business logic extension started")
        ten_env.on_start_done()

    def on_cmd(self, ten_env: TenEnv, cmd: Cmd) -> None:
        cmd_name = cmd.get_name()
        
        if cmd_name == "custom_command":
            # Handle custom command
            result = self.process_business_logic(cmd)
            ten_env.send_cmd(result)
        
        ten_env.on_cmd_done()

    def on_data(self, ten_env: TenEnv, data: Data) -> None:
        # Process text from ASR
        text = data.get_property_string("text")
        
        # Execute business logic
        processed = self.analyze_user_intent(text)
        
        # Send result
        result_data = Data.create("processed_intent")
        result_data.set_property_string("intent", processed)
        ten_env.send_data(result_data)
        
        ten_env.on_data_done()
```

#### Step 4: Build and Run

```bash
task install
task run
```

### Method 3: Use TEN Extensions as SDK in Existing Code

If you want to directly use TEN's voice capabilities in your existing Python/Node.js/Go project, you can use TEN Extensions as libraries.

#### Install TEN SDK

**Python**:
```bash
pip install ten-framework
```

**Node.js**:
```bash
npm install @ten-framework/ten-runtime
```

#### Use in Code

```python
from ten import App, TenEnv, Extension

# Create app
app = App()

# Add voice extensions
app.add_extension("deepgram_asr_python")
app.add_extension("openai_llm2_python")
app.add_extension("elevenlabs_tts2_python")

# Start app
app.run()
```

## Configuration Examples

### Basic Voice Assistant Configuration

**Using Deepgram ASR + OpenAI LLM + ElevenLabs TTS**:

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
                  "language": "en-US",
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
                "greeting": "Hello!"
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

### Configuration Using Chinese Service Providers

**Using Alibaba Cloud ASR + Tencent Cloud TTS**:

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

### Using Minimax Streaming TTS

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

### Adding VAD (Voice Activity Detection)

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

## FAQ

### 1. How to choose the right ASR and TTS providers?

**Considerations**:

| Factor | Recommendation |
|--------|---------------|
| **Language** | Chinese: Alibaba, Tencent, iFlytek; English: Deepgram, OpenAI |
| **Latency** | Real-time: Deepgram, Minimax; Transcription: Any |
| **Cost** | Cost-effective: Deepgram, Azure; Low-cost: Chinese providers |
| **Quality** | Natural: ElevenLabs, OpenAI, Fish Audio |
| **Customization** | Voice cloning: ElevenLabs, PlayHT |

### 2. Can I use TEN's voice features if my project already has LLM integration?

Yes! Two approaches:

**Approach A**: Use only ASR and TTS, handle text with your LLM
- TEN Agent provides ASR → text
- Your project handles text → LLM → response text
- TEN Agent provides text → TTS → voice

**Approach B**: Replace LLM extension in TEN
- Create custom extension that calls your LLM API
- Keep using TEN's ASR and TTS extensions

### 3. What audio formats are supported?

TEN Framework internally uses **PCM (16000Hz, 16-bit, Mono)** format.

If your audio is in other formats (e.g., MP3, WAV), convert first:

```python
from pydub import AudioSegment

# Convert to PCM
audio = AudioSegment.from_file("input.mp3")
audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
pcm_data = audio.raw_data
```

### 4. How to reduce latency?

**Optimization strategies**:

1. **Choose low-latency providers**:
   - ASR: Deepgram WebSocket, Minimax
   - TTS: Cartesia, Minimax WebSocket

2. **Use streaming**:
   ```json
   {
     "property": {
       "streaming": true
     }
   }
   ```

3. **Enable VAD**: Reduce silent audio transmission
   ```json
   {
     "addon": "webrtc_vad_cpp"
   }
   ```

4. **Optimize network**:
   - Use nearest cloud service region
   - Increase bandwidth

### 5. How to handle multi-language conversations?

**Dynamic language switching**:

```python
# Detect user language
detected_lang = detect_language(user_audio)

# Switch ASR language
update_property_cmd = Cmd.create("update_property")
update_property_cmd.set_property_string("language", detected_lang)
ten_env.send_cmd(update_property_cmd, "stt")
```

**Multi-language configuration example**:

```json
{
  "nodes": [
    {
      "name": "stt",
      "property": {
        "params": {
          "language": "auto",  // Auto-detect
          "enable_language_detection": true
        }
      }
    }
  ]
}
```

### 6. How to deploy in production?

Refer to [Agent Examples Self-Hosting](../../README.md#agent-examples-self-hosting) section in the main README:

**Using Docker**:
```bash
cd ai_agents
docker build -f agents/examples/voice-assistant/Dockerfile -t my-voice-agent .
docker run --env-file .env -p 8080:8080 -p 3000:3000 my-voice-agent
```

**Using cloud services**:
- Backend: Deploy to Fly.io, Render, AWS ECS, Google Cloud Run
- Frontend: Deploy to Vercel, Netlify

### 7. How to monitor and debug voice interaction?

**Log configuration**:

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

**Using Grafana monitoring**:

Refer to [WebSocket Voice Assistant Quick Start - Monitoring Configuration](./websocket-voice-assistant-quick-start.md#monitoring-configuration)

### 8. What are the API key costs?

Costs depend on your chosen providers:

| Provider | ASR Pricing | TTS Pricing | Free Tier |
|----------|------------|-------------|-----------|
| Deepgram | $0.0043/min | - | $200 free credits |
| OpenAI | $0.006/min | $15/M chars | No free tier |
| ElevenLabs | - | $0.30/K chars | 10K chars/month |
| Azure | $1/hour | $16/M chars | 12 months free |
| Alibaba Cloud | ¥0.0003/sec | ¥0.1/K chars | Free tier available |

> 💡 **Tip**: Actual costs vary by usage, region, and plan. Visit provider websites for latest pricing.

## Next Steps

- **[Quick Start](./quick-start.md)** - Run your first TEN app in 5 minutes
- **[WebSocket Voice Assistant Quick Start](./websocket-voice-assistant-quick-start.md)** - Build a complete voice assistant
- **[Extension Development Guide](../development/how_to_develop_with_ext.md)** - Develop custom extensions
- **[Example Projects](../../ai_agents/agents/examples/)** - Explore 12+ voice assistant examples
- **[API Documentation](../api/)** - Deep dive into TEN Framework APIs

## Get Help

- **GitHub Issues**: [https://github.com/TEN-framework/ten-framework/issues](https://github.com/TEN-framework/ten-framework/issues)
- **Discord Community**: [Join Discord](https://discord.gg/VnPftUzAMJ)
- **Documentation Hub**: [https://theten.ai/docs](https://theten.ai/docs)
- **WeChat Group**: [Join WeChat Discussion](https://github.com/TEN-framework/ten-agent/discussions/170)
