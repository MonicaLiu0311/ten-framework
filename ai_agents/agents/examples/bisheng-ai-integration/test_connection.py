#!/usr/bin/env python3
"""
Test script for Bisheng AI integration
测试脚本，用于验证毕昇AI集成配置是否正确
"""

import os
import sys
import asyncio
import aiohttp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


async def test_bisheng_ai_connection():
    """Test connection to Bisheng AI service"""
    print("\n" + "="*60)
    print("Testing Bisheng AI Connection / 测试毕昇AI连接")
    print("="*60 + "\n")
    
    # Get configuration from environment
    url = os.getenv("BISHENG_AI_URL")
    api_key = os.getenv("BISHENG_AI_API_KEY")
    assistant_id = os.getenv("BISHENG_AI_ASSISTANT_ID")
    workflow_id = os.getenv("BISHENG_AI_WORKFLOW_ID")
    
    # Validate configuration
    if not url:
        print(f"{RED}❌ BISHENG_AI_URL is not configured{RESET}")
        print(f"{YELLOW}Please set BISHENG_AI_URL in your .env file{RESET}")
        return False
    
    print(f"URL: {url}")
    print(f"API Key: {'***' + api_key[-4:] if api_key else 'Not configured'}")
    print(f"Assistant ID: {assistant_id or 'Not configured'}")
    print(f"Workflow ID: {workflow_id or 'Not configured'}")
    
    if not assistant_id and not workflow_id:
        print(f"{YELLOW}⚠️  Neither BISHENG_AI_ASSISTANT_ID nor BISHENG_AI_WORKFLOW_ID is configured{RESET}")
        print(f"{YELLOW}Please configure at least one of them{RESET}")
        return False
    
    # Prepare request
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    request_data = {
        "input": "你好，这是一个测试消息",
        "session_id": "test_session_123",
    }
    
    if assistant_id:
        request_data["assistant_id"] = assistant_id
    if workflow_id:
        request_data["workflow_id"] = workflow_id
    
    print(f"\n{YELLOW}Sending test request...{RESET}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=request_data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as response:
                print(f"\nStatus Code: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print(f"{GREEN}✓ Connection successful!{RESET}")
                    print(f"\nResponse:")
                    print(f"  {result}")
                    
                    # Try to extract response text
                    response_text = (
                        result.get("output")
                        or result.get("response")
                        or result.get("text")
                        or result.get("answer")
                    )
                    
                    if response_text:
                        print(f"\n{GREEN}✓ Successfully extracted response text:{RESET}")
                        print(f"  {response_text}")
                    else:
                        print(f"\n{YELLOW}⚠️  Could not find response text in standard fields{RESET}")
                        print(f"{YELLOW}You may need to adjust the response parsing logic{RESET}")
                    
                    return True
                else:
                    print(f"{RED}❌ Request failed with status {response.status}{RESET}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return False
                    
    except asyncio.TimeoutError:
        print(f"{RED}❌ Request timed out after 30 seconds{RESET}")
        print(f"{YELLOW}Please check if the Bisheng AI service is running{RESET}")
        return False
    except aiohttp.ClientConnectorError as e:
        print(f"{RED}❌ Connection error: {e}{RESET}")
        print(f"{YELLOW}Please check if the URL is correct and the service is accessible{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ Unexpected error: {e}{RESET}")
        return False


def test_environment_variables():
    """Test if all required environment variables are set"""
    print("\n" + "="*60)
    print("Checking Environment Variables / 检查环境变量")
    print("="*60 + "\n")
    
    required_vars = [
        ("DEEPGRAM_API_KEY", "Speech-to-Text (STT)"),
        ("ELEVENLABS_TTS_KEY", "Text-to-Speech (TTS)"),
        ("BISHENG_AI_URL", "Bisheng AI Service"),
    ]
    
    optional_vars = [
        ("BISHENG_AI_API_KEY", "Bisheng AI Authentication"),
        ("BISHENG_AI_ASSISTANT_ID", "Assistant Mode"),
        ("BISHENG_AI_WORKFLOW_ID", "Workflow Mode"),
    ]
    
    all_ok = True
    
    print("Required variables:")
    for var, description in required_vars:
        value = os.getenv(var)
        if value:
            print(f"  {GREEN}✓{RESET} {var:30s} ({description})")
        else:
            print(f"  {RED}❌{RESET} {var:30s} ({description}) - NOT SET")
            all_ok = False
    
    print("\nOptional variables:")
    for var, description in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"  {GREEN}✓{RESET} {var:30s} ({description})")
        else:
            print(f"  {YELLOW}⚠️ {RESET} {var:30s} ({description}) - Not configured")
    
    return all_ok


async def main():
    """Main test function"""
    print("\n" + "="*60)
    print("Bisheng AI Integration Test Script")
    print("毕昇AI集成测试脚本")
    print("="*60)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    if not env_ok:
        print(f"\n{RED}❌ Some required environment variables are missing{RESET}")
        print(f"{YELLOW}Please configure them in your .env file{RESET}")
        sys.exit(1)
    
    # Test Bisheng AI connection
    connection_ok = await test_bisheng_ai_connection()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary / 测试摘要")
    print("="*60 + "\n")
    
    if env_ok and connection_ok:
        print(f"{GREEN}✓ All tests passed!{RESET}")
        print(f"{GREEN}Your Bisheng AI integration is configured correctly.{RESET}")
        print(f"\nYou can now run:")
        print(f"  cd ai_agents/agents/examples/bisheng-ai-integration")
        print(f"  task run")
        sys.exit(0)
    else:
        print(f"{RED}❌ Some tests failed{RESET}")
        print(f"{YELLOW}Please check the errors above and fix your configuration{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
