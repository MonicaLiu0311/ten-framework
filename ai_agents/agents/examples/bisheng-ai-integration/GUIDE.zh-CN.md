# TEN框架毕昇AI语音集成完整指南

## 项目概述

本示例实现了TEN框架与毕昇AI的语音集成，专门为**只需要TEN语音功能**而使用自己的AI服务（如毕昇AI）的开发者设计。

## 核心价值

如果您的情况是：
- ✅ 已经在本地开发了助手和工作流
- ✅ 使用字节跳动或其他厂商的大模型
- ✅ 只想用TEN的语音识别(STT)和语音合成(TTS)功能
- ✅ 不需要TEN内置的大模型对话
- ✅ 关注Web应用的网络开销和服务开销

那么这个方案非常适合您！

## 架构设计

### 简化的数据流
```
┌─────────┐
│ 用户说话 │
└────┬────┘
     │
     ▼
┌──────────────┐
│ TEN 语音识别 │ (Deepgram/字节等)
│    (STT)     │
└──────┬───────┘
       │ 文本
       ▼
┌──────────────┐
│  毕昇AI处理  │ (您的助手/工作流)
│ HTTP API调用 │
└──────┬───────┘
       │ 文本
       ▼
┌──────────────┐
│ TEN 语音合成 │ (ElevenLabs/字节等)
│    (TTS)     │
└──────┬───────┘
       │ 音频
       ▼
┌──────────────┐
│   用户听到   │
└──────────────┘
```

### 与原始架构的区别

**原始TEN框架流程：**
```
语音 → STT → LLM(OpenAI) → TTS → 音频
```

**本示例的流程：**
```
语音 → STT → 毕昇AI(HTTP) → TTS → 音频
```

## 快速开始（5分钟）

### 1. 配置环境变量

```bash
cd ai_agents
cp agents/examples/bisheng-ai-integration/.env.example .env
```

编辑 `.env` 文件：

```bash
# STT服务（语音识别）
DEEPGRAM_API_KEY=your_deepgram_key_here

# TTS服务（语音合成）
ELEVENLABS_TTS_KEY=your_elevenlabs_key_here

# 毕昇AI配置
BISHENG_AI_URL=https://your-bisheng-ai.com/api/v1/chat
BISHENG_AI_ASSISTANT_ID=your_assistant_id
```

### 2. 测试配置

```bash
cd agents/examples/bisheng-ai-integration
python3 test_connection.py
```

如果看到绿色的 ✓ 标记，说明配置正确！

### 3. 运行服务

```bash
task install
task run
```

### 4. 访问应用

打开浏览器访问：http://localhost:3000

## 详细配置说明

### 环境变量说明

| 变量名 | 必需 | 说明 | 示例 |
|--------|------|------|------|
| `DEEPGRAM_API_KEY` | 是 | Deepgram语音识别密钥 | `sk_...` |
| `ELEVENLABS_TTS_KEY` | 是 | ElevenLabs语音合成密钥 | `xi_...` |
| `BISHENG_AI_URL` | 是 | 毕昇AI服务端点 | `https://api.bisheng.ai/v1/chat` |
| `BISHENG_AI_API_KEY` | 否 | 毕昇AI认证密钥 | `bsk_...` |
| `BISHENG_AI_ASSISTANT_ID` | 二选一 | 助手ID | `assistant_123` |
| `BISHENG_AI_WORKFLOW_ID` | 二选一 | 工作流ID | `workflow_456` |

### 毕昇AI接口要求

您的毕昇AI服务需要支持以下接口格式：

**请求：**
```json
POST /api/v1/chat
Content-Type: application/json

{
  "input": "用户说的话",
  "session_id": "会话ID",
  "assistant_id": "助手ID"  // 或 workflow_id
}
```

**响应（支持以下任一格式）：**
```json
{
  "output": "AI的回复"
}
```

或者：
```json
{
  "response": "AI的回复"
}
```

或者：
```json
{
  "text": "AI的回复"
}
```

或者：
```json
{
  "answer": "AI的回复"
}
```

系统会自动识别这些字段。

## 使用字节跳动服务

如果您已经有字节跳动的账号，可以这样配置：

### 1. 在 `.env` 中配置字节服务

```bash
# 字节跳动STT
BYTEDANCE_ASR_KEY=your_bytedance_asr_key
BYTEDANCE_ASR_APPID=your_app_id

# 字节跳动TTS
BYTEDANCE_TTS_KEY=your_bytedance_tts_key
BYTEDANCE_TTS_APPID=your_app_id

# 毕昇AI（您自己的）
BISHENG_AI_URL=https://your-bisheng-ai.com/api/v1/chat
BISHENG_AI_ASSISTANT_ID=your_assistant_id
```

### 2. 在TMAN设计器中切换

1. 启动服务后访问 http://localhost:49483
2. 右键点击 `stt` 节点 → 选择 `bytedance_asr`
3. 右键点击 `tts` 节点 → 选择 `bytedance_tts_duplex`
4. 点击"提交"保存配置

## 性能优化建议

### 网络优化

1. **内网部署**
   - TEN服务和毕昇AI部署在同一内网
   - 延迟可降低到 < 50ms

2. **CDN加速**
   - 前端资源使用CDN
   - 静态资源加载更快

3. **压缩传输**
   - 启用gzip/brotli压缩
   - 减少数据传输量

### 服务优化

1. **连接复用**
   - WebSocket保持长连接
   - 避免频繁建立连接

2. **超时设置**
   ```bash
   # 在 property.json 中调整
   "bisheng_ai_timeout": 30  # 秒
   ```

3. **并发控制**
   - 限制同时处理的请求数
   - 防止服务过载

4. **缓存策略**
   - 对常见问题进行缓存
   - 减少API调用次数

## 故障排查

### 问题1：连接毕昇AI失败

**症状：**
- 日志显示 "Connection error"
- 测试脚本报错

**解决方法：**
1. 检查 `BISHENG_AI_URL` 是否正确
2. 使用 `curl` 测试连接：
   ```bash
   curl -X POST $BISHENG_AI_URL \
     -H "Content-Type: application/json" \
     -d '{"input": "测试", "session_id": "test"}'
   ```
3. 确认防火墙/网络策略允许访问

### 问题2：语音识别不工作

**症状：**
- 说话后没有文本显示
- 浏览器控制台有麦克风权限错误

**解决方法：**
1. 检查 `DEEPGRAM_API_KEY` 是否有效
2. 确认浏览器已授予麦克风权限
3. 查看浏览器控制台的具体错误

### 问题3：没有语音输出

**症状：**
- 有文本但听不到声音
- TTS相关错误

**解决方法：**
1. 检查 `ELEVENLABS_TTS_KEY` 是否有效
2. 确认音量没有静音
3. 查看后端日志的TTS错误

### 问题4：响应很慢

**症状：**
- 等待时间超过5秒
- 用户体验不佳

**优化方法：**
1. 将毕昇AI部署在近距离服务器
2. 检查网络延迟：`ping your-bisheng-ai.com`
3. 考虑使用更快的STT/TTS服务
4. 如果毕昇AI支持，启用流式响应

## 自定义和扩展

### 修改语言

在 `property.json` 中修改 STT 语言：

```json
{
  "name": "stt",
  "property": {
    "params": {
      "language": "zh-CN"  // 中文
      // 或 "en-US" 英文
    }
  }
}
```

### 修改问候语

在 `property.json` 中修改：

```json
{
  "name": "main_control",
  "property": {
    "greeting": "您好，我是AI语音助手，有什么可以帮您的吗？"
  }
}
```

### 自定义毕昇AI请求格式

如果您的毕昇AI接口格式不同，修改 `extension.py` 中的 `_call_bisheng_ai` 方法：

```python
# 修改请求格式
request_data = {
    "query": user_input,  # 改为您的字段名
    "sid": self.session_id,
    # 添加其他字段
}

# 修改响应解析
response_text = result.get("your_response_field")
```

## 文件结构

```
bisheng-ai-integration/
├── README.md                   # 完整文档（中英文）
├── README.zh-CN.md            # 中文快速指南
├── CONFIGURATION.md           # 详细配置说明
├── .env.example               # 环境变量模板
├── test_connection.py         # 连接测试脚本
├── Dockerfile                 # Docker部署文件
├── Taskfile.yml               # 任务配置
├── frontend/                  # 前端应用
│   └── src/                   # React/Next.js代码
└── tenapp/                    # TEN应用
    ├── property.json          # 图表配置
    ├── manifest.json          # 依赖声明
    └── ten_packages/
        └── extension/
            └── main_python/   # 主控扩展
                ├── extension.py   # 核心逻辑
                ├── config.py      # 配置模型
                └── agent/
                    ├── agent.py   # 简化的Agent
                    └── events.py  # 事件定义
```

## 与其他TEN示例的对比

| 特性 | voice-assistant | websocket-example | bisheng-ai-integration |
|------|-----------------|-------------------|------------------------|
| STT | ✅ | ✅ | ✅ |
| TTS | ✅ | ✅ | ✅ |
| 内置LLM | ✅ | ✅ | ❌ |
| 外部AI | ❌ | ❌ | ✅ (HTTP) |
| RTC | ✅ | ❌ | ❌ |
| WebSocket | ❌ | ✅ | ✅ |
| 复杂度 | 高 | 中 | 低 |
| 适用场景 | 完整对话 | Web语音 | 集成现有AI |

## 生产部署

### Docker部署

```bash
# 构建镜像
cd ai_agents
docker build -f agents/examples/bisheng-ai-integration/Dockerfile \
  -t bisheng-voice-assistant .

# 运行
docker run -d \
  --name bisheng-voice \
  --env-file .env \
  -p 3000:3000 \
  -p 8080:8080 \
  -p 8765:8765 \
  bisheng-voice-assistant
```

### 云服务部署

1. **后端**：部署到支持容器的平台（AWS ECS、Google Cloud Run等）
2. **前端**：部署到Vercel或Netlify
3. **环境变量**：在云平台配置界面设置

详见 `README.md` 的"Deploying with other cloud services"章节。

## 最佳实践

1. **开发环境**
   - 使用 `test_connection.py` 验证配置
   - 查看浏览器控制台和后端日志
   - 使用TMAN设计器 (http://localhost:49483) 调试

2. **测试环境**
   - 设置合理的超时时间
   - 模拟不同网络条件
   - 测试错误处理

3. **生产环境**
   - 启用HTTPS
   - 配置日志收集
   - 设置监控告警
   - 准备降级方案

## 支持和反馈

- **文档**: [TEN框架文档](https://doc.theten.ai)
- **Issues**: [GitHub Issues](https://github.com/TEN-framework/ten-framework/issues)
- **社区**: [Discord](https://discord.gg/VnPftUzAMJ)

## 许可证

与TEN框架主项目保持一致（Apache 2.0）。
