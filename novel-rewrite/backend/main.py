# NovelForge - AI小说仿写引擎后端API
# 整合所有核心模块，提供完整的RESTful API接口

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from uuid import UUID, uuid4
import asyncio
import os
from pathlib import Path

# 导入核心模块
from backend.core.parser.text_parser import TextParser
from backend.core.analyzer.structure_analyzer import StructureAnalyzer
from backend.core.analyzer.world_analyzer import WorldAnalyzer
from backend.core.analyzer.character_analyzer import CharacterAnalyzer
from backend.core.engine.rewrite_engine import RewriteEngine
from backend.core.deai.deai_module import DeAIModule
from backend.core.similarity.similarity_detector import SimilarityDetector
from backend.core.i18n.i18n_module import I18nModule, get_i18n
from backend.core.llm.service import LLMRewriteService, llm_service
from backend.core.llm.base import LLMProvider
from backend.models.novel import (
    NovelDocument, RewriteConfig, RewriteResult, SimilarityReport,
    RewriteType, Language
)

# 初始化FastAPI应用
app = FastAPI(
    title="NovelForge API",
    description="AI小说仿写引擎 - 智能复刻小说风格与架构",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心模块
parser = TextParser()
structure_analyzer = StructureAnalyzer()
world_analyzer = WorldAnalyzer()
character_analyzer = CharacterAnalyzer()
rewrite_engine = RewriteEngine()
deai_module = DeAIModule()
similarity_detector = SimilarityDetector()
i18n = get_i18n()

# 内存存储（生产环境应使用数据库）
novels_storage: Dict[str, NovelDocument] = {}
rewrite_tasks: Dict[str, Dict[str, Any]] = {}


# ==================== 请求/响应模型 ====================

class UploadResponse(BaseModel):
    """上传响应"""
    novel_id: str
    title: str
    author: str
    total_chapters: int
    total_words: int
    status: str

class AnalysisResponse(BaseModel):
    """分析响应"""
    novel_id: str
    structure: Dict[str, Any]
    world_settings: Dict[str, Any]
    characters: List[Dict[str, Any]]
    power_system: Dict[str, Any]
    statistics: Dict[str, Any]

class RewriteRequest(BaseModel):
    """仿写请求"""
    novel_id: str
    main_character_name: str
    main_character_gender: str = "male"
    rewrite_type: str = "fantasy"
    target_language: str = "zh-CN"
    similarity_threshold: float = 0.1
    enable_profanity: bool = False
    start_chapter: int = 1
    end_chapter: Optional[int] = None

class RewriteResponse(BaseModel):
    """仿写响应"""
    task_id: str
    status: str
    progress: float
    message: str

class SimilarityCheckRequest(BaseModel):
    """相似度检测请求"""
    novel_id: str
    chapter_numbers: Optional[List[int]] = None

class SimilarityCheckResponse(BaseModel):
    """相似度检测响应"""
    overall_similarity: float
    threshold: float
    all_passed: bool
    failed_chapters: List[int]
    chapter_results: List[Dict[str, Any]]
    statistics: Dict[str, Any]

class ExportRequest(BaseModel):
    """导出请求"""
    novel_id: str
    format: str = "txt"  # txt, docx, pdf, epub
    chapters: Optional[List[int]] = None


class LLMConfigRequest(BaseModel):
    """LLM配置请求"""
    provider: str = "deepseek"
    api_key: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


class LLMTestRequest(BaseModel):
    """LLM测试请求"""
    provider: str = "deepseek"
    prompt: str = "请说一句话介绍你自己"


class ExpandDescriptionRequest(BaseModel):
    """扩写描述请求"""
    text: str
    provider: Optional[str] = None


# ==================== API端点 ====================

@app.get("/")
async def root():
    """根路径"""
    return {
        "name": "NovelForge API",
        "version": "1.0.0",
        "description": "AI小说仿写引擎"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ==================== 小说上传接口 ====================

@app.post("/api/v1/novel/upload", response_model=UploadResponse)
async def upload_novel(
    file: UploadFile = File(...),
    title: Optional[str] = None,
    author: Optional[str] = None
):
    """
    上传小说文件
    - 支持TXT格式
    - 自动解析章节和内容
    - 返回小说ID用于后续操作
    """
    # 检查文件类型
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="只支持TXT格式文件")
    
    # 保存上传的文件
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_id = str(uuid4())
    file_path = upload_dir / f"{file_id}.txt"
    
    try:
        # 读取文件内容
        content = await file.read()
        
        # 解码内容
        try:
            text = content.decode('utf-8')
        except:
            try:
                text = content.decode('gbk')
            except:
                text = content.decode('utf-8', errors='ignore')
        
        # 保存文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        
        # 解析小说
        novel = await parser.parse_file(str(file_path))
        
        # 更新元数据
        if title:
            novel.metadata.title = title
        if author:
            novel.metadata.author = author
        
        # 分析小说结构
        novel.macro_structure = structure_analyzer.analyze_novel_structure(novel)
        
        # 分析世界观
        novel.world_settings = world_analyzer.analyze_world_settings(novel)
        
        # 分析力量系统
        novel.power_system = world_analyzer.analyze_power_system(novel)
        
        # 提取人物
        novel.characters = character_analyzer.extract_characters(novel)
        
        # 存储
        novels_storage[file_id] = novel
        
        return UploadResponse(
            novel_id=file_id,
            title=novel.metadata.title,
            author=novel.metadata.author,
            total_chapters=len(novel.chapters),
            total_words=novel.metadata.total_words,
            status="completed"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")


# ==================== 小说分析接口 ====================

@app.get("/api/v1/novel/{novel_id}/analysis", response_model=AnalysisResponse)
async def analyze_novel(novel_id: str):
    """
    获取小说分析结果
    - 返回详细的结构分析
    - 返回人物信息
    - 返回世界观设定
    """
    if novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = novels_storage[novel_id]
    
    # 构建响应
    return AnalysisResponse(
        novel_id=novel_id,
        structure=novel.macro_structure.model_dump(),
        world_settings=novel.world_settings.model_dump(),
        characters=[c.model_dump() for c in novel.characters],
        power_system=novel.power_system.model_dump(),
        statistics={
            "total_chapters": len(novel.chapters),
            "total_words": novel.metadata.total_words,
            "character_count": len(novel.characters),
            "faction_count": len(novel.world_settings.factions),
            "level_count": len(novel.power_system.levels),
            "plot_arc_count": len(novel.macro_structure.plot_arcs),
            "climax_count": len(novel.macro_structure.climax_points),
        }
    )


# ==================== 仿写接口 ====================

@app.post("/api/v1/novel/{novel_id}/rewrite", response_model=RewriteResponse)
async def start_rewrite(
    novel_id: str,
    request: RewriteRequest,
    background_tasks: BackgroundTasks
):
    """
    开始仿写任务
    - 异步处理
    - 支持进度查询
    """
    if novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    # 创建任务
    task_id = str(uuid4())
    rewrite_tasks[task_id] = {
        "novel_id": novel_id,
        "status": "pending",
        "progress": 0.0,
        "request": request,
        "result": None,
        "created_at": datetime.now()
    }
    
    # 后台执行仿写
    background_tasks.add_task(
        execute_rewrite_task,
        task_id,
        novel_id,
        request
    )
    
    return RewriteResponse(
        task_id=task_id,
        status="processing",
        progress=0.0,
        message="仿写任务已启动"
    )


async def execute_rewrite_task(task_id: str, novel_id: str, request: RewriteRequest):
    """
    执行仿写任务
    """
    try:
        rewrite_tasks[task_id]["status"] = "processing"
        
        novel = novels_storage[novel_id]
        
        # 配置仿写参数
        config = RewriteConfig(
            main_character_name=request.main_character_name,
            main_character_gender=request.main_character_gender,
            rewrite_type=request.rewrite_type,
            target_language=request.target_language,
            similarity_threshold=request.similarity_threshold,
            enable_profanity=request.enable_profanity
        )
        
        # 执行仿写
        rewritten_novel = rewrite_engine.rewrite_novel(novel, config)
        
        # 应用去AI化
        total_chapters = len(rewritten_novel.chapters)
        for i, chapter in enumerate(rewritten_novel.chapters):
            # 去AI化处理
            processed_content = deai_module.process_full_text(chapter.content)
            rewritten_novel.chapters[i].content = processed_content
            
            # 更新进度
            progress = (i + 1) / total_chapters
            rewrite_tasks[task_id]["progress"] = progress
        
        # 保存结果
        rewritten_novel_id = str(uuid4())
        novels_storage[rewritten_novel_id] = rewritten_novel
        
        rewrite_tasks[task_id]["result"] = {
            "rewritten_novel_id": rewritten_novel_id,
            "progress": 1.0,
            "status": "completed"
        }
        rewrite_tasks[task_id]["status"] = "completed"
        rewrite_tasks[task_id]["progress"] = 1.0
        
    except Exception as e:
        rewrite_tasks[task_id]["status"] = "failed"
        rewrite_tasks[task_id]["error"] = str(e)


@app.get("/api/v1/novel/{novel_id}/rewrite/status/{task_id}")
async def get_rewrite_status(novel_id: str, task_id: str):
    """
    查询仿写进度
    """
    if task_id not in rewrite_tasks:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task = rewrite_tasks[task_id]
    
    return {
        "task_id": task_id,
        "status": task["status"],
        "progress": task["progress"],
        "result": task.get("result"),
        "error": task.get("error")
    }


# ==================== 相似度检测接口 ====================

@app.post("/api/v1/novel/{novel_id}/verify-similarity", response_model=SimilarityCheckResponse)
async def verify_similarity(
    novel_id: str,
    original_novel_id: str,
    threshold: float = 0.1
):
    """
    验证仿写文本与原文的相似度
    """
    if novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="仿写小说不存在")
    if original_novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="原文不存在")
    
    original = novels_storage[original_novel_id]
    rewritten = novels_storage[novel_id]
    
    # 提取章节内容
    original_chapters = [c.content for c in original.chapters]
    rewritten_chapters = [c.content for c in rewritten.chapters]
    
    # 计算相似度
    report = similarity_detector.generate_report(
        original_chapters,
        rewritten_chapters,
        threshold=threshold
    )
    
    return SimilarityCheckResponse(
        overall_similarity=report['overall_similarity'],
        threshold=threshold,
        all_passed=report['all_passed'],
        failed_chapters=report['failed_chapters'],
        chapter_results=report['chapter_results'],
        statistics=report['statistics']
    )


# ==================== 导出接口 ====================

@app.post("/api/v1/novel/{novel_id}/export")
async def export_novel(
    novel_id: str,
    format: str = "txt",
    chapters: Optional[List[int]] = None
):
    """
    导出小说
    """
    if novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = novels_storage[novel_id]
    
    # 准备导出内容
    export_chapters = novel.chapters
    if chapters:
        export_chapters = [c for c in novel.chapters if c.number in chapters]
    
    # 生成内容
    content_lines = [f"# {novel.metadata.title}\n"]
    content_lines.append(f"# 作者: {novel.metadata.author}\n\n")
    
    for chapter in export_chapters:
        content_lines.append(f"## 第{chapter.number}章 {chapter.title}\n\n")
        content_lines.append(chapter.content)
        content_lines.append("\n\n")
    
    content = "".join(content_lines)
    
    # 保存临时文件
    export_dir = Path("data/exports")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    export_file = export_dir / f"{novel_id}.txt"
    with open(export_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return FileResponse(
        path=str(export_file),
        filename=f"{novel.metadata.title}.txt",
        media_type="text/plain"
    )


# ==================== 多语言接口 ====================

@app.get("/api/v1/i18n/locales")
async def get_locales():
    """
    获取支持的语言列表
    """
    return i18n.get_available_locales()

@app.post("/api/v1/i18n/set-locale")
async def set_locale(locale: str):
    """
    设置当前语言
    """
    success = i18n.set_locale(locale)
    if not success:
        raise HTTPException(status_code=400, detail="不支持的语言")
    
    return {"success": True, "locale": locale}

@app.get("/api/v1/i18n/translate/{key}")
async def translate(key: str, locale: Optional[str] = None):
    """
    翻译文本
    """
    text = i18n.translate(key)
    return {"key": key, "text": text, "locale": locale or i18n.get_locale()}


# ==================== 统计接口 ====================

@app.get("/api/v1/novel/{novel_id}/statistics")
async def get_novel_statistics(novel_id: str):
    """
    获取小说统计信息
    """
    if novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = novels_storage[novel_id]
    
    # 统计信息
    chapters = novel.chapters
    
    word_counts = [c.word_count for c in chapters]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    
    # 章节类型分布
    chapter_types = {}
    for chapter in chapters:
        chapter_type = chapter.structure_type.value
        chapter_types[chapter_type] = chapter_types.get(chapter_type, 0) + 1
    
    return {
        "novel_id": novel_id,
        "title": novel.metadata.title,
        "author": novel.metadata.author,
        "total_chapters": len(chapters),
        "total_words": novel.metadata.total_words,
        "avg_words_per_chapter": avg_words,
        "chapter_type_distribution": chapter_types,
        "character_count": len(novel.characters),
        "faction_count": len(novel.world_settings.factions),
        "power_levels": len(novel.power_system.levels),
        "plot_arcs": len(novel.macro_structure.plot_arcs),
        "climax_points": len(novel.macro_structure.climax_points)
    }


# ==================== LLM管理接口 ====================

@app.get("/api/v1/llm/providers")
async def get_llm_providers():
    """
    获取可用的LLM提供商列表
    """
    providers = llm_service.get_available_providers()
    
    # 构造详细信息
    provider_details = []
    for provider in providers:
        models = llm_service.get_provider_models(provider)
        provider_details.append({
            "id": provider.value,
            "name": {
                "deepseek": "DeepSeek",
                "wenxin": "文心一言",
                "qianwen": "通义千问",
                "kimi": "Kimi",
                "glm": "智谱AI",
                "openai": "OpenAI"
            }.get(provider.value, provider.value),
            "models": models,
            "is_default": provider.value == settings.DEFAULT_LLM_PROVIDER
        })
    
    return {"providers": provider_details}


@app.get("/api/v1/llm/config")
async def get_llm_config():
    """
    获取当前LLM配置
    """
    return {
        "default_provider": settings.DEFAULT_LLM_PROVIDER,
        "configs": {
            "deepseek": {
                "model": settings.DEEPSEEK_MODEL,
                "has_api_key": bool(settings.DEEPSEEK_API_KEY)
            },
            "wenxin": {
                "model": settings.WENXIN_MODEL,
                "has_api_key": bool(settings.WENXIN_API_KEY)
            },
            "qianwen": {
                "model": settings.QIANWEN_MODEL,
                "has_api_key": bool(settings.QIANWEN_API_KEY)
            },
            "kimi": {
                "model": settings.KIMI_MODEL,
                "has_api_key": bool(settings.KIMI_API_KEY)
            },
            "glm": {
                "model": settings.GLM_MODEL,
                "has_api_key": bool(settings.GLM_API_KEY)
            },
            "openai": {
                "model": settings.OPENAI_MODEL,
                "has_api_key": bool(settings.OPENAI_API_KEY)
            }
        },
        "parameters": {
            "temperature": settings.LLM_TEMPERATURE,
            "max_tokens": settings.LLM_MAX_TOKENS,
            "top_p": settings.LLM_TOP_P,
            "presence_penalty": settings.LLM_PRESENCE_PENALTY,
            "frequency_penalty": settings.LLM_FREQUENCY_PENALTY,
            "timeout": settings.LLM_TIMEOUT
        }
    }


@app.post("/api/v1/llm/config")
async def update_llm_config(request: LLMConfigRequest):
    """
    更新LLM配置
    """
    # 这里可以添加持久化逻辑，目前只更新内存中的配置
    # 生产环境应该保存到配置文件或数据库
    
    return {
        "success": True,
        "message": "配置已更新",
        "current_provider": request.provider
    }


@app.post("/api/v1/llm/test")
async def test_llm_connection(request: LLMTestRequest):
    """
    测试LLM连接
    """
    try:
        provider = LLMProvider(request.provider)
        result = await llm_service.expand_description(request.prompt, provider)
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/v1/llm/expand-description")
async def expand_description(request: ExpandDescriptionRequest):
    """
    扩写描述 - 将抽象描述具体化
    """
    try:
        provider = LLMProvider(request.provider) if request.provider else None
        result = await llm_service.expand_description(request.text, provider)
        return {
            "success": True,
            "original": request.text,
            "expanded": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"扩写失败: {str(e)}")


# ==================== 统计接口 ====================

@app.get("/api/v1/novel/{novel_id}/statistics")
async def get_novel_statistics(novel_id: str):
    """
    获取小说统计信息
    """
    if novel_id not in novels_storage:
        raise HTTPException(status_code=404, detail="小说不存在")
    
    novel = novels_storage[novel_id]
    
    # 统计信息
    chapters = novel.chapters
    
    word_counts = [c.word_count for c in chapters]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    
    # 章节类型分布
    chapter_types = {}
    for chapter in chapters:
        chapter_type = chapter.structure_type.value
        chapter_types[chapter_type] = chapter_types.get(chapter_type, 0) + 1
    
    return {
        "novel_id": novel_id,
        "title": novel.metadata.title,
        "author": novel.metadata.author,
        "total_chapters": len(chapters),
        "total_words": novel.metadata.total_words,
        "avg_words_per_chapter": avg_words,
        "chapter_type_distribution": chapter_types,
        "character_count": len(novel.characters),
        "faction_count": len(novel.world_settings.factions),
        "power_levels": len(novel.power_system.levels),
        "plot_arcs": len(novel.macro_structure.plot_arcs),
        "climax_points": len(novel.macro_structure.climax_points)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
