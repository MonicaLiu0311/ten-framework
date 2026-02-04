# 配置文件修改技术指南

当您使用替代服务提供商（不是默认的 Deepgram + OpenAI + ElevenLabs）时，**必须修改配置文件**。本指南详细解释为什么需要修改、如何修改，以及背后的技术原理。

[English](CONFIG_MODIFICATION_GUIDE.md) | 简体中文

## 目录

- [为什么必须修改配置文件](#为什么必须修改配置文件)
- [技术原理](#技术原理)
- [配置文件结构](#配置文件结构)
- [如何修改配置](#如何修改配置)
- [代码证据](#代码证据)
- [实际示例](#实际示例)
- [常见问题](#常见问题)

## 为什么必须修改配置文件

### 核心原因

TEN Framework 使用**扩展（Extension）架构**，每个服务提供商都是一个独立的扩展模块。不同的扩展：

1. **有不同的名称（addon）** - 系统通过这个名称加载对应的扩展
2. **需要不同的参数** - 不同服务商的 API 接口不同
3. **实现不同的接口** - 虽然都实现 ASR/TTS/LLM 接口，但具体实现各不相同

**如果不修改配置文件，系统会尝试加载默认的扩展，但使用错误的 API 密钥，导致失败。**

### 类比理解

想象配置文件是一张**菜单订单**：

```
默认订单：
- STT（语音识别）: Deepgram 餐厅 → 需要 Deepgram 的菜单和餐票
- LLM（大语言模型）: OpenAI 餐厅 → 需要 OpenAI 的菜单和餐票
- TTS（语音合成）: ElevenLabs 餐厅 → 需要 ElevenLabs 的菜单和餐票
```

如果你想换到 Azure 餐厅，你需要：
1. **改餐厅名称**（addon: "azure_asr_python"）
2. **改菜单选项**（参数：region, key）
3. **用对应餐厅的餐票**（Azure API key）

**不能**拿着 Deepgram 的菜单和餐票去 Azure 餐厅！

## 技术原理

### 1. 扩展加载机制

#### 代码位置：`tenapp/main.go`

```go
// 第 28-40 行：应用初始化
func (p *defaultApp) OnConfigure(tenEnv ten.TenEnv) {
    // 读取 property.json 文件
    if len(p.cfg.PropertyFilePath) > 0 {
        if b, err := os.ReadFile(p.cfg.PropertyFilePath); err != nil {
            log.Fatalf("Failed to read property file %s, err %v\n", 
                       p.cfg.PropertyFilePath, err)
        } else {
            // 将 JSON 配置加载到 TEN runtime
            tenEnv.InitPropertyFromJSONBytes(b)
        }
    }
    tenEnv.OnConfigureDone()
}
```

**关键点**：
- 系统启动时读取 `property.json`
- TEN runtime 根据配置初始化所有扩展
- **每个扩展的 `addon` 字段决定加载哪个具体实现**

### 2. 扩展注册机制

#### 代码位置：`tenapp/manifest.json`

```json
{
  "dependencies": [
    // 注册所有可用的扩展
    { "path": "../../../ten_packages/extension/deepgram_asr_python" },
    { "path": "../../../ten_packages/extension/azure_asr_python" },
    { "path": "../../../ten_packages/extension/openai_llm2_python" },
    { "path": "../../../ten_packages/extension/elevenlabs_tts2_python" }
    // ... 更多扩展
  ]
}
```

**关键点**：
- `manifest.json` 声明应用依赖哪些扩展
- 所有列出的扩展在编译时被包含进应用
- **但是运行时只会加载 `property.json` 中指定的扩展**

### 3. 扩展实现差异

#### Deepgram ASR 扩展

**代码位置**：`ten_packages/extension/deepgram_asr_python/extension.py`

```python
class DeepgramASRExtension(AsyncASRBaseExtension):
    def __init__(self, name: str):
        super().__init__(name)
        self.recognition: DeepgramASRRecognition | None = None
        self.config: DeepgramASRConfig | None = None
        # Deepgram 特定的实现
```

**配置接口**（`manifest.json`）：
```json
{
  "api": {
    "property": {
      "properties": {
        "params": {
          "type": "object",
          "properties": {
            "api_key": { "type": "string" },  // Deepgram 需要 api_key
            "language": { "type": "string" },
            "model": { "type": "string" }
          }
        }
      }
    }
  }
}
```

#### Azure ASR 扩展

**代码位置**：`ten_packages/extension/azure_asr_python/extension.py`

```python
class AzureASRExtension(AsyncASRBaseExtension):
    def __init__(self, name: str):
        super().__init__(name)
        self.client: speechsdk.SpeechRecognizer | None = None
        self.config: AzureASRConfig | None = None
        # Azure 特定的实现（使用 Azure SDK）
    
    @override
    def vendor(self) -> str:
        return "microsoft"  # 不同的供应商
```

**配置接口**（`manifest.json`）：
```json
{
  "api": {
    "property": {
      "properties": {
        "params": {
          "type": "object",
          "properties": {
            "key": { "type": "string" },      // Azure 需要 key（不是 api_key）
            "region": { "type": "string" },   // Azure 特有：需要 region
            "language": { "type": "string" }
          }
        }
      }
    }
  }
}
```

**对比**：

| 特性 | Deepgram | Azure |
|------|----------|-------|
| **扩展名称** | `deepgram_asr_python` | `azure_asr_python` |
| **API 密钥字段** | `api_key` | `key` |
| **特殊参数** | `model` | `region` |
| **实现方式** | WebSocket 连接 | Azure Speech SDK |
| **供应商** | deepgram | microsoft |

## 配置文件结构

### property.json 完整结构

**位置**：`tenapp/property.json`

```json
{
  "ten": {
    "predefined_graphs": [
      {
        "name": "voice_assistant",
        "auto_start": true,
        "graph": {
          "nodes": [
            // ========= STT 节点 =========
            {
              "type": "extension",
              "name": "stt",                    // 节点名称（可自定义）
              "addon": "deepgram_asr_python",   // ⚠️ 扩展名称（必须匹配实际扩展）
              "extension_group": "stt",
              "property": {                      // ⚠️ 扩展的配置参数
                "params": {
                  "api_key": "${env:DEEPGRAM_API_KEY}",  // 从环境变量读取
                  "language": "en-US",
                  "model": "nova-3"
                }
              }
            },
            
            // ========= LLM 节点 =========
            {
              "type": "extension",
              "name": "llm",
              "addon": "openai_llm2_python",    // ⚠️ 扩展名称
              "extension_group": "chatgpt",
              "property": {                      // ⚠️ 配置参数
                "api_key": "${env:OPENAI_API_KEY}",
                "model": "${env:OPENAI_MODEL}",
                "max_tokens": 512
              }
            },
            
            // ========= TTS 节点 =========
            {
              "type": "extension",
              "name": "tts",
              "addon": "elevenlabs_tts2_python", // ⚠️ 扩展名称
              "extension_group": "tts",
              "property": {                       // ⚠️ 配置参数
                "params": {
                  "key": "${env:ELEVENLABS_TTS_KEY}",
                  "model_id": "eleven_multilingual_v2",
                  "voice_id": "pNInz6obpgDQGcFmaJgB"
                }
              }
            }
            
            // ... 其他节点
          ],
          
          "connections": [
            // 定义节点之间的数据流连接
          ]
        }
      }
    ]
  }
}
```

### 关键字段说明

| 字段 | 作用 | 是否必须修改 |
|------|------|-------------|
| `addon` | 指定使用哪个扩展实现 | ✅ **是** - 必须改为新服务商的扩展名 |
| `property` | 扩展的配置参数 | ✅ **是** - 必须符合新扩展的参数要求 |
| `name` | 节点在图中的名称 | ❌ 否 - 通常不需要改 |
| `extension_group` | 扩展所属的组 | ❌ 否 - 通常不需要改 |

## 如何修改配置

### 步骤 1：确定替代服务商

假设你想用以下替代方案：
- **STT**: Azure 替代 Deepgram
- **LLM**: Gemini 替代 OpenAI
- **TTS**: Google 替代 ElevenLabs

### 步骤 2：找到对应的扩展名称

查看 `tenapp/manifest.json` 中的依赖列表，或查看 `ten_packages/extension/` 目录：

```bash
# 查看可用的扩展
ls ai_agents/agents/ten_packages/extension/ | grep -E "asr|tts|llm"
```

找到：
- Azure STT: `azure_asr_python`
- Gemini LLM: `gemini_llm2_python`
- Google TTS: `google_tts_python`

### 步骤 3：查看扩展的参数要求

查看每个扩展的 `manifest.json` 文件：

```bash
# 查看 Azure ASR 的参数要求
cat ten_packages/extension/azure_asr_python/manifest.json
```

提取出需要的参数：
- `key`: Azure API 密钥
- `region`: Azure 区域（如 "eastus"）
- `language`: 语言代码

### 步骤 4：修改 property.json

#### 原始配置（默认）

```json
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
}
```

#### 修改后（Azure）

```json
{
  "type": "extension",
  "name": "stt",
  "addon": "azure_asr_python",           // ✏️ 改扩展名
  "property": {
    "params": {
      "key": "${env:AZURE_ASR_API_KEY}",  // ✏️ 改参数名和值
      "region": "${env:AZURE_ASR_REGION}", // ✏️ 添加 Azure 特有参数
      "language": "en-US"                  // ✏️ 保留通用参数
    }
  }
}
```

### 步骤 5：配置环境变量

在 `.env` 文件中添加新的环境变量：

```bash
# 删除或注释掉旧的
# DEEPGRAM_API_KEY=xxx

# 添加新的
AZURE_ASR_API_KEY=your_azure_key_here
AZURE_ASR_REGION=eastus
```

## 代码证据

### 证据 1：扩展加载入口

**文件**：`tenapp/main.go` (第 36 行)

```go
tenEnv.InitPropertyFromJSONBytes(b)
```

**说明**：这行代码将 `property.json` 的内容加载到 TEN runtime。runtime 会：
1. 解析 JSON 中的所有节点定义
2. 根据每个节点的 `addon` 字段查找对应的扩展
3. 使用 `property` 中的配置初始化扩展

**如果 `addon` 名称错误**：系统找不到扩展，启动失败
**如果 `property` 参数错误**：扩展初始化失败，无法工作

### 证据 2：扩展接口定义

**文件**：`ten_packages/extension/deepgram_asr_python/manifest.json` (第 23-44 行)

```json
{
  "api": {
    "property": {
      "properties": {
        "params": {
          "type": "object",
          "properties": {
            "api_key": { "type": "string" },
            "model": { "type": "string" },
            "language": { "type": "string" }
          }
        }
      }
    }
  }
}
```

**说明**：这定义了 Deepgram 扩展期望接收的参数。如果你在 `property.json` 中提供的参数不匹配（比如用了 Azure 的 `key` 和 `region`），扩展会：
1. 无法找到必需的参数
2. 抛出错误或使用默认值
3. 导致功能异常

### 证据 3：扩展实现差异

**Deepgram 实现** (`ten_packages/extension/deepgram_asr_python/extension.py`):

```python
class DeepgramASRExtension(AsyncASRBaseExtension):
    def __init__(self, name: str):
        super().__init__(name)
        self.recognition: DeepgramASRRecognition | None = None
        self.config: DeepgramASRConfig | None = None
```

**Azure 实现** (`ten_packages/extension/azure_asr_python/extension.py`):

```python
class AzureASRExtension(AsyncASRBaseExtension):
    def __init__(self, name: str):
        super().__init__(name)
        self.client: speechsdk.SpeechRecognizer | None = None
        self.config: AzureASRConfig | None = None
```

**说明**：
- 两个扩展都继承自 `AsyncASRBaseExtension`（接口一致）
- 但内部实现完全不同：
  - Deepgram 使用自定义的 `DeepgramASRRecognition`
  - Azure 使用官方的 `speechsdk.SpeechRecognizer`
- **它们不能互换使用**，必须通过 `addon` 字段选择正确的实现

### 证据 4：参数访问

**文件**：`ten_packages/extension/azure_asr_python/config.py`

```python
class AzureASRConfig:
    def __init__(
        self,
        key: str,          # ⚠️ Azure 需要 'key'
        region: str,       # ⚠️ Azure 需要 'region'
        language: str = "en-US",
        # ...
    ):
        self.key = key
        self.region = region
        self.language = language
```

**对比 Deepgram** (`ten_packages/extension/deepgram_asr_python/config.py`):

```python
class DeepgramASRConfig:
    def __init__(
        self,
        api_key: str,      # ⚠️ Deepgram 需要 'api_key'（不是 'key'）
        language: str,
        model: str,        # ⚠️ Deepgram 需要 'model'
        # ...
    ):
        self.api_key = api_key
        self.language = language
        self.model = model
```

**说明**：参数名称和要求完全不同。如果配置文件中的参数不匹配，扩展的 `__init__` 方法会因为找不到必需的参数而失败。

## 实际示例

### 示例 1：从 Deepgram 切换到 Azure STT

#### 1.1 查看 Azure 扩展要求

```bash
cat ai_agents/agents/ten_packages/extension/azure_asr_python/manifest.json | grep -A 20 '"property"'
```

输出：
```json
"property": {
  "properties": {
    "params": {
      "type": "object",
      "properties": {
        "key": { "type": "string" },
        "region": { "type": "string" },
        "language": { "type": "string" }
      }
    }
  }
}
```

#### 1.2 修改 property.json

找到 STT 节点（通常在第 26-38 行）：

**修改前**：
```json
{
  "type": "extension",
  "name": "stt",
  "addon": "deepgram_asr_python",
  "extension_group": "stt",
  "property": {
    "params": {
      "api_key": "${env:DEEPGRAM_API_KEY}",
      "language": "en-US",
      "model": "nova-3"
    }
  }
}
```

**修改后**：
```json
{
  "type": "extension",
  "name": "stt",
  "addon": "azure_asr_python",              // ✅ 改为 Azure 扩展
  "extension_group": "stt",
  "property": {
    "params": {
      "key": "${env:AZURE_ASR_API_KEY}",     // ✅ 改参数名
      "region": "${env:AZURE_ASR_REGION}",   // ✅ 添加 region
      "language": "en-US"                    // ✅ 保留 language
      // ❌ 移除 model（Azure 不需要）
    }
  }
}
```

#### 1.3 配置 .env 文件

```bash
# 添加到 .env 文件
AZURE_ASR_API_KEY=your_azure_speech_key
AZURE_ASR_REGION=eastus
```

#### 1.4 验证

启动应用并查看日志：

```bash
task run
```

成功的日志应该显示：
```
[INFO] Loading extension: azure_asr_python
[INFO] Azure ASR initialized with region: eastus
```

### 示例 2：从 OpenAI 切换到 Gemini LLM

#### 2.1 查看 Gemini 扩展要求

```bash
cat ai_agents/agents/ten_packages/extension/gemini_llm2_python/manifest.json
```

提取参数：
- `api_key`
- `model` (可选，默认 "gemini-1.5-flash")
- `max_tokens` (可选)

#### 2.2 修改 property.json

找到 LLM 节点（通常在第 39-55 行）：

**修改前**：
```json
{
  "type": "extension",
  "name": "llm",
  "addon": "openai_llm2_python",
  "extension_group": "chatgpt",
  "property": {
    "base_url": "https://api.openai.com/v1",
    "api_key": "${env:OPENAI_API_KEY}",
    "model": "${env:OPENAI_MODEL}",
    "max_tokens": 512,
    "greeting": "TEN Agent connected."
  }
}
```

**修改后**：
```json
{
  "type": "extension",
  "name": "llm",
  "addon": "gemini_llm2_python",           // ✅ 改为 Gemini 扩展
  "extension_group": "chatgpt",
  "property": {
    // ❌ 移除 base_url（Gemini 不需要）
    "api_key": "${env:GEMINI_API_KEY}",     // ✅ 改环境变量名
    "model": "gemini-1.5-flash",            // ✅ 改为 Gemini 模型
    "max_tokens": 512,                      // ✅ 保留
    "greeting": "TEN Agent connected."      // ✅ 保留
  }
}
```

#### 2.3 配置 .env 文件

```bash
# 添加到 .env 文件
GEMINI_API_KEY=your_gemini_api_key
```

### 示例 3：完整替换（所有服务）

如果要全部替换为 Azure 服务：

```json
{
  "ten": {
    "predefined_graphs": [{
      "graph": {
        "nodes": [
          // STT: Azure
          {
            "name": "stt",
            "addon": "azure_asr_python",
            "property": {
              "params": {
                "key": "${env:AZURE_ASR_API_KEY}",
                "region": "${env:AZURE_ASR_REGION}",
                "language": "zh-CN"
              }
            }
          },
          
          // LLM: Azure OpenAI
          {
            "name": "llm",
            "addon": "openai_llm2_python",
            "property": {
              "base_url": "${env:AZURE_OPENAI_ENDPOINT}",
              "api_key": "${env:AZURE_OPENAI_API_KEY}",
              "model": "gpt-4",
              "max_tokens": 512
            }
          },
          
          // TTS: Azure
          {
            "name": "tts",
            "addon": "azure_tts_python",
            "property": {
              "params": {
                "key": "${env:AZURE_TTS_KEY}",
                "region": "${env:AZURE_TTS_REGION}",
                "voice_name": "zh-CN-XiaoxiaoNeural"
              }
            }
          }
        ]
      }
    }]
  }
}
```

`.env` 配置：

```bash
# Azure 配置
AZURE_ASR_API_KEY=your_azure_speech_key
AZURE_ASR_REGION=eastus
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_TTS_KEY=your_azure_speech_key
AZURE_TTS_REGION=eastus
```

## 常见问题

### 1. 我只改了 .env 文件中的 API 密钥，为什么不工作？

**原因**：只改 API 密钥是不够的，因为：
1. **扩展名称（addon）没改**：系统仍然加载旧的扩展（如 Deepgram）
2. **参数结构不匹配**：新的 API 密钥用在了旧的扩展上

**解决方案**：必须同时修改 `property.json` 中的 `addon` 和 `property` 字段。

### 2. 如何知道某个扩展需要什么参数？

**方法 1**：查看扩展的 `manifest.json` 文件

```bash
cat ten_packages/extension/[扩展名]/manifest.json | grep -A 30 '"property"'
```

**方法 2**：查看扩展的文档

```bash
ls ten_packages/extension/[扩展名]/docs/
cat ten_packages/extension/[扩展名]/docs/README.zh-CN.md
```

**方法 3**：查看其他示例项目的配置

```bash
find ai_agents/agents/examples -name "property.json" -exec grep -l "扩展名" {} \;
```

### 3. 可以混合使用不同服务商吗？

**可以！** 例如：
- STT: Deepgram
- LLM: Gemini
- TTS: Azure

只需要分别配置每个节点即可。它们是独立的扩展。

```json
{
  "nodes": [
    { "name": "stt", "addon": "deepgram_asr_python", ... },
    { "name": "llm", "addon": "gemini_llm2_python", ... },
    { "name": "tts", "addon": "azure_tts_python", ... }
  ]
}
```

### 4. 修改配置后需要重新编译吗？

**不需要重新编译**，但需要：
1. **重启应用**：配置在启动时加载
2. **确保扩展已在 `manifest.json` 中注册**：如果是新的扩展，需要重新编译

检查扩展是否已注册：

```bash
grep "你的扩展名" tenapp/manifest.json
```

如果没有，添加依赖后需要重新编译：

```bash
task build
```

### 5. 为什么不同扩展的参数名称不一样？

**原因**：
1. **不同服务商的 API 不同**：每个服务商有自己的 API 设计
2. **历史原因**：扩展是不同时间、不同开发者创建的
3. **技术实现差异**：有些用 REST API，有些用 SDK，有些用 WebSocket

**示例对比**：

| 扩展 | API 密钥字段 | 原因 |
|------|-------------|------|
| Deepgram | `api_key` | 遵循 Deepgram API 命名 |
| Azure | `key` | 遵循 Azure SDK 命名 |
| ElevenLabs | `key` | 遵循 ElevenLabs API 命名 |
| OpenAI | `api_key` | 遵循 OpenAI API 命名 |

### 6. 有没有工具可以自动生成配置？

目前没有自动化工具，但你可以：

1. **使用 TMAN Designer（可视化编辑器）**：
   ```bash
   # 访问 http://localhost:49483
   ```
   - 可视化选择扩展
   - 图形界面配置参数
   - 自动生成 property.json

2. **复制现有示例**：
   ```bash
   # 查找使用特定扩展的示例
   find ai_agents/agents/examples -name "property.json" -exec grep -l "azure_asr_python" {} \;
   ```

3. **参考文档模板**：
   - 查看本仓库的 [FREE_TRIAL_GUIDE.zh-CN.md](FREE_TRIAL_GUIDE.zh-CN.md)
   - 包含多种配置方案的完整示例

### 7. 如果我用错了扩展名称会发生什么？

**症状**：
```
[ERROR] Failed to load extension: invalid_extension_name
[FATAL] Extension not found in registry
```

**原因**：TEN runtime 在注册表中找不到该扩展名称

**解决方案**：
1. 检查拼写（大小写敏感）
2. 确认扩展在 `manifest.json` 中注册
3. 查看可用扩展列表：
   ```bash
   ls ten_packages/extension/ | grep -E "asr|tts|llm"
   ```

### 8. 如果我用错了参数会发生什么？

**症状**：
```
[ERROR] Missing required parameter: 'region'
[ERROR] Invalid parameter value for 'key'
[WARN] Unknown parameter 'model' will be ignored
```

**原因**：扩展验证配置时发现问题

**解决方案**：
1. 查看扩展的 `manifest.json` 确认参数要求
2. 查看错误日志中的具体提示
3. 对照本文档的示例修改

## 总结

### 核心要点

1. **必须修改配置文件** - 因为不同扩展有不同的名称和参数要求
2. **两个关键字段**：
   - `addon`：指定扩展名称（必须匹配实际扩展）
   - `property`：提供扩展所需的参数（必须符合扩展的接口定义）
3. **技术原理**：TEN Framework 使用扩展架构，runtime 根据配置动态加载扩展
4. **代码证据**：
   - `main.go` 加载配置
   - `manifest.json` 定义接口
   - 各扩展实现有明确的参数要求差异

### 快速检查清单

使用替代服务时，请确认：

- [ ] 修改了 `property.json` 中的 `addon` 字段
- [ ] 修改了 `property.json` 中的 `property` 字段
- [ ] 参数名称与新扩展的要求匹配
- [ ] 在 `.env` 中配置了新的环境变量
- [ ] 新扩展已在 `manifest.json` 中注册
- [ ] 重启了应用以加载新配置

### 相关资源

- [免费试用指南](FREE_TRIAL_GUIDE.zh-CN.md) - 包含多种服务商的配置示例
- [集成指南](VOICE_INTEGRATION_GUIDE.zh-CN.md) - 项目集成详细说明
- [README](README.zh-CN.md) - 快速开始指南

## 获取帮助

如果遇到配置问题：

1. **查看日志**：
   ```bash
   tail -f /tmp/ten_agent/log/app.log
   ```

2. **验证配置**：
   ```bash
   # 验证 JSON 格式
   python3 -m json.tool tenapp/property.json
   ```

3. **联系社区**：
   - GitHub Issues: https://github.com/TEN-framework/ten-framework/issues
   - Discord: https://discord.gg/VnPftUzAMJ
   - 微信群: https://github.com/TEN-framework/ten-agent/discussions/170

---

**文档版本**：1.0  
**最后更新**：2026-02-04  
**适用版本**：TEN Framework 0.11+
