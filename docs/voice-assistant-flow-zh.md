# TEN Framework 语音助手完整数据流程详解

本文档详细说明 TEN Framework 语音助手从用户语音输入到音频输出的完整数据流转过程。

## 目录

1. [完整流程概览](#完整流程概览)
2. [详细流程说明](#详细流程说明)
3. [所有接口列表](#所有接口列表)
4. [数据结构说明](#数据结构说明)
5. [配置文件说明](#配置文件说明)

---

## 完整流程概览

```
用户语音输入
    ↓
Agora RTC Extension (接收 pcm_frame AudioFrame)
    ↓ [pcm_frame AudioFrame]
Stream ID Adapter Extension (添加会话元数据)
    ↓ [pcm_frame AudioFrame]
ASR Extension (语音识别：Deepgram/OpenAI/Azure 等)
    ↓ [asr_result Data + 文本]
Main Control Extension (主控扩展 - 协调器)
    ↓ [排队到 LLM]
LLM Extension (大语言模型：OpenAI/Coze 等)
    ↓ [LLM 响应流]
Main Control Extension (文本解析 + 句子分割)
    ↓ [tts_text_input Data]
TTS Extension (语音合成：ElevenLabs/Azure 等)
    ↓ [pcm_frame AudioFrame]
Agora RTC Extension (发布音频)
    ↓
用户音频输出
```

---

## 详细流程说明

### 第一步：用户语音输入

#### 1.1 接口入口

**文件位置：** `core/src/ten_runtime/binding/python/interface/ten_runtime/audio_frame.py`

**类名：** `AudioFrame`

**接收位置：** Agora RTC Extension

**函数：** `on_audio_frame(ten_env: AsyncTenEnv, frame: AudioFrame)`

**输入参数：**
- `ten_env`: TEN 环境对象，用于发送消息和日志记录
- `frame`: AudioFrame 对象，包含以下属性：
  - `data`: bytes - PCM 音频原始数据
  - `sample_rate`: int - 采样率（如 16000, 24000, 48000）
  - `samples_per_channel`: int - 每通道的样本数
  - `bytes_per_sample`: int - 每样本字节数（通常为 2，表示 16 位）
  - `number_of_channels`: int - 声道数（1 = 单声道，2 = 立体声）
  - `timestamp`: int - 时间戳（毫秒）
  - `data_fmt`: AudioFrameDataFmt - 数据格式（交错或非交错）

**AudioFrame 创建方法：**
```python
frame = AudioFrame.create("pcm_frame")
frame.set_sample_rate(16000)
frame.set_bytes_per_sample(2)
frame.set_number_of_channels(1)
frame.set_data_fmt(AudioFrameDataFmt.INTERLEAVE)
frame.alloc_buf(buffer_size)
buf = frame.lock_buf()
# 写入 PCM 数据到 buf
frame.unlock_buf(buf)
```

**处理函数：** Agora RTC Extension 中的 `on_audio_frame()`

**输出：** 转发 `pcm_frame` AudioFrame 到下一个扩展（Stream ID Adapter）

---

### 第二步：Stream ID 适配

**文件位置：** `ai_agents/agents/ten_packages/extension/streamid_adapter/extension.py`

**类名：** `StreamIdAdapterExtension(AsyncExtension)`

**函数：** `async def on_audio_frame(ten_env: AsyncTenEnv, frame: AudioFrame)`

**输入参数：**
- `frame`: AudioFrame 对象，包含 `stream_id` 属性

**处理逻辑：**
```python
async def on_audio_frame(self, ten_env: AsyncTenEnv, frame: AudioFrame) -> None:
    # 1. 获取 stream_id
    stream_id, _ = frame.get_property_int("stream_id")
    
    # 2. 将 stream_id 转换为 session_id 并添加到元数据
    frame.set_property_from_json(
        "metadata",
        json.dumps({
            "session_id": f"{stream_id}",
        })
    )
    
    # 3. 转发音频帧
    await ten_env.send_audio_frame(audio_frame=frame)
```

**输出：** 添加了 `metadata` 的 AudioFrame，转发到 ASR Extension

---

### 第三步：ASR (自动语音识别)

**文件位置：** `packages/core_extensions/default_asr_extension_python/extension.py`

**基类：** `AsyncASRBaseExtension`

**具体实现示例：** 
- `ai_agents/agents/ten_packages/extension/deepgram_asr_python/extension.py`
- `ai_agents/agents/ten_packages/extension/openai_asr_python/extension.py`
- `ai_agents/agents/ten_packages/extension/azure_asr_python/extension.py`

#### 3.1 接收音频帧

**函数：** `async def on_audio_frame(ten_env: AsyncTenEnv, frame: AudioFrame)`

**输入参数：**
- `frame`: AudioFrame 对象，包含 PCM 音频数据

**处理流程：**
```python
async def on_audio_frame(self, ten_env: AsyncTenEnv, frame: AudioFrame) -> None:
    # 1. 从帧中提取元数据
    metadata = frame.get_property_to_json("metadata")
    session_id = json.loads(metadata)["session_id"]
    
    # 2. 获取音频数据
    buf = frame.lock_buf()
    audio_data = bytes(buf)
    frame.unlock_buf(buf)
    
    # 3. 发送到 ASR 供应商
    await self.send_audio(audio_data, session_id)
```

#### 3.2 ASR 关键方法

**初始化连接：**
```python
async def start_connection(self, ten_env: AsyncTenEnv) -> None:
    # 建立与 ASR 服务的连接（WebSocket/HTTP）
    pass
```

**发送音频：**
```python
async def send_audio(self, audio_data: bytes, session_id: str) -> None:
    # 将 PCM 数据发送到 ASR 服务进行识别
    pass
```

**接收识别结果（回调）：**
```python
async def on_transcription_result(self, text: str, is_final: bool, session_id: str):
    # 创建 ASR 结果对象
    result = ASRResult(
        text=text,
        is_final=is_final,
        stream_id=session_id
    )
    
    # 发送结果到下游
    await self.send_asr_result(result)
```

#### 3.3 输出 ASR 结果

**输出函数：** `async def send_asr_result(result: ASRResult)`

**输出数据类型：** `Data` 对象，名称为 `"asr_result"`

**数据结构：**
```python
data = Data.create("asr_result")
data.set_property_from_json(None, json.dumps({
    "text": "你好，我需要帮助",
    "is_final": True,
    "stream_id": "100",
    "timestamp": 1234567890
}))
```

**输出目标：** Main Control Extension

---

### 第四步：Main Control Extension (主控扩展)

**文件位置：** `ai_agents/agents/examples/voice-assistant/tenapp/ten_packages/extension/main_python/extension.py`

**类名：** `MainControlExtension(AsyncExtension)`

**Agent 类位置：** `agent/agent.py`

#### 4.1 接收 ASR 结果

**函数：** `async def on_data(ten_env: AsyncTenEnv, data: Data)`

**输入参数：**
- `data`: Data 对象，名称为 `"asr_result"`

**处理逻辑：**
```python
async def on_data(self, ten_env: AsyncTenEnv, data: Data) -> None:
    # 1. 获取数据名称
    data_name = data.get_name()
    
    if data_name == "asr_result":
        # 2. 解析 ASR 结果
        asr_json = data.get_property_to_json(None)
        asr_data = json.loads(asr_json)
        
        text = asr_data.get("text", "")
        is_final = asr_data.get("is_final", False)
        stream_id = asr_data.get("stream_id", "")
        
        # 3. 创建 ASR 事件并发送到 Agent
        event = ASRResultEvent(
            text=text,
            is_final=is_final,
            stream_id=stream_id
        )
        
        # 4. 触发 Agent 处理
        await self._emit_asr(event)
```

#### 4.2 Agent 处理 ASR 事件

**文件位置：** `agent/agent.py`

**函数：** `async def on_asr_result(event: ASRResultEvent)`

**处理流程：**
```python
async def on_asr_result(self, event: ASRResultEvent):
    # 1. 累积 ASR 文本
    self.accumulated_text += event.text
    
    # 2. 如果是最终结果，触发 LLM 处理
    if event.is_final:
        # 3. 构建 LLM 请求
        llm_request = LLMRequest(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.accumulated_text}
            ],
            tools=self.registered_tools  # 如果有工具
        )
        
        # 4. 调用 LLM 执行器
        await self.llm_exec.execute(llm_request)
        
        # 5. 重置累积文本
        self.accumulated_text = ""
```

---

### 第五步：LLM (大语言模型) 处理

**文件位置：** `packages/core_extensions/default_llm_extension_python/extension.py`

**基类：** `AsyncLLM2BaseExtension`

**具体实现示例：**
- `ai_agents/agents/ten_packages/extension/openai_llm2_python/extension.py`
- `ai_agents/agents/ten_packages/extension/coze_llm2_python/extension.py`
- `ai_agents/agents/ten_packages/extension/gemini_llm2_python/extension.py`

#### 5.1 LLM 请求

**函数：** `async def on_call_chat_completion(ten_env: AsyncTenEnv, input: LLMRequest) -> AsyncGenerator[LLMResponse, None]`

**输入参数：**
- `input`: LLMRequest 对象
  ```python
  class LLMRequest:
      messages: list[dict]  # 对话历史
      temperature: float = 0.7
      max_tokens: int = 2048
      top_p: float = 1.0
      stream: bool = True
      tools: list[dict] = []  # 可用工具列表
  ```

**LLM 请求示例：**
```python
request = LLMRequest(
    messages=[
        {
            "role": "system",
            "content": "你是一个有帮助的AI助手"
        },
        {
            "role": "user",
            "content": "你好，我需要帮助"
        }
    ],
    temperature=0.7,
    max_tokens=1024,
    stream=True
)
```

#### 5.2 LLM 响应流

**返回类型：** `AsyncGenerator[LLMResponse, None]`

**LLMResponse 结构：**
```python
class LLMResponse:
    delta: str          # 增量文本片段（当前块）
    text: str           # 累积的完整文本
    is_final: bool      # 是否为最后一个响应块
    tool_calls: list    # 工具调用（如果有）
```

**流式响应处理：**
```python
async def on_call_chat_completion(self, ten_env, input):
    # 1. 调用 LLM API（如 OpenAI）
    response_stream = await openai.chat.completions.create(
        model="gpt-4",
        messages=input.messages,
        stream=True
    )
    
    # 2. 流式产出响应
    accumulated_text = ""
    async for chunk in response_stream:
        delta = chunk.choices[0].delta.content or ""
        accumulated_text += delta
        
        # 3. Yield LLM 响应
        yield LLMResponse(
            delta=delta,
            text=accumulated_text,
            is_final=chunk.choices[0].finish_reason is not None
        )
```

#### 5.3 Agent 接收 LLM 响应

**文件位置：** `agent/llm_exec.py`

**类名：** `LLMExec`

**函数：** `async def on_response(delta: str, text: str, is_final: bool)`

**处理逻辑：**
```python
async def on_response(self, delta: str, text: str, is_final: bool):
    # 1. 累积响应文本
    self.current_text += delta
    
    # 2. 句子分割（用于流式 TTS）
    sentences = parse_sentences(self.current_text)
    
    # 3. 对每个完整句子触发 TTS
    for sentence in sentences:
        if sentence not in self.sent_sentences:
            await self._send_to_tts(sentence, is_final=False)
            self.sent_sentences.add(sentence)
    
    # 4. 如果是最终响应，发送剩余文本
    if is_final:
        remaining_text = get_remaining_text(self.current_text, self.sent_sentences)
        if remaining_text:
            await self._send_to_tts(remaining_text, is_final=True)
```

---

### 第六步：发送到 TTS

**文件位置：** `extension.py` (Main Control)

**函数：** `async def _send_to_tts(text: str, is_final: bool)`

**处理逻辑：**
```python
async def _send_to_tts(self, text: str, is_final: bool):
    # 1. 创建 TTS 输入数据
    data = Data.create("tts_text_input")
    
    # 2. 设置 TTS 参数
    tts_input = {
        "request_id": f"tts-request-{self.turn_id}-{self.sentence_id}",
        "text": text,
        "text_input_end": is_final,
        "metadata": {
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "sentence_id": self.sentence_id
        }
    }
    
    # 3. 将数据序列化为 JSON
    data.set_property_from_json(None, json.dumps(tts_input))
    
    # 4. 发送到 TTS 扩展
    await self.ten_env.send_data(data)
    
    # 5. 增加句子计数
    self.sentence_id += 1
```

**输出数据结构：**
```json
{
    "request_id": "tts-request-0-1",
    "text": "你好，我可以帮助你。",
    "text_input_end": false,
    "metadata": {
        "session_id": "100",
        "turn_id": 0,
        "sentence_id": 1
    }
}
```

---

### 第七步：TTS (文本转语音) 处理

**文件位置：** `packages/core_extensions/default_tts_extension_python/extension.py`

**基类：** `AsyncTTS2BaseExtension`

**具体实现示例：**
- `ai_agents/agents/ten_packages/extension/elevenlabs_tts2_python/extension.py`
- `ai_agents/agents/ten_packages/extension/azure_tts_python/extension.py`
- `ai_agents/agents/ten_packages/extension/openai_tts2_python/extension.py`

#### 7.1 接收 TTS 文本输入

**函数：** `async def on_data(ten_env: AsyncTenEnv, data: Data)`

**输入参数：**
- `data`: Data 对象，名称为 `"tts_text_input"`

**处理逻辑：**
```python
async def on_data(self, ten_env: AsyncTenEnv, data: Data) -> None:
    # 1. 获取数据名称
    data_name = data.get_name()
    
    if data_name == "tts_text_input":
        # 2. 解析 TTS 输入
        data_json = data.get_property_to_json(None)
        text_input = TTSTextInput.model_validate_json(data_json)
        
        # 3. 调用 TTS 请求
        await self.request_tts(text_input)
```

#### 7.2 TTS 请求处理

**函数：** `async def request_tts(text_input: TTSTextInput)`

**TTSTextInput 结构：**
```python
class TTSTextInput(BaseModel):
    request_id: str
    text: str
    text_input_end: bool
    metadata: dict
```

**处理流程：**
```python
async def request_tts(self, text_input: TTSTextInput):
    # 1. 调用 TTS API（如 ElevenLabs）
    response = await elevenlabs.text_to_speech(
        text=text_input.text,
        voice_id=self.voice_id,
        model_id=self.model_id,
        output_format="pcm_16000"  # PCM 16kHz
    )
    
    # 2. 接收音频流
    async for audio_chunk in response:
        # 3. 创建音频帧
        await self._send_audio_chunk(audio_chunk, text_input)
```

#### 7.3 发送音频帧

**函数：** `async def send_audio_out(frame: AudioFrame)`

**处理逻辑：**
```python
async def _send_audio_chunk(self, audio_data: bytes, text_input: TTSTextInput):
    # 1. 创建音频帧
    frame = AudioFrame.create("pcm_frame")
    
    # 2. 设置音频参数
    frame.set_sample_rate(self.sample_rate)  # 如 16000
    frame.set_bytes_per_sample(2)  # 16-bit PCM
    frame.set_number_of_channels(1)  # 单声道
    frame.set_data_fmt(AudioFrameDataFmt.INTERLEAVE)
    
    # 3. 分配缓冲区并写入数据
    frame.alloc_buf(len(audio_data))
    buf = frame.lock_buf()
    buf[:] = audio_data
    frame.unlock_buf(buf)
    
    # 4. 设置元数据
    frame.set_property_from_json(
        "metadata",
        json.dumps(text_input.metadata)
    )
    
    # 5. 发送音频帧到下游（Agora RTC）
    await self.ten_env.send_audio_frame(frame)
```

**输出：** `pcm_frame` AudioFrame，发送到 Agora RTC Extension

---

### 第八步：音频输出

**处理位置：** Agora RTC Extension

**函数：** `on_audio_frame(ten_env, frame: AudioFrame)`

**处理逻辑：**
```python
def on_audio_frame(self, ten_env: TenEnv, frame: AudioFrame):
    # 1. 获取音频数据
    buf = frame.lock_buf()
    audio_data = bytes(buf)
    frame.unlock_buf(buf)
    
    # 2. 获取会话信息
    metadata = frame.get_property_to_json("metadata")
    session_id = json.loads(metadata)["session_id"]
    
    # 3. 通过 Agora RTC 发布音频到指定用户
    self.publish_audio(session_id, audio_data)
```

**输出：** 音频通过 Agora RTC 网络传输到用户端

---

## 所有接口列表

### 1. Extension 生命周期接口

#### 同步接口 (Extension 基类)

**文件：** `core/src/ten_runtime/binding/python/interface/ten_runtime/extension.py`

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `on_configure(ten_env)` | TenEnv | None | 配置阶段，在 init 之前 |
| `on_init(ten_env)` | TenEnv | None | 初始化资源 |
| `on_start(ten_env)` | TenEnv | None | 启动扩展，开始处理消息 |
| `on_stop(ten_env)` | TenEnv | None | 停止扩展 |
| `on_deinit(ten_env)` | TenEnv | None | 清理资源 |

#### 异步接口 (AsyncExtension 基类)

**文件：** `core/src/ten_runtime/binding/python/interface/ten_runtime/async_extension.py`

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `async on_configure(ten_env)` | AsyncTenEnv | None | 异步配置 |
| `async on_init(ten_env)` | AsyncTenEnv | None | 异步初始化 |
| `async on_start(ten_env)` | AsyncTenEnv | None | 异步启动 |
| `async on_stop(ten_env)` | AsyncTenEnv | None | 异步停止 |
| `async on_deinit(ten_env)` | AsyncTenEnv | None | 异步清理 |

---

### 2. 消息处理接口

#### 命令接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `on_cmd(ten_env, cmd)` | TenEnv, Cmd | None | 处理命令（同步） |
| `async on_cmd(ten_env, cmd)` | AsyncTenEnv, Cmd | None | 处理命令（异步） |

**Cmd 对象方法：**
- `cmd.get_name()` → str: 获取命令名称
- `cmd.get_property_string(key)` → str: 获取字符串属性
- `cmd.get_property_to_json(key)` → str: 获取 JSON 属性
- `cmd.set_property_*()`: 设置属性

**CmdResult 创建：**
```python
result = CmdResult.create(StatusCode.OK, cmd)
result.set_property_string("key", "value")
await ten_env.return_result(result)
```

#### 数据接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `on_data(ten_env, data)` | TenEnv, Data | None | 处理数据（同步） |
| `async on_data(ten_env, data)` | AsyncTenEnv, Data | None | 处理数据（异步） |

**Data 对象方法：**
- `data.get_name()` → str: 获取数据名称
- `data.get_property_to_json(key)` → str: 获取 JSON 数据
- `data.set_property_from_json(key, json_str)`: 设置 JSON 数据

**Data 创建：**
```python
data = Data.create("asr_result")
data.set_property_from_json(None, json.dumps({
    "text": "识别结果",
    "is_final": True
}))
await ten_env.send_data(data)
```

#### 音频帧接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `on_audio_frame(ten_env, frame)` | TenEnv, AudioFrame | None | 处理音频帧（同步） |
| `async on_audio_frame(ten_env, frame)` | AsyncTenEnv, AudioFrame | None | 处理音频帧（异步） |

**AudioFrame 对象方法：**
- `frame.get_sample_rate()` → int: 获取采样率
- `frame.get_bytes_per_sample()` → int: 获取每样本字节数
- `frame.get_number_of_channels()` → int: 获取声道数
- `frame.get_timestamp()` → int: 获取时间戳
- `frame.get_data_fmt()` → AudioFrameDataFmt: 获取数据格式
- `frame.lock_buf()` → memoryview: 锁定并访问缓冲区
- `frame.unlock_buf(buf)`: 解锁缓冲区
- `frame.alloc_buf(size)`: 分配缓冲区

**AudioFrame 创建：**
```python
frame = AudioFrame.create("pcm_frame")
frame.set_sample_rate(16000)
frame.set_bytes_per_sample(2)
frame.set_number_of_channels(1)
frame.set_data_fmt(AudioFrameDataFmt.INTERLEAVE)
frame.alloc_buf(buffer_size)
buf = frame.lock_buf()
buf[:] = audio_data
frame.unlock_buf(buf)
await ten_env.send_audio_frame(frame)
```

#### 视频帧接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `on_video_frame(ten_env, frame)` | TenEnv, VideoFrame | None | 处理视频帧（同步） |
| `async on_video_frame(ten_env, frame)` | AsyncTenEnv, VideoFrame | None | 处理视频帧（异步） |

---

### 3. TenEnv/AsyncTenEnv 接口

#### 发送消息接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `send_cmd(cmd, result_handler)` | Cmd, callable | None | 发送命令（同步） |
| `await send_cmd(cmd, result_handler)` | Cmd, callable | None | 发送命令（异步） |
| `send_data(data)` | Data | None | 发送数据（同步） |
| `await send_data(data)` | Data | None | 发送数据（异步） |
| `send_audio_frame(frame)` | AudioFrame | None | 发送音频帧（同步） |
| `await send_audio_frame(frame)` | AudioFrame | None | 发送音频帧（异步） |
| `send_video_frame(frame)` | VideoFrame | None | 发送视频帧（同步） |
| `await send_video_frame(frame)` | VideoFrame | None | 发送视频帧（异步） |
| `return_result(result)` | CmdResult | None | 返回命令结果（同步） |
| `await return_result(result)` | CmdResult | None | 返回命令结果（异步） |

#### 属性访问接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `get_property_string(key)` | str | str | 获取字符串属性 |
| `await get_property_string(key)` | str | str | 异步获取字符串属性 |
| `get_property_int(key)` | str | int | 获取整数属性 |
| `await get_property_int(key)` | str | int | 异步获取整数属性 |
| `get_property_float(key)` | str | float | 获取浮点数属性 |
| `await get_property_float(key)` | str | float | 异步获取浮点数属性 |
| `get_property_bool(key)` | str | bool | 获取布尔属性 |
| `await get_property_bool(key)` | str | bool | 异步获取布尔属性 |
| `get_property_to_json(key)` | str | str | 获取 JSON 属性 |
| `await get_property_to_json(key)` | str | str | 异步获取 JSON 属性 |
| `set_property_*()` | str, value | None | 设置各类属性 |

#### 日志接口

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `log_verbose(msg)` | str | None | 详细日志 |
| `log_debug(msg)` | str | None | 调试日志 |
| `log_info(msg)` | str | None | 信息日志 |
| `log_warn(msg)` | str | None | 警告日志 |
| `log_error(msg)` | str | None | 错误日志 |
| `log_fatal(msg)` | str | None | 致命错误日志 |

---

### 4. ASR 扩展接口

**基类：** `AsyncASRBaseExtension`

**文件：** `packages/core_extensions/default_asr_extension_python/extension.py`

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `async start_connection(ten_env)` | AsyncTenEnv | None | 启动 ASR 连接 |
| `async send_audio(data, session_id)` | bytes, str | None | 发送音频数据 |
| `async finalize(session_id)` | str | None | 结束会话 |
| `async stop_connection(ten_env)` | AsyncTenEnv | None | 停止连接 |
| `async send_asr_result(result)` | ASRResult | None | 发送识别结果 |

**ASRResult 结构：**
```python
class ASRResult:
    text: str           # 识别的文本
    is_final: bool      # 是否为最终结果
    stream_id: str      # 会话 ID
    timestamp: int      # 时间戳（可选）
```

---

### 5. LLM 扩展接口

**基类：** `AsyncLLM2BaseExtension`

**文件：** `packages/core_extensions/default_llm_extension_python/extension.py`

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `async on_call_chat_completion(ten_env, input)` | AsyncTenEnv, LLMRequest | AsyncGenerator[LLMResponse] | 调用 LLM 生成响应 |

**LLMRequest 结构：**
```python
class LLMRequest:
    messages: list[dict]        # 对话历史
    temperature: float = 0.7    # 温度参数
    max_tokens: int = 2048      # 最大 token 数
    top_p: float = 1.0          # Top-p 采样
    stream: bool = True         # 是否流式输出
    tools: list[dict] = []      # 可用工具
```

**LLMResponse 结构：**
```python
class LLMResponse:
    delta: str              # 增量文本
    text: str               # 累积文本
    is_final: bool          # 是否最终响应
    tool_calls: list = []   # 工具调用
```

---

### 6. TTS 扩展接口

**基类：** `AsyncTTS2BaseExtension`

**文件：** `packages/core_extensions/default_tts_extension_python/extension.py`

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `async request_tts(text_input)` | TTSTextInput | None | 请求语音合成 |
| `async send_audio_out(frame)` | AudioFrame | None | 发送合成的音频 |
| `synthesize_audio_sample_rate()` | None | int | 返回输出采样率 |

**TTSTextInput 结构：**
```python
class TTSTextInput(BaseModel):
    request_id: str         # 请求 ID
    text: str               # 要合成的文本
    text_input_end: bool    # 是否为最后一段文本
    metadata: dict          # 元数据（session_id 等）
```

---

### 7. LLM Tool 扩展接口

**基类：** `AsyncLLMToolBaseExtension`

**文件：** `ten_ai_base/llm_tool.py`

| 方法 | 输入 | 输出 | 说明 |
|------|------|------|------|
| `get_tool_metadata(ten_env)` | AsyncTenEnv | list[LLMToolMetadata] | 返回工具元数据 |
| `async run_tool(ten_env, name, args)` | AsyncTenEnv, str, dict | LLMToolResult | 执行工具 |

**LLMToolMetadata 结构：**
```python
class LLMToolMetadata:
    name: str                           # 工具名称
    description: str                    # 工具描述
    parameters: list[LLMToolMetadataParameter]  # 参数列表
```

**LLMToolMetadataParameter 结构：**
```python
class LLMToolMetadataParameter:
    name: str           # 参数名称
    type: str           # 参数类型（string, int, array 等）
    description: str    # 参数描述
    required: bool      # 是否必需
    items: dict = {}    # 数组类型的子项定义
```

**LLMToolResult 结构：**
```python
class LLMToolResult:
    type: str           # 结果类型（"llmresult" 等）
    content: str        # 结果内容（通常是 JSON）
```

---

## 数据结构说明

### AudioFrame 数据结构

**文件：** `core/src/ten_runtime/binding/python/interface/ten_runtime/audio_frame.py`

```python
class AudioFrame(Msg):
    # 属性
    name: str                       # 帧名称（通常是 "pcm_frame"）
    sample_rate: int                # 采样率（Hz）
    samples_per_channel: int        # 每通道样本数
    bytes_per_sample: int           # 每样本字节数（1, 2, 4）
    number_of_channels: int         # 声道数（1 = 单声道，2 = 立体声）
    timestamp: int                  # 时间戳（毫秒）
    data_fmt: AudioFrameDataFmt     # 数据格式
    
    # 数据格式枚举
    class AudioFrameDataFmt:
        INTERLEAVE = 1      # 交错格式：LRLRLR...
        NON_INTERLEAVE = 2  # 非交错格式：LLL...RRR...
```

**PCM 数据计算：**
```python
# 缓冲区大小 = 样本数 × 字节数 × 声道数
buffer_size = samples_per_channel * bytes_per_sample * number_of_channels

# 示例：16kHz, 16-bit, 单声道, 100ms 音频
sample_rate = 16000
duration_ms = 100
samples = int(sample_rate * duration_ms / 1000)  # 1600 samples
buffer_size = samples * 2 * 1  # 3200 bytes
```

---

### Data 数据结构

**文件：** `core/src/ten_runtime/binding/python/interface/ten_runtime/data.py`

```python
class Data(Msg):
    # 属性
    name: str           # 数据名称（如 "asr_result", "tts_text_input"）
    
    # 方法（继承自 Msg）
    def get_property_to_json(key: str) -> str
    def set_property_from_json(key: str, json_str: str)
    def get_property_string(key: str) -> str
    def set_property_string(key: str, value: str)
```

**常用 Data 类型：**

1. **asr_result** - ASR 识别结果
```json
{
    "text": "你好，我需要帮助",
    "is_final": true,
    "stream_id": "100",
    "timestamp": 1234567890
}
```

2. **tts_text_input** - TTS 文本输入
```json
{
    "request_id": "tts-request-0-1",
    "text": "你好，我可以帮助你。",
    "text_input_end": false,
    "metadata": {
        "session_id": "100",
        "turn_id": 0,
        "sentence_id": 1
    }
}
```

---

### Cmd 数据结构

**文件：** `core/src/ten_runtime/binding/python/interface/ten_runtime/cmd.py`

```python
class Cmd(Msg):
    # 属性
    name: str           # 命令名称
    
    # 方法
    def get_name() -> str
    def get_property_to_json(key: str) -> str
    def set_property_from_json(key: str, json_str: str)
```

**常用命令：**

1. **on_user_joined** - 用户加入
```json
{
    "stream_id": 100,
    "user_id": "user123"
}
```

2. **on_user_left** - 用户离开
```json
{
    "stream_id": 100,
    "user_id": "user123"
}
```

3. **tool_register** - 工具注册
```json
{
    "name": "get_weather",
    "description": "获取天气信息",
    "parameters": [...]
}
```

4. **tool_call** - 工具调用
```json
{
    "name": "get_weather",
    "args": {
        "city": "北京"
    }
}
```

5. **flush** - 刷新状态
```json
{}
```

---

### Msg 基类

**文件：** `core/src/ten_runtime/binding/python/interface/ten_runtime/msg.py`

```python
class Msg:
    # 获取消息源
    def get_source() -> Loc
    
    # 设置目标
    def set_dest(app_uri: str, graph_id: str, extension_name: str)
    def set_dests(locs: list[Loc])
    
    # 属性访问
    def get_property_*(key: str) -> value
    def set_property_*(key: str, value)
    def get_property_to_json(key: str) -> str
    def set_property_from_json(key: str, json_str: str)
```

**Loc 结构：**
```python
class Loc:
    app_uri: str            # 应用 URI
    graph_id: str           # 图 ID
    extension_name: str     # 扩展名称
```

---

## 配置文件说明

### 1. 应用配置 (property.json)

**文件位置：** `tenapp/property.json`

**用途：** 定义整个应用的图结构和扩展连接

**结构：**
```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "voice_assistant",
        "auto_start": true,
        "nodes": [
          {
            "type": "extension",
            "name": "agora_rtc",
            "addon": "agora_rtc",
            "extension_group": "default"
          },
          {
            "type": "extension",
            "name": "stt",
            "addon": "deepgram_asr_python",
            "extension_group": "default"
          },
          {
            "type": "extension",
            "name": "llm",
            "addon": "openai_llm2_python",
            "extension_group": "default"
          },
          {
            "type": "extension",
            "name": "tts",
            "addon": "elevenlabs_tts2_python",
            "extension_group": "default"
          },
          {
            "type": "extension",
            "name": "main_control",
            "addon": "main_python",
            "extension_group": "default"
          }
        ],
        "connections": [
          {
            "extension": "agora_rtc",
            "audio_frame": [
              {
                "name": "pcm_frame",
                "dest": [
                  {
                    "extension": "streamid_adapter"
                  }
                ]
              }
            ]
          },
          {
            "extension": "streamid_adapter",
            "audio_frame": [
              {
                "name": "pcm_frame",
                "dest": [
                  {
                    "extension": "stt"
                  }
                ]
              }
            ]
          },
          {
            "extension": "stt",
            "data": [
              {
                "name": "asr_result",
                "dest": [
                  {
                    "extension": "main_control"
                  }
                ]
              }
            ]
          },
          {
            "extension": "main_control",
            "data": [
              {
                "name": "tts_text_input",
                "dest": [
                  {
                    "extension": "tts"
                  }
                ]
              }
            ]
          },
          {
            "extension": "tts",
            "audio_frame": [
              {
                "name": "pcm_frame",
                "dest": [
                  {
                    "extension": "agora_rtc"
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
}
```

**关键字段说明：**

- **nodes**: 图中的所有扩展节点
  - `type`: 节点类型（"extension"）
  - `name`: 扩展实例名称（用于路由）
  - `addon`: 扩展插件名称（对应 manifest.json 中的 name）
  - `extension_group`: 扩展组（通常为 "default"）

- **connections**: 扩展之间的连接
  - `extension`: 源扩展名称
  - `audio_frame`/`data`/`cmd`: 消息类型
    - `name`: 消息名称
    - `dest`: 目标扩展列表

---

### 2. 扩展配置 (manifest.json)

**文件位置：** `ten_packages/extension/*/manifest.json`

**用途：** 定义扩展的元数据、依赖和 API

**结构：**
```json
{
  "type": "extension",
  "name": "main_python",
  "version": "0.1.0",
  "dependencies": [
    {
      "type": "system",
      "name": "ten_runtime_python",
      "version": "0.11"
    },
    {
      "type": "system",
      "name": "ten_ai_base",
      "version": "0.7"
    }
  ],
  "package": {
    "include": [
      "manifest.json",
      "property.json",
      "**.py",
      "README.md"
    ]
  },
  "api": {
    "property": {
      "properties": {
        "greeting": {
          "type": "string"
        },
        "max_memory_length": {
          "type": "int64"
        }
      }
    },
    "data_in": [
      {
        "name": "asr_result",
        "property": {
          "text": {
            "type": "string"
          },
          "is_final": {
            "type": "bool"
          }
        }
      }
    ],
    "data_out": [
      {
        "name": "tts_text_input",
        "property": {
          "text": {
            "type": "string"
          }
        }
      }
    ],
    "cmd_in": [
      {
        "name": "on_user_joined"
      },
      {
        "name": "on_user_left"
      },
      {
        "name": "flush"
      }
    ],
    "audio_frame_in": [
      {
        "name": "pcm_frame"
      }
    ],
    "audio_frame_out": [
      {
        "name": "pcm_frame"
      }
    ]
  }
}
```

**关键字段说明：**

- **type**: 包类型（"extension"）
- **name**: 扩展名称
- **version**: 版本号
- **dependencies**: 依赖列表
- **api**: API 定义
  - **property**: 配置属性定义
  - **data_in**: 输入数据定义
  - **data_out**: 输出数据定义
  - **cmd_in**: 输入命令定义
  - **cmd_out**: 输出命令定义
  - **audio_frame_in**: 输入音频帧定义
  - **audio_frame_out**: 输出音频帧定义
  - **video_frame_in**: 输入视频帧定义
  - **video_frame_out**: 输出视频帧定义

---

### 3. 扩展属性配置 (property.json)

**文件位置：** `ten_packages/extension/*/property.json`

**用途：** 扩展的默认配置值

**Main Control 示例：**
```json
{
  "greeting": "TEN Agent connected. How can I help you today?",
  "max_memory_length": 10
}
```

**ASR 扩展示例（Deepgram）：**
```json
{
  "api_key": "",
  "language": "zh",
  "model": "nova-2",
  "sample_rate": 16000
}
```

**LLM 扩展示例（OpenAI）：**
```json
{
  "api_key": "",
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2048,
  "top_p": 1.0,
  "prompt": "你是一个有帮助的AI助手。",
  "base_url": "https://api.openai.com/v1"
}
```

**TTS 扩展示例（ElevenLabs）：**
```json
{
  "api_key": "",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "model_id": "eleven_turbo_v2",
  "sample_rate": 16000,
  "optimize_streaming_latency": 4
}
```

---

## 总结

TEN Framework 语音助手的完整数据流程是一个基于图的消息传递架构，主要特点：

1. **模块化设计**：每个功能（ASR、LLM、TTS）都是独立的扩展
2. **异步处理**：使用 async/await 实现高并发、低延迟
3. **流式处理**：支持流式 ASR、LLM 响应和 TTS 输出
4. **灵活配置**：通过 JSON 配置文件定义图结构和扩展属性
5. **标准接口**：统一的消息类型（AudioFrame、Data、Cmd）和生命周期接口

整个流程从用户语音输入到音频输出，经过 8 个主要步骤，每个步骤都有明确的输入输出和处理逻辑，确保了系统的可扩展性和可维护性。
