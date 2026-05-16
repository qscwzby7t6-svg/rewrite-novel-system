# NovelForge - LLM模块初始化
# 导出所有核心模块

from backend.core.llm.base import (
    BaseLLMProvider,
    LLMProvider,
    LLMConfig,
    ChatMessage,
    LLMResponse,
    MessageRole
)
from backend.core.llm.providers import (
    DeepSeekProvider,
    WenxinProvider,
    QianwenProvider,
    KimiProvider,
    GLMProvider,
    OpenAIProvider
)
from backend.core.llm.factory import LLMFactory, LLMManager
from backend.core.llm.service import LLMRewriteService, llm_service

__all__ = [
    # Base
    'BaseLLMProvider',
    'LLMProvider',
    'LLMConfig',
    'ChatMessage',
    'LLMResponse',
    'MessageRole',
    # Providers
    'DeepSeekProvider',
    'WenxinProvider',
    'QianwenProvider',
    'KimiProvider',
    'GLMProvider',
    'OpenAIProvider',
    # Factory
    'LLMFactory',
    'LLMManager',
    # Service
    'LLMRewriteService',
    'llm_service'
]
