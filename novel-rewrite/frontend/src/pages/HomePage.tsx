// NovelForge - 首页

import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const HomePage: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <section className="text-center py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="gradient-text">NovelForge</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
            智能小说仿写引擎 - 深度分析原版小说的宏观架构、章节结构、世界观、力量系统、人物性格，生成风格相似但内容原创的新小说
          </p>
          
          <div className="flex gap-4 justify-center">
            <Link to="/upload" className="btn btn-primary text-lg px-8 py-4">
              🚀 开始仿写
            </Link>
            <button className="btn btn-secondary text-lg px-8 py-4">
              了解更多
            </button>
          </div>
        </motion.div>
      </section>

      {/* Features Grid */}
      <section className="py-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          <span className="gradient-text">核心功能</span>
        </h2>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature 1 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="card"
          >
            <div className="w-12 h-12 bg-purple-600 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">📖</span>
            </div>
            <h3 className="text-xl font-semibold mb-3">深度结构分析</h3>
            <p className="text-gray-400">
              智能分析小说的宏观架构、章节结构、高潮分布、伏笔埋设，精准复刻原著框架
            </p>
          </motion.div>

          {/* Feature 2 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="card"
          >
            <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">🌍</span>
            </div>
            <h3 className="text-xl font-semibold mb-3">世界观复刻</h3>
            <p className="text-gray-400">
              完整提取并重建世界观设定、力量系统、地理环境、势力关系，保持原著风格
            </p>
          </motion.div>

          {/* Feature 3 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="card"
          >
            <div className="w-12 h-12 bg-pink-600 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">👥</span>
            </div>
            <h3 className="text-xl font-semibold mb-3">人物性格分析</h3>
            <p className="text-gray-400">
              精准识别人物性格特点、关系网络、成长弧线，确保角色塑造与原著一致
            </p>
          </motion.div>

          {/* Feature 4 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="card"
          >
            <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">✍️</span>
            </div>
            <h3 className="text-xl font-semibold mb-3">智能内容生成</h3>
            <p className="text-gray-400">
              AI引擎智能生成内容，支持打斗场景具体化、描述具体化、情节高潮控制
            </p>
          </motion.div>

          {/* Feature 5 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="card"
          >
            <div className="w-12 h-12 bg-yellow-600 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">🛡️</span>
            </div>
            <h3 className="text-xl font-semibold mb-3">去AI化处理</h3>
            <p className="text-gray-400">
              消除AI生成痕迹，添加自然语言变化，确保文本风格自然流畅
            </p>
          </motion.div>

          {/* Feature 6 */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
            className="card"
          >
            <div className="w-12 h-12 bg-red-600 rounded-xl flex items-center justify-center mb-4">
              <span className="text-2xl">⚖️</span>
            </div>
            <h3 className="text-xl font-semibold mb-3">相似度检测</h3>
            <p className="text-gray-400">
              严格控制相似度低于10%，逐章验证，确保仿写内容的原创性
            </p>
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16">
        <h2 className="text-3xl font-bold text-center mb-12">
          <span className="gradient-text">使用流程</span>
        </h2>
        
        <div className="grid md:grid-cols-4 gap-8">
          {[
            { step: 1, title: '上传小说', desc: '上传TXT格式小说文件', icon: '📁' },
            { step: 2, title: '智能分析', desc: '系统自动分析结构和人设', icon: '🔍' },
            { step: 3, title: '配置参数', desc: '设置主角名和仿写类型', icon: '⚙️' },
            { step: 4, title: '开始仿写', desc: '一键生成风格相似的新小说', icon: '✨' },
          ].map((item) => (
            <motion.div
              key={item.step}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: item.step * 0.1 }}
              className="text-center"
            >
              <div className="w-20 h-20 bg-gradient-to-br from-purple-600 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4 text-4xl">
                {item.icon}
              </div>
              <div className="text-3xl font-bold text-purple-400 mb-2">
                Step {item.step}
              </div>
              <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
              <p className="text-gray-400">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 text-center">
        <div className="card max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">
            准备好开始创作了吗？
          </h2>
          <p className="text-gray-400 mb-8 text-lg">
            上传您想要仿写的小说，AI将帮助您创作出风格相似但完全原创的新作品
          </p>
          <Link to="/upload" className="btn btn-primary text-lg px-12 py-4">
            🚀 立即开始
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
