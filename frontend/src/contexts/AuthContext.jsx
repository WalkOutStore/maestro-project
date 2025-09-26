import { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/api';

// إنشاء سياق المصادقة
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // التحقق من المصادقة عند تحميل التطبيق
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await authService.getCurrentUser();
          setUser(response.data);
        } catch (err) {
          console.error('فشل التحقق من المصادقة:', err);
          localStorage.removeItem('token');
          setUser(null);
        }
      } else {
        setUser(null);
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  // تسجيل الدخول
  const login = async (credentials) => {
    try {
      setError(null);
      const response = await authService.login(credentials);
      localStorage.setItem('token', response.data.access_token);
      
      // الحصول على بيانات المستخدم بعد تسجيل الدخول
      const userResponse = await authService.getCurrentUser();
      setUser(userResponse.data);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'فشل تسجيل الدخول');
      return false;
    }
  };

  // تسجيل مستخدم جديد
  const register = async (userData) => {
    try {
      setError(null);
      await authService.register(userData);
      // تسجيل الدخول بعد التسجيل
      return await login({
        username: userData.email,
        password: userData.password
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'فشل التسجيل');
      return false;
    }
  };

  // تسجيل الخروج
  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  // تحديث بيانات المستخدم
  const updateUserProfile = async (userData) => {
    try {
      setError(null);
      const response = await authService.updateUser(userData);
      setUser(response.data);
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'فشل تحديث البيانات');
      return false;
    }
  };

  // القيم التي سيتم توفيرها للمكونات
  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    updateUserProfile,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// هوك مخصص لاستخدام سياق المصادقة
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('يجب استخدام useAuth داخل AuthProvider');
  }
  return context;
};

export default AuthContext;
