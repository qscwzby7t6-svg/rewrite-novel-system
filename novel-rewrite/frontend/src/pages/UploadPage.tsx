// NovelForge - 上传页面

import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { useUploadNovel } from '../hooks/useNovel';
import toast from 'react-hot-toast';

const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const uploadMutation = useUploadNovel();
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [file, setFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
  });

  const handleUpload = async () => {
    if (!file) {
      toast.error('请先选择文件');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);
    if (author) formData.append('author', author);

    try {
      const result = await uploadMutation.mutateAsync(formData);
      toast.success('上传成功！');
      navigate(`/analysis/${result.novel_id}`);
    } catch (error) {
      toast.error('上传失败，请重试');
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-12"
      >
        <h1 className="text-4xl font-bold mb-4 gradient-text">上传小说</h1>
        <p className="text-gray-400">上传TXT格式的小说文件，系统将自动进行分析</p>
      </motion.div>

      <div className="space-y-6">
        {/* 文件上传区域 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          {...getRootProps()}
          className={`
            card cursor-pointer transition-all duration-300
            ${isDragActive ? 'border-purple-500 bg-purple-500/10' : 'hover:border-purple-500/50'}
          `}
        >
          <input {...getInputProps()} />
          <div className="text-center py-12">
            {file ? (
              <>
                <div className="text-6xl mb-4">📄</div>
                <p className="text-xl font-semibold mb-2">{file.name}</p>
                <p className="text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                <p className="text-sm text-purple-400 mt-4">点击或拖拽更换文件</p>
              </>
            ) : (
              <>
                <div className="text-6xl mb-4">📁</div>
                <p className="text-xl font-semibold mb-2">
                  {isDragActive ? '松开以上传' : '拖拽小说文件到这里'}
                </p>
                <p className="text-gray-400">或者点击选择文件</p>
                <p className="text-sm text-purple-400 mt-4">支持 TXT 格式</p>
              </>
            )}
          </div>
        </motion.div>

        {/* 元数据输入 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="card"
        >
          <h3 className="text-lg font-semibold mb-4">小说信息（可选）</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">书名</label>
              <input
                type="text"
                className="input"
                placeholder="如果不填，将自动从文件中提取"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">作者</label>
              <input
                type="text"
                className="input"
                placeholder="如果不填，将自动从文件中提取"
                value={author}
                onChange={(e) => setAuthor(e.target.value)}
              />
            </div>
          </div>
        </motion.div>

        {/* 上传按钮 */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex justify-center"
        >
          <button
            onClick={handleUpload}
            disabled={!file || uploadMutation.isPending}
            className="btn btn-primary text-lg px-12 py-4 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploadMutation.isPending ? (
              <>
                <div className="loading-spinner" />
                上传中...
              </>
            ) : (
              '🚀 开始上传并分析'
            )}
          </button>
        </motion.div>
      </div>
    </div>
  );
};

export default UploadPage;
