# Free Trial Guide

If you don't have all the required API keys yet, this guide will help you get started with free trial accounts or use alternative services to experience the voice conversation features.

English | [简体中文](FREE_TRIAL_GUIDE.zh-CN.md)

## Table of Contents

- [Quick Overview: What Services You Need](#quick-overview-what-services-you-need)
- [Free Trial Options](#free-trial-options)
- [Alternative Service Providers](#alternative-service-providers)
- [Minimal Configuration Plans](#minimal-configuration-plans)
- [FAQ](#faq)

## Quick Overview: What Services You Need

A voice conversation system requires four types of services:

| Service Type | Purpose | Required |
|-------------|---------|----------|
| **RTC (Real-Time Communication)** | Audio/video transmission | ✅ Yes |
| **STT (Speech-to-Text)** | Recognize user speech | ✅ Yes |
| **LLM (Large Language Model)** | Understand and generate responses | ✅ Yes |
| **TTS (Text-to-Speech)** | Convert responses to speech | ✅ Yes |

**Good News**: All of these services offer free trials or free tiers!

## Free Trial Options

### 1. Agora (Real-Time Communication)

**Free Tier**:
- ✅ 10,000 minutes per month free
- ✅ No credit card required
- ✅ Permanent free tier

**Sign-up Steps**:
1. Visit [Agora Console](https://console.agora.io/)
2. Register (supports email, GitHub, Google login)
3. Create a project
4. Get App ID (immediately available)
5. Enable App Certificate if needed (optional)

**Time to Get**: < 5 minutes

### 2. OpenAI (Large Language Model)

**Free Tier**:
- ⚠️ New users may get $5 free credits (policy may change)
- 💰 Requires payment method
- 💡 Cost: GPT-4o mini ~$0.15/million tokens (very affordable)

**Sign-up Steps**:
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Register an account
3. Add payment method (credit card or PayPal)
4. Create API Key

**Time to Get**: 5-10 minutes

**Alternative Options (Recommended)**:

#### 2a. Gemini (Google) - Recommended ⭐

**Free Tier**:
- ✅ 15 requests per minute free
- ✅ 1,500 requests per day free
- ✅ Permanent free tier (Gemini 1.5 Flash)
- ✅ No credit card required

**Sign-up Steps**:
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Login with Google account
3. Click "Get API Key"
4. Create API Key (immediately available)

**Time to Get**: < 3 minutes

**Configuration**:
```bash
# In .env file
GEMINI_API_KEY=your_gemini_api_key

# In property.json, change LLM to gemini_llm2_python
```

#### 2b. Qwen (Alibaba Cloud) - For Chinese Users ⭐⭐

**Free Tier**:
- ✅ 1 million tokens per month free (Qwen-Turbo)
- ✅ Additional trial credits for new users
- ✅ Excellent Chinese language support

**Sign-up Steps**:
1. Visit [Alibaba Cloud DashScope](https://dashscope.aliyun.com/)
2. Register Alibaba Cloud account
3. Enable DashScope service
4. Create API Key

**Time to Get**: 5 minutes

**Configuration**:
```bash
# In .env file
QWEN_API_KEY=your_qwen_api_key

# In property.json, change LLM addon to qwen_llm
```

#### 2c. DeepSeek - Most Affordable ⭐⭐⭐

**Pricing**:
- 💰 Very low cost: $0.14/million input tokens, $0.28/million output tokens
- ✅ New users get free trial credits
- ✅ OpenAI API compatible

**Sign-up Steps**:
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Register an account
3. Add small amount of credits (e.g., $5)
4. Create API Key

**Time to Get**: 5 minutes

**Configuration**:
```bash
# In .env file
DEEPSEEK_API_KEY=your_deepseek_api_key

# In property.json, use deepseek_llm
```

### 3. Deepgram (Speech-to-Text)

**Free Tier**:
- ✅ $200 free credits
- ✅ ~45,000 minutes of transcription
- ✅ No credit card required

**Sign-up Steps**:
1. Visit [Deepgram Console](https://console.deepgram.com/)
2. Register (supports email, GitHub, Google login)
3. Automatically get $200 credits
4. Create API Key

**Time to Get**: < 5 minutes

**Alternative Options**:

#### 3a. Azure STT - Recommended ⭐

**Free Tier**:
- ✅ 5 hours per month free (Standard)
- ✅ Supports multiple languages
- 💳 Requires credit card (no auto-charge)

**Sign-up Steps**:
1. Visit [Azure Portal](https://portal.azure.com/)
2. Register Microsoft account
3. Create Speech service resource
4. Get API Key and region

**Configuration**:
```bash
# In .env file
AZURE_ASR_API_KEY=your_azure_key
AZURE_ASR_REGION=your_region

# In property.json, change STT to azure_asr_python
```

#### 3b. Google STT

**Free Tier**:
- ✅ 60 minutes per month free

**Configuration**:
```bash
# In property.json, change STT to google_asr_python
```

### 4. ElevenLabs (Text-to-Speech)

**Free Tier**:
- ✅ 10,000 characters per month free
- ✅ ~10-15 minutes of speech
- ✅ No credit card required

**Sign-up Steps**:
1. Visit [ElevenLabs](https://elevenlabs.io/)
2. Register an account
3. Automatically get free quota
4. Find API Key in settings

**Time to Get**: < 5 minutes

**Alternative Options**:

#### 4a. Azure TTS - Recommended ⭐

**Free Tier**:
- ✅ 5 million characters per month free (Neural Voice)
- ✅ Supports multiple languages
- 💳 Requires credit card

**Configuration**:
```bash
# In .env file
AZURE_TTS_KEY=your_azure_key
AZURE_TTS_REGION=your_region

# In property.json, change TTS to azure_tts_python
```

#### 4b. Google TTS

**Free Tier**:
- ✅ 4 million characters per month free
- ✅ Supports multiple languages

**Configuration**:
```bash
# In property.json, change TTS to google_tts_python
```

## Alternative Service Providers

TEN Framework supports multiple service providers. Choose based on your situation:

### STT (Speech-to-Text) Providers

| Provider | Free Tier | Multi-Language | Recommendation |
|----------|-----------|----------------|----------------|
| **Deepgram** | $200 credits | ✅ | ⭐⭐⭐ |
| **Azure** | 5 hours/month | ✅ | ⭐⭐⭐ |
| **Google** | 60 minutes/month | ✅ | ⭐⭐ |
| **OpenAI Whisper** | Pay-as-you-go | ✅ | ⭐⭐ |
| **AssemblyAI** | $50 credits | ✅ | ⭐⭐ |

### LLM (Language Model) Providers

| Provider | Free Tier | Multi-Language | Recommendation |
|----------|-----------|----------------|----------------|
| **Gemini** | 1500 requests/day | ✅ | ⭐⭐⭐ |
| **Qwen** | 1M tokens/month | ✅ | ⭐⭐⭐ |
| **DeepSeek** | Very low cost | ✅ | ⭐⭐⭐ |
| **OpenAI** | Requires payment | ✅ | ⭐⭐ |
| **Azure OpenAI** | Requires payment | ✅ | ⭐⭐ |

### TTS (Text-to-Speech) Providers

| Provider | Free Tier | Multi-Language | Recommendation |
|----------|-----------|----------------|----------------|
| **Azure** | 5M chars/month | ✅ | ⭐⭐⭐ |
| **Google** | 4M chars/month | ✅ | ⭐⭐⭐ |
| **ElevenLabs** | 10K chars/month | ⚠️ | ⭐⭐ |
| **OpenAI TTS** | Pay-as-you-go | ✅ | ⭐⭐ |

## Minimal Configuration Plans

### Plan 1: Completely Free (Recommended) ⭐⭐⭐

**Total Cost**: $0
**Time Required**: ~20 minutes

```bash
# .env configuration
AGORA_APP_ID=your_agora_app_id          # Free: 10,000 min/month
GEMINI_API_KEY=your_gemini_api_key      # Free: 1,500 req/day
AZURE_ASR_API_KEY=your_azure_key        # Free: 5 hours/month
AZURE_ASR_REGION=your_region
AZURE_TTS_KEY=your_azure_key            # Free: 5M chars/month
AZURE_TTS_REGION=your_region
```

**Features**:
- ✅ Completely free
- ✅ Generous quotas (sufficient for personal use)
- ⚠️ Azure requires credit card (no auto-charge)

### Plan 2: Minimal Cost (DeepSeek) ⭐

**Total Cost**: ~$5-10 (lasts a long time)
**Time Required**: ~25 minutes

```bash
# .env configuration
AGORA_APP_ID=your_agora_app_id          # Free: 10,000 min/month
DEEPSEEK_API_KEY=your_deepseek_api_key  # Very low cost
AZURE_ASR_API_KEY=your_azure_key        # Free: 5 hours/month
AZURE_ASR_REGION=your_region
AZURE_TTS_KEY=your_azure_key            # Free: 5M chars/month
AZURE_TTS_REGION=your_region
```

**Features**:
- 💰 Extremely low total cost
- ✅ Excellent performance
- ✅ Good for production use

## Configuration Steps

### 1. Choose Your Plan

Select the most suitable configuration based on the plans above.

### 2. Get API Keys

Follow the instructions above to register and obtain API keys for each service.

### 3. Configure .env File

```bash
cd ai_agents
cp .env.example .env
# Edit .env file and fill in your API keys
```

### 4. Modify property.json (If Using Alternatives)

If you're using alternative services (not the default Deepgram + OpenAI + ElevenLabs), you need to modify the configuration file:

**Location**: `agents/examples/voice-assistant/tenapp/property.json`

**Example: Using Gemini + Azure STT + Azure TTS**:

Find the STT configuration:
```json
{
  "name": "stt",
  "addon": "azure_asr_python",  // Change to azure_asr_python
  "property": {
    "params": {
      "api_key": "${env:AZURE_ASR_API_KEY}",
      "region": "${env:AZURE_ASR_REGION}",
      "language": "en-US"
    }
  }
}
```

Find the LLM configuration:
```json
{
  "name": "llm",
  "addon": "gemini_llm2_python",  // Change to gemini_llm2_python
  "property": {
    "api_key": "${env:GEMINI_API_KEY}",
    "model": "gemini-1.5-flash",
    "max_tokens": 512
  }
}
```

Find the TTS configuration:
```json
{
  "name": "tts",
  "addon": "azure_tts_python",  // Change to azure_tts_python
  "property": {
    "params": {
      "key": "${env:AZURE_TTS_KEY}",
      "region": "${env:AZURE_TTS_REGION}",
      "voice_name": "en-US-JennyNeural"
    }
  }
}
```

### 5. Start the Service

```bash
cd agents/examples/voice-assistant
task install
task run
```

### 6. Access the Application

Open your browser and visit: http://localhost:3000

## FAQ

### 1. Can I try it without a credit card?

**Yes!** Use Plan 1:
- Agora: No credit card needed, 10,000 minutes/month free
- Gemini: No credit card needed, 1,500 requests/day free
- Note: Azure requires credit card but won't auto-charge

### 2. Are the free quotas sufficient?

For personal trial and learning:
- **Completely sufficient** ✅
- Agora 10,000 minutes = 166 hours
- Azure TTS 5M characters = ~5-10 hours of speech
- Gemini 1,500 requests/day = thousands of conversations

For small projects:
- **Generally sufficient** ✅
- Can handle hundreds of daily users

For production:
- Need paid plans, but costs are reasonable
- Pay-as-you-go based on actual usage

### 3. Which plan is most recommended?

**Plan 1 (Gemini + Azure)** is most recommended:
- Completely free
- Generous quotas
- Good performance
- Only requires credit card for Azure (no charges)

### 4. How do I verify my API keys are correct?

After starting the service, check the log output:
```bash
# View logs in container
docker exec -it ten_agent_dev tail -f /tmp/ten_agent/log/app.log
```

If you see connection errors, check:
1. API keys are copied correctly (no extra spaces)
2. Environment variables are set correctly
3. Addon names in property.json are correct

### 5. Can I mix different providers?

**Absolutely!** This is a key advantage of TEN Framework.

Example:
- RTC: Agora
- STT: Deepgram (better English recognition)
- LLM: Qwen (better Chinese understanding)
- TTS: Azure (natural Chinese voices)

Each service is configured independently and can be freely combined.

### 6. What happens when free quota runs out?

**Option 1**: Switch to another provider
- TEN Framework supports multiple providers
- Just modify the configuration file

**Option 2**: Pay for usage
- Most services have affordable pricing
- Pay-as-you-go based on actual usage

**Option 3**: Wait for next month
- Most free quotas reset monthly

### 7. Are there educational discounts?

**Yes!**

- **Azure**: Students get $100 free credits (12 months)
  - Visit: https://azure.microsoft.com/en-us/free/students/
  
- **Google Cloud**: New users get $300 free credits (90 days)
  - Visit: https://cloud.google.com/free
  
- **AWS**: Students get $50-100 AWS Educate credits
  - Visit: https://aws.amazon.com/education/awseducate/

- **GitHub Student Pack**: Includes discounts for multiple services
  - Visit: https://education.github.com/pack

## Next Steps

1. **Choose a plan**: Select the most suitable plan for your situation
2. **Get API keys**: Register and obtain API keys following the guide
3. **Configure services**: Modify .env and property.json files
4. **Start and test**: Run the service and test the experience
5. **Optimize**: Adjust configuration based on actual usage

## Get Help

If you encounter problems during configuration:

- **Documentation**: See [README.md](README.md)
- **Integration Guide**: See [VOICE_INTEGRATION_GUIDE.md](VOICE_INTEGRATION_GUIDE.md)
- **Discord**: https://discord.gg/VnPftUzAMJ
- **GitHub Issues**: https://github.com/TEN-framework/ten-framework/issues

---

**Happy Trying!** 🎉

If you find TEN Framework useful, please give us a ⭐ Star: https://github.com/TEN-framework/ten-framework
