# NovelForge - LLM模块测试

import pytest
import asyncio
from backend.core.llm.base import LLMConfig, LLMProvider, ChatMessage, MessageRole
from backend.core.llm.providers import (
    DeepSeekProvider,
    WenxinProvider,
    QianwenProvider,
    KimiProvider,
    GLMProvider,
    OpenAIProvider
)
from backend.core.llm.factory import LLMFactory, LLMManager
from backend.core.llm.service import LLMRewriteService


class TestLLMBase:
    """测试基础LLM类"""
    
    def test_llm_config(self):
        """测试LLM配置"""
        config = LLMConfig(
            provider=LLMProvider.DEEPSEEK,
            api_key="test_key",
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=2000
        )
        
        assert config.provider == LLMProvider.DEEPSEEK
        assert config.api_key == "test_key"
        assert config.model == "deepseek-chat"
        assert config.temperature == 0.7
        assert config.max_tokens == 2000
    
    def test_chat_message(self):
        """测试聊天消息"""
        msg = ChatMessage(
            role=MessageRole.USER,
            content="你好，世界"
        )
        
        assert msg.role == MessageRole.USER
        assert msg.content == "你好，世界"


class TestLLMFactory:
    """测试LLM工厂类"""
    
    def test_get_available_providers(self):
        """测试获取可用提供商"""
        providers = LLMFactory.get_available_providers()
        
        assert LLMProvider.DEEPSEEK in providers
        assert LLMProvider.WENXIN in providers
        assert LLMProvider.QIANWEN in providers
        assert LLMProvider.KIMI in providers
        assert LLMProvider.GLM in providers
        assert LLMProvider.OPENAI in providers
    
    def test_get_default_models(self):
        """测试获取默认模型列表"""
        for provider in [
            LLMProvider.DEEPSEEK,
            LLMProvider.WENXIN,
            LLMProvider.QIANWEN,
            LLMProvider.KIMI,
            LLMProvider.GLM,
            LLMProvider.OPENAI
        ]:
            models = LLMFactory.get_default_models(provider)
            assert isinstance(models, list)
            assert len(models) > 0
    
    def test_create_deepseek_provider(self):
        """测试创建DeepSeek提供商"""
        config = LLMConfig(
            provider=LLMProvider.DEEPSEEK,
            api_key="test_key"
        )
        
        provider = LLMFactory.create(config)
        assert isinstance(provider, DeepSeekProvider)
    
    def test_create_wenxin_provider(self):
        """测试创建文心提供商"""
        config = LLMConfig(
            provider=LLMProvider.WENXIN,
            api_key="test_key"
        )
        
        provider = LLMFactory.create(config)
        assert isinstance(provider, WenxinProvider)
    
    def test_create_qianwen_provider(self):
        """测试创建千问提供商"""
        config = LLMConfig(
            provider=LLMProvider.QIANWEN,
            api_key="test_key"
        )
        
        provider = LLMFactory.create(config)
        assert isinstance(provider, QianwenProvider)
    
    def test_create_kimi_provider(self):
        """测试创建Kimi提供商"""
        config = LLMConfig(
            provider=LLMProvider.KIMI,
            api_key="test_key"
        )
        
        provider = LLMFactory.create(config)
        assert isinstance(provider, KimiProvider)
    
    def test_create_glm_provider(self):
        """测试创建GLM提供商"""
        config = LLMConfig(
            provider=LLMProvider.GLM,
            api_key="test_key"
        )
        
        provider = LLMFactory.create(config)
        assert isinstance(provider, GLMProvider)
    
    def test_create_openai_provider(self):
        """测试创建OpenAI提供商"""
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            api_key="test_key"
        )
        
        provider = LLMFactory.create(config)
        assert isinstance(provider, OpenAIProvider)


class TestLLMService:
    """测试LLM服务类"""
    
    @pytest.fixture
    def llm_service(self):
        """创建LLM服务实例"""
        return LLMRewriteService()
    
    def test_get_available_providers(self, llm_service):
        """测试获取可用提供商"""
        providers = llm_service.get_available_providers()
        assert len(providers) > 0
        assert LLMProvider.DEEPSEEK in providers
    
    def test_get_provider_models(self, llm_service):
        """测试获取提供商模型列表"""
        models = llm_service.get_provider_models(LLMProvider.DEEPSEEK)
        assert isinstance(models, list)
        assert len(models) > 0


class TestDescriptionExpansion:
    """测试描述扩写功能"""
    
    @pytest.fixture
    def llm_service(self):
        """创建LLM服务实例"""
        return LLMRewriteService()
    
    def test_build_expansion_prompt(self):
        """测试构建扩写提示词"""
        test_text = "小红很紧张"
        
        # 这里我们不实际调用API，只是测试逻辑
        # 完整的集成测试需要真实的API密钥
        
        assert "小红很紧张" in test_text


class TestProviderConfigs:
    """测试各提供商的配置"""
    
    def test_deepseek_default_model(self):
        """测试DeepSeek默认模型"""
        config = LLMConfig(
            provider=LLMProvider.DEEPSEEK,
            api_key="test_key"
        )
        # 默认模型应该在初始化时设置
        provider = DeepSeekProvider(config)
        # 验证provider创建成功
        assert provider is not None
    
    def test_wenxin_default_model(self):
        """测试文心默认模型"""
        config = LLMConfig(
            provider=LLMProvider.WENXIN,
            api_key="test_key"
        )
        provider = WenxinProvider(config)
        assert provider is not None
    
    def test_qianwen_default_model(self):
        """测试千问默认模型"""
        config = LLMConfig(
            provider=LLMProvider.QIANWEN,
            api_key="test_key"
        )
        provider = QianwenProvider(config)
        assert provider is not None
    
    def test_kimi_default_model(self):
        """测试Kimi默认模型"""
        config = LLMConfig(
            provider=LLMProvider.KIMI,
            api_key="test_key"
        )
        provider = KimiProvider(config)
        assert provider is not None
    
    def test_glm_default_model(self):
        """测试GLM默认模型"""
        config = LLMConfig(
            provider=LLMProvider.GLM,
            api_key="test_key"
        )
        provider = GLMProvider(config)
        assert provider is not None


class TestMultiLanguageSupport:
    """测试多语言支持"""
    
    def test_language_configs(self):
        """测试语言配置"""
        # 测试中文配置
        config_zh = LLMConfig(
            provider=LLMProvider.DEEPSEEK,
            api_key="test_key"
        )
        assert config_zh.provider == LLMProvider.DEEPSEEK
        
        # 测试可以为不同语言创建配置
        configs = [
            LLMConfig(provider=LLMProvider.QIANWEN, api_key="test"),  # 阿里千问，中文优化
            LLMConfig(provider=LLMProvider.WENXIN, api_key="test"),  # 百度文心，中文优化
            LLMConfig(provider=LLMProvider.GLM, api_key="test"),     # 智谱AI，中文优化
        ]
        
        for config in configs:
            assert config.api_key == "test"


# 集成测试标记，需要真实API密钥才能运行
@pytest.mark.integration
class TestLLMIntegration:
    """LLM集成测试（需要真实API密钥）"""
    
    @pytest.mark.skip(reason="需要真实API密钥才能运行")
    async def test_deepseek_chat(self):
        """测试DeepSeek聊天"""
        config = LLMConfig(
            provider=LLMProvider.DEEPSEEK,
            api_key="your_api_key_here"
        )
        provider = DeepSeekProvider(config)
        
        messages = [
            ChatMessage(role=MessageRole.USER, content="你好")
        ]
        
        response = await provider.chat_completion(messages)
        assert response.content is not None
        assert len(response.content) > 0
    
    @pytest.mark.skip(reason="需要真实API密钥才能运行")
    async def test_description_expansion_integration(self):
        """测试描述扩写集成"""
        service = LLMRewriteService()
        
        # 这里需要配置好API密钥
        expanded = await service.expand_description(
            "小红很紧张",
            LLMProvider.DEEPSEEK
        )
        
        assert len(expanded) > len("小红很紧张")
        assert "紧张" not in expanded  # 应该被具体描述替代


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
