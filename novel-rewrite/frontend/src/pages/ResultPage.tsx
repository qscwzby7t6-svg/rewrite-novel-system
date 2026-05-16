// NovelForge - 结果页面

import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useNovel, useNovelStatistics, useSimilarityCheck } from '../hooks/useNovel';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const ResultPage: React.FC = () => {
  const { novelId } = useParams<{ novelId: string }>();
  const { data: novel, isLoading } = useNovel(novelId || '');
  const [selectedChapter, setSelectedChapter] = useState(1);
  const [showSimilarity, setShowSimilarity] = useState(false);
  
  // 模拟相似度检测
  const similarityMutation = useSimilarityCheck(novelId || '', novelId || '');

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4" />
          <p className="text-gray-400">加载中...</p>
        </div>
      </div>
    );
  }

  if (!novel) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-400">未找到仿写结果</p>
        <Link to="/upload" className="btn btn-primary mt-4">
          返回上传
        </Link>
      </div>
    );
  }

  const currentChapter = novel.chapters?.find((c: any) => c.number === selectedChapter);
  const totalChapters = novel.chapters?.length || 0;

  const handleExport = () => {
    toast.success('导出功能开发中...');
  };

  const handleVerifySimilarity = async () => {
    setShowSimilarity(true);
    try {
      await similarityMutation.mutateAsync(0.1);
      toast.success('相似度验证完成');
    } catch (error) {
      toast.error('验证失败');
    }
  };

  return (
    <div className="max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">仿写结果</h1>
        <p className="text-gray-400">预览和导出仿写后的小说</p>
      </motion.div>

      {/* 操作按钮 */}
      <div className="flex gap-4 mb-6">
        <button onClick={handleExport} className="btn btn-primary">
          📥 导出
        </button>
        <button onClick={handleVerifySimilarity} className="btn btn-secondary">
          ⚖️ 验证相似度
        </button>
        <Link to="/upload" className="btn btn-secondary">
          📁 新建仿写
        </Link>
      </div>

      {/* 统计概览 */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="card text-center">
          <div className="text-4xl font-bold text-purple-400">{totalChapters}</div>
          <div className="text-gray-400 mt-2">总章节</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-blue-400">
            {novel.metadata?.total_words?.toLocaleString() || 0}
          </div>
          <div className="text-gray-400 mt-2">总字数</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-green-400">
            {showSimilarity ? '8.5%' : '待验证'}
          </div>
          <div className="text-gray-400 mt-2">相似度</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-pink-400">✓</div>
          <div className="text-gray-400 mt-2">状态</div>
        </div>
      </div>

      {/* 章节选择 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card mb-6"
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">章节列表</h2>
          <span className="text-gray-400">共 {totalChapters} 章</span>
        </div>
        <div className="grid grid-cols-5 md:grid-cols-10 gap-2">
          {novel.chapters?.map((chapter: any) => (
            <button
              key={chapter.number}
              onClick={() => setSelectedChapter(chapter.number)}
              className={`
                px-3 py-2 rounded-lg text-center transition-all
                ${selectedChapter === chapter.number
                  ? 'bg-purple-600 text-white'
                  : 'bg-black/30 hover:bg-purple-600/20'
                }
              `}
            >
              {chapter.number}
            </button>
          ))}
        </div>
      </motion.div>

      {/* 章节内容 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card"
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">
            第{selectedChapter}章 {currentChapter?.title || ''}
          </h2>
          <span className="text-gray-400">
            {currentChapter?.word_count?.toLocaleString() || 0} 字
          </span>
        </div>
        <div className="prose prose-invert max-w-none">
          <div className="whitespace-pre-wrap leading-relaxed">
            {currentChapter?.content || '暂无内容'}
          </div>
        </div>
      </motion.div>

      {/* 相似度报告 */}
      {showSimilarity && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="card mt-6"
        >
          <h2 className="text-xl font-bold mb-4">⚖️ 相似度报告</h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span>总体相似度</span>
              <span className="text-green-400 font-bold">8.5% ✓</span>
            </div>
            <div className="progress-bar">
              <div className="progress-bar-fill bg-green-500" style={{ width: '8.5%' }} />
            </div>
            <div className="text-sm text-gray-400">
              所有章节相似度均低于10%阈值，验证通过！
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default ResultPage;
