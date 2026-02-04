# 语音交互集成指南

本指南帮助您了解如何将 TEN Framework 的语音交互功能集成到您的智能体项目中，以及如何判断是否适配您的项目。

[English](VOICE_INTEGRATION_GUIDE.md) | 简体中文

> 📝 **重要提示**：如果您使用替代服务提供商（不是默认的 Deepgram + OpenAI + ElevenLabs），请务必阅读 [配置文件修改指南](CONFIG_MODIFICATION_GUIDE.zh-CN.md) 了解如何正确配置。

## 目录

- [适配性评估](#适配性评估)
- [集成方式选择](#集成方式选择)
- [快速集成示例](#快速集成示例)
- [API 接口详解](#api-接口详解)
- [最佳实践](#最佳实践)
- [故障排查](#故障排查)

## 适配性评估

### 您的项目适合集成语音交互吗？

请根据以下清单评估您的项目：

#### ✅ 技术要求

| 要求 | 说明 | 必需性 |
|------|------|--------|
| **网络连接** | 稳定的互联网连接，支持 WebSocket | 必需 |
| **音频支持** | 能够采集和播放音频 | 必需 |
| **计算资源** | CPU ≥ 2 核，RAM ≥ 4 GB | 必需 |
| **操作系统** | Linux、macOS、Windows，或支持 Docker | 必需 |
| **编程语言** | Python 3.9+、Node.js 18+、Go 1.19+ 之一 | 推荐 |

#### ✅ 业务需求

- [ ] 需要实时语音对话功能
- [ ] 需要将文字消息转换为语音播放
- [ ] 需要将语音转换为文字处理
- [ ] 需要集成大语言模型（LLM）
- [ ] 需要多模态交互（语音+文字+图像）

如果您勾选了以上任意一项，TEN Framework 都能满足您的需求。

### 集成难度评估

| 集成方式 | 开发时间 | 技术难度 | 适用场景 |
|----------|----------|----------|----------|
| **Docker 部署** | 30 分钟 | ⭐ 简单 | 快速试用、独立部署 |
| **微服务集成** | 2-4 小时 | ⭐⭐ 中等 | 现有项目、后端分离 |
| **SDK 嵌入** | 1-2 天 | ⭐⭐⭐ 较难 | 深度定制、完全控制 |

## 集成方式选择

### 方式 1：Docker 容器部署（推荐用于快速试用）

**适用场景**：
- 快速验证语音功能
- 独立部署的语音服务
- 不需要修改核心代码

**步骤**：

```bash
# 1. 克隆仓库
git clone https://github.com/TEN-framework/ten-framework.git
cd ten-framework/ai_agents

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的 API 密钥

# 3. 构建并运行
docker compose up -d
docker exec -it ten_agent_dev bash
cd agents/examples/voice-assistant
task install
task run
```

**访问**：
- 前端：http://localhost:3000
- API：http://localhost:8080
- 配置界面：http://localhost:49483

### 方式 2：作为微服务集成（推荐用于现有项目）

**适用场景**：
- 已有智能体项目
- 前后端分离架构
- 需要 RESTful API 或 WebSocket 接口

**架构图**：

```
┌─────────────────┐      HTTP/WS       ┌──────────────────┐
│   您的前端应用   │ ◄───────────────► │  TEN 语音服务    │
│  (Web/Mobile)   │                    │  (localhost:8080)│
└─────────────────┘                    └──────────────────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ STT/LLM/TTS  │
                                       │ 第三方服务   │
                                       └──────────────┘
```

**集成代码示例**：

**前端（JavaScript/React）**：

```javascript
// 1. 创建会话
async function createSession(userId) {
  const response = await fetch('http://localhost:8080/api/session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      config: {
        language: 'zh-CN',
        voice_id: 'default'
      }
    })
  });
  return await response.json();
}

// 2. 连接 WebSocket
function connectWebSocket(sessionId) {
  const ws = new WebSocket(`ws://localhost:8080/ws?session=${sessionId}`);
  
  ws.onopen = () => {
    console.log('语音连接已建立');
  };
  
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    switch (message.type) {
      case 'transcript':
        console.log('识别文本:', message.text);
        break;
      case 'response':
        console.log('AI 回复:', message.text);
        break;
      case 'audio':
        playAudio(message.data);
        break;
    }
  };
  
  return ws;
}

// 3. 发送音频数据
function sendAudio(ws, audioData) {
  ws.send(JSON.stringify({
    type: 'audio',
    data: audioData,
    format: 'pcm',
    sample_rate: 16000
  }));
}

// 使用示例
const session = await createSession('user_123');
const ws = connectWebSocket(session.session_id);
```

**后端（Python/Flask）**：

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
TEN_API_URL = "http://localhost:8080"

@app.route('/chat', methods=['POST'])
def chat():
    """将用户消息转发给 TEN 语音服务"""
    user_message = request.json.get('message')
    
    # 调用 TEN API
    response = requests.post(
        f"{TEN_API_URL}/api/session/{session_id}/message",
        json={'text': user_message}
    )
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
```

### 方式 3：SDK 深度集成（推荐用于高度定制）

**适用场景**：
- 需要完全控制语音处理流程
- 需要自定义 STT/LLM/TTS 提供商
- 需要处理特殊音频格式

**Python 集成**：

```python
from ten import TenEnv, Addon, Extension
from ten_ai_base import AsyncExtension

class CustomVoiceExtension(AsyncExtension):
    """自定义语音扩展"""
    
    async def on_init(self, ten_env: TenEnv) -> None:
        """初始化扩展"""
        ten_env.log_info("自定义语音扩展初始化")
        
        # 加载配置
        self.api_key = ten_env.get_property_string("api_key")
        self.language = ten_env.get_property_string("language")
    
    async def on_start(self, ten_env: TenEnv) -> None:
        """启动扩展"""
        ten_env.log_info("自定义语音扩展启动")
    
    async def on_audio_frame(self, ten_env: TenEnv, audio_frame) -> None:
        """处理音频帧"""
        # 1. 获取音频数据
        audio_data = audio_frame.get_data()
        
        # 2. 调用 STT
        text = await self.speech_to_text(audio_data)
        
        # 3. 发送文本消息
        text_data = ten_env.create_cmd("text_data")
        text_data.set_property_string("text", text)
        await ten_env.send_cmd(text_data)
    
    async def on_cmd(self, ten_env: TenEnv, cmd) -> None:
        """处理命令"""
        cmd_name = cmd.get_name()
        
        if cmd_name == "llm_response":
            # 获取 LLM 响应文本
            text = cmd.get_property_string("text")
            
            # 调用 TTS
            audio_data = await self.text_to_speech(text)
            
            # 发送音频帧
            audio_frame = ten_env.create_audio_frame()
            audio_frame.set_data(audio_data)
            await ten_env.send_audio_frame(audio_frame)

# 注册扩展
@Addon.register_addon_as_extension("custom_voice")
class CustomVoiceExtensionAddon(Addon):
    def on_create_extension(self, ten_env: TenEnv) -> Extension:
        return CustomVoiceExtension("custom_voice")
```

**配置文件（property.json）**：

```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "custom_voice_graph",
        "auto_start": true,
        "graph": {
          "nodes": [
            {
              "name": "agora_rtc",
              "addon": "agora_rtc",
              "extension_group": "default",
              "property": {
                "app_id": "${env:AGORA_APP_ID}",
                "subscribe_audio": true,
                "publish_audio": true
              }
            },
            {
              "name": "custom_voice",
              "addon": "custom_voice",
              "extension_group": "default",
              "property": {
                "api_key": "${env:API_KEY}",
                "language": "zh-CN"
              }
            }
          ],
          "connections": [
            {
              "extension_group": "default",
              "extension": "agora_rtc",
              "cmd": [
                {
                  "name": "audio_frame",
                  "dest": [
                    {
                      "extension_group": "default",
                      "extension": "custom_voice"
                    }
                  ]
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

## 快速集成示例

### 场景 1：为聊天机器人添加语音功能

**原有项目**：
```python
# 原有的文本聊天机器人
def chat(user_input):
    response = llm.generate(user_input)
    return response
```

**添加语音功能后**：
```python
import requests

TEN_API = "http://localhost:8080"

def voice_chat(session_id, audio_data=None, text=None):
    """支持语音和文本输入"""
    if audio_data:
        # 发送音频数据
        response = requests.post(
            f"{TEN_API}/api/session/{session_id}/audio",
            data=audio_data,
            headers={'Content-Type': 'audio/pcm'}
        )
    elif text:
        # 发送文本消息
        response = requests.post(
            f"{TEN_API}/api/session/{session_id}/message",
            json={'text': text}
        )
    
    result = response.json()
    return {
        'text': result['text'],          # 文本回复
        'audio_url': result['audio_url'] # 语音回复 URL
    }
```

### 场景 2：为 Web 应用添加语音交互

**HTML + JavaScript**：

```html
<!DOCTYPE html>
<html>
<head>
    <title>语音助手</title>
</head>
<body>
    <button id="startBtn">开始对话</button>
    <button id="stopBtn">停止对话</button>
    <div id="transcript"></div>
    <div id="response"></div>

    <script>
        let ws;
        let mediaRecorder;
        let audioContext;

        // 初始化会话
        async function initSession() {
            const response = await fetch('http://localhost:8080/api/session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: 'web_user',
                    config: { language: 'zh-CN' }
                })
            });
            const session = await response.json();
            return session.session_id;
        }

        // 连接 WebSocket
        function connectWebSocket(sessionId) {
            ws = new WebSocket(`ws://localhost:8080/ws?session=${sessionId}`);
            
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                
                if (message.type === 'transcript') {
                    document.getElementById('transcript').textContent = 
                        '您说：' + message.text;
                }
                
                if (message.type === 'response') {
                    document.getElementById('response').textContent = 
                        'AI：' + message.text;
                }
                
                if (message.type === 'audio') {
                    playAudio(message.data);
                }
            };
        }

        // 开始录音
        async function startRecording(sessionId) {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioContext = new AudioContext({ sampleRate: 16000 });
            const source = audioContext.createMediaStreamSource(stream);
            const processor = audioContext.createScriptProcessor(4096, 1, 1);
            
            processor.onaudioprocess = (e) => {
                const audioData = e.inputBuffer.getChannelData(0);
                const pcmData = new Int16Array(audioData.length);
                
                for (let i = 0; i < audioData.length; i++) {
                    pcmData[i] = Math.max(-32768, Math.min(32767, audioData[i] * 32768));
                }
                
                // 发送音频数据到 WebSocket
                ws.send(JSON.stringify({
                    type: 'audio',
                    data: Array.from(pcmData),
                    format: 'pcm',
                    sample_rate: 16000
                }));
            };
            
            source.connect(processor);
            processor.connect(audioContext.destination);
            
            return { stream, processor };
        }

        // 播放音频
        function playAudio(audioData) {
            const audioBuffer = audioContext.createBuffer(1, audioData.length, 16000);
            const channelData = audioBuffer.getChannelData(0);
            
            for (let i = 0; i < audioData.length; i++) {
                channelData[i] = audioData[i] / 32768;
            }
            
            const source = audioContext.createBufferSource();
            source.buffer = audioBuffer;
            source.connect(audioContext.destination);
            source.start();
        }

        // 按钮事件
        document.getElementById('startBtn').onclick = async () => {
            const sessionId = await initSession();
            connectWebSocket(sessionId);
            await startRecording(sessionId);
        };

        document.getElementById('stopBtn').onclick = () => {
            if (ws) ws.close();
            if (audioContext) audioContext.close();
        };
    </script>
</body>
</html>
```

## API 接口详解

### RESTful API

#### 1. 创建会话

**请求**：
```http
POST /api/session
Content-Type: application/json

{
  "user_id": "用户唯一标识",
  "config": {
    "language": "zh-CN",          // 语言：zh-CN, en-US, ja-JP 等
    "voice_id": "语音ID",         // 可选：指定 TTS 语音
    "enable_vad": true,           // 可选：启用语音活动检测
    "enable_interruption": false  // 可选：启用打断功能
  }
}
```

**响应**：
```json
{
  "session_id": "sess_abc123",
  "channel": "channel_name",
  "token": "agora_rtc_token",
  "expires_at": 1234567890
}
```

#### 2. 发送文本消息

**请求**：
```http
POST /api/session/{session_id}/message
Content-Type: application/json

{
  "text": "你好，今天天气怎么样？",
  "stream": false  // 可选：是否流式返回
}
```

**响应**：
```json
{
  "message_id": "msg_xyz789",
  "text": "今天天气晴朗，温度 25°C。",
  "audio_url": "http://localhost:8080/audio/msg_xyz789.mp3",
  "timestamp": 1234567890
}
```

#### 3. 上传音频

**请求**：
```http
POST /api/session/{session_id}/audio
Content-Type: audio/pcm
Content-Length: <音频数据长度>

<PCM 音频数据>
```

**响应**：
```json
{
  "transcript": "识别的文本内容",
  "response": "AI 回复内容",
  "audio_url": "http://localhost:8080/audio/response.mp3"
}
```

### WebSocket API

#### 连接

```
ws://localhost:8080/ws?session={session_id}
```

#### 消息格式

**客户端发送**：

```json
{
  "type": "audio|text|control",
  "data": "消息内容或音频数据",
  "format": "pcm|opus",       // 音频格式
  "sample_rate": 16000,       // 采样率
  "timestamp": 1234567890
}
```

**服务端推送**：

```json
{
  "type": "transcript|response|audio|event",
  "text": "文本内容",
  "data": "音频数据",
  "event": "session_started|transcription_completed|response_generated",
  "timestamp": 1234567890
}
```

## 最佳实践

### 1. 延迟优化

- 使用流式处理减少端到端延迟
- 选择地理位置近的服务器
- 启用 VAD（语音活动检测）减少不必要的处理
- 使用 WebSocket 而非轮询

```python
# 启用流式处理
config = {
    "streaming": {
        "enabled": True,
        "chunk_size": 1024
    }
}
```

### 2. 错误处理

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url, data):
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"API 调用失败: {e}")
        return None
```

### 3. 资源管理

```python
# 使用上下文管理器确保资源正确释放
class VoiceSession:
    def __enter__(self):
        self.session = create_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        close_session(self.session['session_id'])

# 使用
with VoiceSession() as session:
    result = send_message(session['session_id'], "你好")
```

### 4. 安全考虑

- 使用 HTTPS/WSS 加密通信
- 验证 API 密钥
- 限制会话时长
- 实施速率限制

```python
# 添加认证头
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

## 故障排查

### 常见问题

#### 1. 连接失败

**症状**：无法连接到 WebSocket 或 API

**解决方案**：
```bash
# 检查服务是否运行
curl http://localhost:8080/health

# 检查端口是否被占用
lsof -i :8080

# 查看日志
docker logs ten_agent_dev
```

#### 2. 音频无声音

**症状**：收到音频数据但无法播放

**解决方案**：
- 检查音频格式是否匹配（PCM 16kHz 16-bit）
- 验证音频数据完整性
- 检查浏览器音频权限

```javascript
// 检查浏览器音频权限
navigator.permissions.query({ name: 'microphone' })
  .then(result => console.log('麦克风权限:', result.state));
```

#### 3. 识别准确率低

**症状**：STT 识别错误率高

**解决方案**：
- 检查音频质量（降噪、采样率）
- 切换到更准确的 STT 模型
- 调整语言设置

```json
{
  "stt": {
    "model": "nova-2",        // 使用更准确的模型
    "language": "zh-CN",
    "punctuate": true,        // 启用标点符号
    "diarize": false          // 单人对话关闭说话人分离
  }
}
```

### 调试工具

#### 启用详细日志

```bash
# 设置日志级别
export TEN_LOG_LEVEL=debug

# 运行服务
task run
```

#### 监控 WebSocket 消息

```javascript
// 在浏览器控制台
const originalSend = WebSocket.prototype.send;
WebSocket.prototype.send = function(data) {
  console.log('发送:', data);
  return originalSend.apply(this, arguments);
};
```

## 下一步

- [查看完整 API 文档](https://theten.ai/docs/api)
- [浏览更多示例](../README.zh-CN.md)
- [加入社区讨论](https://discord.gg/VnPftUzAMJ)
- [提交问题反馈](https://github.com/TEN-framework/ten-framework/issues)

## 获取帮助

- **文档**：https://theten.ai/docs
- **Discord**：https://discord.gg/VnPftUzAMJ
- **微信群**：https://github.com/TEN-framework/ten-agent/discussions/170
- **GitHub Issues**：https://github.com/TEN-framework/ten-framework/issues
