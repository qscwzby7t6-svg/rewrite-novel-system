# 多语言支持模块
# 支持中文、英文、日文、韩文等多种语言的文本处理和界面国际化

from typing import Dict, List, Optional, Any
from enum import Enum
import gettext
import locale

class Language(str, Enum):
    """支持的语言枚举"""
    ZH_CN = "zh-CN"    # 简体中文
    ZH_TW = "zh-TW"    # 繁体中文
    EN_US = "en-US"    # 英语
    JA_JP = "ja-JP"    # 日语
    KO_KR = "ko-KR"    # 韩语

class I18nModule:
    """国际化模块"""
    
    def __init__(self, default_locale: str = "zh-CN"):
        self.current_locale = default_locale
        self.supported_locales = {
            "zh-CN": "简体中文",
            "zh-TW": "繁體中文",
            "en-US": "English",
            "ja-JP": "日本語",
            "ko-KR": "한국어"
        }
        
        # 翻译字典
        self.translations = self._load_translations()
    
    def _load_translations(self) -> Dict[str, Dict[str, str]]:
        """
        加载翻译字典
        """
        translations = {
            "zh-CN": {
                # 通用
                "app_name": "小说仿写工具",
                "welcome": "欢迎使用小说仿写工具",
                "loading": "加载中...",
                "error": "错误",
                "success": "成功",
                "cancel": "取消",
                "confirm": "确认",
                "save": "保存",
                "delete": "删除",
                "edit": "编辑",
                "close": "关闭",
                
                # 上传页面
                "upload_title": "上传小说",
                "upload_subtitle": "上传TXT格式的小说文件或输入书名",
                "select_file": "选择文件",
                "drag_drop": "或将文件拖放到此处",
                "book_title": "书名",
                "author": "作者",
                "file_type": "支持TXT格式",
                
                # 参数配置
                "config_title": "仿写配置",
                "main_character": "主角名字",
                "rewrite_type": "仿写类型",
                "target_language": "目标语言",
                "enable_profanity": "允许脏话",
                "similarity_threshold": "相似度阈值",
                
                # 仿写类型
                "type_fantasy": "玄幻",
                "type_xianxia": "仙侠",
                "type_urban": "都市",
                "type_scifi": "科幻",
                "type_game": "游戏",
                "type_history": "历史",
                "type_other": "其他",
                
                # 分析页面
                "analysis_title": "小说分析",
                "structure_analysis": "结构分析",
                "world_analysis": "世界观分析",
                "character_analysis": "人物分析",
                "power_analysis": "力量系统分析",
                
                # 仿写页面
                "rewrite_title": "开始仿写",
                "progress": "进度",
                "current_chapter": "当前章节",
                "estimated_time": "预计时间",
                "start_rewrite": "开始仿写",
                "pause": "暂停",
                "resume": "继续",
                "stop": "停止",
                
                # 结果页面
                "result_title": "仿写结果",
                "similarity_report": "相似度报告",
                "chapter_count": "章节数",
                "total_words": "总字数",
                "overall_similarity": "总体相似度",
                "export": "导出",
                "preview": "预览",
                
                # 验证
                "verification": "相似度验证",
                "verification_passed": "验证通过",
                "verification_failed": "验证失败",
                "similarity_too_high": "相似度过高，需要修改",
                
                # 错误信息
                "error_file_too_large": "文件过大，请上传小于100MB的文件",
                "error_invalid_format": "文件格式不正确，请上传TXT文件",
                "error_parse_failed": "文件解析失败",
                "error_network": "网络错误，请检查网络连接",
                
                # 统计
                "statistics": "统计信息",
                "chapters": "章节",
                "words": "字数",
                "characters": "人物",
                "factions": "势力",
                "levels": "等级",
            },
            "en-US": {
                # Common
                "app_name": "Novel Rewrite Tool",
                "welcome": "Welcome to Novel Rewrite Tool",
                "loading": "Loading...",
                "error": "Error",
                "success": "Success",
                "cancel": "Cancel",
                "confirm": "Confirm",
                "save": "Save",
                "delete": "Delete",
                "edit": "Edit",
                "close": "Close",
                
                # Upload page
                "upload_title": "Upload Novel",
                "upload_subtitle": "Upload TXT novel file or enter book title",
                "select_file": "Select File",
                "drag_drop": "or drag and drop file here",
                "book_title": "Book Title",
                "author": "Author",
                "file_type": "TXT format supported",
                
                # Config
                "config_title": "Rewrite Config",
                "main_character": "Main Character Name",
                "rewrite_type": "Rewrite Type",
                "target_language": "Target Language",
                "enable_profanity": "Enable Profanity",
                "similarity_threshold": "Similarity Threshold",
                
                # Rewrite types
                "type_fantasy": "Fantasy",
                "type_xianxia": "Xianxia",
                "type_urban": "Urban",
                "type_scifi": "Sci-Fi",
                "type_game": "Game",
                "type_history": "History",
                "type_other": "Other",
                
                # Analysis page
                "analysis_title": "Novel Analysis",
                "structure_analysis": "Structure Analysis",
                "world_analysis": "World Analysis",
                "character_analysis": "Character Analysis",
                "power_analysis": "Power System Analysis",
                
                # Rewrite page
                "rewrite_title": "Start Rewrite",
                "progress": "Progress",
                "current_chapter": "Current Chapter",
                "estimated_time": "Estimated Time",
                "start_rewrite": "Start Rewrite",
                "pause": "Pause",
                "resume": "Resume",
                "stop": "Stop",
                
                # Result page
                "result_title": "Rewrite Result",
                "similarity_report": "Similarity Report",
                "chapter_count": "Chapters",
                "total_words": "Total Words",
                "overall_similarity": "Overall Similarity",
                "export": "Export",
                "preview": "Preview",
                
                # Verification
                "verification": "Verification",
                "verification_passed": "Verification Passed",
                "verification_failed": "Verification Failed",
                "similarity_too_high": "Similarity too high, revision needed",
                
                # Errors
                "error_file_too_large": "File too large, please upload files under 100MB",
                "error_invalid_format": "Invalid file format, please upload TXT files",
                "error_parse_failed": "File parsing failed",
                "error_network": "Network error, please check connection",
                
                # Statistics
                "statistics": "Statistics",
                "chapters": "Chapters",
                "words": "Words",
                "characters": "Characters",
                "factions": "Factions",
                "levels": "Levels",
            },
            "ja-JP": {
                # 共通
                "app_name": "小説書き換えツール",
                "welcome": "小説書き換えツールへようこそ",
                "loading": "読み込み中...",
                "error": "エラー",
                "success": "成功",
                "cancel": "キャンセル",
                "confirm": "確認",
                "save": "保存",
                "delete": "削除",
                "edit": "編集",
                "close": "閉じる",
                
                # アップロードページ
                "upload_title": "小説をアップロード",
                "upload_subtitle": "TXT形式の小説ファイルをアップロードするか、タイトルを入力",
                "select_file": "ファイルを選択",
                "drag_drop": "またはここにファイルをドロップ",
                "book_title": "タイトル",
                "author": "著者",
                "file_type": "TXT形式をサポート",
                
                # 設定
                "config_title": "書き換え設定",
                "main_character": "主人公の名前",
                "rewrite_type": "書き換えタイプ",
                "target_language": "目標言語",
                "enable_profanity": "暴言を許可",
                "similarity_threshold": "類似度しきい値",
                
                # 書き換えタイプ
                "type_fantasy": "ファンタジー",
                "type_xianxia": "仙侠",
                "type_urban": "現代",
                "type_scifi": "SF",
                "type_game": "ゲーム",
                "type_history": "歴史",
                "type_other": "その他",
                
                # 分析ページ
                "analysis_title": "小説分析",
                "structure_analysis": "構造分析",
                "world_analysis": "世界観分析",
                "character_analysis": "キャラクター分析",
                "power_analysis": "力体系分析",
                
                # 書き換えページ
                "rewrite_title": "書き換え開始",
                "progress": "進捗",
                "current_chapter": "現在の章",
                "estimated_time": "予定時間",
                "start_rewrite": "書き換え開始",
                "pause": "一時停止",
                "resume": "再開",
                "stop": "停止",
                
                # 結果ページ
                "result_title": "書き換え結果",
                "similarity_report": "類似度レポート",
                "chapter_count": "章数",
                "total_words": "総文字数",
                "overall_similarity": "全体類似度",
                "export": "エクスポート",
                "preview": "プレビュー",
                
                # 検証
                "verification": "検証",
                "verification_passed": "検証合格",
                "verification_failed": "検証失敗",
                "similarity_too_high": "類似度が高すぎます、改訂が必要です",
                
                # エラー
                "error_file_too_large": "ファイルが大きすぎます、100MB以下のファイルをアップロードしてください",
                "error_invalid_format": "ファイル形式が無効です、TXTファイルをアップロードしてください",
                "error_parse_failed": "ファイルの解析に失敗しました",
                "error_network": "ネットワークエラー、接続を確認してください",
                
                # 統計
                "statistics": "統計情報",
                "chapters": "章",
                "words": "文字数",
                "characters": "キャラクター",
                "factions": "勢力",
                "levels": "レベル",
            }
        }
        
        return translations
    
    def set_locale(self, locale_code: str) -> bool:
        """
        设置当前语言
        """
        if locale_code in self.supported_locales:
            self.current_locale = locale_code
            return True
        return False
    
    def get_locale(self) -> str:
        """
        获取当前语言
        """
        return self.current_locale
    
    def get_available_locales(self) -> List[Dict[str, str]]:
        """
        获取所有可用的语言
        """
        return [
            {"code": code, "name": name}
            for code, name in self.supported_locales.items()
        ]
    
    def translate(self, key: str, **kwargs) -> str:
        """
        翻译文本
        Args:
            key: 翻译键
            **kwargs: 格式化参数
        Returns:
            翻译后的文本
        """
        # 首先尝试当前语言
        locale_trans = self.translations.get(self.current_locale, {})
        
        if key in locale_trans:
            text = locale_trans[key]
        else:
            # 回退到中文
            zh_trans = self.translations.get("zh-CN", {})
            text = zh_trans.get(key, key)
        
        # 格式化参数
        if kwargs:
            try:
                text = text.format(**kwargs)
            except:
                pass
        
        return text
    
    def get_text(self, key: str, locale: Optional[str] = None) -> str:
        """
        获取指定语言的翻译
        """
        target_locale = locale or self.current_locale
        
        locale_trans = self.translations.get(target_locale, {})
        return locale_trans.get(key, key)
    
    def format_number(self, num: float, locale: Optional[str] = None) -> str:
        """
        格式化数字
        """
        target_locale = locale or self.current_locale
        
        if target_locale.startswith("zh"):
            return f"{num:,.2f}"
        elif target_locale == "en-US":
            return f"{num:,.2f}"
        elif target_locale == "ja-JP":
            return f"{num:,.2f}"
        else:
            return f"{num:,.2f}"
    
    def format_date(self, date, locale: Optional[str] = None) -> str:
        """
        格式化日期
        """
        target_locale = locale or self.current_locale
        
        if target_locale == "zh-CN":
            return date.strftime("%Y年%m月%d日")
        elif target_locale == "zh-TW":
            return date.strftime("%Y年%m月%d日")
        elif target_locale == "en-US":
            return date.strftime("%Y-%m-%d")
        elif target_locale == "ja-JP":
            return date.strftime("%Y年%m月%d日")
        else:
            return date.strftime("%Y-%m-%d")
    
    def format_percentage(self, value: float, locale: Optional[str] = None) -> str:
        """
        格式化百分比
        """
        target_locale = locale or self.current_locale
        
        if target_locale.startswith("zh"):
            return f"{value * 100:.1f}%"
        else:
            return f"{value * 100:.1f}%"


class TextProcessor:
    """多语言文本处理器"""
    
    def __init__(self):
        self.processors = {
            "zh-CN": self._process_chinese,
            "zh-TW": self._process_chinese,
            "en-US": self._process_english,
            "ja-JP": self._process_japanese,
            "ko-KR": self._process_korean,
        }
    
    def process(self, text: str, language: str) -> str:
        """
        处理文本
        """
        processor = self.processors.get(language, self._process_chinese)
        return processor(text)
    
    def _process_chinese(self, text: str) -> str:
        """
        处理中文文本
        """
        import jieba
        
        # 简单清理
        text = text.strip()
        
        # jieba分词（仅用于分析，不改变原文）
        words = list(jieba.cut(text))
        
        return text
    
    def _process_english(self, text: str) -> str:
        """
        处理英文文本
        """
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        # 简单清理
        text = text.strip()
        
        # 分句
        sentences = nltk.sent_tokenize(text)
        
        return text
    
    def _process_japanese(self, text: str) -> str:
        """
        处理日文文本
        """
        # 简单清理
        text = text.strip()
        
        # 日文分词（使用简单规则）
        # 实际生产环境应使用专门的分词器如MeCab
        
        return text
    
    def _process_korean(self, text: str) -> str:
        """
        处理韩文文本
        """
        # 简单清理
        text = text.strip()
        
        # 韩文分词（使用简单规则）
        # 实际生产环境应使用专门的分词器
        
        return text
    
    def detect_language(self, text: str) -> str:
        """
        检测文本语言
        """
        if not text:
            return "zh-CN"
        
        # 检测中文字符
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        
        # 检测日文字符
        japanese_chars = len(re.findall(r'[\u3040-\u309f\u30a0-\u30ff]', text))
        
        # 检测韩文字符
        korean_chars = len(re.findall(r'[\uac00-\ud7af]', text))
        
        total_chars = len(text)
        
        if chinese_chars / total_chars > 0.3:
            return "zh-CN"
        elif japanese_chars / total_chars > 0.3:
            return "ja-JP"
        elif korean_chars / total_chars > 0.3:
            return "ko-KR"
        else:
            return "en-US"
    
    def tokenize(self, text: str, language: str) -> List[str]:
        """
        分词
        """
        if language.startswith("zh"):
            import jieba
            return list(jieba.cut(text))
        elif language == "en-US":
            import nltk
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
            return nltk.word_tokenize(text)
        else:
            # 其他语言使用简单分词
            return text.split()
    
    def count_words(self, text: str, language: str) -> int:
        """
        统计字数
        """
        if language.startswith("zh"):
            # 中文字符数
            return len(re.findall(r'[\u4e00-\u9fff]', text))
        else:
            # 英文单词数
            words = text.split()
            return len(words)


# 全局实例
i18n = I18nModule()
text_processor = TextProcessor()


def get_i18n() -> I18nModule:
    """获取国际化模块实例"""
    return i18n


def get_text_processor() -> TextProcessor:
    """获取文本处理器实例"""
    return text_processor
