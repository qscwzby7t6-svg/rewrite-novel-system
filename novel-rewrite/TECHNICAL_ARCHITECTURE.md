# NovelForge 技术架构文档

## 1. 系统架构设计

### 1.1 整体架构
```
┌─────────────────────────────────────────────────────┐
│                  用户界面层 (Frontend)                │
│  React 18 + TypeScript + TailwindCSS               │
└────────────────────┬────────────────────────────────┘
                     │ HTTP/WebSocket
┌────────────────────▼────────────────────────────────┐
│                  API网关层 (API Gateway)            │
│  FastAPI + Uvicorn                                  │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                  业务逻辑层 (Services)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │文本解析  │ │结构分析  │ │仿写引擎  │            │
│  │服务      │ │服务      │ │服务      │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │人物分析  │ │去AI化    │ │相似度    │            │
│  │服务      │ │服务      │ │检测      │            │
│  └──────────┘ └──────────┘ └──────────┘            │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                  数据存储层 (Data Layer)             │
│  SQLite + File System + Redis Cache                 │
└─────────────────────────────────────────────────────┘
```

### 1.2 技术栈

#### 后端技术栈
- **框架**: FastAPI 0.104+
- **语言**: Python 3.11+
- **异步**: asyncio, aiofiles
- **数据库**: SQLite (本地), PostgreSQL (可选云端)
- **缓存**: Redis (可选)
- **AI接口**: OpenAI API, Claude API
- **文本处理**: 
  - nltk 3.8+
  - spaCy 3.7+
  - jieba (中文分词)
  - textblob
- **相似度检测**: 
  - scikit-learn
  - numpy
  - scipy

#### 前端技术栈
- **框架**: React 18+
- **语言**: TypeScript 5+
- **UI库**: TailwindCSS 3+
- **状态管理**: Zustand
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **路由**: React Router 6

### 1.3 核心模块设计

#### 2.1 文本解析模块 (TextParser)
```python
class TextParser:
    - parse_file(file_path: str) -> NovelDocument
    - detect_chapters(text: str) -> List[Chapter]
    - extract_metadata(text: str) -> NovelMetadata
    - split_sentences(text: str) -> List[str]
    - tokenize_chinese(text: str) -> List[str]
```

#### 2.2 结构分析模块 (StructureAnalyzer)
```python
class StructureAnalyzer:
    - analyze_macro_structure(novel: NovelDocument) -> MacroStructure
    - analyze_chapter_structure(chapter: Chapter) -> ChapterStructure
    - identify_plot_arcs(novel: NovelDocument) -> List[PlotArc]
    - detect_climax_points(novel: NovelDocument) -> List[ClimaxPoint]
    - extract_foreshadowing(novel: NovelDocument) -> List[Foreshadowing]
```

#### 2.3 世界观分析模块 (WorldBuilder)
```python
class WorldBuilder:
    - extract_world_settings(novel: NovelDocument) -> WorldSettings
    - analyze_power_system(novel: NovelDocument) -> PowerSystem
    - build_geography(novel: NovelDocument) -> Geography
    - map_factions(novel: NovelDocument) -> FactionMap
```

#### 2.4 人物分析模块 (CharacterAnalyzer)
```python
class CharacterAnalyzer:
    - extract_characters(novel: NovelDocument) -> List[Character]
    - analyze_relationships(novel: NovelDocument) -> RelationshipGraph
    - trace_growth_arcs(novel: NovelDocument) -> List[GrowthArc]
    - identify_character_traits(novel: NovelDocument) -> Dict[str, List[str]]
```

#### 2.5 仿写引擎模块 (RewriteEngine)
```python
class RewriteEngine:
    - rewrite_chapter(chapter: Chapter, config: RewriteConfig) -> Chapter
    - generate_scene(scene_type: str, context: Dict) -> Scene
    - generate_dialogue(character: Character, situation: str) -> Dialogue
    - generate_battle(battle_config: BattleConfig) -> BattleScene
    - concretize_abstract(description: str) -> str
```

#### 2.6 去AI化模块 (DeAIModule)
```python
class DeAIModule:
    - detect_ai_patterns(text: str) -> List[AIPattern]
    - add_natural_irregularity(text: str) -> str
    - inject_human_fluency(text: str) -> str
    - adjust_rhythm_and_pause(text: str) -> str
```

#### 2.7 相似度检测模块 (SimilarityDetector)
```python
class SimilarityDetector:
    - calculate_similarity(text1: str, text2: str) -> float
    - batch_check_similarity(original: List, rewritten: List) -> List[float]
    - verify_threshold(similarities: List[float], threshold: float) -> bool
    - generate_report(original: Novel, rewritten: Novel) -> Report
```

#### 2.8 多语言支持模块 (I18nModule)
```python
class I18nModule:
    - set_locale(locale: str) -> None
    - translate(key: str, **kwargs) -> str
    - get_available_locales() -> List[str]
    - format_number(num: float, locale: str) -> str
```

### 1.4 API接口设计

#### 3.1 文本上传接口
```
POST /api/v1/novel/upload
Content-Type: multipart/form-data

Request:
{
  "file": File,
  "main_character_name": "张伟",
  "rewrite_type": "玄幻",
  "target_language": "zh-CN"
}

Response:
{
  "novel_id": "uuid",
  "metadata": {
    "title": "小说标题",
    "author": "作者名",
    "total_chapters": 100,
    "total_words": 1000000
  },
  "analysis_status": "completed"
}
```

#### 3.2 仿写执行接口
```
POST /api/v1/novel/{novel_id}/rewrite
Request:
{
  "start_chapter": 1,
  "end_chapter": 10,
  "main_character_name": "李明",
  "similarity_threshold": 0.1
}

Response:
{
  "task_id": "uuid",
  "status": "processing",
  "progress": 0.3
}
```

#### 3.3 相似度检测接口
```
POST /api/v1/novel/{novel_id}/verify-similarity
Request:
{
  "chapter_numbers": [1, 2, 3, 5, 10]
}

Response:
{
  "verification_results": [
    {
      "chapter": 1,
      "similarity": 0.08,
      "passed": true
    }
  ],
  "overall_similarity": 0.07,
  "all_passed": true
}
```

### 1.5 数据模型

#### 4.1 小说数据模型
```python
class NovelDocument:
    id: UUID
    title: str
    author: str
    chapters: List[Chapter]
    metadata: NovelMetadata
    structure: MacroStructure
    world_settings: WorldSettings
    characters: List[Character]
    relationships: RelationshipGraph

class Chapter:
    number: int
    title: str
    content: str
    word_count: int
    structure_type: ChapterType
    scenes: List[Scene]

class Character:
    id: UUID
    name: str
    traits: List[str]
    appearance: str
    background: str
    growth_arc: GrowthArc
    relationships: Dict[str, RelationshipType]
```

### 1.6 安全与防侵权设计

#### 5.1 防侵权机制
1. **内容替换**
   - 自动替换所有人物名称
   - 自动替换地名和场景名
   - 生成全新的物品名称

2. **情节随机化**
   - 相同类型情节不同发展
   - 随机组合情节元素
   - 变化因果关系

3. **表述改写**
   - 同义词替换
   - 句式重构
   - 主动被动切换

4. **原创性验证**
   - 逐章相似度检测
   - 全文相似度检测
   - 段落级对比分析

#### 5.2 数据安全
- 本地处理优先
- 敏感数据加密存储
- 定期清理临时文件
- 操作日志审计

### 1.7 部署架构

#### 6.1 Docker部署
```yaml
# docker-compose.yml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/novel.db
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

#### 6.2 环境变量配置
```bash
# .env
DATABASE_URL=sqlite:///./data/novel.db
REDIS_URL=redis://localhost:6379
OPENAI_API_KEY=your-api-key
ANTHROPIC_API_KEY=your-api-key
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

---

## 2. 核心算法设计

### 2.1 文本相似度算法
- **Jaccard相似度**: 词集合相似度
- **余弦相似度**: TF-IDF向量相似度
- **句子嵌入相似度**: BERT语义相似度
- **综合评分**: 加权平均多维度评分

### 2.2 结构分析算法
- **HMM模型**: 章节类型识别
- **依存句法分析**: 句子关系分析
- **命名实体识别**: 人物/地点/组织识别
- **情感分析**: 情节情绪曲线

### 2.3 风格复刻算法
- **语言模型微调**: 基于原文风格训练
- **模板替换**: 结构化内容生成
- **增强生成**: 加入随机性和变化

---

## 3. 性能优化策略

### 3.1 文本处理优化
- 使用mmap映射大文件
- 分批处理文本块
- 多进程并行分析
- 缓存中间结果

### 3.2 内存优化
- 生成器替代列表
- 及时释放大对象
- 使用紧凑数据结构
- 分页加载数据

### 3.3 响应速度优化
- 异步I/O操作
- 增量处理结果
- 预加载下一个任务
- CDN加速静态资源

---

## 4. 测试策略

### 4.1 单元测试
- 每个模块独立测试
- Mock外部依赖
- 边界条件测试
- 异常处理测试

### 4.2 集成测试
- API端到端测试
- 工作流测试
- 性能基准测试
- 并发测试

### 4.3 用户验收测试
- 功能完整性测试
- 易用性测试
- 性能测试
- 安全性测试
