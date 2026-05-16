# NovelForge - 大模型抽象接口
# 提供统一的LLM调用接口，支持国内主流大模型

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
from enum import Enum
import asyncio
import httpx
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """LLM提供商枚举"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"  # DeepSeek系列
    WENXIN = "wenxin"      # 文心大模型
    QIANWEN = "qianwen"    # 千问系列
    KIMI = "kimi"          # Kimi/月之暗面
    GLM = "glm"            # GLM/智谱AI


class MessageRole(str, Enum):
    """消息角色"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    """聊天消息"""
    role: MessageRole
    content: str
    name: Optional[str] = None


class LLMResponse(BaseModel):
    """LLM响应"""
    content: str
    model: str
    provider: LLMProvider
    usage: Dict[str, Any] = Field(default_factory=dict)
    raw_response: Any = None


class LLMConfig(BaseModel):
    """LLM配置"""
    provider: LLMProvider
    api_key: str
    base_url: Optional[str] = None
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 1.0
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    timeout: int = 60


class BaseLLMProvider(ABC):
    """LLM提供商基类"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = httpx.AsyncClient(
            timeout=config.timeout,
            follow_redirects=True
        )
    
    @abstractmethod
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        """聊天补全"""
        pass
    
    @abstractmethod
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """流式聊天补全"""
        pass
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
