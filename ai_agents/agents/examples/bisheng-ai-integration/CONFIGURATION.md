# 配置指南 / Configuration Guide

## 环境变量配置 / Environment Variable Configuration

### 基本配置 / Basic Configuration

在 `ai_agents/.env` 文件中配置以下变量：

```bash
# ====================================
# STT配置 - Speech-to-Text Configuration
# ====================================

# Deepgram（推荐用于英文）
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# 或者使用其他STT服务 / Or use other STT services:
# AZURE_ASR_KEY=your_azure_key
# BYTEDANCE_ASR_KEY=your_bytedance_key  # 字节跳动
# XFYUN_ASR_KEY=your_xfyun_key          # 讯飞

# ====================================
# TTS配置 - Text-to-Speech Configuration
# ====================================

# ElevenLabs（推荐用于英文）
ELEVENLABS_TTS_KEY=your_elevenlabs_api_key_here

# 或者使用其他TTS服务 / Or use other TTS services:
# AZURE_TTS_KEY=your_azure_key
# BYTEDANCE_TTS_KEY=your_bytedance_key  # 字节跳动
# FISH_AUDIO_TTS_KEY=your_fish_audio_key

# ====================================
# 毕昇AI配置 - Bisheng AI Configuration
# ====================================

# 必需：毕昇AI服务URL / Required: Bisheng AI service URL
BISHENG_AI_URL=https://your-bisheng-ai-domain.com/api/v1/chat

# 可选：API密钥 / Optional: API Key
BISHENG_AI_API_KEY=your_bisheng_api_key_here

# 选择一个模式 / Choose one mode:
# 模式1：助手模式 / Mode 1: Assistant mode
BISHENG_AI_ASSISTANT_ID=your_assistant_id

# 模式2：工作流模式 / Mode 2: Workflow mode
BISHENG_AI_WORKFLOW_ID=your_workflow_id

# 注意：两个模式都提供时，优先使用助手模式
# Note: If both are provided, assistant mode takes priority
```

## 毕昇AI服务配置示例 / Bisheng AI Service Configuration Examples

### 示例1：本地开发环境 / Example 1: Local Development

```bash
# 本地毕昇AI服务
BISHENG_AI_URL=http://localhost:7860/api/v1/chat
BISHENG_AI_ASSISTANT_ID=assistant_123
```

### 示例2：云端部署 / Example 2: Cloud Deployment

```bash
# 使用云端毕昇AI服务
BISHENG_AI_URL=https://api.bisheng.ai/v1/chat
BISHENG_AI_API_KEY=bsk-1234567890abcdef
BISHENG_AI_WORKFLOW_ID=workflow_456
```

### 示例3：内网部署 / Example 3: Intranet Deployment

```bash
# 内网环境，减少延迟
BISHENG_AI_URL=http://10.0.1.100:8080/api/chat
BISHENG_AI_ASSISTANT_ID=assistant_789
```

## 使用字节跳动服务 / Using ByteDance Services

如果您想使用字节跳动的STT/TTS服务（因为已有大模型账号），可以这样配置：

```bash
# 字节跳动STT
BYTEDANCE_ASR_KEY=your_bytedance_asr_key
BYTEDANCE_ASR_APPID=your_app_id
BYTEDANCE_ASR_CLUSTER=your_cluster

# 字节跳动TTS
BYTEDANCE_TTS_KEY=your_bytedance_tts_key
BYTEDANCE_TTS_APPID=your_app_id

# 毕昇AI（使用您自己的服务）
BISHENG_AI_URL=https://your-bisheng-ai.com/api/v1/chat
BISHENG_AI_ASSISTANT_ID=your_assistant_id
```

然后在TMAN设计器 (http://localhost:49483) 中：
1. 右键点击 `stt` 节点
2. 选择 `bytedance_asr` 作为addon
3. 右键点击 `tts` 节点
4. 选择 `bytedance_tts_duplex` 作为addon

## 高级配置 / Advanced Configuration

### 修改语音识别语言 / Modify Speech Recognition Language

在 `tenapp/property.json` 中：

```json
{
  "name": "stt",
  "addon": "deepgram_asr_python",
  "property": {
    "params": {
      "api_key": "${env:DEEPGRAM_API_KEY}",
      "language": "zh-CN",  // 改为 "zh-CN" 识别中文
      "model": "nova-3"
    }
  }
}
```

### 调整超时时间 / Adjust Timeout

在 `tenapp/property.json` 中：

```json
{
  "name": "main_control",
  "addon": "main_python",
  "property": {
    "greeting": "您好！",
    "bisheng_ai_url": "${env:BISHENG_AI_URL}",
    "bisheng_ai_timeout": 60  // 增加超时时间到60秒
  }
}
```

### 修改问候语 / Modify Greeting

在 `tenapp/property.json` 中修改：

```json
{
  "name": "main_control",
  "property": {
    "greeting": "欢迎使用AI语音助手！有什么可以帮您的吗？"
  }
}
```

## 测试配置 / Testing Configuration

### 1. 检查环境变量 / Check Environment Variables

```bash
cd ai_agents/agents/examples/bisheng-ai-integration
# 查看配置是否正确加载
grep BISHENG_AI ../../.env
```

### 2. 测试STT服务 / Test STT Service

```bash
# 启动服务后，打开浏览器控制台
# 说话时应该能看到转录文本
```

### 3. 测试毕昇AI连接 / Test Bisheng AI Connection

```bash
# 使用curl测试毕昇AI接口
curl -X POST https://your-bisheng-ai.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "input": "你好",
    "session_id": "test123"
  }'
```

### 4. 测试TTS服务 / Test TTS Service

```bash
# 启动服务后，毕昇AI返回文本应该能听到语音播放
```

## 故障排查 / Troubleshooting

### 问题1：无法连接毕昇AI / Cannot Connect to Bisheng AI

**检查清单：**
- [ ] BISHENG_AI_URL是否正确
- [ ] 网络是否可达（使用curl测试）
- [ ] API密钥是否有效
- [ ] 助手ID或工作流ID是否正确

### 问题2：语音识别不工作 / Speech Recognition Not Working

**检查清单：**
- [ ] DEEPGRAM_API_KEY是否有效
- [ ] 麦克风权限是否授予
- [ ] 浏览器控制台是否有错误

### 问题3：没有语音输出 / No Audio Output

**检查清单：**
- [ ] ELEVENLABS_TTS_KEY是否有效
- [ ] 扬声器/耳机是否正常
- [ ] 浏览器音量是否打开

### 问题4：延迟太高 / High Latency

**优化建议：**
1. 将毕昇AI部署在近距离服务器
2. 使用更快的STT/TTS服务
3. 检查网络连接质量
4. 减少`bisheng_ai_timeout`值

## 性能优化建议 / Performance Optimization Tips

### 减少网络延迟 / Reduce Network Latency

1. **同机房部署**：TEN服务和毕昇AI服务部署在同一机房
2. **使用内网**：通过内网IP访问，避免公网转发
3. **CDN加速**：前端资源使用CDN分发

### 优化服务性能 / Optimize Service Performance

1. **连接复用**：WebSocket保持长连接
2. **合理超时**：根据实际响应时间调整timeout
3. **缓存策略**：对常见问题进行缓存
4. **负载均衡**：多实例部署毕昇AI

## 更多帮助 / More Help

- [TEN框架文档](https://doc.theten.ai)
- [毕昇AI文档](https://bisheng.dataelem.com/)
- [Deepgram文档](https://developers.deepgram.com/)
- [ElevenLabs文档](https://docs.elevenlabs.io/)
