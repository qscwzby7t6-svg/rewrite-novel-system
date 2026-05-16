# NovelForge - 仿写小说软件配置文件

import os
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class RewriteType(str, Enum):
    """仿写类型枚举"""
    FANTASY = "fantasy"  # 玄幻
    XIANXIA = "xianxia"  # 仙侠
    URBAN = "urban"  # 都市
    SCI_FI = "sci_fi"  # 科幻
    GAME = "game"  # 游戏
    HISTORY = "history"  # 历史
    OTHER = "other"  # 其他

class Language(str, Enum):
    """支持的语言"""
    ZH_CN = "zh-CN"  # 简体中文
    ZH_TW = "zh-TW"  # 繁体中文
    EN_US = "en-US"  # 英语
    JA_JP = "ja-JP"  # 日语
    KO_KR = "ko-KR"  # 韩语

class RewriteConfig(BaseModel):
    """仿写配置模型"""
    main_character_name: str  # 主角名字
    rewrite_type: RewriteType  # 仿写类型
    target_language: Language  # 目标语言
    similarity_threshold: float = 0.1  # 相似度阈值
    chapter_word_count_range: tuple[int, int] = (3000, 5000)  # 章节字数范围
    enable_profanity: bool = False  # 是否允许脏话
    custom_names: Optional[dict] = {}  # 自定义人名地名

class Settings(BaseModel):
    """系统设置"""
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/novel.db"
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_ENABLED: bool = False
    
    # LLM配置
    DEFAULT_LLM_PROVIDER: str = "deepseek"  # 默认使用DeepSeek
    DEEPSEEK_API_KEY: Optional[str] = None
    DEEPSEEK_BASE_URL: Optional[str] = None
    DEEPSEEK_MODEL: str = "deepseek-chat"
    
    WENXIN_API_KEY: Optional[str] = None
    WENXIN_BASE_URL: Optional[str] = None
    WENXIN_MODEL: str = "ERNIE-4.0-Turbo-8K"
    
    QIANWEN_API_KEY: Optional[str] = None
    QIANWEN_BASE_URL: Optional[str] = None
    QIANWEN_MODEL: str = "qwen-turbo"
    
    KIMI_API_KEY: Optional[str] = None
    KIMI_BASE_URL: Optional[str] = None
    KIMI_MODEL: str = "moonshot-v1-8k"
    
    GLM_API_KEY: Optional[str] = None
    GLM_BASE_URL: Optional[str] = None
    GLM_MODEL: str = "glm-4-flash"
    
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    
    # LLM通用参数
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 2000
    LLM_TOP_P: float = 1.0
    LLM_PRESENCE_PENALTY: float = 0.0
    LLM_FREQUENCY_PENALTY: float = 0.0
    LLM_TIMEOUT: int = 60
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    
    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS: List[str] = [".txt", ".doc", ".docx"]
    
    # 仿写配置
    DEFAULT_SIMILARITY_THRESHOLD: float = 0.1
    CHAPTER_WORD_COUNT_MIN: int = 3000
    CHAPTER_WORD_COUNT_MAX: int = 5000
    CLIMAX_INTERVAL: int = 10  # 每10章一个小高潮
    
    # 相似度检测配置
    SIMILARITY_ALGORITHM: str = "combined"  # combined, jaccard, cosine, embedding
    
    # 去AI化配置
    DEAI_STRENGTH: float = 0.7  # 0-1，越高越激进
    ADD_NATURAL_ERRORS: bool = True
    VARIABLE_SENTENCE_LENGTH: bool = True
    
    # 多语言支持
    SUPPORTED_LANGUAGES: List[str] = ["zh-CN", "zh-TW", "en-US", "ja-JP", "ko-KR"]
    DEFAULT_LANGUAGE: str = "zh-CN"
    
    # 性能配置
    MAX_WORKERS: int = 4
    BATCH_SIZE: int = 10
    TIMEOUT: int = 300  # 5分钟

# 全局设置实例
settings = Settings()

# 从环境变量覆盖配置
if os.getenv("DATABASE_URL"):
    settings.DATABASE_URL = os.getenv("DATABASE_URL")

# LLM配置
if os.getenv("DEFAULT_LLM_PROVIDER"):
    settings.DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER")
if os.getenv("DEEPSEEK_API_KEY"):
    settings.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if os.getenv("DEEPSEEK_BASE_URL"):
    settings.DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL")
if os.getenv("DEEPSEEK_MODEL"):
    settings.DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")

if os.getenv("WENXIN_API_KEY"):
    settings.WENXIN_API_KEY = os.getenv("WENXIN_API_KEY")
if os.getenv("WENXIN_BASE_URL"):
    settings.WENXIN_BASE_URL = os.getenv("WENXIN_BASE_URL")
if os.getenv("WENXIN_MODEL"):
    settings.WENXIN_MODEL = os.getenv("WENXIN_MODEL")

if os.getenv("QIANWEN_API_KEY"):
    settings.QIANWEN_API_KEY = os.getenv("QIANWEN_API_KEY")
if os.getenv("QIANWEN_BASE_URL"):
    settings.QIANWEN_BASE_URL = os.getenv("QIANWEN_BASE_URL")
if os.getenv("QIANWEN_MODEL"):
    settings.QIANWEN_MODEL = os.getenv("QIANWEN_MODEL")

if os.getenv("KIMI_API_KEY"):
    settings.KIMI_API_KEY = os.getenv("KIMI_API_KEY")
if os.getenv("KIMI_BASE_URL"):
    settings.KIMI_BASE_URL = os.getenv("KIMI_BASE_URL")
if os.getenv("KIMI_MODEL"):
    settings.KIMI_MODEL = os.getenv("KIMI_MODEL")

if os.getenv("GLM_API_KEY"):
    settings.GLM_API_KEY = os.getenv("GLM_API_KEY")
if os.getenv("GLM_BASE_URL"):
    settings.GLM_BASE_URL = os.getenv("GLM_BASE_URL")
if os.getenv("GLM_MODEL"):
    settings.GLM_MODEL = os.getenv("GLM_MODEL")

if os.getenv("OPENAI_API_KEY"):
    settings.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if os.getenv("OPENAI_BASE_URL"):
    settings.OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
if os.getenv("OPENAI_MODEL"):
    settings.OPENAI_MODEL = os.getenv("OPENAI_MODEL")
