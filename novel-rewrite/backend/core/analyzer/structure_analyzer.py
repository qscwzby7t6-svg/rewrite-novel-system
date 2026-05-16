# 小说结构分析模块
# 用于分析小说的宏观架构、章节架构、高潮点、伏笔等

from typing import List, Dict, Optional, Tuple
import re
from backend.models.novel import (
    NovelDocument, Chapter, ChapterType, MacroStructure,
    PlotArc, PlotArcType, ClimaxPoint, Sentence
)

class StructureAnalyzer:
    """结构分析器"""
    
    def __init__(self):
        # 高潮相关关键词
        self.climax_keywords = [
            '爆发', '激战', '决战', '对决', '突破', '觉醒',
            '爆发', '逆转', '爆发', '高潮', '关键时刻',
            '生死', '危机', '转折', '大招', '底牌'
        ]
        
        # 伏笔相关关键词
        self.foreshadowing_keywords = [
            '埋下', '伏笔', '暗示', '预示', '日后', '将来',
            '注定', '似乎', '也许', '仿佛', '隐约', '似乎要'
        ]
        
        # 过渡相关关键词
        self.transition_keywords = [
            '翌日', '次日', '几天后', '过了一段时间',
            '转眼', '时光飞逝', '很快', '不多时'
        ]
    
    def analyze_novel_structure(self, novel: NovelDocument) -> MacroStructure:
        """
        分析小说宏观结构
        """
        # 分析章节结构
        self._analyze_chapter_structures(novel.chapters)
        
        # 识别情节线
        plot_arcs = self._identify_plot_arcs(novel)
        
        # 识别高潮点
        climax_points = self._identify_climax_points(novel)
        
        # 识别伏笔
        foreshadowing_list = self._extract_foreshadowing(novel)
        
        # 确定整体结构类型
        structure_type = self._determine_structure_type(novel)
        
        # 分析章节分布
        acts = self._analyze_act_distribution(novel)
        
        return MacroStructure(
            structure_type=structure_type,
            acts=acts,
            plot_arcs=plot_arcs,
            climax_points=climax_points,
            foreshadowing_list=foreshadowing_list
        )
    
    def _analyze_chapter_structures(self, chapters: List[Chapter]) -> None:
        """
        分析每个章节的结构类型
        """
        total_chapters = len(chapters)
        
        for i, chapter in enumerate(chapters):
            # 计算章节的激动程度
            climax_score = self._calculate_climax_score(chapter)
            chapter.climax_intensity = climax_score
            
            # 判断章节类型
            progress = i / total_chapters if total_chapters > 0 else 0
            
            if climax_score > 0.7 or self._is_battle_chapter(chapter):
                chapter.structure_type = ChapterType.CLIMAX
            elif progress < 0.1:
                chapter.structure_type = ChapterType.SETUP
            elif progress > 0.9:
                chapter.structure_type = ChapterType.RESOLUTION
            elif self._is_transition_chapter(chapter):
                chapter.structure_type = ChapterType.TRANSITION
            else:
                chapter.structure_type = ChapterType.DEVELOPMENT
    
    def _calculate_climax_score(self, chapter: Chapter) -> float:
        """
        计算章节的高潮得分
        基于关键词密度和情感强度
        """
        text = chapter.content
        text_lower = text.lower()
        
        score = 0.0
        
        # 关键词密度
        keyword_count = sum(1 for kw in self.climax_keywords if kw in text)
        score += min(keyword_count * 0.1, 0.3)
        
        # 感叹号和问号密度
        exclamation_count = text.count('！') + text.count('!')
        question_count = text.count('？') + text.count('?')
        total_punctuation = text.count('。') + text.count('，')
        
        if total_punctuation > 0:
            excitement_ratio = (exclamation_count + question_count) / total_punctuation
            score += min(excitement_ratio * 0.3, 0.3)
        
        # 字数因素（高潮章节通常较长）
        word_count = chapter.word_count
        if word_count > 5000:
            score += 0.2
        
        # 战斗场景得分
        if self._is_battle_chapter(chapter):
            score += 0.2
        
        return min(score, 1.0)
    
    def _is_battle_chapter(self, chapter: Chapter) -> bool:
        """判断是否为战斗章节"""
        battle_keywords = ['战斗', '厮杀', '对决', '搏斗', '攻击', '出手', '招式', '灵力', '法力']
        text = chapter.content
        
        matches = sum(1 for kw in battle_keywords if kw in text)
        return matches >= 3
    
    def _is_transition_chapter(self, chapter: Chapter) -> bool:
        """判断是否为过渡章节"""
        return any(kw in chapter.content for kw in self.transition_keywords)
    
    def _identify_plot_arcs(self, novel: NovelDocument) -> List[PlotArc]:
        """
        识别情节线
        """
        plot_arcs = []
        
        # 主线情节
        main_arc = PlotArc(
            type=PlotArcType.MAIN,
            name="主线剧情",
            description="小说的主要情节线",
            start_chapter=1,
            end_chapter=len(novel.chapters),
            key_events=self._extract_main_events(novel)
        )
        plot_arcs.append(main_arc)
        
        # 识别支线情节
        subplot_arcs = self._identify_subplots(novel)
        plot_arcs.extend(subplot_arcs)
        
        return plot_arcs
    
    def _identify_subplots(self, novel: NovelDocument) -> List[PlotArc]:
        """识别支线情节"""
        subplots = []
        
        # 基于人物识别支线
        for character in novel.characters[:3]:  # 最多3条支线
            if character.first_appearance_chapter > 1:
                subplot = PlotArc(
                    type=PlotArcType.SUBPLOT,
                    name=f"{character.name}的支线",
                    description=character.background[:100] if character.background else "",
                    start_chapter=character.first_appearance_chapter,
                    end_chapter=len(novel.chapters),
                    key_events=[]
                )
                subplots.append(subplot)
        
        return subplots
    
    def _extract_main_events(self, novel: NovelDocument) -> List[str]:
        """
        提取主线关键事件
        """
        events = []
        
        # 提取高潮章节的事件
        for climax in self._identify_climax_points(novel):
            if climax.type in ['battle', 'revelation']:
                events.append(f"第{climax.chapter}章: {climax.description}")
        
        return events[:10]  # 最多10个关键事件
    
    def _identify_climax_points(self, novel: NovelDocument) -> List[ClimaxPoint]:
        """
        识别高潮点
        """
        climax_points = []
        
        for chapter in novel.chapters:
            if chapter.climax_intensity > 0.6:
                # 判断高潮类型
                climax_type = "general"
                if self._is_battle_chapter(chapter):
                    climax_type = "battle"
                elif '揭露' in chapter.content or '真相' in chapter.content:
                    climax_type = "revelation"
                elif '突破' in chapter.content or '觉醒' in chapter.content:
                    climax_type = "transformation"
                
                climax = ClimaxPoint(
                    chapter=chapter.number,
                    type=climax_type,
                    intensity=chapter.climax_intensity,
                    description=self._extract_climax_description(chapter),
                    involved_characters=chapter.characters
                )
                climax_points.append(climax)
        
        # 确保每10章有一个高潮
        climax_chapters = [c.chapter for c in climax_points]
        total_chapters = len(novel.chapters)
        
        for i in range(10, total_chapters, 10):
            if i not in climax_chapters:
                # 在附近找一个最接近的高潮
                nearby = min(climax_points, key=lambda x: abs(x.chapter - i), default=None)
                if nearby and abs(nearby.chapter - i) <= 2:
                    climax_points.append(ClimaxPoint(
                        chapter=i,
                        type="mini_climax",
                        intensity=0.5,
                        description=f"第{i}章小高潮",
                        involved_characters=[]
                    ))
        
        return sorted(climax_points, key=lambda x: x.chapter)
    
    def _extract_climax_description(self, chapter: Chapter) -> str:
        """提取高潮描述"""
        # 找到最激烈的句子
        max_length = 0
        climax_sentence = ""
        
        for sentence in chapter.sentences:
            if len(sentence.text) > max_length and any(kw in sentence.text for kw in self.climax_keywords):
                climax_sentence = sentence.text
                max_length = len(sentence.text)
        
        return climax_sentence[:100] if climax_sentence else chapter.content[:100]
    
    def _extract_foreshadowing(self, novel: NovelDocument) -> List[str]:
        """
        提取伏笔
        """
        foreshadowing = []
        
        for chapter in novel.chapters:
            for sentence in chapter.sentences:
                if any(kw in sentence.text for kw in self.foreshadowing_keywords):
                    foreshadowing.append(sentence.text[:150])
        
        return foreshadowing[:20]  # 最多20个伏笔
    
    def _determine_structure_type(self, novel: NovelDocument) -> str:
        """
        确定整体结构类型
        """
        total_chapters = len(novel.chapters)
        
        if total_chapters <= 30:
            return "三幕结构"
        elif total_chapters <= 100:
            return "五幕结构"
        else:
            return "史诗结构"
    
    def _analyze_act_distribution(self, novel: NovelDocument) -> List[Dict]:
        """
        分析章节分布
        """
        total = len(novel.chapters)
        
        if total == 0:
            return []
        
        acts = [
            {"name": "第一幕（开端）", "start": 1, "end": int(total * 0.25)},
            {"name": "第二幕（发展）", "start": int(total * 0.25) + 1, "end": int(total * 0.5)},
            {"name": "第三幕（高潮）", "start": int(total * 0.5) + 1, "end": int(total * 0.75)},
            {"name": "第四幕（结局）", "start": int(total * 0.75) + 1, "end": total},
        ]
        
        return acts
    
    def analyze_chapter_structure(self, chapter: Chapter) -> Dict:
        """
        分析单个章节的详细结构
        """
        # 场景分析
        scene_distribution = {}
        for scene in chapter.scenes:
            scene_type = scene.type.value
            scene_distribution[scene_type] = scene_distribution.get(scene_type, 0) + 1
        
        # 对话与叙述比例
        dialogue_ratio = scene_distribution.get('dialogue', 0) / max(len(chapter.scenes), 1)
        narration_ratio = scene_distribution.get('narration', 0) / max(len(chapter.scenes), 1)
        
        # 节奏分析
        rhythm_score = self._analyze_rhythm(chapter)
        
        return {
            "scene_distribution": scene_distribution,
            "dialogue_ratio": dialogue_ratio,
            "narration_ratio": narration_ratio,
            "rhythm_score": rhythm_score,
            "climax_intensity": chapter.climax_intensity,
            "structure_type": chapter.structure_type.value
        }
    
    def _analyze_rhythm(self, chapter: Chapter) -> float:
        """
        分析章节节奏
        """
        if not chapter.sentences:
            return 0.5
        
        # 计算句子长度变化
        lengths = [len(s.text) for s in chapter.sentences]
        
        if len(lengths) < 2:
            return 0.5
        
        # 计算变化系数
        avg_length = sum(lengths) / len(lengths)
        variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
        
        # 节奏变化越大，系数越高
        rhythm_variation = min(variance / (avg_length ** 2), 1.0)
        
        return rhythm_variation
    
    def get_plot_progression(self, novel: NovelDocument) -> List[Tuple[int, float]]:
        """
        获取情节发展曲线
        Returns:
            [(章节号, 激动程度), ...]
        """
        progression = []
        
        for chapter in novel.chapters:
            progression.append((chapter.number, chapter.climax_intensity))
        
        return progression
