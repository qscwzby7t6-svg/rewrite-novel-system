# NovelForge - LLM服务模块
# 整合所有大模型功能，提供小说仿写专用接口

from typing import Optional, Dict, Any, List
from backend.config import settings
from backend.core.llm.base import LLMConfig, LLMProvider, ChatMessage
from backend.core.llm.factory import LLMManager, LLMFactory
from backend.models.novel import NovelDocument, Chapter, Character, ChapterContext


class LLMRewriteService:
    """LLM仿写服务"""
    
    def __init__(self):
        self._current_provider = None
        self._manager_cache = {}
    
    def _get_llm_config(self, provider: Optional[LLMProvider] = None) -> LLMConfig:
        """获取LLM配置"""
        provider = provider or LLMProvider(settings.DEFAULT_LLM_PROVIDER)
        
        # 根据提供商获取对应的API密钥和配置
        provider_configs = {
            LLMProvider.DEEPSEEK: {
                "api_key": settings.DEEPSEEK_API_KEY,
                "base_url": settings.DEEPSEEK_BASE_URL,
                "model": settings.DEEPSEEK_MODEL
            },
            LLMProvider.WENXIN: {
                "api_key": settings.WENXIN_API_KEY,
                "base_url": settings.WENXIN_BASE_URL,
                "model": settings.WENXIN_MODEL
            },
            LLMProvider.QIANWEN: {
                "api_key": settings.QIANWEN_API_KEY,
                "base_url": settings.QIANWEN_BASE_URL,
                "model": settings.QIANWEN_MODEL
            },
            LLMProvider.KIMI: {
                "api_key": settings.KIMI_API_KEY,
                "base_url": settings.KIMI_BASE_URL,
                "model": settings.KIMI_MODEL
            },
            LLMProvider.GLM: {
                "api_key": settings.GLM_API_KEY,
                "base_url": settings.GLM_BASE_URL,
                "model": settings.GLM_MODEL
            },
            LLMProvider.OPENAI: {
                "api_key": settings.OPENAI_API_KEY,
                "base_url": settings.OPENAI_BASE_URL,
                "model": settings.OPENAI_MODEL
            }
        }
        
        config = provider_configs[provider]
        
        return LLMConfig(
            provider=provider,
            api_key=config["api_key"],
            base_url=config["base_url"],
            model=config["model"],
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            top_p=settings.LLM_TOP_P,
            presence_penalty=settings.LLM_PRESENCE_PENALTY,
            frequency_penalty=settings.LLM_FREQUENCY_PENALTY,
            timeout=settings.LLM_TIMEOUT
        )
    
    def _get_manager(self, provider: Optional[LLMProvider] = None) -> LLMManager:
        """获取LLM管理器"""
        provider = provider or LLMProvider(settings.DEFAULT_LLM_PROVIDER)
        
        if provider not in self._manager_cache:
            config = self._get_llm_config(provider)
            self._manager_cache[provider] = LLMManager(config)
        
        return self._manager_cache[provider]
    
    async def rewrite_chapter(
        self,
        original_chapter: Chapter,
        main_character: Character,
        world_settings: Dict[str, Any],
        provider: Optional[LLMProvider] = None
    ) -> str:
        """仿写单个章节"""
        manager = self._get_manager(provider)
        
        system_prompt = self._build_system_prompt(world_settings)
        rewrite_prompt = self._build_chapter_prompt(original_chapter, main_character)
        
        return await manager.generate_text(
            prompt=rewrite_prompt,
            system_prompt=system_prompt
        )
    
    async def generate_character_dialogue(
        self,
        character: Character,
        context: str,
        situation: str,
        provider: Optional[LLMProvider] = None
    ) -> str:
        """生成角色对话"""
        manager = self._get_manager(provider)
        
        prompt = self._build_dialogue_prompt(character, context, situation)
        
        return await manager.generate_text(prompt)
    
    async def generate_battle_scene(
        self,
        attacker: Character,
        defender: Character,
        environment: str,
        power_system: Dict[str, Any],
        provider: Optional[LLMProvider] = None
    ) -> str:
        """生成战斗场景"""
        manager = self._get_manager(provider)
        
        prompt = self._build_battle_prompt(attacker, defender, environment, power_system)
        
        return await manager.generate_text(prompt)
    
    async def expand_description(
        self,
        abstract_text: str,
        provider: Optional[LLMProvider] = None
    ) -> str:
        """扩写描述 - 将抽象描述具体化"""
        manager = self._get_manager(provider)
        
        prompt = f"""
请将以下抽象描述具体化，使用具体的动作、场景、细节描写代替直白的形容词堆砌。
要求：
1. 使用感官描写（视觉、听觉、触觉等）
2. 包含具体的动作描写
3. 避免使用过多抽象形容词
4. 保持原文的情感和意境

原描述：
{abstract_text}

请直接输出扩写后的内容：
"""
        
        return await manager.generate_text(prompt)
    
    def _build_system_prompt(self, world_settings: Dict[str, Any]) -> str:
        """构建系统提示词"""
        return f"""你是一位专业的网络小说作家，擅长创作引人入胜的小说内容。

写作要求：
1. 使用动作、场景、细节描写代替直白的形容词堆砌
2. 描写要生动具体，有画面感
3. 保持语言自然流畅，避免AI写作痕迹
4. 保持人物性格一致性
5. 打斗场景要详细具体化

世界观背景：
{world_settings}
"""
    
    def _build_chapter_prompt(self, chapter: Chapter, main_character: Character) -> str:
        """构建章节仿写提示词"""
        return f"""请基于以下信息仿写新的章节内容，要求：
1. 保持原章节的结构和节奏
2. 替换人物名称和地点名称
3. 重新安排情节发展
4. 保持相似的风格
5. 确保内容原创，不要直接复制原文

原章节信息：
标题：{chapter.title}
字数：{chapter.word_count}
类型：{chapter.structure_type}

主要角色信息：
姓名：{main_character.name}
性格：{', '.join(main_character.personality_traits)}

原章节内容：
{chapter.content}

请直接输出仿写后的新章节：
"""
    
    def _build_dialogue_prompt(self, character: Character, context: str, situation: str) -> str:
        """构建对话生成提示词"""
        return f"""请根据以下信息生成符合角色性格的对话：

角色信息：
姓名：{character.name}
性格特点：{', '.join(character.personality_traits)}
说话风格：{character.speech_style}

背景语境：
{context}

当前情景：
{situation}

请直接输出{character.name}应该说的话：
"""
    
    def _build_battle_prompt(
        self,
        attacker: Character,
        defender: Character,
        environment: str,
        power_system: Dict[str, Any]
    ) -> str:
        """构建战斗场景提示词"""
        return f"""请根据以下信息生成详细的战斗场景描写：

战斗双方：
攻击者：{attacker.name}
  - 性格：{', '.join(attacker.personality_traits)}
  - 能力：{', '.join(attacker.abilities)}

防守者：{defender.name}
  - 性格：{', '.join(defender.personality_traits)}
  - 能力：{', '.join(defender.abilities)}

战斗环境：
{environment}

力量系统背景：
{power_system}

请详细描写战斗过程，包括：
1. 具体的招式和动作
2. 环境的变化
3. 人物的心理活动
4. 灵力/能量的流动描写
5. 战斗的节奏变化

请直接输出战斗场景：
"""
    
    def get_available_providers(self) -> list:
        """获取可用的LLM提供商"""
        return LLMFactory.get_available_providers()
    
    def get_provider_models(self, provider: LLMProvider) -> list:
        """获取指定提供商的模型列表"""
        return LLMFactory.get_default_models(provider)
    
    async def rewrite_chapter_with_context(
        self,
        original_chapter: Chapter,
        main_character: Character,
        world_settings: Dict[str, Any],
        context: ChapterContext,
        provider: Optional[LLMProvider] = None
    ) -> str:
        """
        带上下文信息仿写单个章节
        
        规则：仿写第N章前，必须阅读原小说和仿写小说的N-5到N-1章
        
        Args:
            original_chapter: 要仿写的原文章节
            main_character: 主要角色
            world_settings: 世界观设定
            context: 上下文信息（包含前N章的原文和仿写内容）
            provider: LLM提供商
        
        Returns:
            str: 仿写后的章节内容
        """
        manager = self._get_manager(provider)
        
        system_prompt = self._build_system_prompt(world_settings)
        rewrite_prompt = self._build_context_chapter_prompt(
            original_chapter, 
            main_character, 
            context
        )
        
        return await manager.generate_text(
            prompt=rewrite_prompt,
            system_prompt=system_prompt
        )
    
    def _build_context_chapter_prompt(
        self, 
        chapter: Chapter, 
        main_character: Character,
        context: ChapterContext
    ) -> str:
        """
        构建带上下文的章节仿写提示词
        
        严格遵循阅读上下文规则：
        - 必须包含前N章的原文内容
        - 必须包含前N章的仿写内容
        - 确保内容的连贯性
        
        Args:
            chapter: 要仿写的原文章节
            main_character: 主要角色
            context: 上下文信息
        
        Returns:
            str: 完整的提示词
        """
        # 构建上下文摘要
        context_summary = self._build_context_summary(context)
        
        return f"""请基于以下信息仿写新的章节内容，要求：

【重要规则】
1. 仿写第{context.chapter_number}章前，必须先阅读下面的前几章上下文
2. 保持剧情的连贯性和一致性
3. 替换人物名称和地点名称
4. 重新安排情节发展
5. 保持相似的风格
6. 确保内容原创，不要直接复制原文

【阅读上下文（必读）】
{context_summary}

【当前要仿写的章节信息】
标题：{chapter.title}
字数：{chapter.word_count}
类型：{chapter.structure_type}

【主要角色信息】
姓名：{main_character.name}
性格：{', '.join(main_character.personality_traits)}

【原章节内容】
{chapter.content}

请直接输出仿写后的新章节："""
    
    def _build_context_summary(self, context: ChapterContext) -> str:
        """
        构建上下文摘要
        
        Args:
            context: 上下文信息
        
        Returns:
            str: 格式化的上下文摘要
        """
        summary = []
        
        # 添加原文上下文
        if context.original_chapters:
            summary.append("=== 原文前几章内容 ===")
            for i, (title, content) in enumerate(zip(context.original_chapter_titles, context.original_chapters)):
                chapter_num = context.chapter_number - len(context.original_chapters) + i
                summary.append(f"--- 原文第{chapter_num}章：{title} ---")
                # 截取前1000字符，避免过长
                preview = content[:1000] + "..." if len(content) > 1000 else content
                summary.append(preview)
                summary.append("")
        
        # 添加已仿写内容上下文
        if context.rewritten_chapters:
            summary.append("=== 已仿写的前几章内容 ===")
            for i, (title, content) in enumerate(zip(context.rewritten_chapter_titles, context.rewritten_chapters)):
                chapter_num = context.chapter_number - len(context.rewritten_chapters) + i
                summary.append(f"--- 仿写第{chapter_num}章：{title} ---")
                preview = content[:1000] + "..." if len(content) > 1000 else content
                summary.append(preview)
                summary.append("")
        
        if not summary:
            summary.append("（无前置章节）")
        
        return '\n'.join(summary)


# 全局LLM服务实例
llm_service = LLMRewriteService()
