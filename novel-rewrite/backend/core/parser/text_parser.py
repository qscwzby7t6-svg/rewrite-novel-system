# 文本解析和预处理模块
# 用于解析TXT小说文档，提取章节、句子等结构

import re
import chardet
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import aiofiles
from backend.models.novel import (
    NovelDocument, NovelMetadata, Chapter, Sentence, Scene,
    Character, WorldSetting, PowerSystem, MacroStructure,
    SceneType, ChapterType
)
import jieba
import nltk
from nltk.tokenize import sent_tokenize

class TextParser:
    """文本解析器"""
    
    def __init__(self):
        self.chapter_patterns = [
            r'^第[一二三四五六七八九十百千万\d]+章[：:\s].+$',  # 第X章
            r'^Chapter\s+\d+[：:\s]*.*$',  # Chapter X
            r'^第[一二三四五六七八九十百千万\d]+节[：:\s].+$',  # 第X节
            r'^\d+\.[\s].+$',  # 1. 标题
        ]
        self.compiled_patterns = [re.compile(p, re.MULTILINE) for p in self.chapter_patterns]
        
        # 初始化中文分词
        jieba.initialize()
        
    async def parse_file(self, file_path: str) -> NovelDocument:
        """
        解析TXT文件
        Args:
            file_path: 文件路径
        Returns:
            NovelDocument: 解析后的完整小说文档
        """
        # 读取文件
        content = await self._read_file(file_path)
        
        # 检测编码
        encoding = self._detect_encoding(content)
        
        # 解码内容
        try:
            text = content.decode(encoding)
        except:
            text = content.decode('utf-8', errors='ignore')
        
        # 提取元数据
        metadata = self._extract_metadata(text)
        
        # 分割章节
        chapters = self._split_chapters(text)
        
        # 构建文档
        doc = NovelDocument(
            metadata=metadata,
            chapters=chapters,
            original_text=text
        )
        
        return doc
    
    async def _read_file(self, file_path: str) -> bytes:
        """异步读取文件"""
        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()
    
    def _detect_encoding(self, content: bytes) -> str:
        """检测文件编码"""
        result = chardet.detect(content)
        return result.get('encoding', 'utf-8')
    
    def _extract_metadata(self, text: str) -> NovelMetadata:
        """提取小说元数据"""
        lines = text.split('\n')
        
        # 提取标题（通常在第一行或标题标签后）
        title = ""
        author = ""
        genre = ""
        
        # 常见标题模式
        title_patterns = [
            r'^书名[：:]\s*(.+)$',
            r'^《(.+?)》',
            r'^(.+?)\s*$',
        ]
        
        # 常见作者模式
        author_patterns = [
            r'^作者[：:]\s*(.+)$',
            r'^by\s+(.+)$',
        ]
        
        for line in lines[:20]:  # 只检查前20行
            line = line.strip()
            
            if not title:
                for pattern in title_patterns:
                    match = re.search(pattern, line)
                    if match:
                        title = match.group(1).strip()
                        break
            
            if not author:
                for pattern in author_patterns:
                    match = re.search(pattern, line)
                    if match:
                        author = match.group(1).strip()
                        break
            
            if title and author:
                break
        
        # 计算总字数
        total_words = len(text.replace('\n', '').replace(' ', ''))
        
        return NovelMetadata(
            title=title or "未命名小说",
            author=author or "未知作者",
            genre=genre,
            total_words=total_words
        )
    
    def _split_chapters(self, text: str) -> List[Chapter]:
        """
        分割章节
        使用多种模式识别章节标题
        """
        chapters = []
        
        # 尝试不同的分割模式
        split_positions = []
        
        for pattern in self.compiled_patterns:
            matches = pattern.finditer(text)
            for match in matches:
                split_positions.append(match.start())
        
        # 去重并排序
        split_positions = sorted(set(split_positions))
        
        # 如果没有找到章节标题，按字数分割
        if len(split_positions) < 2:
            split_positions = self._split_by_word_count(text, min_chapters=10)
        
        # 提取每个章节
        for i, start in enumerate(split_positions):
            end = split_positions[i + 1] if i + 1 < len(split_positions) else len(text)
            chapter_text = text[start:end].strip()
            
            if chapter_text:
                # 解析章节
                chapter = self._parse_chapter(chapter_text, i + 1)
                chapters.append(chapter)
        
        # 更新元数据
        if chapters:
            total_words = sum(c.word_count for c in chapters)
            chapters[0].word_count = len(text.replace('\n', '').replace(' ', ''))
        
        return chapters
    
    def _split_by_word_count(self, text: str, min_chapters: int = 10) -> List[int]:
        """按字数分割章节"""
        words_per_chapter = len(text.replace('\n', '').replace(' ', '')) // min_chapters
        
        positions = [0]
        current_pos = 0
        current_words = 0
        
        for i, char in enumerate(text):
            if char not in ['\n', ' ', '\t']:
                current_words += 1
            
            if current_words >= words_per_chapter and i < len(text) - 100:
                # 找到段落边界
                for j in range(i, max(i - 100, 0), -1):
                    if text[j] in ['\n', '。', '！', '？']:
                        positions.append(j + 1)
                        break
        
        return sorted(set(positions))
    
    def _parse_chapter(self, text: str, chapter_number: int) -> Chapter:
        """
        解析单个章节
        """
        lines = text.split('\n')
        
        # 提取章节标题
        title = ""
        content_start = 0
        
        for i, line in enumerate(lines[:5]):
            if self._is_chapter_title(line):
                title = self._clean_chapter_title(line)
                content_start = i + 1
                break
        
        # 提取章节内容
        content_lines = lines[content_start:]
        content = '\n'.join(content_lines)
        
        # 计算字数
        word_count = len(content.replace('\n', '').replace(' ', ''))
        
        # 分句
        sentences = self._split_sentences(content)
        
        # 识别场景
        scenes = self._identify_scenes(content, sentences)
        
        return Chapter(
            number=chapter_number,
            title=title or f"第{chapter_number}章",
            content=content,
            word_count=word_count,
            sentences=sentences,
            scenes=scenes
        )
    
    def _is_chapter_title(self, line: str) -> bool:
        """判断是否为章节标题"""
        line = line.strip()
        for pattern in self.chapter_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _clean_chapter_title(self, title: str) -> str:
        """清理章节标题"""
        title = title.strip()
        # 移除章节编号，只保留标题
        patterns = [
            r'^第[一二三四五六七八九十百千万\d]+章[：:\s]*',
            r'^Chapter\s+\d+[：:\s]*',
            r'^第[一二三四五六七八九十百千万\d]+节[：:\s]*',
        ]
        for pattern in patterns:
            title = re.sub(pattern, '', title)
        return title.strip()
    
    def _split_sentences(self, text: str) -> List[Sentence]:
        """
        分句
        """
        sentences = []
        
        # 使用标点符号分割
        pattern = r'[。！？\.!?]+'
        parts = re.split(pattern, text)
        
        for part in parts:
            part = part.strip()
            if part and len(part) > 2:
                # 判断句子类型
                if part.endswith('？') or part.endswith('?'):
                    sentence_type = "interrogative"
                elif part.endswith('！') or part.endswith('!'):
                    sentence_type = "exclamatory"
                else:
                    sentence_type = "declarative"
                
                sentences.append(Sentence(
                    text=part,
                    type=sentence_type
                ))
        
        return sentences
    
    def _identify_scenes(self, content: str, sentences: List[Sentence]) -> List[Scene]:
        """
        识别场景
        基于关键词和上下文判断场景类型
        """
        scenes = []
        
        # 场景关键词
        battle_keywords = ['战斗', '厮杀', '对决', '搏斗', '攻击', '出手', '招式']
        dialogue_keywords = ['说', '道', '问', '答', '叫', '喊', '骂']
        description_keywords = ['只见', '看到', '望去', '周围', '远处']
        
        current_scene = None
        current_content = []
        
        for sentence in sentences:
            text = sentence.text
            scene_type = SceneType.NARRATION
            
            # 判断场景类型
            if any(kw in text for kw in battle_keywords):
                scene_type = SceneType.BATTLE
            elif any(kw in text for kw in dialogue_keywords):
                scene_type = SceneType.DIALOGUE
            elif any(kw in text for kw in description_keywords):
                scene_type = SceneType.DESCRIPTION
            
            # 如果场景类型改变，保存当前场景
            if current_scene and current_scene.type != scene_type:
                scenes.append(Scene(
                    type=current_scene.type,
                    content='。'.join(current_content),
                    emotional_intensity=0.5
                ))
                current_content = []
            
            current_content.append(text)
            current_scene = Scene(
                type=scene_type,
                content=text,
                emotional_intensity=0.5
            )
        
        # 保存最后一个场景
        if current_content and current_scene:
            current_scene.content = '。'.join(current_content)
            scenes.append(current_scene)
        
        return scenes
    
    def tokenize(self, text: str, language: str = "zh-CN") -> List[str]:
        """
        分词
        Args:
            text: 待分词文本
            language: 语言类型
        Returns:
            分词结果列表
        """
        if language.startswith("zh"):
            return list(jieba.cut(text))
        else:
            return nltk.word_tokenize(text)
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[Tuple[str, float]]:
        """
        提取关键词
        使用TF-IDF算法
        """
        # TODO: 实现TF-IDF关键词提取
        words = self.tokenize(text)
        
        # 简单词频统计
        word_freq = {}
        for word in words:
            if len(word) > 1:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # 返回top_n
        total = sum(w[1] for w in sorted_words[:top_n])
        return [(w, f / total) for w, f in sorted_words[:top_n]]
