// NovelForge - 仿写页面

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useRewriteNovel, useRewriteStatus } from '../hooks/useNovel';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';

const RewritePage: React.FC = () => {
  const { novelId } = useParams<{ novelId: string }>();
  const navigate = useNavigate();
  const rewriteMutation = useRewriteNovel();
  
  const [config, setConfig] = useState({
    main_character_name: '李明',
    main_character_gender: 'male',
    rewrite_type: 'fantasy',
    target_language: 'zh-CN',
    similarity_threshold: 0.1,
    enable_profanity: false,
    start_chapter: 1,
    end_chapter: undefined as number | undefined,
  });

  const [taskId, setTaskId] = useState<string | null>(null);
  const [isRewriting, setIsRewriting] = useState(false);
  
  // 轮询进度
  const { data: status } = useRewriteStatus(novelId || '', taskId || '');

  useEffect(() => {
    if (status?.status === 'completed') {
      toast.success('仿写完成！');
      if (status.result?.rewritten_novel_id) {
        navigate(`/result/${status.result.rewritten_novel_id}`);
      }
      setIsRewriting(false);
    } else if (status?.status === 'failed') {
      toast.error('仿写失败: ' + status.error);
      setIsRewriting(false);
    }
  }, [status, navigate]);

  const handleStartRewrite = async () => {
    if (!novelId) return;
    
    if (!config.main_character_name) {
      toast.error('请输入主角名字');
      return;
    }

    setIsRewriting(true);
    setTaskId(null);

    try {
      const result = await rewriteMutation.mutateAsync({
        novel_id: novelId,
        ...config,
      });
      
      setTaskId(result.task_id);
      toast.success('仿写任务已启动');
    } catch (error) {
      toast.error('启动失败');
      setIsRewriting(false);
    }
  };

  const rewriteTypes = [
    { value: 'fantasy', label: '玄幻' },
    { value: 'xianxia', label: '仙侠' },
    { value: 'urban', label: '都市' },
    { value: 'sci_fi', label: '科幻' },
    { value: 'game', label: '游戏' },
    { value: 'history', label: '历史' },
  ];

  const languages = [
    { value: 'zh-CN', label: '简体中文' },
    { value: 'zh-TW', label: '繁體中文' },
    { value: 'en-US', label: 'English' },
    { value: 'ja-JP', label: '日本語' },
  ];

  return (
    <div className="max-w-5xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl font-bold mb-4 gradient-text">开始仿写</h1>
        <p className="text-gray-400">配置仿写参数，启动智能仿写引擎</p>
      </motion.div>

      <div className="space-y-6">
        {/* 基础配置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-6">基础配置</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">
                主角名字 <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                className="input"
                placeholder="输入新主角的名字"
                value={config.main_character_name}
                onChange={(e) => setConfig({ ...config, main_character_name: e.target.value })}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-2">主角性别</label>
              <select
                className="select"
                value={config.main_character_gender}
                onChange={(e) => setConfig({ ...config, main_character_gender: e.target.value })}
              >
                <option value="male">男</option>
                <option value="female">女</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">仿写类型</label>
              <select
                className="select"
                value={config.rewrite_type}
                onChange={(e) => setConfig({ ...config, rewrite_type: e.target.value })}
              >
                {rewriteTypes.map((type) => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">目标语言</label>
              <select
                className="select"
                value={config.target_language}
                onChange={(e) => setConfig({ ...config, target_language: e.target.value })}
              >
                {languages.map((lang) => (
                  <option key={lang.value} value={lang.value}>
                    {lang.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </motion.div>

        {/* 高级配置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-6">高级配置</h2>
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2">
                相似度阈值: {config.similarity_threshold * 100}%
              </label>
              <input
                type="range"
                min="0.05"
                max="0.2"
                step="0.01"
                className="w-full"
                value={config.similarity_threshold}
                onChange={(e) => setConfig({ ...config, similarity_threshold: parseFloat(e.target.value) })}
              />
              <p className="text-sm text-gray-400 mt-1">
                相似度必须低于此值，建议保持10%以下
              </p>
            </div>

            <div className="flex items-center gap-3">
              <input
                type="checkbox"
                id="enable_profanity"
                checked={config.enable_profanity}
                onChange={(e) => setConfig({ ...config, enable_profanity: e.target.checked })}
                className="w-5 h-5 rounded"
              />
              <label htmlFor="enable_profanity" className="text-sm font-medium">
                允许适当的脏话（仅在合适的情节中）
              </label>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">起始章节</label>
                <input
                  type="number"
                  className="input"
                  min="1"
                  value={config.start_chapter}
                  onChange={(e) => setConfig({ ...config, start_chapter: parseInt(e.target.value) })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">结束章节（留空则全部）</label>
                <input
                  type="number"
                  className="input"
                  min="1"
                  placeholder="全部章节"
                  value={config.end_chapter || ''}
                  onChange={(e) => setConfig({ 
                    ...config, 
                    end_chapter: e.target.value ? parseInt(e.target.value) : undefined 
                  })}
                />
              </div>
            </div>
          </div>
        </motion.div>

        {/* 进度显示 */}
        {isRewriting && status && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card"
          >
            <h2 className="text-xl font-bold mb-4">仿写进度</h2>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-gray-400">状态</span>
                <span className="font-semibold capitalize">{status.status}</span>
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-400">进度</span>
                  <span className="font-semibold">{Math.round(status.progress * 100)}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-bar-fill"
                    style={{ width: `${status.progress * 100}%` }}
                  />
                </div>
              </div>
            </div>
          </motion.div>
        )}

        {/* 开始按钮 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-center"
        >
          <button
            onClick={handleStartRewrite}
            disabled={isRewriting || !config.main_character_name}
            className="btn btn-primary text-lg px-12 py-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isRewriting ? (
              <>
                <div className="loading-spinner" />
                仿写中...
              </>
            ) : (
              '✨ 开始仿写'
            )}
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default RewritePage;
