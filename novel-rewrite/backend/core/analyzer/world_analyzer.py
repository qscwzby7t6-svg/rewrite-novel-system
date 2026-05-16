# 世界观和力量系统分析模块
# 用于分析小说的世界观设定、力量系统、地理环境、势力关系等

from typing import List, Dict, Optional, Set, Tuple
import re
from backend.models.novel import (
    NovelDocument, Character, WorldSetting, PowerSystem, Faction,
    RelationshipType
)

class WorldAnalyzer:
    """世界观分析器"""
    
    def __init__(self):
        # 力量等级关键词
        self.power_level_keywords = {
            'mortal': ['凡人', '普通人', '常人', '百姓'],
            'cultivator': ['修士', '修炼', '筑基', '金丹', '元婴', '修炼者'],
            'great_eminence': ['大能', '强者', '高手', '尊者', '宗主'],
            'immortal': ['仙人', '真仙', '金仙', '大罗金仙'],
            'divine': ['神', '神明', '神级', '天神', '帝君']
        }
        
        # 修炼体系关键词
        self.cultivation_keywords = [
            '修炼', '功法', '心法', '秘籍', '传承',
            '灵气', '灵力', '真元', '法力', '元气'
        ]
        
        # 地理环境关键词
        self.geography_keywords = [
            '山脉', '河流', '森林', '沙漠', '海洋', '平原',
            '城池', '宗门', '门派', '遗迹', '秘境', '洞府'
        ]
        
        # 势力类型
        self.faction_types = {
            'sect': ['宗门', '门派', '教派', '门派'],
            'country': ['王朝', '帝国', '国家', '皇朝'],
            'family': ['家族', '世家', '氏族'],
            'organization': ['组织', '势力', '帮派', '商会']
        }
    
    def analyze_world_settings(self, novel: NovelDocument) -> WorldSetting:
        """
        分析世界观设定
        """
        text = novel.original_text
        
        # 提取地理环境
        geography = self._extract_geography(text)
        
        # 提取社会结构
        social_structure = self._extract_social_structure(text)
        
        # 提取文化背景
        culture = self._extract_culture(text)
        
        # 提取历史背景
        history = self._extract_history(text)
        
        # 提取世界规则
        rules = self._extract_world_rules(text)
        
        # 识别势力
        factions = self._identify_factions(text, novel.characters)
        
        return WorldSetting(
            geography=geography,
            social_structure=social_structure,
            culture=culture,
            history=history,
            rules=rules,
            factions=factions
        )
    
    def _extract_geography(self, text: str) -> Dict[str, str]:
        """
        提取地理环境
        """
        geography = {}
        
        # 提取地点
        locations = []
        for keyword in self.geography_keywords:
            pattern = rf'{keyword}[的]*(.{2,10}?[地境域界])'
            matches = re.findall(pattern, text)
            locations.extend(matches)
        
        # 去重并限制数量
        unique_locations = list(set(locations))[:20]
        
        for loc in unique_locations:
            geography[loc] = f"{loc}是一个重要的地理区域"
        
        return geography
    
    def _extract_social_structure(self, text: str) -> Dict[str, str]:
        """
        提取社会结构
        """
        social = {}
        
        # 等级制度
        if any(kw in text for kw in ['上下', '等级', '阶层', '尊卑']):
            social['等级制度'] = "存在严格的等级划分制度"
        
        # 宗门社会
        if any(kw in text for kw in ['宗门', '门派', '修仙界']):
            social['宗门体系'] = "以宗门为核心的修仙社会结构"
        
        # 世俗社会
        if any(kw in text for kw in ['王朝', '帝国', '皇朝']):
            social['王朝体系'] = "世俗王朝与修仙宗门并存"
        
        return social
    
    def _extract_culture(self, text: str) -> Dict[str, str]:
        """
        提取文化背景
        """
        culture = {}
        
        # 修仙文化
        if any(kw in text for kw in ['修炼', '功法', '境界']):
            culture['修炼文化'] = "以修炼为核心的修仙文化"
        
        # 武侠文化
        if any(kw in text for kw in ['武功', '秘籍', '武林']):
            culture['武侠文化'] = "以武功为核心的武侠文化"
        
        return culture
    
    def _extract_history(self, text: str) -> List[str]:
        """
        提取历史背景
        """
        history = []
        
        # 查找历史叙述
        history_keywords = ['曾经', '上古', '远古', '万年前', '千年前', '多年前']
        
        for keyword in history_keywords:
            pattern = rf'{keyword}[，,](.{{10,50}})'
            matches = re.findall(pattern, text)
            history.extend(matches[:5])
        
        return list(set(history))[:10]
    
    def _extract_world_rules(self, text: str) -> List[str]:
        """
        提取世界规则
        """
        rules = []
        
        # 自然规则
        nature_rules = ['天道', '因果', '轮回', '命运']
        for rule in nature_rules:
            if rule in text:
                rules.append(f"存在{rule}的自然法则")
        
        # 修炼规则
        cultivation_rules = ['境界', '瓶颈', '突破', '雷劫']
        for rule in cultivation_rules:
            if rule in text:
                rules.append(f"修炼存在{rule}的限制")
        
        return rules
    
    def _identify_factions(self, text: str, characters: List[Character]) -> List[Faction]:
        """
        识别势力
        """
        factions = []
        seen_factions = set()
        
        # 识别宗门
        sect_keywords = ['宗门', '门派', '教派']
        for keyword in sect_keywords:
            pattern = rf'([^\s，。]{2,10}){keyword}'
            matches = re.findall(pattern, text)
            
            for match in matches:
                if match not in seen_factions:
                    seen_factions.add(match)
                    
                    # 查找该势力的人物
                    members = [c.name for c in characters if c.name in text[text.find(match):text.find(match)+500] if match]
                    
                    faction = Faction(
                        name=match,
                        original_name=match,
                        type="sect",
                        members=members[:5]
                    )
                    factions.append(faction)
        
        # 识别国家
        country_keywords = ['王朝', '帝国', '皇朝', '国家']
        for keyword in country_keywords:
            pattern = rf'([^\s，。]{2,10}){keyword}'
            matches = re.findall(pattern, text)
            
            for match in matches:
                if match not in seen_factions:
                    seen_factions.add(match)
                    
                    faction = Faction(
                        name=match,
                        original_name=match,
                        type="country",
                        members=[]
                    )
                    factions.append(faction)
        
        # 识别家族
        family_keywords = ['家族', '世家', '氏族']
        for keyword in family_keywords:
            pattern = rf'([^\s，。]{2,10}){keyword}'
            matches = re.findall(pattern, text)
            
            for match in matches:
                if match not in seen_factions:
                    seen_factions.add(match)
                    
                    faction = Faction(
                        name=match,
                        original_name=match,
                        type="family",
                        members=[]
                    )
                    factions.append(faction)
        
        return factions[:10]  # 最多10个势力
    
    def analyze_power_system(self, novel: NovelDocument) -> PowerSystem:
        """
        分析力量系统
        """
        text = novel.original_text
        
        # 识别力量等级
        levels = self._identify_power_levels(text)
        
        # 提取等级描述
        level_descriptions = self._extract_level_descriptions(text, levels)
        
        # 识别修炼方法
        cultivation_methods = self._identify_cultivation_methods(text)
        
        # 提取特殊能力
        special_abilities = self._extract_special_abilities(text)
        
        # 提取规则限制
        rules = self._extract_power_rules(text)
        
        return PowerSystem(
            levels=levels,
            level_descriptions=level_descriptions,
            cultivation_methods=cultivation_methods,
            special_abilities=special_abilities,
            rules=rules
        )
    
    def _identify_power_levels(self, text: str) -> List[str]:
        """
        识别力量等级
        """
        levels = []
        
        # 修仙等级模式
        cultivation_levels = [
            '炼气', '筑基', '金丹', '元婴', '化神',
            '炼虚', '合体', '大乘', '渡劫', '真仙',
            '金仙', '太乙', '大罗', '混元', '道祖'
        ]
        
        for level in cultivation_levels:
            if level in text:
                levels.append(level)
        
        # 武侠等级模式
        martial_levels = [
            '三流', '二流', '一流', '后天', '先天',
            '宗师', '大宗师', '天人', '陆地神仙'
        ]
        
        for level in martial_levels:
            if level in text:
                levels.append(level)
        
        # 玄幻等级模式
        fantasy_levels = [
            '凡境', '灵境', '王境', '皇境', '帝境',
            '圣境', '神境', '帝君', '圣帝', '天帝'
        ]
        
        for level in fantasy_levels:
            if level in text:
                levels.append(level)
        
        # 去重并保持顺序
        unique_levels = list(dict.fromkeys(levels))
        
        return unique_levels if unique_levels else ['凡人', '修士', '大能', '仙人', '神']
    
    def _extract_level_descriptions(self, text: str, levels: List[str]) -> Dict[str, str]:
        """
        提取等级描述
        """
        descriptions = {}
        
        for i, level in enumerate(levels):
            # 在文本中查找该等级的描述
            pattern = rf'{level}[^。]*'
            match = re.search(pattern, text)
            
            if match:
                desc = match.group(0)[:50]
                descriptions[level] = desc
            else:
                descriptions[level] = f"达到{level}境界"
        
        return descriptions
    
    def _identify_cultivation_methods(self, text: str) -> List[str]:
        """
        识别修炼方法
        """
        methods = []
        
        # 常见修炼方法
        method_keywords = ['功法', '心法', '秘籍', '传承', '法术', '神通', '秘术']
        
        for keyword in method_keywords:
            pattern = rf'([^\s，。]{2,10}){keyword}'
            matches = re.findall(pattern, text)
            methods.extend(matches[:5])
        
        # 去重
        unique_methods = list(set(methods))[:10]
        
        return unique_methods if unique_methods else ['基础修炼功法']
    
    def _extract_special_abilities(self, text: str) -> Dict[str, str]:
        """
        提取特殊能力
        """
        abilities = {}
        
        # 神通
        supernatural_keywords = ['神通', '秘术', '绝技', '大招']
        for keyword in supernatural_keywords:
            pattern = rf'([^\s，。]{2,10}){keyword}'
            matches = re.findall(pattern, text)
            
            for match in matches[:5]:
                abilities[match] = f"{match}是一种强大的特殊能力"
        
        # 元素能力
        element_keywords = ['火', '水', '木', '金', '土', '雷', '风', '冰']
        for element in element_keywords:
            pattern = rf'{element}系[法术技能能力]?'
            if re.search(pattern, text):
                abilities[f'{element}系能力'] = f"操控{element}元素的能力"
        
        return abilities
    
    def _extract_power_rules(self, text: str) -> List[str]:
        """
        提取力量规则
        """
        rules = []
        
        # 境界限制
        if '境界' in text:
            rules.append("修炼存在境界限制，必须逐步突破")
        
        # 瓶颈
        if '瓶颈' in text:
            rules.append("突破时可能遇到瓶颈，需要特殊条件")
        
        # 雷劫
        if '雷劫' in text or '天劫' in text:
            rules.append("高境界突破需要渡过雷劫/天劫")
        
        # 因果
        if '因果' in text or '业力' in text:
            rules.append("行为会累积因果，影响修炼")
        
        # 消耗
        if '消耗' in text or '代价' in text:
            rules.append("使用强大力量需要付出代价")
        
        return rules
    
    def generate_world_description(self, world_settings: WorldSetting, power_system: PowerSystem) -> str:
        """
        生成世界观描述（用于仿写参考）
        """
        description = []
        
        description.append("=== 世界观设定 ===\n")
        
        if world_settings.geography:
            description.append("【地理环境】")
            for loc, desc in list(world_settings.geography.items())[:5]:
                description.append(f"- {loc}: {desc}")
            description.append("")
        
        if world_settings.social_structure:
            description.append("【社会结构】")
            for struct, desc in world_settings.social_structure.items():
                description.append(f"- {struct}: {desc}")
            description.append("")
        
        if power_system.levels:
            description.append("【力量等级】")
            for i, level in enumerate(power_system.levels):
                desc = power_system.level_descriptions.get(level, '')
                description.append(f"{i+1}. {level} - {desc}")
            description.append("")
        
        if power_system.cultivation_methods:
            description.append("【修炼方法】")
            for method in power_system.cultivation_methods[:5]:
                description.append(f"- {method}")
            description.append("")
        
        if power_system.rules:
            description.append("【力量规则】")
            for rule in power_system.rules:
                description.append(f"- {rule}")
        
        return '\n'.join(description)
