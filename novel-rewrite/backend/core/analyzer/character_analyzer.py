# 人物性格和成长线分析模块
# 用于分析小说中的人物性格、关系网络、成长弧线等

from typing import List, Dict, Optional, Set, Tuple
import re
from collections import defaultdict
from backend.models.novel import (
    NovelDocument, Chapter, Character, RelationshipType, Sentence
)

class CharacterAnalyzer:
    """人物分析器"""
    
    def __init__(self):
        # 人物称谓模式
        self.name_patterns = [
            r'([A-Z\u4e00-\u9fa5]{2,4})(?:说|道|问|答|叫|喊|骂|笑|怒|惊)',
            r'([A-Z\u4e00-\u9fa5]{2,4})(?:的|对|与|和|向)(?:她|他|它|我)',
            r'([A-Z\u4e00-\u9fa5]{2,4})(?:是|为|被|把|将)',
            r'对([A-Z\u4e00-\u9fa5]{2,4})说',
            r'和([A-Z\u4e00-\u9fa5]{2,4})一起',
        ]
        
        # 性格关键词
        self.personality_keywords = {
            '勇敢': ['勇敢', '无畏', '豪迈', '胆大', '不惧'],
            '懦弱': ['胆小', '怯懦', '害怕', '畏缩'],
            '聪明': ['聪明', '机智', '智慧', '狡黠', '精明'],
            '愚笨': ['愚笨', '蠢笨', '笨拙', '傻'],
            '善良': ['善良', '仁慈', '好心', '心善'],
            '邪恶': ['邪恶', '狠毒', '残忍', '恶毒'],
            '忠诚': ['忠诚', '忠心', '忠义', '效忠'],
            '狡诈': ['狡诈', '阴险', '虚伪', '奸诈'],
            '坚强': ['坚强', '坚韧', '顽强', '不屈'],
            '软弱': ['软弱', '脆弱', '动摇'],
            '乐观': ['乐观', '开朗', '积极', '向上'],
            '悲观': ['悲观', '消极', '沮丧', '抑郁'],
        }
        
        # 关系关键词
        self.relationship_keywords = {
            RelationshipType.FAMILY: ['父亲', '母亲', '儿子', '女儿', '兄弟', '姐妹', ' family', 'parent'],
            RelationshipType.FRIEND: ['朋友', '好友', '闺蜜', '兄弟', '哥们', 'friend'],
            RelationshipType.MENTOR: ['师父', '师傅', '老师', ' mentor', 'teacher'],
            RelationshipType.RIVAL: ['对手', '竞争对手', 'rival', 'competitor'],
            RelationshipType.ENEMY: ['敌人', '仇人', '仇敌', '敌方', 'enemy'],
            RelationshipType.LOVER: ['爱人', '恋人', '情侣', '心上人', 'lover'],
            RelationshipType.MASTER_DISCIPLE: ['徒弟', '弟子', '传人', 'disciple'],
        }
        
        # 外貌描述关键词
        self.appearance_keywords = ['身穿', '身穿', '披着', '头戴', '脚踏', '面容', '容貌', '长相', '身材']
        
        # 成长阶段关键词
        self.growth_keywords = {
            'start': ['最初', '刚开始', '起初', '一开始'],
            'challenge': ['遇到', '面临', '陷入', '经历'],
            'breakthrough': ['突破', '成长', '提升', '蜕变', '觉醒'],
            'transformation': ['蜕变', '改变', '成长', '成熟']
        }
    
    def extract_characters(self, novel: NovelDocument) -> List[Character]:
        """
        提取所有人物
        """
        characters = []
        character_names = set()
        
        # 第一次扫描：收集所有可能的人名
        for chapter in novel.chapters:
            names = self._extract_names_from_chapter(chapter)
            character_names.update(names)
        
        # 过滤短名称和常见词
        filtered_names = self._filter_names(character_names)
        
        # 第二次扫描：为每个人物建立档案
        for name in filtered_names:
            character = self._build_character_profile(name, novel)
            if character:
                characters.append(character)
        
        # 按出场顺序排序
        characters.sort(key=lambda c: c.first_appearance_chapter)
        
        # 更新小说对象
        novel.characters = characters
        
        return characters
    
    def _extract_names_from_chapter(self, chapter: Chapter) -> Set[str]:
        """
        从章节中提取人名
        """
        names = set()
        text = chapter.content
        
        # 使用正则表达式提取
        for pattern in self.name_patterns:
            matches = re.findall(pattern, text)
            names.update(matches)
        
        # 提取引号中的人名
        quote_pattern = r'["""]([^"""]+)["""]'
        quotes = re.findall(quote_pattern, text)
        for quote in quotes:
            if len(quote) <= 4 and len(quote) >= 2:
                names.add(quote)
        
        return names
    
    def _filter_names(self, names: Set[str]) -> Set[str]:
        """
        过滤无效名称
        """
        filtered = set()
        
        # 常见排除词
        exclude_words = {
            '什么', '这个', '那个', '他们', '我们', '自己',
            '怎么', '为何', '为何', '如何', '哪里', '哪个',
            '小说', '故事', '人物', '情节', '这里', '那里'
        }
        
        for name in names:
            # 过滤太短或太长的
            if len(name) < 2 or len(name) > 4:
                continue
            
            # 过滤常见词
            if name in exclude_words:
                continue
            
            # 过滤纯数字
            if name.isdigit():
                continue
            
            filtered.add(name)
        
        return filtered
    
    def _build_character_profile(self, name: str, novel: NovelDocument) -> Optional[Character]:
        """
        构建人物档案
        """
        # 收集该人物的所有出现
        appearances = []
        first_chapter = 0
        
        for chapter in novel.chapters:
            if name in chapter.content:
                appearances.append(chapter)
                if first_chapter == 0:
                    first_chapter = chapter.number
        
        if not appearances:
            return None
        
        # 提取外貌描述
        appearance = self._extract_appearance(name, appearances)
        
        # 提取性格特点
        personality = self._extract_personality(name, appearances)
        
        # 提取背景故事
        background = self._extract_background(name, appearances)
        
        # 提取能力
        abilities = self._extract_abilities(name, appearances)
        
        # 提取说话风格
        speech_style = self._extract_speech_style(name, appearances)
        
        # 识别关系
        relationships = self._identify_relationships(name, novel)
        
        # 分析成长弧线
        growth_arc = self._analyze_growth_arc(name, appearances)
        
        # 人物弧光
        arc_description = self._generate_arc_description(name, growth_arc, personality)
        
        return Character(
            name=name,
            original_name=name,
            appearance=appearance,
            personality_traits=personality,
            background=background,
            abilities=abilities,
            speech_style=speech_style,
            first_appearance_chapter=first_chapter,
            relationships=relationships,
            growth_arc=growth_arc,
            arc_description=arc_description
        )
    
    def _extract_appearance(self, name: str, chapters: List[Chapter]) -> str:
        """
        提取外貌描述
        """
        descriptions = []
        
        for chapter in chapters[:5]:  # 只检查前5章
            text = chapter.content
            
            # 查找外貌描述
            for keyword in self.appearance_keywords:
                pattern = rf'{keyword}[^。！？（）]+'
                matches = re.findall(pattern, text)
                descriptions.extend(matches[:2])
        
        # 去重并限制长度
        unique_desc = list(dict.fromkeys(descriptions))[:3]
        return '。'.join(unique_desc) if unique_desc else f"{name}的外貌特征"
    
    def _extract_personality(self, name: str, chapters: List[Chapter]) -> List[str]:
        """
        提取性格特点
        """
        traits = []
        
        text = ' '.join([c.content for c in chapters[:10]])
        
        for trait, keywords in self.personality_keywords.items():
            if any(keyword in text for keyword in keywords):
                if trait not in traits:
                    traits.append(trait)
        
        return traits if traits else ['性格复杂']
    
    def _extract_background(self, name: str, chapters: List[Chapter]) -> str:
        """
        提取背景故事
        """
        backgrounds = []
        
        for chapter in chapters[:10]:
            text = chapter.content
            
            # 查找背景描述
            bg_patterns = [
                rf'{name}(?:是|原本|曾经|过去).{10,50}[。，]',
                rf'原来{name}.{10,50}[。，]',
            ]
            
            for pattern in bg_patterns:
                matches = re.findall(pattern, text)
                backgrounds.extend(matches[:2])
        
        if backgrounds:
            return backgrounds[0][:200]
        return f"{name}的背景故事"
    
    def _extract_abilities(self, name: str, chapters: List[Chapter]) -> List[str]:
        """
        提取能力
        """
        abilities = []
        
        text = ' '.join([c.content for c in chapters])
        
        # 武功/法术
        ability_keywords = ['功法', '招式', '法术', '神通', '秘术', '绝技', '能力']
        for keyword in ability_keywords:
            pattern = rf'{name}的([^{keyword}]+?){keyword}'
            matches = re.findall(pattern, text)
            abilities.extend(matches[:3])
        
        return abilities[:5] if abilities else ['普通能力']
    
    def _extract_speech_style(self, name: str, chapters: List[Chapter]) -> str:
        """
        提取说话风格
        """
        # 收集该人物的对话
        dialogues = []
        
        for chapter in chapters[:10]:
            text = chapter.content
            
            # 提取对话
            pattern = rf'{name}[说问道答叫喊骂笑道怒惊道：:"]+([^""]+)'
            matches = re.findall(pattern, text)
            dialogues.extend(matches[:10])
        
        if dialogues:
            # 分析对话特征
            has_question = any('？' in d or '?' in d for d in dialogues)
            has_exclamation = any('！' in d or '!' in d for d in dialogues)
            avg_length = sum(len(d) for d in dialogues) / len(dialogues)
            
            style_parts = []
            if has_question:
                style_parts.append("喜欢提问")
            if has_exclamation:
                style_parts.append("语气强烈")
            if avg_length > 20:
                style_parts.append("话语较长")
            else:
                style_parts.append("话语简洁")
            
            return '，'.join(style_parts)
        
        return "说话风格平淡"
    
    def _identify_relationships(self, name: str, novel: NovelDocument) -> Dict[str, RelationshipType]:
        """
        识别人物关系
        """
        relationships = {}
        text = novel.original_text
        
        for rel_type, keywords in self.relationship_keywords.items():
            for keyword in keywords:
                pattern = rf'{name}.{keyword}'
                if re.search(pattern, text):
                    # 提取关系对象
                    rel_pattern = rf'{name}[^，,。！]{0,10}{keyword}[^，,。！]{0,10}([A-Z\u4e00-\u9fa5]{{2,4}})'
                    matches = re.findall(rel_pattern, text)
                    
                    for match in matches[:3]:
                        if match != name:
                            relationships[match] = rel_type
        
        return relationships
    
    def _analyze_growth_arc(self, name: str, chapters: List[Chapter]) -> Dict[str, any]:
        """
        分析成长弧线
        """
        arc = {
            'start_state': '',
            'challenges': [],
            'breakthroughs': [],
            'final_state': ''
        }
        
        # 分析每个阶段
        for chapter in chapters:
            text = chapter.content
            
            # 查找阶段关键词
            for keyword in self.growth_keywords['start']:
                if keyword in text[:500]:  # 只检查章节开头
                    arc['start_state'] = f"{name}处于初始阶段"
            
            for keyword in self.growth_keywords['challenge']:
                if keyword in text:
                    arc['challenges'].append(f"第{chapter.number}章遇到挑战")
            
            for keyword in self.growth_keywords['breakthrough']:
                if keyword in text:
                    arc['breakthroughs'].append(f"第{chapter.number}章实现突破")
            
            # 最后阶段
            if chapter == chapters[-1]:
                arc['final_state'] = f"{name}达到新的境界"
        
        # 限制长度
        arc['challenges'] = arc['challenges'][:5]
        arc['breakthroughs'] = arc['breakthroughs'][:5]
        
        return arc
    
    def _generate_arc_description(self, name: str, growth_arc: Dict, personality: List[str]) -> str:
        """
        生成人物弧光描述
        """
        parts = []
        
        if personality:
            parts.append(f"{name}的性格以{personality[0]}为主")
        
        if growth_arc['challenges']:
            parts.append(f"经历了{len(growth_arc['challenges'])}次重大挑战")
        
        if growth_arc['breakthroughs']:
            parts.append(f"实现了{len(growth_arc['breakthroughs'])}次重要突破")
        
        return '，'.join(parts) if parts else f"{name}的成长历程"
    
    def build_relationship_graph(self, characters: List[Character]) -> Dict[str, List[Tuple[str, str]]]:
        """
        构建人物关系图谱
        Returns:
            {人物名: [(关系人物, 关系类型), ...]}
        """
        graph = defaultdict(list)
        
        for character in characters:
            for related_name, rel_type in character.relationships.items():
                graph[character.name].append((related_name, rel_type.value))
        
        return dict(graph)
    
    def identify_character_groups(self, characters: List[Character]) -> List[List[Character]]:
        """
        识别人物阵营/团队
        """
        groups = []
        
        # 基于关系分组
        for character in characters:
            added = False
            
            # 检查是否应该加入现有组
            for group in groups:
                # 检查是否与组内某人有关系
                for group_char in group:
                    if (character.name in group_char.relationships or 
                        group_char.name in character.relationships):
                        group.append(character)
                        added = True
                        break
                
                if added:
                    break
            
            # 如果没有加入任何组，创建新组
            if not added:
                groups.append([character])
        
        return groups
    
    def get_main_character(self, characters: List[Character]) -> Optional[Character]:
        """
        识别主角
        """
        if not characters:
            return None
        
        # 基于多个因素评分
        scores = {}
        
        for character in characters:
            score = 0
            
            # 出场早加分
            if character.first_appearance_chapter <= 3:
                score += 10
            elif character.first_appearance_chapter <= 10:
                score += 5
            
            # 描述多加分
            score += len(character.appearance) / 10
            score += len(character.background) / 20
            score += len(character.personality_traits) * 2
            
            # 关系多加分
            score += len(character.relationships) * 2
            
            # 成长弧线完整加分
            if character.growth_arc.get('breakthroughs'):
                score += len(character.growth_arc['breakthroughs']) * 3
            
            scores[character.name] = score
        
        # 返回最高分的人物
        if scores:
            max_name = max(scores.items(), key=lambda x: x[1])[0]
            return next((c for c in characters if c.name == max_name), None)
        
        return characters[0]
    
    def generate_character_summary(self, character: Character) -> str:
        """
        生成人物总结（用于仿写参考）
        """
        summary_parts = []
        
        summary_parts.append(f"【{character.name}】\n")
        
        if character.personality_traits:
            summary_parts.append(f"性格特点: {', '.join(character.personality_traits)}\n")
        
        if character.appearance:
            summary_parts.append(f"外貌: {character.appearance[:100]}...\n")
        
        if character.background:
            summary_parts.append(f"背景: {character.background[:150]}...\n")
        
        if character.abilities:
            summary_parts.append(f"能力: {', '.join(character.abilities[:5])}\n")
        
        if character.speech_style:
            summary_parts.append(f"说话风格: {character.speech_style}\n")
        
        if character.relationships:
            rel_str = ', '.join([f"{n}({r.value})" for n, r in list(character.relationships.items())[:5]])
            summary_parts.append(f"人际关系: {rel_str}\n")
        
        if character.arc_description:
            summary_parts.append(f"成长弧光: {character.arc_description}\n")
        
        return ''.join(summary_parts)
