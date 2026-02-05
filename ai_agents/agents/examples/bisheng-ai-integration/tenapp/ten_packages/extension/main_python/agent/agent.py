import asyncio
import json
from typing import Awaitable, Callable, Optional
from ten_runtime import AsyncTenEnv, Cmd, CmdResult, Data, StatusCode
from .events import *


class Agent:
    """
    简化的Agent类，用于Bisheng AI集成
    只处理ASR事件和用户事件，不包含LLM执行逻辑
    """
    def __init__(self, ten_env: AsyncTenEnv):
        self.ten_env: AsyncTenEnv = ten_env
        self.stopped = False

        # Callback registry
        self._callbacks: dict[
            AgentEvent, list[Callable[[AgentEvent], Awaitable]]
        ] = {}

        # Queue for ordered ASR processing
        self._asr_queue: asyncio.Queue[ASRResultEvent] = asyncio.Queue()

        # Current consumer task
        self._asr_consumer: Optional[asyncio.Task] = None

        # Start consumer
        self._asr_consumer = asyncio.create_task(self._consume_asr())

    # === Register handlers ===
    def on(
        self,
        event_type: AgentEvent,
        handler: Callable[[AgentEvent], Awaitable] = None,
    ):
        """
        Register a callback for a given event type.
        """
        def decorator(fn: Callable[[AgentEvent], Awaitable]):
            if event_type not in self._callbacks:
                self._callbacks[event_type] = []
            self._callbacks[event_type].append(fn)
            return fn

        if handler is None:
            return decorator
        else:
            return decorator(handler)

    async def _dispatch(self, event: AgentEvent):
        """Dispatch event to registered handlers sequentially."""
        for etype, handlers in self._callbacks.items():
            if isinstance(event, etype):
                for h in handlers:
                    try:
                        await h(event)
                    except asyncio.CancelledError:
                        raise
                    except Exception as e:
                        self.ten_env.log_error(
                            f"Handler error for {etype}: {e}"
                        )

    # === Consumers ===
    async def _consume_asr(self):
        """Consumer for ASR events"""
        while not self.stopped:
            event = await self._asr_queue.get()
            await self._dispatch(event)

    # === Emit events ===
    async def _emit_asr(self, event: ASRResultEvent):
        """Emit ASR event to the queue"""
        await self._asr_queue.put(event)

    async def _emit_direct(self, event: AgentEvent):
        """Emit event directly without queueing"""
        await self._dispatch(event)

    # === Incoming from runtime ===
    async def on_cmd(self, cmd: Cmd):
        """Handle incoming commands"""
        try:
            name = cmd.get_name()
            if name == "on_user_joined":
                await self._emit_direct(UserJoinedEvent())
            elif name == "on_user_left":
                await self._emit_direct(UserLeftEvent())
            else:
                self.ten_env.log_warn(f"Unhandled cmd: {name}")

            await self.ten_env.return_result(
                CmdResult.create(StatusCode.OK, cmd)
            )
        except Exception as e:
            self.ten_env.log_error(f"on_cmd error: {e}")
            await self.ten_env.return_result(
                CmdResult.create(StatusCode.ERROR, cmd)
            )

    async def on_data(self, data: Data):
        """Handle incoming data (ASR results)"""
        try:
            if data.get_name() == "asr_result":
                asr_json, _ = data.get_property_to_json(None)
                asr = json.loads(asr_json)
                await self._emit_asr(
                    ASRResultEvent(
                        text=asr.get("text", ""),
                        final=asr.get("final", False),
                        metadata=asr.get("metadata", {}),
                    )
                )
            else:
                self.ten_env.log_warn(f"Unhandled data: {data.get_name()}")
        except Exception as e:
            self.ten_env.log_error(f"on_data error: {e}")

    async def stop(self):
        """Stop the agent processing"""
        self.stopped = True
        if self._asr_consumer:
            self._asr_consumer.cancel()
            try:
                await self._asr_consumer
            except asyncio.CancelledError:
                pass
