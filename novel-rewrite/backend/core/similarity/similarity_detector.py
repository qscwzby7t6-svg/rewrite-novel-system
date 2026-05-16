# 相似度检测模块
# 用于检测仿写文本与原文的相似度，确保相似度低于10%

from typing import List, Dict, Tuple, Optional
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import jieba

class SimilarityDetector:
    """相似度检测器"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            token_pattern=r'(?u)\b\w+\b'  # 包含单字
        )
        
        # 相似度阈值
        self.threshold = 0.1  # 10%
        
        # 分词器
        jieba.initialize()
    
    def calculate_similarity(
        self,
        original: str,
        rewritten: str,
        method: str = 'combined'
    ) -> float:
        """
        计算两个文本的相似度
        Args:
            original: 原文
            rewritten: 仿写文本
            method: 计算方法 ('jaccard', 'cosine', 'combined')
        Returns:
            相似度分数 (0-1)
        """
        if method == 'jaccard':
            return self._jaccard_similarity(original, rewritten)
        elif method == 'cosine':
            return self._cosine_similarity(original, rewritten)
        elif method == 'combined':
            # 综合多种方法
            jaccard = self._jaccard_similarity(original, rewritten)
            cosine = self._cosine_similarity(original, rewritten)
            ngram = self._ngram_similarity(original, rewritten)
            
            # 加权平均
            return (jaccard * 0.3 + cosine * 0.4 + ngram * 0.3)
        else:
            return self._cosine_similarity(original, rewritten)
    
    def _tokenize(self, text: str) -> set:
        """
        分词
        """
        words = set(jieba.cut(text))
        # 过滤停用词和单字
        stopwords = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        words = {w for w in words if w not in stopwords and len(w) >= 2}
        return words
    
    def _jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Jaccard相似度 - 基于词集合
        """
        words1 = self._tokenize(text1)
        words2 = self._tokenize(text2)
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union)
    
    def _cosine_similarity(self, text1: str, text2: str) -> float:
        """
        余弦相似度 - 基于TF-IDF向量
        """
        try:
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def _ngram_similarity(self, text1: str, text2: str, n: int = 3) -> float:
        """
        N-gram相似度
        """
        ngrams1 = self._get_ngrams(text1, n)
        ngrams2 = self._get_ngrams(text2, n)
        
        if not ngrams1 or not ngrams2:
            return 0.0
        
        intersection = ngrams1 & ngrams2
        union = ngrams1 | ngrams2
        
        return len(intersection) / len(union)
    
    def _get_ngrams(self, text: str, n: int) -> set:
        """
        获取N-gram
        """
        text = re.sub(r'[^\w]', '', text)  # 去除标点
        ngrams = set()
        
        for i in range(len(text) - n + 1):
            ngrams.add(text[i:i+n])
        
        return ngrams
    
    def calculate_chapter_similarities(
        self,
        original_chapters: List[str],
        rewritten_chapters: List[str]
    ) -> List[Dict[str, any]]:
        """
        计算每章的相似度
        Returns:
            [{'chapter': 1, 'similarity': 0.08, 'passed': True, 'details': {...}}, ...]
        """
        results = []
        
        for i, (orig, rew) in enumerate(zip(original_chapters, rewritten_chapters)):
            similarity = self.calculate_similarity(orig, rew)
            
            # 详细分析
            details = self._analyze_differences(orig, rew)
            
            results.append({
                'chapter': i + 1,
                'similarity': similarity,
                'passed': similarity < self.threshold,
                'details': details
            })
        
        return results
    
    def _analyze_differences(self, original: str, rewritten: str) -> Dict[str, any]:
        """
        分析两个文本的具体差异
        """
        # 提取关键信息
        orig_chars = set(original)
        rew_chars = set(rewritten)
        
        orig_words = self._tokenize(original)
        rew_words = self._tokenize(rewritten)
        
        return {
            'original_length': len(original),
            'rewritten_length': len(rewritten),
            'length_ratio': len(rewritten) / max(len(original), 1),
            'common_chars': len(orig_chars & rew_chars),
            'common_words': len(orig_words & rew_words),
            'unique_to_original': len(orig_words - rew_words),
            'unique_to_rewritten': len(rew_words - orig_words),
        }
    
    def verify_threshold(
        self,
        similarities: List[float],
        threshold: float = 0.1
    ) -> Tuple[bool, List[int]]:
        """
        验证所有章节是否满足相似度阈值
        Returns:
            (是否全部通过, 不合格的章节列表)
        """
        failed_chapters = [
            i + 1 for i, sim in enumerate(similarities)
            if sim >= threshold
        ]
        
        return (len(failed_chapters) == 0, failed_chapters)
    
    def generate_report(
        self,
        original_chapters: List[str],
        rewritten_chapters: List[str],
        threshold: float = 0.1
    ) -> Dict[str, any]:
        """
        生成完整的相似度检测报告
        """
        chapter_results = self.calculate_chapter_similarities(
            original_chapters,
            rewritten_chapters
        )
        
        similarities = [r['similarity'] for r in chapter_results]
        
        # 计算总体统计
        overall_similarity = np.mean(similarities)
        max_similarity = np.max(similarities)
        min_similarity = np.min(similarities)
        
        all_passed, failed_chapters = self.verify_threshold(similarities, threshold)
        
        # 按相似度排序，找出最相似的章节
        sorted_results = sorted(
            zip(range(1, len(similarities) + 1), similarities),
            key=lambda x: x[1],
            reverse=True
        )
        most_similar = sorted_results[:3]  # 前3个最相似的
        
        return {
            'overall_similarity': overall_similarity,
            'max_similarity': max_similarity,
            'min_similarity': min_similarity,
            'threshold': threshold,
            'all_passed': all_passed,
            'failed_chapters': failed_chapters,
            'chapter_count': len(similarities),
            'passed_count': len(similarities) - len(failed_chapters),
            'failed_count': len(failed_chapters),
            'chapter_results': chapter_results,
            'most_similar_chapters': most_similar,
            'statistics': {
                'mean': float(overall_similarity),
                'median': float(np.median(similarities)),
                'std': float(np.std(similarities)),
                'variance': float(np.var(similarities))
            }
        }
    
    def find_high_similarity_segments(
        self,
        original: str,
        rewritten: str,
        min_length: int = 50,
        similarity_threshold: float = 0.3
    ) -> List[Dict[str, any]]:
        """
        找出高相似度的段落
        """
        # 分段比较
        segment_length = 200  # 每段200字
        
        segments = []
        
        for i in range(0, len(original) - segment_length, segment_length // 2):
            orig_segment = original[i:i + segment_length]
            
            # 在rewritten中找到最相似的段落
            best_similarity = 0
            best_match_pos = 0
            
            for j in range(0, len(rewritten) - segment_length, segment_length // 2):
                rew_segment = rewritten[j:j + segment_length]
                sim = self._jaccard_similarity(orig_segment, rew_segment)
                
                if sim > best_similarity:
                    best_similarity = sim
                    best_match_pos = j
            
            if best_similarity > similarity_threshold:
                segments.append({
                    'original_position': i,
                    'rewritten_position': best_match_pos,
                    'original_text': orig_segment[:100],
                    'similarity': best_similarity
                })
        
        return segments
    
    def check_plagiarism_risk(
        self,
        original: str,
        rewritten: str
    ) -> Dict[str, any]:
        """
        检查抄袭风险
        """
        # 直接引用检测
        direct_quotes = self._find_direct_quotes(original, rewritten)
        
        # 复制粘贴检测
        copied_segments = self._find_copied_segments(original, rewritten)
        
        # 计算风险等级
        risk_factors = len(direct_quotes) + len(copied_segments)
        
        if risk_factors == 0:
            risk_level = 'low'
        elif risk_factors < 3:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'risk_level': risk_level,
            'direct_quotes': direct_quotes,
            'copied_segments': copied_segments,
            'total_risk_factors': risk_factors,
            'recommendation': self._get_recommendation(risk_level)
        }
    
    def _find_direct_quotes(self, original: str, rewritten: str) -> List[str]:
        """
        找出直接引用
        """
        # 提取原文中的引号内容
        quote_pattern = r'["""]([^"""]+)["""]'
        original_quotes = re.findall(quote_pattern, original)
        
        found = []
        for quote in original_quotes:
            if len(quote) > 10 and quote in rewritten:
                found.append(quote)
        
        return found
    
    def _find_copied_segments(
        self,
        original: str,
        rewritten: str,
        min_segment_length: int = 50
    ) -> List[Dict[str, any]]:
        """
        找出复制粘贴的段落
        """
        copied = []
        
        # 检查连续的相似段落
        window_size = 100
        
        for i in range(0, len(original) - window_size, 10):
            segment = original[i:i + window_size]
            
            if segment in rewritten:
                copied.append({
                    'position': i,
                    'text': segment[:50],
                    'length': window_size
                })
        
        # 去重 - 合并相邻的复制段落
        if not copied:
            return []
        
        merged = [copied[0]]
        for seg in copied[1:]:
            if seg['position'] - merged[-1]['position'] < 20:
                merged[-1]['length'] = seg['position'] + seg['length'] - merged[-1]['position']
            else:
                merged.append(seg)
        
        return [m for m in merged if m['length'] >= min_segment_length]
    
    def _get_recommendation(self, risk_level: str) -> str:
        """
        根据风险等级给出建议
        """
        recommendations = {
            'low': '相似度控制在合理范围内，风险较低。',
            'medium': '存在一定的相似段落，建议进一步修改高相似度部分。',
            'high': '存在大量相似内容，需要大幅修改以降低风险。'
        }
        return recommendations.get(risk_level, '')
    
    def suggest_improvements(
        self,
        original: str,
        rewritten: str,
        high_similarity_segments: List[Dict]
    ) -> List[str]:
        """
        给出改进建议
        """
        suggestions = []
        
        if high_similarity_segments:
            suggestions.append(
                f"发现{len(high_similarity_segments)}处高相似度段落，建议重写。"
            )
        
        # 检查句式重复
        orig_sentences = re.split(r'[。！？]', original)
        rew_sentences = re.split(r'[。！？]', rewritten)
        
        if len(rew_sentences) < len(orig_sentences) * 0.8:
            suggestions.append("仿写文本字数偏少，建议适当扩充内容。")
        elif len(rew_sentences) > len(orig_sentences) * 1.2:
            suggestions.append("仿写文本字数偏多，建议适当精简。")
        
        # 检查关键情节是否过于相似
        plot_keywords = ['突然', '然而', '但是', '所以', '因为']
        keyword_count = sum(1 for kw in plot_keywords if kw in rewritten)
        
        if keyword_count > 10:
            suggestions.append(
                "某些关键词使用过于频繁，建议增加同义词替换。"
            )
        
        return suggestions
