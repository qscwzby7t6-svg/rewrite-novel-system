# NovelForge - 单元测试文件
# 测试文本解析模块

import pytest
import asyncio
from backend.core.parser.text_parser import TextParser
from backend.models.novel import NovelDocument

@pytest.fixture
def sample_text():
    """示例小说文本"""
    return """第一章 穿越异世

李明睁开眼睛，发现自己躺在一张陌生的床上。

"这是哪里？"他喃喃自语。

周围的环境古色古香，明显不是他熟悉的现代都市。

第二章 修炼开始

李明开始了解这个世界的规则。这是一个修仙的世界，
存在着各种强大的修士。

他决定踏上修炼之路。

第三章 初次战斗

一天，李明遇到了一个敌人。

"小子，把东西交出来！"敌人喊道。

李明毫不畏惧，运转功法迎战。
"""

@pytest.fixture
def parser():
    """文本解析器实例"""
    return TextParser()

class TestTextParser:
    """文本解析器测试"""
    
    def test_parse_file_structure(self, parser, sample_text, tmp_path):
        """测试文件解析结构"""
        # 创建临时文件
        test_file = tmp_path / "test.txt"
        test_file.write_text(sample_text, encoding='utf-8')
        
        # 解析文件
        doc = asyncio.run(parser.parse_file(str(test_file)))
        
        # 验证结构
        assert isinstance(doc, NovelDocument)
        assert len(doc.chapters) > 0
        assert doc.metadata.total_words > 0
    
    def test_chapter_splitting(self, parser, sample_text):
        """测试章节分割"""
        chapters = parser._split_chapters(sample_text)
        
        assert len(chapters) >= 1
        assert all(hasattr(ch, 'number') for ch in chapters)
        assert all(hasattr(ch, 'content') for ch in chapters)
    
    def test_sentence_splitting(self, parser):
        """测试分句功能"""
        text = "李明很高兴。他笑了。真是太棒了！"
        sentences = parser._split_sentences(text)
        
        assert len(sentences) >= 2
        assert all(hasattr(s, 'text') for s in sentences)
        assert all(hasattr(s, 'type') for s in sentences)
    
    def test_chinese_tokenization(self, parser):
        """测试中文分词"""
        text = "李明是一个修士"
        words = parser.tokenize(text, "zh-CN")
        
        assert len(words) > 0
        assert "李明" in words or "李" in words
        assert "修士" in words
    
    def test_metadata_extraction(self, parser):
        """测试元数据提取"""
        text = """书名：玄幻大作
作者：张三

第一章 开头

这里是正文内容。
"""
        metadata = parser._extract_metadata(text)
        
        assert metadata.title == "玄幻大作"
        assert metadata.author == "张三"
    
    def test_scene_identification(self, parser):
        """测试场景识别"""
        text = "李明说：'我要战斗！'他出手攻击敌人。"
        sentences = parser._split_sentences(text)
        scenes = parser._identify_scenes(text, sentences)
        
        assert len(scenes) >= 0
    
    def test_empty_text_handling(self, parser):
        """测试空文本处理"""
        chapters = parser._split_chapters("")
        assert len(chapters) == 0

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
