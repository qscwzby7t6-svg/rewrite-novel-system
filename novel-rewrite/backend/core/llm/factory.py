# NovelForge - LLM工厂类
# 统一的LLM创建和管理接口

from typing import Optional, Dict, Any
from backend.core.llm.base import (
    BaseLLMProvider,
    LLMConfig,
    LLMProvider,
    ChatMessage
)
from backend.core.llm.providers import (
    DeepSeekProvider,
    WenxinProvider,
    QianwenProvider,
    KimiProvider,
    GLMProvider,
    OpenAIProvider
)


class LLMFactory:
    """LLM工厂类"""
    
    _providers = {
        LLMProvider.DEEPSEEK: DeepSeekProvider,
        LLMProvider.WENXIN: WenxinProvider,
        LLMProvider.QIANWEN: QianwenProvider,
        LLMProvider.KIMI: KimiProvider,
        LLMProvider.GLM: GLMProvider,
        LLMProvider.OPENAI: OpenAIProvider,
    }
    
    _model_defaults = {
        LLMProvider.DEEPSEEK: ["deepseek-chat", "deepseek-coder"],
        LLMProvider.WENXIN: ["ERNIE-4.0-Turbo-8K", "ERNIE-3.5-8K"],
        LLMProvider.QIANWEN: ["qwen-turbo", "qwen-plus", "qwen-max"],
        LLMProvider.KIMI: ["moonshot-v1-8k", "moonshot-v1-32k"],
        LLMProvider.GLM: ["glm-4-flash", "glm-4", "glm-3-turbo"],
        LLMProvider.OPENAI: ["gpt-4", "gpt-3.5-turbo"],
    }
    
    @classmethod
    def create(cls, config: LLMConfig) -> BaseLLMProvider:
        """创建LLM提供者"""
        provider_class = cls._providers.get(config.provider)
        if not provider_class:
            raise ValueError(f"Unsupported LLM provider: {config.provider}")
        return provider_class(config)
    
    @classmethod
    def get_available_providers(cls) -> list:
        """获取可用的LLM提供商列表"""
        return list(cls._providers.keys())
    
    @classmethod
    def get_default_models(cls, provider: LLMProvider) -> list:
        """获取指定提供商的默认模型列表"""
        return cls._model_defaults.get(provider, [])


class LLMManager:
    """LLM管理器 - 封装常用调用方法"""
    
    def __init__(self, config: LLMConfig):
        self.provider = LLMFactory.create(config)
        self.config = config
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """生成文本 - 简化接口"""
        messages = []
        
        if system_prompt:
            messages.append(ChatMessage(
                role="system",
                content=system_prompt
            ))
        
        messages.append(ChatMessage(
            role="user",
            content=prompt
        ))
        
        response = await self.provider.chat_completion(messages, **kwargs)
        return response.content
    
    async def generate_with_context(
        self,
        messages: list,
        **kwargs: Any
    ) -> str:
        """带上下文生成文本"""
        response = await self.provider.chat_completion(messages, **kwargs)
        return response.content
    
    async def stream_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs: Any
    ):
        """流式生成文本"""
        messages = []
        
        if system_prompt:
            messages.append(ChatMessage(
                role="system",
                content=system_prompt
            ))
        
        messages.append(ChatMessage(
            role="user",
            content=prompt
        ))
        
        async for chunk in self.provider.stream_chat_completion(messages, **kwargs):
            yield chunk
    
    async def close(self):
        """关闭连接"""
        await self.provider.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
