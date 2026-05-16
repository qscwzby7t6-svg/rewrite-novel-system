// NovelForge - 分析页面

import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useNovelAnalysis } from '../hooks/useNovel';
import { motion } from 'framer-motion';

const AnalysisPage: React.FC = () => {
  const { novelId } = useParams<{ novelId: string }>();
  const { data: analysis, isLoading } = useNovelAnalysis(novelId || '');

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4" />
          <p className="text-gray-400">正在分析小说...</p>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="text-center py-20">
        <p className="text-gray-400">未找到小说分析结果</p>
        <Link to="/upload" className="btn btn-primary mt-4">
          返回上传
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">小说分析结果</h1>
        <p className="text-gray-400">详细的结构分析和世界观解析</p>
      </motion.div>

      {/* 统计概览 */}
      <div className="grid md:grid-cols-4 gap-4 mb-8">
        <div className="card text-center">
          <div className="text-4xl font-bold text-purple-400">{analysis.statistics.total_chapters}</div>
          <div className="text-gray-400 mt-2">总章节数</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-blue-400">{analysis.statistics.total_words}</div>
          <div className="text-gray-400 mt-2">总字数</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-pink-400">{analysis.statistics.character_count}</div>
          <div className="text-gray-400 mt-2">人物数量</div>
        </div>
        <div className="card text-center">
          <div className="text-4xl font-bold text-green-400">{analysis.statistics.faction_count}</div>
          <div className="text-gray-400 mt-2">势力数量</div>
        </div>
      </div>

      {/* 结构分析 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold mb-4">📖 结构分析</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">结构类型</h3>
            <p className="text-gray-400">{analysis.structure.structure_type}</p>
          </div>
          <div>
            <h3 className="font-semibold mb-2">情节线</h3>
            <div className="space-y-2">
              {analysis.structure.plot_arcs?.slice(0, 5).map((arc: any, i: number) => (
                <div key={i} className="bg-black/30 rounded-lg p-3">
                  <div className="font-medium">{arc.name}</div>
                  <div className="text-sm text-gray-400">{arc.description}</div>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h3 className="font-semibold mb-2">高潮点</h3>
            <p className="text-gray-400">
              共 {analysis.structure.climax_points?.length || 0} 个高潮点
            </p>
          </div>
        </div>
      </motion.div>

      {/* 人物分析 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold mb-4">👥 人物分析</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {analysis.characters?.slice(0, 9).map((char: any, i: number) => (
            <div key={i} className="bg-black/30 rounded-lg p-4">
              <div className="font-semibold text-lg mb-2">{char.name}</div>
              <div className="text-sm space-y-1">
                <div className="text-gray-400">
                  性格: {char.personality_traits?.slice(0, 3).join(', ') || '未知'}
                </div>
                <div className="text-gray-400">
                  出场: 第{char.first_appearance_chapter}章
                </div>
                <div className="text-gray-400">
                  关系: {Object.keys(char.relationships || {}).slice(0, 2).join(', ') || '暂无'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* 世界观分析 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold mb-4">🌍 世界观设定</h2>
        <div className="space-y-6">
          <div>
            <h3 className="font-semibold mb-2">地理环境</h3>
            <div className="flex flex-wrap gap-2">
              {Object.keys(analysis.world_settings?.geography || {}).slice(0, 8).map((loc, i) => (
                <span key={i} className="tag">{loc}</span>
              ))}
            </div>
          </div>
          <div>
            <h3 className="font-semibold mb-2">势力分布</h3>
            <div className="grid md:grid-cols-2 gap-3">
              {analysis.world_settings?.factions?.slice(0, 6).map((faction: any, i: number) => (
                <div key={i} className="bg-black/30 rounded-lg p-3">
                  <div className="font-medium">{faction.name}</div>
                  <div className="text-sm text-gray-400">{faction.type}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* 力量系统 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card mb-8"
      >
        <h2 className="text-2xl font-bold mb-4">⚔️ 力量系统</h2>
        <div className="space-y-4">
          <div>
            <h3 className="font-semibold mb-2">力量等级</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.power_system?.levels?.map((level: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full text-sm">
                  {level}
                </span>
              ))}
            </div>
          </div>
          <div>
            <h3 className="font-semibold mb-2">修炼方法</h3>
            <div className="flex flex-wrap gap-2">
              {analysis.power_system?.cultivation_methods?.slice(0, 8).map((method: string, i: number) => (
                <span key={i} className="tag">{method}</span>
              ))}
            </div>
          </div>
        </div>
      </motion.div>

      {/* 开始仿写按钮 */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="text-center"
      >
        <Link
          to={`/rewrite/${novelId}`}
          className="btn btn-primary text-lg px-12 py-4"
        >
          ✨ 开始仿写
        </Link>
      </motion.div>
    </div>
  );
};

export default AnalysisPage;
