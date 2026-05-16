// NovelForge - 自定义Hooks集合

import { useState, useEffect, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';

// API配置
const API_BASE_URL = 'http://localhost:8000/api/v1';

// 创建axios实例
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== 小说Hook ====================

export const useNovel = (novelId: string) => {
  return useQuery({
    queryKey: ['novel', novelId],
    queryFn: async () => {
      const response = await api.get(`/novel/${novelId}`);
      return response.data;
    },
    enabled: !!novelId,
  });
};

export const useNovelAnalysis = (novelId: string) => {
  return useQuery({
    queryKey: ['novelAnalysis', novelId],
    queryFn: async () => {
      const response = await api.get(`/novel/${novelId}/analysis`);
      return response.data;
    },
    enabled: !!novelId,
  });
};

export const useNovelStatistics = (novelId: string) => {
  return useQuery({
    queryKey: ['novelStatistics', novelId],
    queryFn: async () => {
      const response = await api.get(`/novel/${novelId}/statistics`);
      return response.data;
    },
    enabled: !!novelId,
  });
};

// ==================== 上传Hook ====================

export const useUploadNovel = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (formData: FormData) => {
      const response = await api.post('/novel/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['novels'] });
    },
  });
};

// ==================== 仿写Hook ====================

export const useRewriteNovel = () => {
  return useMutation({
    mutationFn: async (data: any) => {
      const response = await api.post(`/novel/${data.novelId}/rewrite`, data);
      return response.data;
    },
  });
};

export const useRewriteStatus = (novelId: string, taskId: string) => {
  return useQuery({
    queryKey: ['rewriteStatus', taskId],
    queryFn: async () => {
      const response = await api.get(`/novel/${novelId}/rewrite/status/${taskId}`);
      return response.data;
    },
    enabled: !!taskId,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data && (data.status === 'processing' || data.status === 'pending')) {
        return 2000; // 每2秒轮询
      }
      return false;
    },
  });
};

// ==================== 相似度检测Hook ====================

export const useSimilarityCheck = (novelId: string, originalNovelId: string) => {
  return useMutation({
    mutationFn: async (threshold: number) => {
      const response = await api.post(`/novel/${novelId}/verify-similarity`, {
        original_novel_id: originalNovelId,
        threshold,
      });
      return response.data;
    },
  });
};

// ==================== 国际化Hook ====================

export const useI18n = () => {
  const [locale, setLocale] = useState('zh-CN');
  const [translations, setTranslations] = useState<Record<string, string>>({});

  useEffect(() => {
    // 加载翻译
    const loadTranslations = async () => {
      try {
        const response = await api.get(`/i18n/locales`);
        // 这里应该根据locale加载对应的翻译文件
        setTranslations({});
      } catch (error) {
        console.error('加载翻译失败:', error);
      }
    };
    
    loadTranslations();
  }, [locale]);

  const t = useCallback((key: string): string => {
    return translations[key] || key;
  }, [translations]);

  return {
    locale,
    setLocale,
    t,
    availableLocales: [
      { code: 'zh-CN', name: '简体中文' },
      { code: 'en-US', name: 'English' },
      { code: 'ja-JP', name: '日本語' },
    ],
  };
};

// ==================== 表单Hook ====================

export const useForm = <T extends Record<string, any>>(initialValues: T) => {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});

  const handleChange = useCallback((
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setValues(prev => ({ ...prev, [name]: value }));
    
    // 清除错误
    if (errors[name as keyof T]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  }, [errors]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
  }, [initialValues]);

  const validate = useCallback((validationRules: Partial<Record<keyof T, (value: any) => string | null>>) => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    let isValid = true;

    for (const [key, validator] of Object.entries(validationRules)) {
      const error = validator(values[key as keyof T]);
      if (error) {
        newErrors[key as keyof T] = error;
        isValid = false;
      }
    }

    setErrors(newErrors);
    return isValid;
  }, [values]);

  return {
    values,
    errors,
    handleChange,
    setValues,
    reset,
    validate,
  };
};

// ==================== 文件上传Hook ====================

export const useFileUpload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const upload = useCallback(async (file: File) => {
    setUploading(true);
    setProgress(0);
    setFile(file);

    const formData = new FormData();
    formData.append('file', file);

    try {
      // 模拟上传进度
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90));
      }, 200);

      const response = await api.post('/novel/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total || 1)
          );
          setProgress(percentCompleted);
        },
      });

      clearInterval(progressInterval);
      setProgress(100);

      return response.data;
    } catch (error) {
      throw error;
    } finally {
      setUploading(false);
    }
  }, []);

  const remove = useCallback(() => {
    setFile(null);
    setProgress(0);
  }, []);

  return {
    file,
    uploading,
    progress,
    upload,
    remove,
  };
};

// ==================== 轮询Hook ====================

export const usePolling = (
  callback: () => void | Promise<void>,
  interval: number,
  enabled: boolean = true
) => {
  useEffect(() => {
    if (!enabled) return;

    const timer = setInterval(callback, interval);
    return () => clearInterval(timer);
  }, [callback, interval, enabled]);
};

// ==================== 本地存储Hook ====================

export const useLocalStorage = <T>(key: string, initialValue: T) => {
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue] as const;
};

// ==================== 主题Hook ====================

export const useTheme = () => {
  const [theme, setTheme] = useLocalStorage('theme', 'dark');

  const toggleTheme = useCallback(() => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  }, [setTheme]);

  return {
    theme,
    setTheme,
    toggleTheme,
    isDark: theme === 'dark',
  };
};

// ==================== Toast通知Hook ====================

export const useToast = () => {
  const toast = require('react-hot-toast').default;

  const success = useCallback((message: string) => {
    toast.success(message, {
      duration: 3000,
      position: 'top-right',
    });
  }, []);

  const error = useCallback((message: string) => {
    toast.error(message, {
      duration: 4000,
      position: 'top-right',
    });
  }, []);

  const loading = useCallback((message: string) => {
    return toast.loading(message, {
      position: 'top-right',
    });
  }, []);

  const dismiss = useCallback((toastId?: string) => {
    if (toastId) {
      toast.dismiss(toastId);
    } else {
      toast.dismiss();
    }
  }, []);

  return {
    success,
    error,
    loading,
    dismiss,
  };
};

// ==================== 响应式Hook ====================

export const useResponsive = () => {
  const [isMobile, setIsMobile] = useState(false);
  const [isTablet, setIsTablet] = useState(false);
  const [isDesktop, setIsDesktop] = useState(true);

  useEffect(() => {
    const checkWidth = () => {
      const width = window.innerWidth;
      setIsMobile(width < 768);
      setIsTablet(width >= 768 && width < 1024);
      setIsDesktop(width >= 1024);
    };

    checkWidth();
    window.addEventListener('resize', checkWidth);

    return () => window.removeEventListener('resize', checkWidth);
  }, []);

  return {
    isMobile,
    isTablet,
    isDesktop,
    isDesktopOrTablet: isTablet || isDesktop,
  };
};

// 导出API实例和所有hooks
export {
  api,
  API_BASE_URL,
};
