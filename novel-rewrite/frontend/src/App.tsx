// NovelForge - 主应用组件

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { useI18n } from './hooks/useI18n';

// 导入页面组件
import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import AnalysisPage from './pages/AnalysisPage';
import RewritePage from './pages/RewritePage';
import ResultPage from './pages/ResultPage';
import SettingsPage from './pages/SettingsPage';

// 创建QueryClient实例
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// 导航链接组件
const NavLink: React.FC<{ to: string; children: React.ReactNode; className?: string }> = ({ 
  to, 
  children, 
  className = '' 
}) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Link
      to={to}
      className={`
        px-4 py-2 rounded-lg transition-all duration-300
        ${isActive 
          ? 'bg-purple-600 text-white shadow-lg' 
          : 'text-gray-300 hover:text-white hover:bg-white/10'
        }
        ${className}
      `}
    >
      {children}
    </Link>
  );
};

// 主布局组件
const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const location = useLocation();
  const isHome = location.pathname === '/';
  
  return (
    <div className="min-h-screen flex flex-col">
      {/* 导航栏 */}
      <nav className="glass-dark sticky top-0 z-50 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-pink-600 rounded-xl flex items-center justify-center shadow-lg">
              <span className="text-2xl">📚</span>
            </div>
            <div>
              <h1 className="text-xl font-bold gradient-text">NovelForge</h1>
              <p className="text-xs text-gray-400">智能小说仿写引擎</p>
            </div>
          </Link>
          
          {/* 导航链接 */}
          <div className="flex items-center gap-4">
            {!isHome && (
              <>
                <NavLink to="/upload">上传</NavLink>
                <NavLink to="/analysis">分析</NavLink>
                <NavLink to="/rewrite">仿写</NavLink>
                <NavLink to="/settings">设置</NavLink>
              </>
            )}
          </div>
        </div>
      </nav>
      
      {/* 主内容区 */}
      <main className="flex-1 page-container">
        {children}
      </main>
      
      {/* 页脚 */}
      <footer className="glass-dark px-6 py-8 mt-12">
        <div className="max-w-7xl mx-auto text-center text-gray-400">
          <p>© 2024 NovelForge - AI小说仿写引擎</p>
          <p className="mt-2 text-sm">
            深度分析原版小说的宏观架构、章节结构、世界观、力量系统、人物性格
          </p>
        </div>
      </footer>
      
      {/* Toast通知 */}
      <Toaster
        position="top-right"
        toastOptions={{
          className: '!bg-gray-800 !text-white !rounded-lg',
          style: {
            background: 'rgba(30, 41, 59, 0.95)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
          },
        }}
      />
    </div>
  );
};

// App组件
const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/analysis/:novelId" element={<AnalysisPage />} />
            <Route path="/rewrite/:novelId" element={<RewritePage />} />
            <Route path="/result/:novelId" element={<ResultPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </Layout>
      </Router>
    </QueryClientProvider>
  );
};

export default App;
