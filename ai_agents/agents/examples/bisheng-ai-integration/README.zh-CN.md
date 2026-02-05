# Bisheng AI 语音集成示例

## 概述

这是一个简化的TEN框架示例，专门用于集成**毕昇AI（Bisheng AI）**的助手或工作流功能。

### 为什么选择这个方案？

如果您已经在本地开发了助手和工作流，并且：
- 使用的是字节跳动或其他厂商的大模型
- 只想使用TEN框架的语音相关功能（STT和TTS）
- 不需要TEN框架内置的大模型对话能力
- 需要考虑Web应用的网络开销和服务开销

那么这个示例非常适合您！

**简化的架构：**
```
用户语音 → TEN语音识别 → 文本 → 毕昇AI处理 → 文本 → TEN语音合成 → 音频输出
```

## 快速开始

### 1. 环境准备

确保您已安装：
- Docker 和 Docker Compose
- Node.js (LTS) v18+

### 2. 配置环境变量

在 `ai_agents/.env` 文件中添加以下配置：

```bash
# STT服务配置（语音识别）
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# TTS服务配置（语音合成）
ELEVENLABS_TTS_KEY=your_elevenlabs_api_key_here

# 毕昇AI配置（必需）
BISHENG_AI_URL=https://your-bisheng-ai-domain.com/api/v1/chat
BISHENG_AI_API_KEY=your_bisheng_api_key_here  # 如果需要认证
BISHENG_AI_ASSISTANT_ID=your_assistant_id      # 助手ID（二选一）
BISHENG_AI_WORKFLOW_ID=your_workflow_id        # 工作流ID（二选一）
```

### 3. 启动服务

```bash
# 进入示例目录
cd ai_agents/agents/examples/bisheng-ai-integration

# 安装依赖
task install

# 启动服务
task run
```

### 4. 访问应用

打开浏览器访问：http://localhost:3000

## 核心特性

### 1. 只使用语音功能

- ✅ 使用TEN的STT（语音转文本）
- ✅ 使用TEN的TTS（文本转语音）
- ❌ 不使用TEN的LLM
- ✅ 所有AI逻辑由您的毕昇AI服务处理

### 2. 灵活的集成方式

支持两种模式：
- **助手模式**：配置 `BISHENG_AI_ASSISTANT_ID`
- **工作流模式**：配置 `BISHENG_AI_WORKFLOW_ID`

### 3. 优化的性能

- WebSocket长连接，减少连接开销
- 支持流式音频传输
- 可配置的超时时间
- 本地化部署友好

## 毕昇AI接口要求

您的毕昇AI服务需要提供一个HTTP接口，接受以下格式的请求：

**请求示例：**
```json
POST /api/v1/chat
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY

{
  "input": "用户说的话（已经通过STT识别）",
  "session_id": "会话ID",
  "assistant_id": "助手ID",  // 可选
  "workflow_id": "工作流ID"  // 可选
}
```

**响应示例：**
```json
{
  "output": "AI的回复文本"
}
```

响应支持多种字段名：`output`、`response`、`text`、`answer` 等，系统会自动识别。

## 工作原理

### 数据流程

1. **用户说话** → 浏览器采集音频
2. **发送音频** → WebSocket传输PCM音频（base64编码）
3. **语音识别** → TEN的STT模块（Deepgram）转换为文本
4. **调用毕昇AI** → HTTP POST请求发送文本
5. **接收响应** → 获取毕昇AI的回复文本
6. **语音合成** → TEN的TTS模块（ElevenLabs）转换为语音
7. **播放音频** → WebSocket返回音频，浏览器播放

### 架构图

```
┌─────────────┐
│   浏览器     │
│  (前端UI)   │
└──────┬──────┘
       │ WebSocket (音频 + 文本)
       ▼
┌─────────────────────────────────────────┐
│           TEN Framework                  │
│                                          │
│  ┌──────────┐  ┌─────────┐  ┌────────┐│
│  │WebSocket │→ │  STT    │→ │ main_  ││
│  │ Server   │  │(Deepgram)│  │control ││
│  └────┬─────┘  └─────────┘  └───┬────┘│
│       │                          │      │
│       │                          │ HTTP │
│       │                          ▼      │
│       │                    ┌──────────┐│
│       │                    │毕昇AI    ││ 
│       │                    │服务      ││
│       │                    └────┬─────┘│
│       │                         │      │
│       │  ┌─────────┐           │      │
│       └─ │  TTS    │←──────────┘      │
│          │(ElevenLabs)                 │
│          └─────────┘                   │
└─────────────────────────────────────────┘
```

## 性能优化建议

### 网络优化

1. **内网部署**：将TEN服务和毕昇AI服务部署在同一内网
2. **CDN加速**：前端资源使用CDN分发
3. **压缩传输**：启用gzip/br压缩
4. **连接复用**：WebSocket保持长连接

### 服务优化

1. **合理超时**：根据实际情况调整 `bisheng_ai_timeout`
2. **并发控制**：限制同时处理的请求数
3. **缓存策略**：对常见问题进行缓存
4. **负载均衡**：多实例部署毕昇AI服务

## 常见问题

### Q1: 可以使用字节跳动的STT/TTS吗？

A: 可以！在TMAN设计器(http://localhost:49483)中可以轻松切换到字节跳动或其他服务商的STT/TTS模块。

### Q2: 支持中文吗？

A: 完全支持！在STT配置中设置语言为 `zh-CN` 即可。

### Q3: 毕昇AI返回的响应格式不一样怎么办？

A: 可以修改 `extension.py` 中的 `_call_bisheng_ai` 方法，调整响应解析逻辑。

### Q4: 如何减少延迟？

A: 
- 使用低延迟的STT/TTS服务
- 将毕昇AI部署在近距离的服务器
- 考虑使用流式响应（需要毕昇AI支持）

### Q5: 可以不用WebSocket吗？

A: 目前的实现基于WebSocket，如果需要其他传输方式，可以参考 `transcription` 示例使用Agora RTC。

## 技术支持

- [TEN框架文档](https://doc.theten.ai)
- [毕昇AI文档](https://bisheng.dataelem.com/)
- [GitHub Issues](https://github.com/TEN-framework/ten-framework/issues)

## 许可证

与TEN框架主项目保持一致。
