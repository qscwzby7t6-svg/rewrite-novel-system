# 反AI检测和去AI化模块
# 用于消除AI生成文本的痕迹，使文本更加自然

from typing import List, Dict, Set, Tuple
import re
import random
from collections import Counter

class DeAIModule:
    """去AI化模块"""
    
    def __init__(self):
        # AI写作特征模式
        self.ai_patterns = {
            # 过度规律的句子开头
            'regular_starts': [
                '首先', '其次', '最后', '第一', '第二', '第三',
                '一方面', '另一方面', '总的来说', '总之'
            ],
            
            # 过度使用的连接词
            'overused_connectors': [
                '因此', '所以', '然而', '但是', '不过', '然而',
                '与此同时', '值得注意的是', '毋庸置疑'
            ],
            
            # 过度流畅的过渡
            'smooth_transitions': [
                '随后', '紧接着', '在此之后', '与此同时',
                '毫无疑问', '显而易见', '不言而喻'
            ],
            
            # AI喜欢用的强调词
            'ai_emphasis': [
                '非常', '极其', '格外', '特别', '十分', '相当',
                '显著', '明显', '尤为', '至关重要'
            ],
            
            # 规律性的段落结构
            'patterned_structure': [
                r'^第\d+[章节段部分]',  # 规律的第X章开头
                r'^首先，',  # 规律的开头
                r'^其次，',  # 规律的开头
            ]
        }
        
        # 自然语言变化词库
        self.natural_variations = {
            '首先': ['开头的时候', '一开始', '最初', '最初的时候'],
            '其次': ['接下来', '然后', '之后', '接着'],
            '最后': ['到头来', '最终', '末了', '结束时'],
            '因此': ['于是', '这么一来', '所以', '故而'],
            '但是': ['不过', '只是', '然而', '可'],
            '非常': ['挺', '挺挺', '怪', '蛮', '相当'],
            '十分': ['很', '挺', '相当', '颇'],
            '显然': ['看样子', '看起来', '显然', '明显'],
        }
        
        # 人类写作的不规则性
        self.human_irregularities = [
            '（', '）', '——', '……', '——',
            '嗯', '啊', '哦', '呃', '唉',
            '哎呀', '这不', '话说', '说起来',
            '对了', '那个', '这个', '那个什么'
        ]
        
        # 口语化表达
        self.colloquial_expressions = {
            '思考': ['琢磨', '寻思', '想来想去', '暗暗思忖'],
            '说话': ['道', '说', '喊', '嚷', '念叨'],
            '看': ['瞅', '瞄', '瞥', '盯着看', '张望'],
            '走': ['迈步', '踱步', '溜达', '走过去'],
            '好': ['不错', '挺好', '蛮好', '还行'],
        }
    
    def detect_ai_patterns(self, text: str) -> List[Dict[str, any]]:
        """
        检测AI写作特征
        Returns:
            [{'pattern': '具体模式', 'count': 数量, 'positions': [位置列表]}, ...]
        """
        detected = []
        
        for category, patterns in self.ai_patterns.items():
            if isinstance(patterns, list):
                for pattern in patterns:
                    positions = []
                    for match in re.finditer(re.escape(pattern), text):
                        positions.append(match.start())
                    
                    if positions:
                        detected.append({
                            'category': category,
                            'pattern': pattern,
                            'count': len(positions),
                            'positions': positions
                        })
        
        return detected
    
    def remove_ai_patterns(self, text: str, strength: float = 0.7) -> str:
        """
        移除AI写作模式
        Args:
            text: 待处理文本
            strength: 强度 (0-1)，越高越激进
        Returns:
            处理后的文本
        """
        result = text
        
        # 1. 替换规律性开头
        result = self._replace_regular_starts(result)
        
        # 2. 替换过度使用的连接词
        result = self._replace_overused_connectors(result, strength)
        
        # 3. 添加自然的句子变化
        result = self._add_sentence_variation(result, strength)
        
        # 4. 打破规律段落结构
        result = self._break_patterned_structure(result)
        
        # 5. 添加人类写作的不规则性
        result = self._add_human_irregularities(result, strength)
        
        return result
    
    def _replace_regular_starts(self, text: str) -> str:
        """
        替换规律性的句子开头
        """
        result = text
        
        for ai_start, alternatives in self.natural_variations.items():
            pattern = rf'^({ai_start}[，,]?\s*)'
            matches = list(re.finditer(pattern, result, re.MULTILINE))
            
            # 替换一半
            for i, match in enumerate(matches):
                if i % 2 == 0:
                    replacement = random.choice(alternatives) + '，'
                    result = result[:match.start()] + replacement + result[match.end():]
        
        return result
    
    def _replace_overused_connectors(self, text: str, strength: float) -> str:
        """
        替换过度使用的连接词
        """
        result = text
        
        for connector, alternatives in self.natural_variations.items():
            count = result.count(connector)
            
            # 随机替换一部分
            replace_count = int(count * strength)
            
            for _ in range(replace_count):
                if connector in result:
                    pos = result.find(connector)
                    replacement = random.choice(alternatives)
                    result = result[:pos] + replacement + result[pos+len(connector):]
        
        return result
    
    def _add_sentence_variation(self, text: str, strength: float) -> str:
        """
        添加句子变化 - 打破AI的规律句式
        """
        sentences = re.split(r'([。！？])', text)
        varied_sentences = []
        
        for i, part in enumerate(sentences):
            if not part.strip():
                continue
            
            # 检查是否需要变化
            if len(part) > 15 and random.random() < strength * 0.3:
                # 添加插入语
                insertions = [
                    f'，说实话，',
                    f'，说真的，',
                    f'，没想到，',
                    f'，偏偏，',
                    f'，谁知道，',
                ]
                insertion = random.choice(insertions)
                
                # 在句子中间插入
                if len(part) > 20:
                    insert_pos = len(part) // 2
                    # 找到一个合适的断点
                    for p in range(insert_pos, len(part) - 5):
                        if part[p] in '，、':
                            part = part[:p+1] + insertion[1:] + part[p+1:]
                            break
            
            varied_sentences.append(part)
        
        return ''.join(varied_sentences)
    
    def _break_patterned_structure(self, text: str) -> str:
        """
        打破规律的段落结构
        """
        paragraphs = text.split('\n\n')
        varied_paragraphs = []
        
        for i, para in enumerate(paragraphs):
            # 随机跳过某些段落开头
            if para.strip():
                lines = para.split('\n')
                if len(lines) > 2:
                    # 随机打乱某些段落顺序
                    if random.random() > 0.7:
                        middle = lines[1:-1]
                        random.shuffle(middle)
                        lines = [lines[0]] + middle + [lines[-1]]
                        para = '\n'.join(lines)
                
                varied_paragraphs.append(para)
            else:
                varied_paragraphs.append(para)
        
        return '\n\n'.join(varied_paragraphs)
    
    def _add_human_irregularities(self, text: str, strength: float) -> str:
        """
        添加人类写作的不规则性
        """
        result = text
        
        # 添加次数
        num_insertions = int(len(text) / 500 * strength)
        
        for _ in range(num_insertions):
            # 选择插入位置
            insert_points = [i for i, c in enumerate(result) if c in '，。！？、']
            
            if insert_points:
                pos = random.choice(insert_points)
                
                # 选择插入内容
                if random.random() > 0.5:
                    # 括号内的补充
                    insertion = random.choice(['（其实）', '（不过）', '（说起来）', '（话说）'])
                else:
                    # 口语化表达
                    insertion = random.choice(['嗯，', '啊，', '哦，', '这个，', '那个，'])
                
                result = result[:pos+1] + insertion + result[pos+1:]
        
        return result
    
    def add_appropriate_errors(self, text: str, error_rate: float = 0.05) -> str:
        """
        添加适当的"错误"，模拟人类写作
        """
        result = text
        chars = list(result)
        
        # 随机修改一些字符
        for i in range(len(chars)):
            if random.random() < error_rate:
                char = chars[i]
                
                # 同音替换
                homophone_map = {
                    '在': '再',
                    '的': '得',
                    '地': '的',
                    '做': '作',
                    '像': '向',
                }
                
                if char in homophone_map and random.random() > 0.5:
                    chars[i] = homophone_map[char]
        
        return ''.join(chars)
    
    def adjust_reading_level(self, text: str, target_level: str = 'mixed') -> str:
        """
        调整阅读水平，使其更加自然
        """
        result = text
        
        # 替换过度书面的词汇
        formal_to_informal = {
            '然而': '不过',
            '因此': '所以',
            '若干': '几个',
            '立即': '马上',
            '似乎': '好像',
            '由于': '因为',
            '关于': '对于',
        }
        
        for formal, informal in formal_to_informal.items():
            if random.random() > 0.5:
                result = result.replace(formal, informal)
        
        return result
    
    def introduce_narrative_breaks(self, text: str, break_rate: float = 0.1) -> str:
        """
        引入叙述性停顿，模拟人类写作的自然节奏
        """
        result = text
        
        breaks = [
            '\n——\n',
            '\n\n',
            '……',
            '——',
        ]
        
        # 在合适的位置添加停顿
        pause_points = []
        for i, char in enumerate(result):
            if char in '，。！？' and random.random() < break_rate:
                pause_points.append(i)
        
        for pos in pause_points:
            if result[pos+1:pos+3] not in ['——', '……', '\n']:
                insert = random.choice(breaks[:2])
                result = result[:pos+1] + insert + result[pos+1:]
        
        return result
    
    def process_full_text(self, text: str, config: Dict[str, any] = None) -> str:
        """
        完整的去AI化处理流程
        """
        if config is None:
            config = {
                'strength': 0.7,
                'add_errors': True,
                'error_rate': 0.02,
                'adjust_reading_level': True,
                'introduce_breaks': True,
                'break_rate': 0.1
            }
        
        result = text
        
        # 1. 检测AI模式
        patterns = self.detect_ai_patterns(result)
        
        # 2. 移除AI模式
        result = self.remove_ai_patterns(result, config['strength'])
        
        # 3. 添加句子变化
        result = self._add_sentence_variation(result, config['strength'])
        
        # 4. 调整阅读水平
        if config.get('adjust_reading_level', True):
            result = self.adjust_reading_level(result)
        
        # 5. 添加适当的错误
        if config.get('add_errors', True):
            result = self.add_appropriate_errors(result, config.get('error_rate', 0.02))
        
        # 6. 引入叙述停顿
        if config.get('introduce_breaks', True):
            result = self.introduce_narrative_breaks(result, config.get('break_rate', 0.1))
        
        # 7. 最终检查和清理
        result = self._cleanup_text(result)
        
        return result
    
    def _cleanup_text(self, text: str) -> str:
        """
        清理文本，移除可能的异常
        """
        # 移除连续的空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 移除连续的特殊符号
        text = re.sub(r'[——]{3,}', '——', text)
        
        # 修复可能的断句问题
        text = re.sub(r'([^\n])正好([^\n])', r'\1，恰好\2', text)
        
        return text
    
    def get_deai_report(self, original: str, processed: str) -> Dict[str, any]:
        """
        生成去AI化处理报告
        """
        original_patterns = self.detect_ai_patterns(original)
        processed_patterns = self.detect_ai_patterns(processed)
        
        original_count = sum(p['count'] for p in original_patterns)
        processed_count = sum(p['count'] for p in processed_patterns)
        
        reduction = (original_count - processed_count) / max(original_count, 1) * 100
        
        return {
            'original_ai_patterns': original_count,
            'processed_ai_patterns': processed_count,
            'reduction_percentage': reduction,
            'patterns_detected': len(original_patterns),
            'patterns_removed': len(original_patterns) - len(processed_patterns)
        }
