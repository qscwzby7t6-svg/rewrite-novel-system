// NovelForge - 设置页面

import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import axios from 'axios';

interface LLMProvider {
  id: string;
  name: string;
  models: string[];
  is_default: boolean;
}

interface LLMConfig {
  default_provider: string;
  configs: { [key: string]: { model: string; has_api_key: boolean } };
  parameters: {
    temperature: number;
    max_tokens: number;
    top_p: number;
    presence_penalty: number;
    frequency_penalty: number;
    timeout: number;
  };
}

const SettingsPage: React.FC = () => {
  const [selectedProvider, setSelectedProvider] = useState('deepseek');
  const [apiKeys, setApiKeys] = useState<{ [key: string]: string }>({});
  const [testResult, setTestResult] = useState<{ success: boolean; result?: string; error?: string } | null>(null);
  const [isTesting, setIsTesting] = useState(false);

  const { data: providers, isLoading: providersLoading } = useQuery({
    queryKey: ['llmProviders'],
    queryFn: async () => {
      const response = await axios.get('/api/v1/llm/providers');
      return response.data.providers as LLMProvider[];
    }
  });

  const { data: config, isLoading: configLoading } = useQuery({
    queryKey: ['llmConfig'],
    queryFn: async () => {
      const response = await axios.get('/api/v1/llm/config');
      return response.data as LLMConfig;
    }
  });

  useEffect(() => {
    if (config?.default_provider) {
      setSelectedProvider(config.default_provider);
    }
  }, [config]);

  const handleTestConnection = async () => {
    setIsTesting(true);
    setTestResult(null);
    
    try {
      const response = await axios.post('/api/v1/llm/test', {
        provider: selectedProvider,
        prompt: '请说一句话介绍你自己'
      });
      setTestResult(response.data);
    } catch (error: any) {
      setTestResult({
        success: false,
        error: error.response?.data?.detail || '连接测试失败'
      });
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold mb-2 gradient-text">设置</h1>
        <p className="text-gray-400">配置系统参数和偏好设置</p>
      </motion.div>

      <div className="space-y-8">
        {/* LLM大模型设置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-6">🤖 大模型设置</h2>
          
          <div className="space-y-6">
            {/* 选择LLM提供商 */}
            <div>
              <label className="block text-sm font-medium mb-3">选择大模型提供商</label>
              {providersLoading ? (
                <div className="text-gray-400">加载中...</div>
              ) : (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {providers?.map((provider) => (
                    <button
                      key={provider.id}
                      onClick={() => setSelectedProvider(provider.id)}
                      className={`p-4 rounded-lg border-2 transition-all ${
                        selectedProvider === provider.id
                          ? 'border-purple-600 bg-purple-600/20'
                          : 'border-white/10 hover:border-purple-600/50'
                      }`}
                    >
                      <div className="font-medium">{provider.name}</div>
                      <div className="text-xs text-gray-400 mt-1">
                        {provider.models.length}个模型可用
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* API密钥配置 */}
            <div>
              <label className="block text-sm font-medium mb-3">
                API密钥配置
              </label>
              <div className="space-y-4">
                {/* DeepSeek */}
                <div>
                  <label className="block text-sm mb-2">DeepSeek API Key</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="sk-..."
                    value={apiKeys.deepseek || ''}
                    onChange={(e) => setApiKeys({ ...apiKeys, deepseek: e.target.value })}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    从 https://platform.deepseek.com 获取
                  </p>
                </div>

                {/* 文心一言 */}
                <div>
                  <label className="block text-sm mb-2">文心一言 API Key</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="API密钥"
                    value={apiKeys.wenxin || ''}
                    onChange={(e) => setApiKeys({ ...apiKeys, wenxin: e.target.value })}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    从 https://cloud.baidu.com 获取
                  </p>
                </div>

                {/* 通义千问 */}
                <div>
                  <label className="block text-sm mb-2">通义千问 API Key</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="sk-..."
                    value={apiKeys.qianwen || ''}
                    onChange={(e) => setApiKeys({ ...apiKeys, qianwen: e.target.value })}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    从 https://dashscope.aliyuncs.com 获取
                  </p>
                </div>

                {/* Kimi */}
                <div>
                  <label className="block text-sm mb-2">Kimi API Key</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="sk-..."
                    value={apiKeys.kimi || ''}
                    onChange={(e) => setApiKeys({ ...apiKeys, kimi: e.target.value })}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    从 https://platform.moonshot.cn 获取
                  </p>
                </div>

                {/* GLM智谱AI */}
                <div>
                  <label className="block text-sm mb-2">智谱AI API Key</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="API密钥"
                    value={apiKeys.glm || ''}
                    onChange={(e) => setApiKeys({ ...apiKeys, glm: e.target.value })}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    从 https://open.bigmodel.cn 获取
                  </p>
                </div>

                {/* OpenAI */}
                <div>
                  <label className="block text-sm mb-2">OpenAI API Key</label>
                  <input
                    type="password"
                    className="input"
                    placeholder="sk-..."
                    value={apiKeys.openai || ''}
                    onChange={(e) => setApiKeys({ ...apiKeys, openai: e.target.value })}
                  />
                  <p className="text-xs text-gray-400 mt-1">
                    从 https://platform.openai.com 获取
                  </p>
                </div>
              </div>
            </div>

            {/* 测试连接 */}
            <div>
              <button
                onClick={handleTestConnection}
                disabled={isTesting}
                className="btn btn-primary"
              >
                {isTesting ? '测试中...' : '测试连接'}
              </button>
              
              {testResult && (
                <div className={`mt-4 p-4 rounded-lg ${
                  testResult.success ? 'bg-green-600/20 border border-green-600' : 
                  'bg-red-600/20 border border-red-600'
                }`}>
                  <div className="font-medium">
                    {testResult.success ? '✓ 连接成功' : '✗ 连接失败'}
                  </div>
                  {testResult.result && (
                    <p className="text-sm mt-2 text-gray-300">
                      {testResult.result}
                    </p>
                  )}
                  {testResult.error && (
                    <p className="text-sm mt-2 text-red-300">
                      {testResult.error}
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        </motion.div>

        {/* 模型参数设置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-6">⚙️ 模型参数</h2>
          
          {configLoading ? (
            <div className="text-gray-400">加载中...</div>
          ) : (
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">
                  Temperature (温度): {config?.parameters.temperature}
                </label>
                <input
                  type="range"
                  min="0"
                  max="2"
                  step="0.1"
                  defaultValue={config?.parameters.temperature || 0.7}
                  className="w-full"
                />
                <p className="text-xs text-gray-400 mt-1">
                  较高的值使输出更随机，较低的值使输出更确定
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Max Tokens (最大令牌数): {config?.parameters.max_tokens}
                </label>
                <input
                  type="number"
                  className="input"
                  defaultValue={config?.parameters.max_tokens || 2000}
                  min="100"
                  max="8000"
                />
                <p className="text-xs text-gray-400 mt-1">
                  控制生成文本的最大长度
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">
                  Top P (核采样): {config?.parameters.top_p}
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.05"
                  defaultValue={config?.parameters.top_p || 1}
                  className="w-full"
                />
                <p className="text-xs text-gray-400 mt-1">
                  控制随机性的另一种方式
                </p>
              </div>
            </div>
          )}
        </motion.div>

        {/* 仿写设置 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="card"
        >
          <h2 className="text-xl font-bold mb-6">📝 仿写设置</h2>
          
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
              <p className="text-xs text-gray-400 mt-1">
                保持相似度低于此阈值以确保原创性
              </p>
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
