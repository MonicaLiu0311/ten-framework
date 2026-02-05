import asyncio
import json
import time
from typing import Literal, Optional
import aiohttp

from .agent.decorators import agent_event_handler
from ten_runtime import (
    AsyncExtension,
    AsyncTenEnv,
    Cmd,
    Data,
)

from .agent.agent import Agent
from .agent.events import (
    ASRResultEvent,
    UserJoinedEvent,
    UserLeftEvent,
)
from .helper import _send_cmd, _send_data
from .config import MainControlConfig

import uuid


class MainControlExtension(AsyncExtension):
    """
    简化的主控扩展，用于TEN语音识别 → Bisheng AI → TEN语音合成流程
    不使用内置的LLM，而是调用外部的Bisheng AI服务
    """

    def __init__(self, name: str):
        super().__init__(name)
        self.ten_env: AsyncTenEnv = None
        self.agent: Agent = None
        self.config: MainControlConfig = None

        self.stopped: bool = False
        self._rtc_user_count: int = 0
        self.turn_id: int = 0
        self.session_id: str = "0"
        self.http_session: Optional[aiohttp.ClientSession] = None

    def _current_metadata(self) -> dict:
        return {"session_id": self.session_id, "turn_id": self.turn_id}

    async def on_init(self, ten_env: AsyncTenEnv):
        self.ten_env = ten_env

        # Load config from runtime properties
        config_json, _ = await ten_env.get_property_to_json(None)
        self.config = MainControlConfig.model_validate_json(config_json)

        # Create HTTP session for Bisheng AI requests
        self.http_session = aiohttp.ClientSession()

        self.agent = Agent(ten_env)

        # Now auto-register decorated methods
        for attr_name in dir(self):
            fn = getattr(self, attr_name)
            event_type = getattr(fn, "_agent_event_type", None)
            if event_type:
                self.agent.on(event_type, fn)

    # === Register handlers with decorators ===
    @agent_event_handler(UserJoinedEvent)
    async def _on_user_joined(self, event: UserJoinedEvent):
        self._rtc_user_count += 1
        if self._rtc_user_count == 1 and self.config and self.config.greeting:
            await self._send_to_tts(self.config.greeting, True)
            await self._send_transcript(
                "assistant", self.config.greeting, True, 100
            )

    @agent_event_handler(UserLeftEvent)
    async def _on_user_left(self, event: UserLeftEvent):
        self._rtc_user_count -= 1

    @agent_event_handler(ASRResultEvent)
    async def _on_asr_result(self, event: ASRResultEvent):
        """处理语音识别结果，发送到Bisheng AI"""
        self.session_id = event.metadata.get("session_id", "100")
        stream_id = int(self.session_id)
        if not event.text:
            return
        
        # 发送用户输入的转录文本
        await self._send_transcript("user", event.text, event.final, stream_id)
        
        if event.final:
            self.turn_id += 1
            # 当识别完成时，调用Bisheng AI
            await self._call_bisheng_ai(event.text, stream_id)

    async def _call_bisheng_ai(self, user_input: str, stream_id: int):
        """
        调用Bisheng AI API获取响应
        支持助手(assistant)和工作流(workflow)两种模式
        """
        if not self.config.bisheng_ai_url:
            error_msg = "Bisheng AI URL未配置"
            self.ten_env.log_error(f"[MainControlExtension] {error_msg}")
            await self._send_to_tts(error_msg, True)
            return

        try:
            # 准备请求头
            headers = {"Content-Type": "application/json"}
            if self.config.bisheng_ai_api_key:
                headers["Authorization"] = f"Bearer {self.config.bisheng_ai_api_key}"

            # 准备请求数据
            request_data = {
                "input": user_input,
                "session_id": self.session_id,
            }

            # 根据配置选择调用助手或工作流
            if self.config.bisheng_ai_assistant_id:
                request_data["assistant_id"] = self.config.bisheng_ai_assistant_id
            if self.config.bisheng_ai_workflow_id:
                request_data["workflow_id"] = self.config.bisheng_ai_workflow_id

            self.ten_env.log_info(
                f"[MainControlExtension] 调用Bisheng AI: {self.config.bisheng_ai_url}"
            )

            # 发送请求到Bisheng AI
            async with self.http_session.post(
                self.config.bisheng_ai_url,
                json=request_data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=self.config.bisheng_ai_timeout),
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    # 从响应中提取文本（支持多种常见的响应格式）
                    response_text = (
                        result.get("output")
                        or result.get("response")
                        or result.get("text")
                        or result.get("answer")
                        or str(result)
                    )
                    
                    self.ten_env.log_info(
                        f"[MainControlExtension] Bisheng AI响应: {response_text}"
                    )

                    # 发送助手回复的转录
                    await self._send_transcript("assistant", response_text, True, stream_id)
                    
                    # 发送到TTS进行语音合成
                    await self._send_to_tts(response_text, True)
                else:
                    error_msg = f"Bisheng AI返回错误: {response.status}"
                    self.ten_env.log_error(
                        f"[MainControlExtension] {error_msg}, {await response.text()}"
                    )
                    await self._send_to_tts("抱歉，处理您的请求时出现错误。", True)

        except asyncio.TimeoutError:
            error_msg = "Bisheng AI请求超时"
            self.ten_env.log_error(f"[MainControlExtension] {error_msg}")
            await self._send_to_tts("抱歉，请求超时了。", True)
        except Exception as e:
            error_msg = f"调用Bisheng AI时出错: {str(e)}"
            self.ten_env.log_error(f"[MainControlExtension] {error_msg}")
            await self._send_to_tts("抱歉，处理您的请求时出现错误。", True)

    async def on_start(self, ten_env: AsyncTenEnv):
        ten_env.log_info("[MainControlExtension] on_start")

    async def on_stop(self, ten_env: AsyncTenEnv):
        ten_env.log_info("[MainControlExtension] on_stop")
        self.stopped = True
        if self.http_session:
            await self.http_session.close()
        await self.agent.stop()

    async def on_cmd(self, ten_env: AsyncTenEnv, cmd: Cmd):
        await self.agent.on_cmd(cmd)

    async def on_data(self, ten_env: AsyncTenEnv, data: Data):
        await self.agent.on_data(data)

    # === helpers ===
    async def _send_transcript(
        self,
        role: str,
        text: str,
        final: bool,
        stream_id: int,
        data_type: Literal["text", "reasoning"] = "text",
    ):
        """
        发送转录文本到websocket客户端
        """
        if data_type == "text":
            await _send_data(
                self.ten_env,
                "text_data",
                "websocket_server",
                {
                    "data_type": "transcribe",
                    "role": role,
                    "text": text,
                    "text_ts": int(time.time() * 1000),
                    "is_final": final,
                    "stream_id": stream_id,
                },
            )
        self.ten_env.log_info(
            f"[MainControlExtension] 发送转录: {role}, final={final}, text={text}"
        )

    async def _send_to_tts(self, text: str, is_final: bool):
        """
        发送文本到TTS系统进行语音合成
        """
        request_id = f"tts-request-{self.turn_id}"
        await _send_data(
            self.ten_env,
            "tts_text_input",
            "tts",
            {
                "request_id": request_id,
                "text": text,
                "text_input_end": is_final,
                "metadata": self._current_metadata(),
            },
        )
        self.ten_env.log_info(
            f"[MainControlExtension] 发送到TTS: is_final={is_final}, text={text}"
        )
