// NovelForge - 设置页面

import React from 'react';
import { motion } from 'framer-motion';
import { useI18n } from '../hooks/useNovel';

const SettingsPage: React.FC = () => {
  const { locale, setLocale, availableLocales } = useI18n();

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">设置</h1>
        <p className="text-gray-400">配置系统参数和偏好设置</p>
      </motion.div>

      <div className="space-y-6">
        {/* 语言设置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-4">🌐 语言设置</h2>
          <div className="space-y-3">
            {availableLocales.map((lang) => (
              <label
                key={lang.code}
                className="flex items-center gap-3 cursor-pointer p-3 rounded-lg hover:bg-white/5 transition-all"
              >
                <input
                  type="radio"
                  name="language"
                  value={lang.code}
                  checked={locale === lang.code}
                  onChange={() => setLocale(lang.code)}
                  className="w-5 h-5 accent-purple-600"
                />
                <span>{lang.name}</span>
              </label>
            ))}
          </div>
        </motion.div>

        {/* 仿写设置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-4">⚙️ 仿写默认设置</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">默认相似度阈值</label>
              <input
                type="number"
                className="input"
                defaultValue="0.1"
                step="0.01"
                min="0.05"
                max="0.2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">章节字数范围</label>
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="number"
                  className="input"
                  placeholder="最小"
                  defaultValue="3000"
                />
                <input
                  type="number"
                  className="input"
                  placeholder="最大"
                  defaultValue="5000"
                />
              </div>
            </div>
          </div>
        </motion.div>

        {/* API设置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-4">🔑 API设置</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">OpenAI API Key</label>
              <input
                type="password"
                className="input"
                placeholder="sk-..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Claude API Key</label>
              <input
                type="password"
                className="input"
                placeholder="sk-..."
              />
            </div>
          </div>
        </motion.div>

        {/* 关于 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-4">ℹ️ 关于</h2>
          <div className="space-y-2 text-gray-400">
            <p>版本: 1.0.0</p>
            <p>描述: AI小说仿写引擎</p>
            <p>功能: 深度分析原版小说的宏观架构、章节结构、世界观、力量系统、人物性格，生成风格相似但内容原创的新小说</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default SettingsPage;
