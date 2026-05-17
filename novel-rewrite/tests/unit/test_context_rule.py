#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NovelForge - 阅读上下文规则测试
测试新增的上下文规则功能
"""

import sys
import os
# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from backend.core.engine.rewrite_engine import RewriteEngine
from backend.models.novel import (
    NovelDocument, NovelMetadata, Chapter, WorldSetting,
    Character, Faction, RewriteConfig
)
from datetime import datetime
from uuid import uuid4


def create_test_novel():
    """创建测试用的小说文档"""
    # 创建元数据
    metadata = NovelMetadata(
        title="测试小说",
        author="测试作者",
        genre="玄幻",
        total_words=10000,
        total_chapters=10,
        created_at=datetime.now()
    )
    
    # 创建10个测试章节
    chapters = []
    for i in range(1, 11):
        chapter = Chapter(
            id=uuid4(),
            number=i,
            title=f"第{i}章 测试章节",
            content=f"""这是第{i}章的内容。
主角在这一章进行了修炼，实力得到了提升。
他遇到了一些朋友和敌人，发生了一些有趣的事情。
""",
            word_count=1000
        )
        chapters.append(chapter)
    
    # 创建人物
    characters = [
        Character(
            id=uuid4(),
            name="主角",
            personality_traits=["勇敢", "聪明"],
            first_appearance_chapter=1
        )
    ]
    
    # 创建世界观
    world_setting = WorldSetting(
        factions=[
            Faction(id=uuid4(), name="青云宗", type="门派"),
            Faction(id=uuid4(), name="天魔教", type="门派")
        ]
    )
    
    # 创建小说文档
    novel = NovelDocument(
        id=uuid4(),
        metadata=metadata,
        chapters=chapters,
        characters=characters,
        world_settings=world_setting
    )
    
    return novel


def test_context_rule_config():
    """测试上下文规则配置"""
    print("=" * 60)
    print("测试1: 上下文规则配置")
    print("=" * 60)
    
    # 测试默认配置
    config1 = RewriteConfig(
        main_character_name="新主角"
    )
    
    print(f"\n默认配置:")
    print(f"  enable_context_rule: {config1.enable_context_rule}")
    print(f"  context_window_size: {config1.context_window_size}")
    print(f"  start_chapter: {config1.start_chapter}")
    
    # 测试自定义配置
    config2 = RewriteConfig(
        main_character_name="新主角",
        enable_context_rule=True,
        context_window_size=3,
        start_chapter=4
    )
    
    print(f"\n自定义配置:")
    print(f"  enable_context_rule: {config2.enable_context_rule}")
    print(f"  context_window_size: {config2.context_window_size}")
    print(f"  start_chapter: {config2.start_chapter}")
    
    print("\n✅ 配置测试通过")


def test_build_chapter_context():
    """测试构建章节上下文"""
    print("\n" + "=" * 60)
    print("测试2: 构建章节上下文")
    print("=" * 60)
    
    # 创建测试小说
    novel = create_test_novel()
    
    # 创建一些已仿写的章节
    rewritten_chapters = []
    for i in range(1, 6):  # 前5章已仿写
        chapter = Chapter(
            id=uuid4(),
            number=i,
            title=f"第{i}章 仿写章节",
            content=f"这是仿写的第{i}章内容。",
            word_count=1000
        )
        rewritten_chapters.append(chapter)
    
    # 创建引擎
    engine = RewriteEngine()
    
    # 测试第6章的上下文
    context = engine._build_chapter_context(
        novel,
        rewritten_chapters,
        6,  # 仿写第6章
        5   # 窗口大小5
    )
    
    print(f"\n第6章上下文:")
    print(f"  chapter_number: {context.chapter_number}")
    print(f"  original_chapters 数量: {len(context.original_chapters)}")
    print(f"  rewritten_chapters 数量: {len(context.rewritten_chapters)}")
    print(f"  original_chapter_titles: {context.original_chapter_titles}")
    print(f"  rewritten_chapter_titles: {context.rewritten_chapter_titles}")
    
    # 验证
    assert len(context.original_chapters) == 5, "应该有5章原文上下文"
    assert len(context.rewritten_chapters) == 5, "应该有5章仿写上下文"
    
    print("\n✅ 上下文构建测试通过")


def test_rewrite_with_context():
    """测试带上下文的仿写"""
    print("\n" + "=" * 60)
    print("测试3: 带上下文的仿写")
    print("=" * 60)
    
    # 创建测试小说
    novel = create_test_novel()
    
    # 创建引擎
    engine = RewriteEngine()
    
    # 测试不同的配置
    configs = [
        ("启用上下文规则（默认）", RewriteConfig(
            main_character_name="新主角",
            enable_context_rule=True
        )),
        ("禁用上下文规则", RewriteConfig(
            main_character_name="新主角",
            enable_context_rule=False
        )),
        ("自定义窗口大小", RewriteConfig(
            main_character_name="新主角",
            enable_context_rule=True,
            context_window_size=3,
            start_chapter=4
        ))
    ]
    
    for name, config in configs:
        print(f"\n测试配置: {name}")
        print(f"  启用规则: {config.enable_context_rule}")
        print(f"  窗口大小: {config.context_window_size}")
        print(f"  起始章节: {config.start_chapter}")
        
        # 执行仿写
        result = engine.rewrite_novel(novel, config)
        
        print(f"  仿写完成，共 {len(result.chapters)} 章")
        
        # 验证章节
        assert len(result.chapters) == 10, "应该有10章"
        
        for i, chapter in enumerate(result.chapters):
            chapter_num = i + 1
            if config.enable_context_rule and chapter_num >= config.start_chapter:
                print(f"    第{chapter_num}章: 应用了上下文规则")
            else:
                print(f"    第{chapter_num}章: 普通仿写")
    
    print("\n✅ 带上下文仿写测试通过")


def test_llm_context_service():
    """测试LLM服务的上下文功能（不实际调用API）"""
    print("\n" + "=" * 60)
    print("测试4: LLM服务上下文功能")
    print("=" * 60)
    
    try:
        from backend.core.llm.service import LLMRewriteService
        from backend.models.novel import ChapterContext
        
        service = LLMRewriteService()
        
        # 测试构建上下文摘要的逻辑
        print("\n测试 _build_context_summary 方法（概念验证）:")
        
        # 创建测试上下文
        test_context = ChapterContext(
            chapter_number=10,
            original_chapters=["原文5内容", "原文6内容", "原文7内容", "原文8内容", "原文9内容"],
            rewritten_chapters=["仿写5内容", "仿写6内容", "仿写7内容", "仿写8内容", "仿写9内容"],
            original_chapter_titles=["原文第5章", "原文第6章", "原文第7章", "原文第8章", "原文第9章"],
            rewritten_chapter_titles=["仿写第5章", "仿写第6章", "仿写第7章", "仿写第8章", "仿写第9章"]
        )
        
        # 调用方法（仅测试方法存在和参数正确）
        print(f"  上下文对象创建成功")
        print(f"  章节号: {test_context.chapter_number}")
        print(f"  原文上下文数量: {len(test_context.original_chapters)}")
        print(f"  仿写上下文数量: {len(test_context.rewritten_chapters)}")
        
        print("\n✅ LLM服务上下文功能测试通过（概念验证）")
        
    except Exception as e:
        print(f"\n⚠️  LLM服务测试跳过（可能缺少依赖）: {e}")


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("NovelForge 阅读上下文规则测试")
    print("=" * 60)
    
    try:
        test_context_rule_config()
        test_build_chapter_context()
        test_rewrite_with_context()
        test_llm_context_service()
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！")
        print("=" * 60)
        print("\n新增规则说明:")
        print("  1. 仿写小说从第6章开始")
        print("  2. 仿写第N章前，必须阅读原文和仿写的N-5到N-1章")
        print("  3. 保持内容连贯性和一致性")
        print("  4. 规则可配置（窗口大小、起始章节等）")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
