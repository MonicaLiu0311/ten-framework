from pydantic import BaseModel
from typing import Optional


class MainControlConfig(BaseModel):
    greeting: str = "Hello, I am your AI assistant."
    bisheng_ai_url: str = ""
    bisheng_ai_api_key: Optional[str] = None
    bisheng_ai_assistant_id: Optional[str] = None
    bisheng_ai_workflow_id: Optional[str] = None
    bisheng_ai_timeout: int = 30
