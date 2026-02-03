# Voice Integration Guide

This guide helps you understand how to integrate TEN Framework's voice interaction features into your AI agent project and determine if it's compatible with your project.

English | [简体中文](VOICE_INTEGRATION_GUIDE.zh-CN.md)

## Table of Contents

- [Compatibility Assessment](#compatibility-assessment)
- [Integration Methods](#integration-methods)
- [Quick Integration Examples](#quick-integration-examples)
- [API Reference](#api-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Compatibility Assessment

### Is Your Project Suitable for Voice Integration?

Evaluate your project using the following checklist:

#### ✅ Technical Requirements

| Requirement | Description | Necessity |
|-------------|-------------|-----------|
| **Network** | Stable internet connection with WebSocket support | Required |
| **Audio** | Ability to capture and play audio | Required |
| **Resources** | CPU ≥ 2 cores, RAM ≥ 4 GB | Required |
| **OS** | Linux, macOS, Windows, or Docker support | Required |
| **Language** | Python 3.9+, Node.js 18+, or Go 1.19+ | Recommended |

#### ✅ Business Requirements

- [ ] Real-time voice conversation needed
- [ ] Text-to-speech conversion needed
- [ ] Speech-to-text conversion needed
- [ ] LLM integration required
- [ ] Multimodal interaction needed (voice + text + image)

If you checked any of the above, TEN Framework can meet your needs.

### Integration Complexity

| Method | Dev Time | Difficulty | Use Case |
|--------|----------|------------|----------|
| **Docker Deploy** | 30 min | ⭐ Easy | Quick trial, standalone deployment |
| **Microservice** | 2-4 hours | ⭐⭐ Medium | Existing projects, backend separation |
| **SDK Embed** | 1-2 days | ⭐⭐⭐ Hard | Deep customization, full control |

## Integration Methods

### Method 1: Docker Container (Recommended for Quick Trial)

**Use Cases**:
- Quick voice feature validation
- Standalone voice service deployment
- No core code modification needed

**Steps**:

```bash
# 1. Clone repository
git clone https://github.com/TEN-framework/ten-framework.git
cd ten-framework/ai_agents

# 2. Configure environment variables
cp .env.example .env
# Edit .env file with your API keys

# 3. Build and run
docker compose up -d
docker exec -it ten_agent_dev bash
cd agents/examples/voice-assistant
task install
task run
```

**Access**:
- Frontend: http://localhost:3000
- API: http://localhost:8080
- Designer: http://localhost:49483

### Method 2: Microservice Integration (Recommended for Existing Projects)

**Use Cases**:
- Existing AI agent projects
- Frontend-backend separation architecture
- RESTful API or WebSocket interface needed

**Architecture**:

```
┌─────────────────┐      HTTP/WS       ┌──────────────────┐
│   Your Frontend │ ◄───────────────► │  TEN Voice API   │
│  (Web/Mobile)   │                    │  (localhost:8080)│
└─────────────────┘                    └──────────────────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │ STT/LLM/TTS  │
                                       │ Services     │
                                       └──────────────┘
```

**Integration Example**:

**Frontend (JavaScript/React)**:

```javascript
// 1. Create session
async function createSession(userId) {
  const response = await fetch('http://localhost:8080/api/session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      config: {
        language: 'en-US',
        voice_id: 'default'
      }
    })
  });
  return await response.json();
}

// 2. Connect WebSocket
function connectWebSocket(sessionId) {
  const ws = new WebSocket(`ws://localhost:8080/ws?session=${sessionId}`);
  
  ws.onopen = () => console.log('Voice connection established');
  
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    switch (message.type) {
      case 'transcript':
        console.log('Transcript:', message.text);
        break;
      case 'response':
        console.log('AI Response:', message.text);
        break;
      case 'audio':
        playAudio(message.data);
        break;
    }
  };
  
  return ws;
}

// 3. Send audio data
function sendAudio(ws, audioData) {
  ws.send(JSON.stringify({
    type: 'audio',
    data: audioData,
    format: 'pcm',
    sample_rate: 16000
  }));
}

// Usage
const session = await createSession('user_123');
const ws = connectWebSocket(session.session_id);
```

**Backend (Python/Flask)**:

```python
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
TEN_API_URL = "http://localhost:8080"

@app.route('/chat', methods=['POST'])
def chat():
    """Forward user message to TEN voice service"""
    user_message = request.json.get('message')
    
    response = requests.post(
        f"{TEN_API_URL}/api/session/{session_id}/message",
        json={'text': user_message}
    )
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
```

### Method 3: Deep SDK Integration (Recommended for High Customization)

**Use Cases**:
- Full control over voice processing pipeline
- Custom STT/LLM/TTS providers
- Special audio format handling

**Python Integration**:

```python
from ten import TenEnv, Addon, Extension
from ten_ai_base import AsyncExtension

class CustomVoiceExtension(AsyncExtension):
    """Custom voice extension"""
    
    async def on_init(self, ten_env: TenEnv) -> None:
        """Initialize extension"""
        ten_env.log_info("Custom voice extension initialized")
        
        # Load configuration
        self.api_key = ten_env.get_property_string("api_key")
        self.language = ten_env.get_property_string("language")
    
    async def on_start(self, ten_env: TenEnv) -> None:
        """Start extension"""
        ten_env.log_info("Custom voice extension started")
    
    async def on_audio_frame(self, ten_env: TenEnv, audio_frame) -> None:
        """Process audio frame"""
        audio_data = audio_frame.get_data()
        
        # Call STT
        text = await self.speech_to_text(audio_data)
        
        # Send text message
        text_data = ten_env.create_cmd("text_data")
        text_data.set_property_string("text", text)
        await ten_env.send_cmd(text_data)
    
    async def on_cmd(self, ten_env: TenEnv, cmd) -> None:
        """Handle command"""
        cmd_name = cmd.get_name()
        
        if cmd_name == "llm_response":
            text = cmd.get_property_string("text")
            
            # Call TTS
            audio_data = await self.text_to_speech(text)
            
            # Send audio frame
            audio_frame = ten_env.create_audio_frame()
            audio_frame.set_data(audio_data)
            await ten_env.send_audio_frame(audio_frame)

# Register extension
@Addon.register_addon_as_extension("custom_voice")
class CustomVoiceExtensionAddon(Addon):
    def on_create_extension(self, ten_env: TenEnv) -> Extension:
        return CustomVoiceExtension("custom_voice")
```

## Quick Integration Examples

### Scenario 1: Add Voice to Chatbot

**Original Project**:
```python
def chat(user_input):
    response = llm.generate(user_input)
    return response
```

**With Voice**:
```python
import requests

TEN_API = "http://localhost:8080"

def voice_chat(session_id, audio_data=None, text=None):
    """Support both voice and text input"""
    if audio_data:
        response = requests.post(
            f"{TEN_API}/api/session/{session_id}/audio",
            data=audio_data,
            headers={'Content-Type': 'audio/pcm'}
        )
    elif text:
        response = requests.post(
            f"{TEN_API}/api/session/{session_id}/message",
            json={'text': text}
        )
    
    result = response.json()
    return {
        'text': result['text'],
        'audio_url': result['audio_url']
    }
```

### Scenario 2: Add Voice Interaction to Web App

**HTML + JavaScript**:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Voice Assistant</title>
</head>
<body>
    <button id="startBtn">Start Conversation</button>
    <button id="stopBtn">Stop Conversation</button>
    <div id="transcript"></div>
    <div id="response"></div>

    <script>
        let ws;
        let audioContext;

        async function initSession() {
            const response = await fetch('http://localhost:8080/api/session', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: 'web_user',
                    config: { language: 'en-US' }
                })
            });
            const session = await response.json();
            return session.session_id;
        }

        function connectWebSocket(sessionId) {
            ws = new WebSocket(`ws://localhost:8080/ws?session=${sessionId}`);
            
            ws.onmessage = (event) => {
                const message = JSON.parse(event.data);
                
                if (message.type === 'transcript') {
                    document.getElementById('transcript').textContent = 
                        'You: ' + message.text;
                }
                
                if (message.type === 'response') {
                    document.getElementById('response').textContent = 
                        'AI: ' + message.text;
                }
                
                if (message.type === 'audio') {
                    playAudio(message.data);
                }
            };
        }

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
                
                ws.send(JSON.stringify({
                    type: 'audio',
                    data: Array.from(pcmData),
                    format: 'pcm',
                    sample_rate: 16000
                }));
            };
            
            source.connect(processor);
            processor.connect(audioContext.destination);
        }

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

## API Reference

### RESTful API

#### 1. Create Session

**Request**:
```http
POST /api/session
Content-Type: application/json

{
  "user_id": "unique_user_id",
  "config": {
    "language": "en-US",
    "voice_id": "voice_id",
    "enable_vad": true,
    "enable_interruption": false
  }
}
```

**Response**:
```json
{
  "session_id": "sess_abc123",
  "channel": "channel_name",
  "token": "agora_rtc_token",
  "expires_at": 1234567890
}
```

#### 2. Send Text Message

**Request**:
```http
POST /api/session/{session_id}/message
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "stream": false
}
```

**Response**:
```json
{
  "message_id": "msg_xyz789",
  "text": "I'm doing well, thank you!",
  "audio_url": "http://localhost:8080/audio/msg_xyz789.mp3",
  "timestamp": 1234567890
}
```

#### 3. Upload Audio

**Request**:
```http
POST /api/session/{session_id}/audio
Content-Type: audio/pcm
Content-Length: <audio_data_length>

<PCM audio data>
```

**Response**:
```json
{
  "transcript": "Recognized text",
  "response": "AI response",
  "audio_url": "http://localhost:8080/audio/response.mp3"
}
```

### WebSocket API

#### Connection

```
ws://localhost:8080/ws?session={session_id}
```

#### Message Format

**Client Send**:

```json
{
  "type": "audio|text|control",
  "data": "message content or audio data",
  "format": "pcm|opus",
  "sample_rate": 16000,
  "timestamp": 1234567890
}
```

**Server Push**:

```json
{
  "type": "transcript|response|audio|event",
  "text": "text content",
  "data": "audio data",
  "event": "session_started|transcription_completed|response_generated",
  "timestamp": 1234567890
}
```

## Best Practices

### 1. Latency Optimization

- Use streaming to reduce end-to-end latency
- Choose geographically close servers
- Enable VAD to reduce unnecessary processing
- Use WebSocket instead of polling

```python
# Enable streaming
config = {
    "streaming": {
        "enabled": true,
        "chunk_size": 1024
    }
}
```

### 2. Error Handling

```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url, data):
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"API call failed: {e}")
        return None
```

### 3. Resource Management

```python
# Use context manager for proper cleanup
class VoiceSession:
    def __enter__(self):
        self.session = create_session()
        return self.session
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        close_session(self.session['session_id'])

# Usage
with VoiceSession() as session:
    result = send_message(session['session_id'], "Hello")
```

### 4. Security

- Use HTTPS/WSS for encrypted communication
- Validate API keys
- Limit session duration
- Implement rate limiting

```python
# Add authentication header
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

## Troubleshooting

### Common Issues

#### 1. Connection Failed

**Symptom**: Cannot connect to WebSocket or API

**Solution**:
```bash
# Check if service is running
curl http://localhost:8080/health

# Check if port is in use
lsof -i :8080

# View logs
docker logs ten_agent_dev
```

#### 2. No Audio Output

**Symptom**: Receiving audio data but cannot play

**Solution**:
- Check audio format matches (PCM 16kHz 16-bit)
- Verify audio data integrity
- Check browser audio permissions

```javascript
// Check browser audio permission
navigator.permissions.query({ name: 'microphone' })
  .then(result => console.log('Microphone permission:', result.state));
```

#### 3. Low Recognition Accuracy

**Symptom**: High STT error rate

**Solution**:
- Check audio quality (noise reduction, sample rate)
- Switch to more accurate STT model
- Adjust language settings

```json
{
  "stt": {
    "model": "nova-2",
    "language": "en-US",
    "punctuate": true,
    "diarize": false
  }
}
```

### Debugging Tools

#### Enable Verbose Logging

```bash
# Set log level
export TEN_LOG_LEVEL=debug

# Run service
task run
```

#### Monitor WebSocket Messages

```javascript
// In browser console
const originalSend = WebSocket.prototype.send;
WebSocket.prototype.send = function(data) {
  console.log('Sending:', data);
  return originalSend.apply(this, arguments);
};
```

## Next Steps

- [View Full API Documentation](https://theten.ai/docs/api)
- [Browse More Examples](../README.md)
- [Join Community Discussion](https://discord.gg/VnPftUzAMJ)
- [Submit Feedback](https://github.com/TEN-framework/ten-framework/issues)

## Get Help

- **Documentation**: https://theten.ai/docs
- **Discord**: https://discord.gg/VnPftUzAMJ
- **WeChat**: https://github.com/TEN-framework/ten-agent/discussions/170
- **GitHub Issues**: https://github.com/TEN-framework/ten-framework/issues
