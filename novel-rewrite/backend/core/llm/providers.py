# NovelForge - 国内主流大模型适配器实现
# 包含DeepSeek、文心、千问、Kimi、GLM等

from typing import List, Dict, Any, AsyncGenerator
import json
from backend.core.llm.base import (
    BaseLLMProvider,
    LLMConfig,
    LLMProvider,
    ChatMessage,
    LLMResponse
)


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek大模型适配器"""
    
    DEFAULT_MODEL = "deepseek-chat"
    DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.config.base_url = config.base_url or self.DEFAULT_BASE_URL
        self.config.model = config.model or self.DEFAULT_MODEL
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
        }
        data.update(kwargs)
        
        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=result["model"],
            provider=LLMProvider.DEEPSEEK,
            usage=result.get("usage", {}),
            raw_response=result
        )
    
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "stream": True
        }
        data.update(kwargs)
        
        async with self.client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        json_data = json.loads(data)
                        if "choices" in json_data and len(json_data["choices"]) > 0:
                            delta = json_data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue


class WenxinProvider(BaseLLMProvider):
    """文心大模型适配器 - 百度文心"""
    
    DEFAULT_MODEL = "ERNIE-4.0-Turbo-8K"
    DEFAULT_BASE_URL = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.config.base_url = config.base_url or self.DEFAULT_BASE_URL
        self.config.model = config.model or self.DEFAULT_MODEL
    
    async def _get_access_token(self) -> str:
        """获取访问令牌 - 文心需要额外的access token"""
        # 简化版本：假设api_key就是access token，实际可以通过OAuth获取
        return self.config.api_key
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        access_token = await self._get_access_token()
        url = f"{self.config.base_url}/{self.config.model}"
        
        params = {"access_token": access_token}
        data = {
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
        }
        data.update(kwargs)
        
        response = await self.client.post(url, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result.get("result", ""),
            model=self.config.model,
            provider=LLMProvider.WENXIN,
            usage={
                "prompt_tokens": result.get("usage", {}).get("prompt_tokens", 0),
                "completion_tokens": result.get("usage", {}).get("completion_tokens", 0),
                "total_tokens": result.get("usage", {}).get("total_tokens", 0)
            },
            raw_response=result
        )
    
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        access_token = await self._get_access_token()
        url = f"{self.config.base_url}/{self.config.model}"
        
        params = {"access_token": access_token}
        data = {
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "top_p": self.config.top_p,
            "stream": True
        }
        data.update(kwargs)
        
        async with self.client.stream("POST", url, params=params, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    try:
                        json_data = json.loads(data)
                        if "result" in json_data:
                            yield json_data["result"]
                    except json.JSONDecodeError:
                        continue


class QianwenProvider(BaseLLMProvider):
    """千问大模型适配器 - 阿里通义千问"""
    
    DEFAULT_MODEL = "qwen-turbo"
    DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.config.base_url = config.base_url or self.DEFAULT_BASE_URL
        self.config.model = config.model or self.DEFAULT_MODEL
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
        }
        data.update(kwargs)
        
        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=result["model"],
            provider=LLMProvider.QIANWEN,
            usage=result.get("usage", {}),
            raw_response=result
        )
    
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "stream": True
        }
        data.update(kwargs)
        
        async with self.client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        json_data = json.loads(data)
                        if "choices" in json_data and len(json_data["choices"]) > 0:
                            delta = json_data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue


class KimiProvider(BaseLLMProvider):
    """Kimi大模型适配器 - 月之暗面"""
    
    DEFAULT_MODEL = "moonshot-v1-8k"
    DEFAULT_BASE_URL = "https://api.moonshot.cn/v1"
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.config.base_url = config.base_url or self.DEFAULT_BASE_URL
        self.config.model = config.model or self.DEFAULT_MODEL
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
        }
        data.update(kwargs)
        
        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=result["model"],
            provider=LLMProvider.KIMI,
            usage=result.get("usage", {}),
            raw_response=result
        )
    
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "stream": True
        }
        data.update(kwargs)
        
        async with self.client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        json_data = json.loads(data)
                        if "choices" in json_data and len(json_data["choices"]) > 0:
                            delta = json_data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue


class GLMProvider(BaseLLMProvider):
    """GLM大模型适配器 - 智谱AI"""
    
    DEFAULT_MODEL = "glm-4-flash"
    DEFAULT_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.config.base_url = config.base_url or self.DEFAULT_BASE_URL
        self.config.model = config.model or self.DEFAULT_MODEL
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
        }
        data.update(kwargs)
        
        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=result["model"],
            provider=LLMProvider.GLM,
            usage=result.get("usage", {}),
            raw_response=result
        )
    
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "stream": True
        }
        data.update(kwargs)
        
        async with self.client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        json_data = json.loads(data)
                        if "choices" in json_data and len(json_data["choices"]) > 0:
                            delta = json_data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue


class OpenAIProvider(BaseLLMProvider):
    """OpenAI适配器 - 作为参考实现"""
    
    DEFAULT_MODEL = "gpt-4"
    DEFAULT_BASE_URL = "https://api.openai.com/v1"
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.config.base_url = config.base_url or self.DEFAULT_BASE_URL
        self.config.model = config.model or self.DEFAULT_MODEL
    
    async def chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> LLMResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
        }
        data.update(kwargs)
        
        response = await self.client.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            model=result["model"],
            provider=LLMProvider.OPENAI,
            usage=result.get("usage", {}),
            raw_response=result
        )
    
    async def stream_chat_completion(
        self,
        messages: List[ChatMessage],
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }
        
        data = {
            "model": self.config.model,
            "messages": [
                {"role": m.role, "content": m.content}
                for m in messages
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "top_p": self.config.top_p,
            "stream": True
        }
        data.update(kwargs)
        
        async with self.client.stream("POST", url, headers=headers, json=data) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        json_data = json.loads(data)
                        if "choices" in json_data and len(json_data["choices"]) > 0:
                            delta = json_data["choices"][0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                    except json.JSONDecodeError:
                        continue
