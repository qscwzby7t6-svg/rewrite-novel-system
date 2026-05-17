# AI仿写核心引擎
# 实现小说内容的智能仿写，包括风格复刻、情节生成、描述具体化等

from typing import List, Dict, Optional, Tuple, Any
import re
import random
from backend.models.novel import (
    NovelDocument, Chapter, Character, WorldSetting, PowerSystem,
    MacroStructure, RewriteConfig, SceneType, RelationshipType,
    ChapterContext
)

class RewriteEngine:
    """仿写引擎核心类"""
    
    def __init__(self):
        # 抽象描述具体化映射
        self.concretization_map = {
            '紧张': [
                '双手紧紧攥着衣角，指节因为用力而微微泛白',
                '不自觉地舔了舔干涩的嘴唇，眼神飘忽不定',
                '心跳骤然加快，胸口像是被什么堵住了一样',
            ],
            '高兴': [
                '嘴角不自觉地上扬，眼角眉梢都带着笑意',
                '脚步轻快得像是踩在云端上',
                '忍不住笑出了声，连忙捂住嘴',
            ],
            '悲伤': [
                '眼眶泛红，却倔强地不让泪水落下',
                '声音哽咽，说不出完整的话来',
                '独自蜷缩在角落里，肩膀微微颤抖',
            ],
            '愤怒': [
                '胸膛剧烈起伏，拳头握得咯咯作响',
                '脸色铁青，一字一顿地说出冰冷的话语',
                '眼中几乎要喷出火来，牙关咬得死紧',
            ],
            '害怕': [
                '后背一阵发凉，浑身的汗毛都竖了起来',
                '不自觉地后退了几步，腿有些发软',
                '瞳孔骤缩，下意识地屏住了呼吸',
            ],
            '惊讶': [
                '眼睛瞪得溜圆，嘴巴张得能塞进一个鸡蛋',
                '整个人像是被定住了一样，愣在原地',
                '倒吸一口凉气，半晌说不出话来',
            ],
            '思考': [
                '眉头紧锁，手指无意识地敲击着桌面',
                '目光深邃，仿佛在脑海中推演着什么',
                '陷入沉思，周围的声响都被自动屏蔽',
            ],
            '得意': [
                '下巴微微扬起，嘴角挂着一丝不易察觉的微笑',
                '背着手踱步，哼着小曲儿',
                '故意清了清嗓子，等待别人的赞叹',
            ],
        }
        
        # 战斗动作库
        self.battle_actions = [
            '挥出', '劈下', '刺出', '横扫', '直击', '猛攻',
            '闪避', '后退', '侧身', '跃起', '俯冲',
            '凝聚', '爆发', '释放', '催动', '运转',
        ]
        
        # 战斗描述模板
        self.battle_templates = [
            '{actor}猛地{action}一掌，掌心灵力涌动，带着呼啸的风声直取{target}的{part}。',
            '{actor}身形一闪，{action}长剑，剑光如虹，直逼{target}面门。',
            '{actor}双手结印，{action}法力，在空中凝聚成一道璀璨的光柱，向着{target}轰去。',
            '{actor}不退反进，{action}拳头，拳风呼啸，每一拳都带着千钧之力。',
        ]
        
        # 场景描写关键词
        self.scene_keywords = {
            '森林': ['参天大树', '斑驳的光影', '鸟鸣声', '清新的空气', '幽静的小径'],
            '山脉': ['巍峨山峰', '云雾缭绕', '陡峭的山路', '呼啸的山风', '远处的群峰'],
            '城市': ['熙熙攘攘的人群', '高耸的建筑', '热闹的街道', '此起彼伏的叫卖声', '灯红酒绿'],
            '宗门': ['庄严的山门', '古朴的建筑', '修炼的弟子', '浓郁的灵气', '威严的殿堂'],
            '战场': ['弥漫的硝烟', '遍地的残骸', '震天的喊杀声', '飞舞的刀光剑影', '鲜血染红的土地'],
        }
        
        # 脏话词库（可配置开关）
        self.profanity_words = ['他妈的', '混蛋', '王八蛋', '狗东西', '杂种']
    
    def rewrite_novel(
        self,
        original: NovelDocument,
        config: RewriteConfig
    ) -> NovelDocument:
        """
        重写整本小说
        Args:
            original: 原始小说文档
            config: 仿写配置
        Returns:
            仿写后的新小说
        """
        # 复制原始文档结构
        rewritten = original.model_copy(deep=True)
        
        # 替换人物名称
        character_mapping = self._generate_character_mapping(
            original.characters,
            config.main_character_name
        )
        
        # 重写每个章节
        new_chapters = []
        
        # 前几章直接保留？或者从第6章开始？
        # 根据新规则：仿写小说从第6章开始，仿写要求必须阅读原小说前5章和仿写的前5章
        # 前N-1章可以简单仿写，从第N章开始应用完整的上下文规则
        start_chapter = config.start_chapter if config.enable_context_rule else 1
        context_window_size = config.context_window_size if config.enable_context_rule else 0
        
        for idx, chapter in enumerate(original.chapters):
            chapter_num = idx + 1
            
            if config.enable_context_rule and chapter_num >= start_chapter:
                # 应用上下文规则：获取前N章的原文和仿写内容
                context = self._build_chapter_context(
                    original,
                    new_chapters,
                    chapter_num,
                    context_window_size
                )
                
                new_chapter = self.rewrite_chapter_with_context(
                    chapter, 
                    original, 
                    config, 
                    character_mapping,
                    context
                )
            else:
                # 前几章或者不启用规则时，使用普通仿写
                new_chapter = self.rewrite_chapter(chapter, original, config, character_mapping)
            
            new_chapters.append(new_chapter)
        
        rewritten.chapters = new_chapters
        
        return rewritten
    
    def _build_chapter_context(
        self,
        original: NovelDocument,
        rewritten_chapters: List[Chapter],
        current_chapter_num: int,
        window_size: int
    ) -> ChapterContext:
        """
        构建章节上下文信息
        规则：仿写第N章时，必须阅读原小说和仿写小说的N-5到N-1章
        
        Args:
            original: 原文小说
            rewritten_chapters: 已仿写的章节
            current_chapter_num: 当前要仿写的章节号（从1开始）
            window_size: 上下文窗口大小
        
        Returns:
            ChapterContext: 上下文信息
        """
        # 计算起始章节（从1开始）
        # 例如仿写第10章，看第5-9章；仿写第6章，看第1-5章
        start_chapter = max(1, current_chapter_num - window_size)
        end_chapter = current_chapter_num - 1
        
        # 收集原文章节
        original_context = []
        original_titles = []
        for i in range(start_chapter, end_chapter + 1):
            if i - 1 < len(original.chapters):
                chapter = original.chapters[i - 1]
                original_context.append(chapter.content)
                original_titles.append(chapter.title)
        
        # 收集已仿写章节
        rewritten_context = []
        rewritten_titles = []
        for i in range(start_chapter, end_chapter + 1):
            if i - 1 < len(rewritten_chapters):
                chapter = rewritten_chapters[i - 1]
                rewritten_context.append(chapter.content)
                rewritten_titles.append(chapter.title)
        
        return ChapterContext(
            chapter_number=current_chapter_num,
            original_chapters=original_context,
            rewritten_chapters=rewritten_context,
            original_chapter_titles=original_titles,
            rewritten_chapter_titles=rewritten_titles
        )
    
    def rewrite_chapter_with_context(
        self,
        chapter: Chapter,
        novel: NovelDocument,
        config: RewriteConfig,
        character_mapping: Dict[str, str],
        context: ChapterContext
    ) -> Chapter:
        """
        带上下文信息的章节仿写
        在仿写时参考前面的章节，保持连贯性
        
        Args:
            chapter: 当前要仿写的原文章节
            novel: 原文小说
            config: 仿写配置
            character_mapping: 人物名称映射
            context: 上下文信息
        
        Returns:
            Chapter: 仿写后的章节
        """
        new_chapter = chapter.model_copy(deep=True)
        
        # 替换内容中的名称
        new_content = chapter.content
        for old_name, new_name in character_mapping.items():
            new_content = new_content.replace(old_name, new_name)
        
        # 替换地点名称
        new_content = self._replace_location_names(new_content, novel.world_settings)
        
        # 具体化抽象描述
        new_content = self._concretize_descriptions(new_content, config.enable_profanity)
        
        # 处理打斗场景
        new_content = self._enhance_battle_scenes(new_content)
        
        # 添加场景细节
        new_content = self._add_scene_details(new_content, novel.world_settings)
        
        # 调整字数
        new_content = self._adjust_word_count(
            new_content,
            chapter.word_count,
            config.chapter_word_count_range
        )
        
        # 添加自然的不规则性
        new_content = self._add_natural_variation(new_content)
        
        # 应用上下文调整：根据前面的章节内容进行调整
        new_content = self._apply_context_adjustment(new_content, context, character_mapping)
        
        new_chapter.content = new_content
        new_chapter.characters = [character_mapping.get(c, c) for c in chapter.characters]
        
        return new_chapter
    
    def _apply_context_adjustment(
        self,
        content: str,
        context: ChapterContext,
        character_mapping: Dict[str, str]
    ) -> str:
        """
        应用上下文调整，确保情节连贯性
        
        Args:
            content: 原始仿写内容
            context: 上下文信息
            character_mapping: 人物映射
        
        Returns:
            str: 调整后的内容
        """
        # 这里可以添加智能逻辑，根据上下文调整内容
        # 1. 检查并保持人物性格的一致性
        # 2. 保持情节的连贯性
        # 3. 避免前后矛盾
        
        paragraphs = content.split('\n')
        adjusted = []
        
        for para in paragraphs:
            # 可以在这里添加上下文感知的调整逻辑
            adjusted.append(para)
        
        return '\n'.join(adjusted)
    
    def rewrite_chapter(
        self,
        chapter: Chapter,
        novel: NovelDocument,
        config: RewriteConfig,
        character_mapping: Dict[str, str]
    ) -> Chapter:
        """
        重写单个章节
        """
        new_chapter = chapter.model_copy(deep=True)
        
        # 替换内容中的名称
        new_content = chapter.content
        for old_name, new_name in character_mapping.items():
            new_content = new_content.replace(old_name, new_name)
        
        # 替换地点名称
        new_content = self._replace_location_names(new_content, novel.world_settings)
        
        # 具体化抽象描述
        new_content = self._concretize_descriptions(new_content, config.enable_profanity)
        
        # 处理打斗场景
        new_content = self._enhance_battle_scenes(new_content)
        
        # 添加场景细节
        new_content = self._add_scene_details(new_content, novel.world_settings)
        
        # 调整字数
        new_content = self._adjust_word_count(
            new_content,
            chapter.word_count,
            config.chapter_word_count_range
        )
        
        # 添加自然的不规则性
        new_content = self._add_natural_variation(new_content)
        
        new_chapter.content = new_content
        new_chapter.characters = [character_mapping.get(c, c) for c in chapter.characters]
        
        return new_chapter
    
    def _generate_character_mapping(
        self,
        characters: List[Character],
        main_character_name: str
    ) -> Dict[str, str]:
        """
        生成角色名称映射
        """
        mapping = {}
        
        # 预设的名字库
        name_pool = {
            'male': ['林风', '叶尘', '萧炎', '秦羽', '陈轩', '李云', '张浩', '王晨', '赵天', '周明'],
            'female': ['苏晴', '林婉儿', '萧玉', '秦雪', '陈婷', '李诗', '张悦', '王琳', '赵月', '周琴'],
        }
        
        used_names = set()
        used_names.add(main_character_name)
        
        # 找到主角
        main_char = None
        other_chars = []
        
        for char in characters:
            if char.first_appearance_chapter <= 3:
                main_char = char
            else:
                other_chars.append(char)
        
        # 分配主角名称
        if main_char:
            mapping[main_char.name] = main_character_name
        
        # 分配其他角色名称
        name_index = {'male': 0, 'female': 0}
        
        for char in other_chars:
            gender = getattr(char, 'gender', 'male') or 'male'
            
            # 生成新名称
            base_names = name_pool.get(gender, name_pool['male'])
            new_name = base_names[name_index[gender] % len(base_names)]
            
            # 确保不重复
            while new_name in used_names:
                name_index[gender] += 1
                new_name = base_names[name_index[gender] % len(base_names)]
            
            mapping[char.name] = new_name
            used_names.add(new_name)
            name_index[gender] += 1
        
        return mapping
    
    def _replace_location_names(
        self,
        content: str,
        world_settings: WorldSetting
    ) -> str:
        """
        替换地点名称
        """
        # 预设地点名称
        location_pool = {
            'region': ['青云域', '玄天界', '苍茫大陆', '九幽冥域', '天元圣地'],
            'city': ['天云城', '青云城', '玄风城', '赤阳城', '凌霄城'],
            'sect': ['青云宗', '天玄门', '紫霄派', '太虚观', '万剑宗'],
            'mountain': ['青云山', '天绝峰', '玄阴山', '赤阳峰', '凌霄峰'],
        }
        
        # 替换势力名称
        for faction in world_settings.factions[:5]:
            new_name = random.choice(location_pool['sect'])
            content = content.replace(faction.name, new_name)
        
        return content
    
    def _concretize_descriptions(self, content: str, enable_profanity: bool = False) -> str:
        """
        将抽象描述具体化
        将"小红很紧张"转换为具体动作描写
        """
        new_content = content
        
        # 替换抽象情感描述
        for emotion, descriptions in self.concretization_map.items():
            # 情感+状态模式
            patterns = [
                rf'([\u4e00-\u9fa5]{{2,4}})很{emotion}',
                rf'([\u4e00-\u9fa5]{{2,4}})非常{emotion}',
                rf'([\u4e00-\u9fa5]{{2,4}})极其{emotion}',
                rf'([\u4e00-\u9fa5]{{2,4}})十分{emotion}',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, new_content)
                for match in matches:
                    character = match.group(1)
                    # 随机选择一个具体描写
                    description = random.choice(descriptions)
                    # 替换
                    replacement = f'{character}{description}'
                    new_content = new_content[:match.start()] + replacement + new_content[match.end():]
        
        # 添加适量的脏话（在合适的场景）
        if enable_profanity:
            profanity_patterns = [
                (r'([\u4e00-\u9fa5]{2,4})发现自己被骗了', 
                 r'\1脸色铁青，低声骂道："他妈的！"'),
                (r'([\u4e00-\u9fa5]{2,4})愤怒地', r'\1恨恨地'),
            ]
            
            for pattern, replacement in profanity_patterns:
                if random.random() > 0.7:  # 30%概率添加
                    new_content = re.sub(pattern, replacement, new_content)
        
        return new_content
    
    def _enhance_battle_scenes(self, content: str) -> str:
        """
        增强打斗场景描写
        """
        # 检查是否包含战斗关键词
        battle_keywords = ['战斗', '对决', '厮杀', '出手', '攻击']
        
        has_battle = any(keyword in content for keyword in battle_keywords)
        
        if not has_battle:
            return content
        
        # 分割段落
        paragraphs = content.split('\n')
        enhanced_paragraphs = []
        
        for para in paragraphs:
            if any(keyword in para for keyword in battle_keywords):
                # 增强这个段落
                enhanced = self._generate_battle_description(para)
                enhanced_paragraphs.append(enhanced)
            else:
                enhanced_paragraphs.append(para)
        
        return '\n'.join(enhanced_paragraphs)
    
    def _generate_battle_description(self, context: str) -> str:
        """
        生成战斗描述
        """
        # 提取参与者
        actors = re.findall(r'([\u4e00-\u9fa5]{2,4})', context[:20])
        actor = actors[0] if actors else '他'
        
        # 提取目标
        targets = re.findall(r'([\u4e00-\u9fa5]{2,4})(?:被|向|对)', context[20:50])
        target = targets[0] if targets else '敌人'
        
        # 选择动作
        action = random.choice(self.battle_actions)
        
        # 生成描述
        template = random.choice(self.battle_templates)
        description = template.format(
            actor=actor,
            action=action,
            target=target,
            part='胸口' if random.random() > 0.5 else '要害'
        )
        
        # 将描述插入到原文中
        return context + '\n' + description
    
    def _add_scene_details(self, content: str, world_settings: WorldSetting) -> str:
        """
        添加场景细节描写
        """
        paragraphs = content.split('\n')
        enhanced = []
        
        for i, para in enumerate(paragraphs):
            enhanced.append(para)
            
            # 每隔几段添加场景描写
            if i > 0 and i % 3 == 0 and len(para) > 20:
                # 根据上下文选择场景类型
                scene_type = self._infer_scene_type(para)
                scene_desc = self._generate_scene_description(scene_type, world_settings)
                
                if scene_desc:
                    enhanced.append(scene_desc)
        
        return '\n'.join(enhanced)
    
    def _infer_scene_type(self, text: str) -> str:
        """
        推断场景类型
        """
        scene_keywords = {
            '森林': ['树', '林', '鸟', '野兽'],
            '山脉': ['山', '峰', '云', '崖'],
            '城市': ['街', '城', '人', '商'],
            '宗门': ['宗', '门', '殿', '修炼'],
            '战场': ['杀', '血', '战', '刀剑'],
        }
        
        max_count = 0
        scene_type = '一般'
        
        for scene, keywords in scene_keywords.items():
            count = sum(1 for kw in keywords if kw in text)
            if count > max_count:
                max_count = count
                scene_type = scene
        
        return scene_type
    
    def _generate_scene_description(
        self,
        scene_type: str,
        world_settings: WorldSetting
    ) -> str:
        """
        生成场景描述
        """
        keywords = self.scene_keywords.get(scene_type, self.scene_keywords['城市'])
        
        # 随机选择2-3个关键词组合
        selected = random.sample(keywords, min(3, len(keywords)))
        
        return f"只见周围{'，'.join(selected)}。"
    
    def _adjust_word_count(
        self,
        content: str,
        target_count: int,
        word_range: Tuple[int, int]
    ) -> str:
        """
        调整字数在目标范围内（±10%）
        """
        current_count = len(content.replace('\n', '').replace(' ', ''))
        
        min_count = int(target_count * 0.9)
        max_count = int(target_count * 1.1)
        
        # 确保在范围内
        if max_count < word_range[0]:
            max_count = word_range[1]
        if min_count > word_range[1]:
            min_count = word_range[0]
        
        if min_count <= current_count <= max_count:
            return content
        
        # 需要扩展
        if current_count < min_count:
            deficit = min_count - current_count
            additions = self._generate_additions(deficit)
            return content + '\n\n' + additions
        
        # 需要缩减
        if current_count > max_count:
            excess = current_count - max_count
            return self._trim_content(content, excess)
        
        return content
    
    def _generate_additions(self, target_length: int) -> str:
        """
        生成填充内容以达到目标字数
        """
        templates = [
            '{}站在那里，目光深邃，似乎在思考着什么重要的事情。',
            '微风拂过，{}的发丝轻轻飘动，脸上带着若有所思的表情。',
            '{}深吸一口气，感受着周围灵气的流动，心中渐渐明悟。',
            '周围的景色如诗如画，{}不禁沉浸在这片刻的宁静之中。',
        ]
        
        addition = ""
        while len(addition) < target_length:
            template = random.choice(templates)
            addition += template.format("他")
        
        return addition[:target_length]
    
    def _trim_content(self, content: str, excess: int) -> str:
        """
        缩减内容
        """
        # 移除多余的段落
        paragraphs = content.split('\n\n')
        
        if len(paragraphs) <= 2:
            return content
        
        # 移除最不重要的段落（中间的过渡段）
        if len(paragraphs) > 4:
            mid = len(paragraphs) // 2
            removed = paragraphs.pop(mid)
            excess -= len(removed)
        
        content = '\n\n'.join(paragraphs)
        
        # 如果还太长，继续缩减
        if excess > 0 and len(content) > excess:
            # 简单截断
            content = content[:-excess]
        
        return content
    
    def _add_natural_variation(self, content: str) -> str:
        """
        添加自然的语言变化，消除AI写作痕迹
        """
        # 1. 随机添加一些口语化表达
        colloquial_expressions = ['说实话', '不由得', '其实吧', '总的来说']
        
        paragraphs = content.split('\n')
        for i in range(len(paragraphs)):
            if random.random() > 0.8 and len(paragraphs[i]) > 30:
                insert_pos = random.randint(10, len(paragraphs[i]) // 2)
                expr = random.choice(colloquial_expressions)
                paragraphs[i] = paragraphs[i][:insert_pos] + expr + paragraphs[i][insert_pos:]
        
        content = '\n'.join(paragraphs)
        
        # 2. 随机调整句式长度
        sentences = content.split('。')
        varied_sentences = []
        
        for sent in sentences:
            if sent.strip():
                # 随机决定是否添加修饰
                if random.random() > 0.7 and len(sent) > 10:
                    modifiers = ['忍不住', '下意识地', '不由自主地', '轻轻地']
                    sent = random.choice(modifiers) + sent
                
                varied_sentences.append(sent + '。')
        
        return ''.join(varied_sentences)
    
    def generate_character_dialogue(
        self,
        character: Character,
        situation: str,
        word_limit: int = 100
    ) -> str:
        """
        生成角色对话
        """
        # 基于性格生成对话
        personality = character.personality_traits[0] if character.personality_traits else 'normal'
        
        # 对话模板
        dialogue_templates = {
            '勇敢': [
                '"有什么可怕的，尽管放马过来！"',
                '"我倒要看看你有多少本事！"',
            ],
            '聪明': [
                '"事情没那么简单，让我仔细想想..."',
                '"这其中必有蹊跷。"',
            ],
            '善良': [
                '"大家都是朋友，何必伤了和气呢？"',
                '"冤家宜解不宜结，我们好好谈谈。"',
            ],
            '邪恶': [
                '"哼哼，这下你可逃不掉了。"',
                '"就凭你？也配和我斗？"',
            ],
            'normal': [
                '"嗯，我知道了。"',
                '"这件事...让我想想。"',
            ],
        }
        
        templates = dialogue_templates.get(personality, dialogue_templates['normal'])
        
        # 生成对话
        dialogue = random.choice(templates)
        
        # 如果需要更长的对话
        if word_limit > 50:
            extra_lines = [
                '"而且，我觉得..."',
                '"不过话说回来..."',
                '"总之，情况就是这样。"',
            ]
            dialogue += random.choice(extra_lines)
        
        return dialogue
    
    def generate_battle_scene(
        self,
        attacker: Character,
        defender: Character,
        power_system: PowerSystem,
        word_count: int = 500
    ) -> str:
        """
        生成完整的战斗场景
        """
        battle_scene = []
        
        # 1. 开场
        battle_scene.append(f"{attacker.name}与{defender.name}相对而立，气氛骤然紧张起来。")
        battle_scene.append("")
        
        # 2. 准备阶段
        level = random.choice(power_system.levels) if power_system.levels else "修士"
        battle_scene.append(f"{attacker.name}运转{level}功法，周身灵力涌动，衣袍猎猎作响。")
        battle_scene.append("")
        
        # 3. 攻击描写
        num_attacks = random.randint(3, 5)
        for i in range(num_attacks):
            action = random.choice(self.battle_actions)
            weapon = random.choice(['长剑', '掌风', '剑气', '拳劲', '法术'])
            target_part = random.choice(['胸口', '面门', '要害', '丹田'])
            
            attack_desc = f"{attacker.name}猛然{action}{weapon}，直奔{defender.name}的{target_part}而去。"
            battle_scene.append(attack_desc)
            
            # 防御反应
            if random.random() > 0.5:
                defense = f"{defender.name}侧身闪避，同时反手一击。\n"
                battle_scene.append(defense)
            
            battle_scene.append("")
        
        # 4. 高潮
        climax = f"双方实力尽出，{attacker.name}使出绝招，"
        
        if power_system.cultivation_methods:
            method = random.choice(power_system.cultivation_methods)
            climax += f"{method}化作一道璀璨光芒，"
        
        climax += f"直取{defender.name}。"
        battle_scene.append(climax)
        battle_scene.append("")
        
        # 5. 结果
        if random.random() > 0.5:
            battle_scene.append(f"最终，{attacker.name}技高一筹，{defender.name}败下阵来。")
        else:
            battle_scene.append(f"一番激战，双方势均力敌，只得暂时罢手。")
        
        return ''.join(battle_scene)
    
    def insert_climax(
        self,
        chapter: Chapter,
        chapter_index: int,
        climax_interval: int = 10
    ) -> Chapter:
        """
        在指定章节插入高潮情节
        每10章一个小高潮
        """
        if (chapter_index + 1) % climax_interval == 0:
            # 这是一个高潮章节，增强内容
            climax_intensity = min(0.3 + (chapter_index // climax_interval) * 0.1, 0.8)
            
            # 添加高潮描写
            climax_text = self._generate_climax_content(climax_intensity)
            
            # 在章节中间插入
            paragraphs = chapter.content.split('\n')
            if len(paragraphs) > 3:
                insert_pos = len(paragraphs) // 2
                paragraphs.insert(insert_pos, climax_text)
                chapter.content = '\n'.join(paragraphs)
            
            chapter.climax_intensity = climax_intensity
        
        return chapter
    
    def _generate_climax_content(self, intensity: float) -> str:
        """
        生成高潮内容
        """
        climax_parts = []
        
        if intensity > 0.5:
            climax_parts.append("就在这千钧一发之际，")
            climax_parts.append("突然，天地变色，风云涌动！")
            climax_parts.append("一道璀璨的光芒从天而降，直冲而下！")
            climax_parts.append("所有人的目光都被这惊天动地的异象所吸引。")
        else:
            climax_parts.append("战斗进入了白热化阶段。")
            climax_parts.append("双方你来我往，互不相让。")
        
        return '\n'.join(climax_parts)
