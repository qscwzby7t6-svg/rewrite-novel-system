# 仿写小说软件 - 数据模型定义
# 用于定义小说、章节、人物等核心数据结构

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime

class ChapterType(str, Enum):
    """章节类型"""
    SETUP = "setup"           # 铺垫
    DEVELOPMENT = "development" # 发展
    CLIMAX = "climax"         # 高潮
    RESOLUTION = "resolution"  # 收尾
    TRANSITION = "transition" # 过渡

class PlotArcType(str, Enum):
    """情节线类型"""
    MAIN = "main"             # 主线
    SUBPLOT = "subplot"       # 支线
    BACKSTORY = "backstory"  # 背景故事
    CHARACTER = "character"   # 人物线

class PowerLevel(str, Enum):
    """力量等级"""
    MORTAL = "mortal"         # 凡人
    CULTIVATOR = "cultivator" # 修士
    GREAT_EMINENCE = "great_eminence"  # 大能
    IMMORTAL = "immortal"     # 仙人
    DIVINE = "divine"         # 神

class RelationshipType(str, Enum):
    """人物关系类型"""
    FAMILY = "family"         # 家人
    FRIEND = "friend"         # 朋友
    MENTOR = "mentor"        # 导师
    RIVAL = "rival"          # 竞争对手
    ENEMY = "enemy"          # 敌人
    LOVER = "lover"          # 恋人
    MASTER_DISCIPLE = "master_disciple"  # 师徒
    TEAMMATE = "teammate"    # 队友

class SceneType(str, Enum):
    """场景类型"""
    DIALOGUE = "dialogue"     # 对话
    BATTLE = "battle"         # 战斗
    DESCRIPTION = "description"  # 描述
    ACTION = "action"         # 动作
    NARRATION = "narration"   # 叙述

class NovelMetadata(BaseModel):
    """小说元数据"""
    title: str = ""
    author: str = ""
    genre: str = ""
    total_words: int = 0
    total_chapters: int = 0
    created_at: datetime = Field(default_factory=datetime.now)

class Sentence(BaseModel):
    """句子"""
    text: str
    type: str = "declarative"  # declarative, interrogative, exclamatory, imperative
    has_profanity: bool = False
    emotional_value: float = 0.0  # -1.0到1.0

class Scene(BaseModel):
    """场景"""
    id: UUID = Field(default_factory=uuid4)
    type: SceneType
    content: str
    characters: List[str] = []
    location: Optional[str] = None
    time: Optional[str] = None
    emotional_intensity: float = 0.0

class Chapter(BaseModel):
    """章节"""
    id: UUID = Field(default_factory=uuid4)
    number: int
    title: str = ""
    content: str = ""
    word_count: int = 0
    sentences: List[Sentence] = []
    scenes: List[Scene] = []
    structure_type: ChapterType = ChapterType.DEVELOPMENT
    climax_intensity: float = 0.0  # 0.0到1.0
    foreshadowing: List[str] = []
    characters: List[str] = []

class Character(BaseModel):
    """人物"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    original_name: str = ""  # 原始名字（用于替换）
    gender: Optional[str] = None
    age: Optional[str] = None
    appearance: str = ""  # 外貌描述
    personality_traits: List[str] = []  # 性格特点
    background: str = ""  # 背景故事
    abilities: List[str] = []  # 能力
    speech_style: str = ""  # 说话风格
    first_appearance_chapter: int = 0
    relationships: Dict[str, RelationshipType] = {}  # 关系网络
    growth_arc: Dict[str, Any] = {}  # 成长弧线
    arc_description: str = ""  # 人物弧光描述

class Faction(BaseModel):
    """势力"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    original_name: str = ""
    type: str = ""  # 门派、组织、国家等
    leader: Optional[str] = None
    members: List[str] = []
    territory: str = ""
    ideology: str = ""

class PowerSystem(BaseModel):
    """力量系统"""
    levels: List[str] = []  # 等级列表
    level_descriptions: Dict[str, str] = {}  # 等级描述
    cultivation_methods: List[str] = []  # 修炼方法
    special_abilities: Dict[str, str] = {}  # 特殊能力描述
    rules: List[str] = []  # 规则限制

class WorldSetting(BaseModel):
    """世界观设定"""
    geography: Dict[str, str] = {}  # 地理环境
    social_structure: Dict[str, str] = {}  # 社会结构
    culture: Dict[str, str] = {}  # 文化背景
    history: List[str] = []  # 历史背景
    rules: List[str] = []  # 世界规则
    factions: List[Faction] = []  # 势力

class PlotArc(BaseModel):
    """情节线"""
    id: UUID = Field(default_factory=uuid4)
    type: PlotArcType
    name: str
    description: str
    start_chapter: int = 0
    end_chapter: int = 0
    key_events: List[str] = []
    climax_point: Optional[int] = None

class ClimaxPoint(BaseModel):
    """高潮点"""
    chapter: int
    type: str  # battle, revelation, transformation, etc.
    intensity: float  # 0.0到1.0
    description: str
    involved_characters: List[str] = []

class MacroStructure(BaseModel):
    """宏观结构"""
    structure_type: str = ""  # 三段式、四段式等
    acts: List[Dict[str, Any]] = []  # 幕/章节
    plot_arcs: List[PlotArc] = []
    climax_points: List[ClimaxPoint] = []
    foreshadowing_list: List[str] = []

class NovelDocument(BaseModel):
    """完整的小说文档"""
    id: UUID = Field(default_factory=uuid4)
    metadata: NovelMetadata
    chapters: List[Chapter] = []
    characters: List[Character] = []
    world_settings: WorldSetting = WorldSetting()
    power_system: PowerSystem = PowerSystem()
    macro_structure: MacroStructure = MacroStructure()
    original_text: str = ""  # 原始文本
    language: str = "zh-CN"

class RewriteConfig(BaseModel):
    """仿写配置"""
    main_character_name: str  # 新主角名字
    main_character_gender: str = "male"  # male, female
    rewrite_type: str = "fantasy"  # 仿写类型
    target_language: str = "zh-CN"
    similarity_threshold: float = 0.1
    enable_profanity: bool = False  # 是否允许脏话
    preserve_word_count: bool = True  # 是否保持字数
    chapter_word_count_range: tuple = (3000, 5000)
    
    # 新规则：阅读上下文配置
    enable_context_rule: bool = True  # 是否启用阅读上下文规则
    context_window_size: int = 5  # 上下文窗口大小（默认5章）
    start_chapter: int = 6  # 从第几章开始仿写（默认第6章）


class ChapterContext(BaseModel):
    """章节生成时使用的上下文信息"""
    chapter_number: int  # 当前要生成的章节号
    original_chapters: List[str]  # 原文的前N章内容
    rewritten_chapters: List[str]  # 已仿写的前N章内容
    original_chapter_titles: List[str]  # 原文前N章标题
    rewritten_chapter_titles: List[str]  # 已仿写前N章标题

class RewriteResult(BaseModel):
    """仿写结果"""
    novel_id: UUID
    chapters: List[Chapter]
    analysis_report: Dict[str, Any] = {}
    similarity_report: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "completed"  # processing, completed, failed

class SimilarityReport(BaseModel):
    """相似度报告"""
    chapter_similarities: Dict[int, float] = {}  # 每章相似度
    overall_similarity: float = 0.0
    all_passed: bool = True
    failed_chapters: List[int] = []
    details: List[Dict[str, Any]] = []
