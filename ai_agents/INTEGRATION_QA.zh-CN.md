# TEN Framework 集成问答指南

本文档回答关于 TEN Framework 集成的三个关键问题。

## 目录

1. [问题 1：API 访问端点](#问题-1api-访问端点)
2. [问题 2：包导入使用](#问题-2包导入使用)
3. [问题 3：音频处理最小示例](#问题-3音频处理最小示例)
4. [附录：完整代码示例](#附录完整代码示例)

---

## 问题 1：API 访问端点

### 用户疑问

> "API 访问是指 dockers 启动后可以使用 POST /api/session 和 POST /api/session/{session_id}/message 访问吗？但是我没有在代码中找到这两个接口。"

### 答案

**简短回答**：❌ `/api/session` 等接口在某些文档中提到，但在实际代码中**不存在**。

**详细说明**：

#### 实际存在的 API 端点

TEN Framework 的 HTTP Server（位于 `ai_agents/server/internal/http_server.go`）实际提供的端点是：

| 端点 | 方法 | 说明 | 请求体示例 |
|------|------|------|-----------|
| `/start` | POST | 启动一个新的语音助手会话 | 见下文 |
| `/stop` | POST | 停止指定会话 | `{"channel_name": "xxx"}` |
| `/ping` | POST | 心跳检测，保持会话活跃 | `{"channel_name": "xxx"}` |
| `/list` | GET | 列出所有活跃会话 | 无 |
| `/token/generate` | POST | 生成 Agora RTC Token | `{"channel_name": "xxx", "uid": 0}` |
| `/graphs` | GET | 获取可用的图配置列表 | 无 |
| `/health` | GET | 健康检查 | 无 |

#### `/start` 端点详解

这是最重要的端点，用于启动一个新的语音助手会话。

**请求示例**：
```bash
curl -X POST http://localhost:8080/start \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "unique-request-id",
    "channel_name": "my-channel-001",
    "graph_name": "voice_assistant",
    "user_uid": 176,
    "bot_uid": 123
  }'
```

**请求字段说明**：
- `request_id`：可选，请求的唯一标识符
- `channel_name`：**必需**，频道名称（会话标识）
- `graph_name`：**必需**，要使用的图配置名称（如 `voice_assistant`）
- `user_uid`：可选，用户的 UID（默认 176）
- `bot_uid`：可选，机器人的 UID（默认 123）

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "channel_name": "my-channel-001",
    "token": "your-agora-token"
  },
  "msg": "success"
}
```

#### 为什么找不到 `/api/session`？

1. **文档错误**：某些早期文档或示例可能使用了 `/api/session` 作为示例端点，但实际实现使用的是 `/start`
2. **架构演进**：TEN Framework 可能在开发过程中更改了 API 设计
3. **RESTful 风格差异**：`/start` 更直接地表达了"启动会话"的动作

#### 如何使用实际的 API

**完整的会话生命周期**：

```python
import requests

BASE_URL = "http://localhost:8080"

# 1. 启动会话
start_response = requests.post(f"{BASE_URL}/start", json={
    "channel_name": "my-channel-001",
    "graph_name": "voice_assistant"
})
start_data = start_response.json()
print(f"会话已启动: {start_data}")

# 2. 保持会话活跃（定期发送心跳）
ping_response = requests.post(f"{BASE_URL}/ping", json={
    "channel_name": "my-channel-001"
})
print(f"心跳响应: {ping_response.json()}")

# 3. 列出所有会话
list_response = requests.get(f"{BASE_URL}/list")
print(f"活跃会话: {list_response.json()}")

# 4. 停止会话
stop_response = requests.post(f"{BASE_URL}/stop", json={
    "channel_name": "my-channel-001"
})
print(f"会话已停止: {stop_response.json()}")
```

#### 音频数据的传输方式

**重要**：音频数据不是通过 HTTP REST API 传输的，而是通过以下方式：

1. **WebSocket**：实时双向通信
2. **Agora RTC**：使用 Agora 的实时通信 SDK
3. **自定义扩展**：开发扩展来处理音频流

详见[问题 3](#问题-3音频处理最小示例)。

---

## 问题 2：包导入使用

### 用户疑问

> "如果我像一个包一样的导入到我的项目中使用它，比如 random 之类的，可以吗？不用下载原始代码，我只需要下载包导入包然后使用它。"

### 答案

**简短回答**：❌ TEN Framework **不能**像 `random` 那样直接 `import` 使用。

**详细说明**：

#### 为什么不能像包一样导入？

TEN Framework 和普通 Python 库有本质区别：

| 对比项 | Python 库（如 random） | TEN Framework |
|--------|----------------------|---------------|
| **类型** | Python 模块/库 | 完整的应用框架 |
| **架构** | 单一语言（Python） | 多语言（Go server + Python extensions） |
| **运行模式** | 在你的进程中运行 | 需要独立的服务进程 |
| **通信方式** | 直接函数调用 | HTTP API / WebSocket / RTC |
| **依赖** | Python 即可 | Go、Python、tman、配置文件等 |
| **启动方式** | 无需启动 | 需要启动 server 和 worker |
| **状态管理** | 无状态或简单状态 | 复杂的会话和状态管理 |
| **适用场景** | 简单的功能调用 | 复杂的多模态处理流水线 |

#### TEN Framework 的架构

```
你的 Python 应用
    ↓ (HTTP/WebSocket)
TEN HTTP Server (Go)
    ↓
TEN Worker Process
    ↓
TEN Runtime (Python)
    ↓
Extensions (STT/LLM/TTS/etc.)
```

这是一个**微服务架构**，不是一个可以直接导入的库。

#### 如何集成 TEN Framework 到你的项目？

虽然不能直接 `import`，但有多种集成方式：

### 方式 1：HTTP API 调用（推荐）

**优点**：
- ✅ 最简单，不需要修改 TEN Framework
- ✅ 语言无关，任何语言都可以调用
- ✅ 容器化部署，隔离性好
- ✅ 易于扩展和维护

**使用方式**：
```python
import requests

# 你的应用代码
def process_audio_with_ten(audio_bytes):
    # 1. 启动 TEN Framework 会话
    response = requests.post("http://localhost:8080/start", json={
        "channel_name": "my-session",
        "graph_name": "voice_assistant"
    })
    
    # 2. 通过 WebSocket 或自定义扩展发送音频
    # （详见问题 3）
    
    # 3. 接收处理结果
    # ...
    
    return result
```

**部署方式**：
```bash
# 在 Docker 中运行 TEN Framework
cd ai_agents
docker compose up -d

# 你的应用通过 HTTP 调用 TEN
python your_app.py
```

### 方式 2：创建自定义扩展（深度集成）

如果你需要深度集成，可以创建一个 TEN 扩展：

**优点**：
- ✅ 完全集成到 TEN 生态
- ✅ 可以访问所有 TEN 内部功能
- ✅ 性能最优（无网络开销）

**缺点**：
- ❌ 需要学习 TEN 扩展开发
- ❌ 需要修改 property.json
- ❌ 需要重新构建和部署

**示例**：
```python
# agents/ten_packages/extension/my_custom_extension/extension.py
from ten_runtime import Extension, Cmd, Data

class MyCustomExtension(Extension):
    async def on_start(self, ten: TenEnv):
        # 初始化你的逻辑
        pass
    
    async def on_data(self, ten: TenEnv, data: Data):
        # 处理接收到的数据
        audio_bytes = data.get_buf("audio")
        # 你的处理逻辑
        result = your_processing_logic(audio_bytes)
        # 发送结果
        out_data = Data.create("result")
        out_data.set_buf("audio", result)
        ten.send_data(out_data)
```

然后在 `property.json` 中配置：
```json
{
  "nodes": [
    {
      "type": "extension",
      "name": "my_custom_extension",
      "addon": "my_custom_extension_python",
      "extension_group": "default"
    }
  ]
}
```

### 方式 3：子进程调用（简单集成）

将 TEN Framework 作为子进程运行：

**优点**：
- ✅ 简单，不需要网络配置
- ✅ 适合单机应用

**缺点**：
- ❌ 进程管理复杂
- ❌ 性能开销较大

**示例**：
```python
import subprocess
import os

# 启动 TEN Framework
ten_process = subprocess.Popen(
    ["docker", "compose", "up"],
    cwd="/path/to/ai_agents",
    env=os.environ
)

# 等待启动
time.sleep(10)

# 使用 HTTP API 调用
# ...

# 停止
ten_process.terminate()
```

### 方式 4：使用 TEN Python SDK（如果可用）

TEN Framework 提供了 Python 绑定（`ten-runtime-python`），但这是用于**开发扩展**的，不是用于外部调用的：

```python
# 这是用于开发扩展的，不是用于导入使用的
from ten_runtime import Extension, TenEnv, Cmd, Data

# 你只能用它来开发扩展，不能直接调用现有功能
```

#### 推荐的集成方式总结

| 场景 | 推荐方式 | 复杂度 |
|------|---------|--------|
| 简单调用，不需要修改 TEN | HTTP API + Docker | ⭐ |
| 中等集成，需要自定义逻辑 | HTTP API + 自定义扩展 | ⭐⭐ |
| 深度集成，高性能要求 | 开发 TEN 扩展 | ⭐⭐⭐ |
| 单机应用 | 子进程 + HTTP API | ⭐⭐ |

**结论**：TEN Framework 不是一个可以 `import` 的库，而是一个需要作为服务运行的框架。推荐使用 HTTP API + Docker 的方式集成。

---

## 问题 3：音频处理最小示例

### 用户疑问

> "我提供以下最小实例，假如我传入的是一个二进制音频数据，请你补全中间传入 ten-framework 将二进制语音数据转为文本传入 qwen，再将 qwen 的回复转为二进制语音数据的代码并做相关注释说明。"

### 用户提供的代码骨架

```python
from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-111111111111111111111",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

voice = data['bytes']  # 从接口请求头中获取的二进制音频数据

# 此处进行 ten-framework 相关转换，如果有多种方式请一一说明
content = # ten-framework 转换后的结果

completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": f"{content}"}
    ]
)
response = completion.choices[0].message.content

# 此处进行 ten-framework 相关转换，转成二进制音频数据
```

### 答案

TEN Framework 处理音频数据有**4 种方式**，我将为每种方式提供完整的代码示例。

#### 方式 1：通过 HTTP API + WebSocket（推荐，最简单）

**说明**：
- 通过 HTTP API 启动会话
- 通过 WebSocket 发送音频数据
- TEN Framework 内部处理 STT → LLM → TTS
- 通过 WebSocket 接收结果

**完整代码**：

```python
import requests
import websocket
import json
import base64
import threading
import queue

class TENFrameworkClient:
    """TEN Framework 客户端，处理音频数据"""
    
    def __init__(self, base_url="http://localhost:8080", ws_url="ws://localhost:8080"):
        self.base_url = base_url
        self.ws_url = ws_url
        self.channel_name = None
        self.ws = None
        self.result_queue = queue.Queue()
        
    def start_session(self, channel_name="audio-session"):
        """启动 TEN Framework 会话"""
        self.channel_name = channel_name
        
        # 1. 调用 /start 端点启动会话
        response = requests.post(f"{self.base_url}/start", json={
            "channel_name": channel_name,
            "graph_name": "voice_assistant",  # 使用语音助手图配置
            "user_uid": 176,
            "bot_uid": 123
        })
        
        if response.status_code != 200:
            raise Exception(f"启动会话失败: {response.text}")
        
        result = response.json()
        print(f"会话已启动: {result}")
        
        # 2. 建立 WebSocket 连接
        self._connect_websocket()
        
        return result
    
    def _connect_websocket(self):
        """建立 WebSocket 连接"""
        ws_url = f"{self.ws_url}/ws?channel={self.channel_name}"
        
        def on_message(ws, message):
            """接收 WebSocket 消息"""
            try:
                data = json.loads(message)
                print(f"收到消息: {data.get('type', 'unknown')}")
                
                # 如果是音频响应，放入队列
                if data.get('type') == 'audio_response':
                    self.result_queue.put(data)
                    
            except Exception as e:
                print(f"处理消息错误: {e}")
        
        def on_error(ws, error):
            print(f"WebSocket 错误: {error}")
        
        def on_close(ws, close_status_code, close_msg):
            print("WebSocket 连接已关闭")
        
        def on_open(ws):
            print("WebSocket 连接已建立")
        
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open
        )
        
        # 在后台线程运行 WebSocket
        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # 等待连接建立
        import time
        time.sleep(2)
    
    def process_audio(self, audio_bytes):
        """
        处理音频数据：二进制音频 → 文本 → LLM → 音频
        
        参数:
            audio_bytes: 二进制音频数据（PCM/WAV/MP3等）
        
        返回:
            二进制音频数据（TTS 生成的语音）
        """
        # 1. 将音频数据编码为 base64
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        # 2. 构造发送给 TEN Framework 的消息
        message = {
            "type": "audio_input",
            "data": {
                "audio": audio_base64,
                "format": "pcm",  # 或 "wav", "mp3" 等
                "sample_rate": 16000,
                "channels": 1
            }
        }
        
        # 3. 通过 WebSocket 发送音频数据
        self.ws.send(json.dumps(message))
        print("音频数据已发送")
        
        # 4. 等待 TEN Framework 处理并返回结果
        # TEN Framework 内部会：
        #   - STT: 将音频转为文本
        #   - LLM: 文本发送给 Qwen 处理
        #   - TTS: 将回复转为音频
        try:
            result = self.result_queue.get(timeout=30)  # 等待最多30秒
            
            # 5. 解码返回的音频数据
            audio_response_base64 = result['data']['audio']
            audio_response_bytes = base64.b64decode(audio_response_base64)
            
            print(f"收到音频响应，大小: {len(audio_response_bytes)} 字节")
            return audio_response_bytes
            
        except queue.Empty:
            raise Exception("等待响应超时")
    
    def stop_session(self):
        """停止会话"""
        if self.ws:
            self.ws.close()
        
        response = requests.post(f"{self.base_url}/stop", json={
            "channel_name": self.channel_name
        })
        print(f"会话已停止: {response.json()}")


# 使用示例
def main():
    # 假设从某个地方获取了二进制音频数据
    voice = data['bytes']  # 二进制音频数据
    
    # 创建 TEN Framework 客户端
    client = TENFrameworkClient()
    
    try:
        # 启动会话
        client.start_session("my-audio-session")
        
        # 处理音频：STT → LLM → TTS
        # 这一步 TEN Framework 会自动完成所有转换
        audio_response = client.process_audio(voice)
        
        # 现在 audio_response 就是 TTS 生成的二进制音频数据
        print(f"处理完成，响应音频大小: {len(audio_response)} 字节")
        
        # 你可以：
        # - 保存为文件: with open("response.wav", "wb") as f: f.write(audio_response)
        # - 返回给客户端: return audio_response
        # - 播放音频: ...
        
    finally:
        # 清理会话
        client.stop_session()

if __name__ == "__main__":
    main()
```

**注意**：
1. 这个示例假设 TEN Framework 配置了自定义的 WebSocket 扩展来接收音频
2. 实际的 WebSocket 消息格式需要根据你的扩展实现调整
3. 如果使用 Agora RTC，流程会不同（见方式 2）

#### 方式 2：使用 Agora RTC SDK（TEN Framework 默认方式）

**说明**：
TEN Framework 默认使用 Agora RTC 进行音频传输，这是最标准的方式。

**完整代码**：

```python
import requests
from agora_python_sdk import RtcEngine, RtcEngineConfig
import threading
import time

class TENFrameworkAgoraClient:
    """通过 Agora RTC 使用 TEN Framework"""
    
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.channel_name = None
        self.token = None
        self.rtc_engine = None
        self.audio_response = None
        
    def start_session(self, channel_name="agora-session"):
        """启动会话并获取 Token"""
        self.channel_name = channel_name
        
        # 1. 启动 TEN Framework 会话
        response = requests.post(f"{self.base_url}/start", json={
            "channel_name": channel_name,
            "graph_name": "voice_assistant",
            "user_uid": 176,
            "bot_uid": 123
        })
        
        result = response.json()
        self.token = result['data']['token']
        print(f"会话已启动，Token: {self.token[:20]}...")
        
        # 2. 初始化 Agora RTC
        config = RtcEngineConfig()
        config.app_id = "YOUR_AGORA_APP_ID"  # 从 .env 读取
        self.rtc_engine = RtcEngine(config)
        
        # 3. 设置音频回调
        self.rtc_engine.register_audio_frame_observer(self._on_audio_frame)
        
        # 4. 加入频道
        self.rtc_engine.join_channel(
            token=self.token,
            channel_id=channel_name,
            uid=176
        )
        
        print("已加入 Agora 频道")
        
    def _on_audio_frame(self, audio_frame):
        """接收音频帧回调"""
        # 这是 TEN Framework（bot）发送的音频响应
        self.audio_response = audio_frame.buffer
        print(f"收到音频帧: {len(audio_frame.buffer)} 字节")
    
    def process_audio(self, audio_bytes):
        """
        通过 Agora RTC 发送音频
        
        参数:
            audio_bytes: 二进制音频数据
        
        返回:
            TEN Framework 处理后的音频数据
        """
        # 1. 将音频数据发送到 Agora 频道
        # TEN Framework 的 bot 会接收并处理
        self.rtc_engine.push_audio_frame(audio_bytes)
        print("音频已发送到 Agora 频道")
        
        # 2. 等待 TEN Framework 处理并返回
        # bot 会执行: STT → LLM → TTS
        timeout = 30
        start_time = time.time()
        
        while self.audio_response is None:
            if time.time() - start_time > timeout:
                raise Exception("等待响应超时")
            time.sleep(0.1)
        
        # 3. 返回音频响应
        response = self.audio_response
        self.audio_response = None  # 重置
        return response
    
    def stop_session(self):
        """停止会话"""
        if self.rtc_engine:
            self.rtc_engine.leave_channel()
        
        requests.post(f"{self.base_url}/stop", json={
            "channel_name": self.channel_name
        })
        print("会话已停止")


# 使用示例
def main():
    voice = data['bytes']  # 二进制音频数据
    
    client = TENFrameworkAgoraClient()
    
    try:
        client.start_session("agora-test")
        audio_response = client.process_audio(voice)
        print(f"响应音频大小: {len(audio_response)} 字节")
    finally:
        client.stop_session()
```

**注意**：
1. 需要安装 Agora Python SDK: `pip install agora-python-sdk`
2. 需要有效的 Agora App ID 和 Token
3. 这是 TEN Framework 的标准使用方式

#### 方式 3：创建自定义扩展（深度集成）

**说明**：
如果你需要完全控制处理流程，可以创建一个自定义扩展。

**步骤**：

1. 创建扩展目录：
```bash
cd ai_agents/agents/ten_packages/extension
mkdir my_audio_processor_python
cd my_audio_processor_python
```

2. 创建 `extension.py`：

```python
# agents/ten_packages/extension/my_audio_processor_python/extension.py
from ten_runtime import Extension, TenEnv, Cmd, Data, AudioFrame, StatusCode
import base64

class MyAudioProcessorExtension(Extension):
    """自定义音频处理扩展"""
    
    async def on_start(self, ten: TenEnv):
        """扩展初始化"""
        ten.log_info("MyAudioProcessor 扩展已启动")
        # 初始化你的服务（如果需要）
    
    async def on_data(self, ten: TenEnv, data: Data):
        """
        处理接收到的数据
        
        这个方法会在收到音频数据时被调用
        """
        # 1. 获取输入的音频数据
        audio_bytes = data.get_buf("audio")
        ten.log_info(f"收到音频数据: {len(audio_bytes)} 字节")
        
        # 2. 发送音频给 STT 扩展进行语音识别
        stt_cmd = Cmd.create("transcribe")
        stt_cmd.set_buf("audio", audio_bytes)
        
        # 发送命令并等待结果
        stt_result = await ten.send_cmd(stt_cmd)
        
        if stt_result.get_status_code() != StatusCode.OK:
            ten.log_error("STT 处理失败")
            return
        
        # 3. 获取识别的文本
        transcribed_text = stt_result.get_property_string("text")
        ten.log_info(f"识别的文本: {transcribed_text}")
        
        # 4. 将文本发送给 LLM（这里使用你自己的 Qwen 客户端）
        from openai import OpenAI
        
        client = OpenAI(
            api_key=ten.get_property_string("qwen_api_key"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "user", "content": transcribed_text}
            ]
        )
        llm_response = completion.choices[0].message.content
        ten.log_info(f"LLM 响应: {llm_response}")
        
        # 5. 将 LLM 响应发送给 TTS 扩展
        tts_cmd = Cmd.create("synthesize")
        tts_cmd.set_property_string("text", llm_response)
        
        tts_result = await ten.send_cmd(tts_cmd)
        
        if tts_result.get_status_code() != StatusCode.OK:
            ten.log_error("TTS 处理失败")
            return
        
        # 6. 获取 TTS 生成的音频
        response_audio = tts_result.get_buf("audio")
        ten.log_info(f"TTS 音频大小: {len(response_audio)} 字节")
        
        # 7. 将结果发送回客户端
        output_data = Data.create("audio_response")
        output_data.set_buf("audio", response_audio)
        ten.send_data(output_data)
        
        ten.log_info("音频处理完成")
    
    async def on_cmd(self, ten: TenEnv, cmd: Cmd):
        """处理命令"""
        cmd_name = cmd.get_name()
        ten.log_info(f"收到命令: {cmd_name}")
        
        # 可以在这里处理自定义命令
        pass


# 注册扩展
def register(addon):
    addon.register_extension("my_audio_processor", MyAudioProcessorExtension)
```

3. 在 `property.json` 中配置：

```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "custom_audio_processor",
        "auto_start": false,
        "nodes": [
          {
            "type": "extension",
            "name": "my_audio_processor",
            "addon": "my_audio_processor_python",
            "extension_group": "default"
          },
          {
            "type": "extension",
            "name": "deepgram_asr",
            "addon": "deepgram_asr_python",
            "extension_group": "default"
          },
          {
            "type": "extension",
            "name": "bytedance_tts",
            "addon": "bytedance_tts_duplex",
            "extension_group": "default"
          }
        ],
        "connections": [
          {
            "extension": "my_audio_processor",
            "data": [
              {"name": "transcribe", "dest": [{"extension": "deepgram_asr"}]}
            ]
          }
        ]
      }
    ]
  }
}
```

4. 使用：

```python
# 通过 HTTP API 启动这个自定义图
response = requests.post("http://localhost:8080/start", json={
    "channel_name": "custom-session",
    "graph_name": "custom_audio_processor"  # 使用你的自定义图
})

# 然后通过 WebSocket 或 Agora 发送音频
```

#### 方式 4：使用子进程（最简单但不推荐）

如果你只想快速测试，可以将 TEN Framework 作为黑盒子使用：

```python
import subprocess
import os
import tempfile
import time
import requests

def process_audio_with_ten_subprocess(audio_bytes):
    """
    通过子进程使用 TEN Framework
    
    这种方式最简单，但不适合生产环境
    """
    # 1. 将音频保存为临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pcm') as f:
        audio_input_path = f.name
        f.write(audio_bytes)
    
    # 2. 启动 TEN Framework（如果还没运行）
    # 假设 TEN Framework 已经通过 Docker 运行在后台
    
    # 3. 使用 HTTP API
    response = requests.post("http://localhost:8080/start", json={
        "channel_name": "subprocess-session",
        "graph_name": "voice_assistant"
    })
    
    # 4. 这里需要实现音频发送逻辑（WebSocket 或 Agora）
    # 见方式 1 或方式 2
    
    # 5. 接收结果并保存
    audio_output_path = tempfile.mktemp(suffix='.pcm')
    
    # ... 等待并接收音频响应 ...
    
    # 6. 读取结果
    with open(audio_output_path, 'rb') as f:
        audio_response = f.read()
    
    # 7. 清理
    os.unlink(audio_input_path)
    os.unlink(audio_output_path)
    
    return audio_response
```

### 四种方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **HTTP API + WebSocket** | 简单、灵活、语言无关 | 需要网络通信 | 大多数场景（推荐） |
| **Agora RTC SDK** | TEN 标准方式、低延迟 | 需要 Agora 账号 | 实时语音通话 |
| **自定义扩展** | 完全控制、高性能 | 开发复杂度高 | 深度定制需求 |
| **子进程** | 最简单 | 性能差、难维护 | 快速原型 |

### 推荐流程

对于你的需求（二进制音频 → 文本 → LLM → 音频），推荐使用**方式 1（HTTP API + WebSocket）**：

```python
# 1. 使用 Docker 启动 TEN Framework
# docker compose up -d

# 2. 使用上面的 TENFrameworkClient
client = TENFrameworkClient()
client.start_session("my-session")

# 3. 处理音频（一行代码）
audio_response = client.process_audio(voice)

# 4. 完成
client.stop_session()
```

所有的 STT → LLM → TTS 转换都由 TEN Framework 自动完成。

---

## 附录：完整代码示例

完整的、可直接运行的代码示例请参见：
- `audio_processing_examples.py` - 包含所有 4 种方式的完整代码

## 总结

1. **API 端点**：使用 `/start`、`/stop`、`/ping` 等端点，不是 `/api/session`
2. **包导入**：TEN Framework 不能像 `random` 那样导入，需要作为服务运行
3. **音频处理**：推荐使用 HTTP API + WebSocket 方式，简单且灵活

## 相关文档

- [Docker 安装指南](DOCKER_ONLY_SETUP.zh-CN.md)
- [配置修改指南](agents/examples/voice-assistant/CONFIG_MODIFICATION_GUIDE.zh-CN.md)
- [集成指南](agents/examples/voice-assistant/VOICE_INTEGRATION_GUIDE.zh-CN.md)

## 获取帮助

- GitHub Issues: https://github.com/TEN-framework/ten-framework/issues
- Discord: https://discord.gg/VnPftUzAMJ
