import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { NotificationProvider } from './contexts/NotificationContext';
import { Toaster } from './components/ui/sonner';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import StrategicMindPage from './pages/StrategicMindPage';
import CreativeSparkPage from './pages/CreativeSparkPage';
import TransparentMentorPage from './pages/TransparentMentorPage';
import LearningLoopPage from './pages/LearningLoopPage';
import CampaignsPage from './pages/CampaignsPage';
import SettingsPage from './pages/SettingsPage';
import ProfilePage from './pages/ProfilePage';
import './App.css';

// مكون حماية المسارات
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  // عرض شاشة التحميل أثناء التحقق من المصادقة
  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }

  // إعادة التوجيه إلى صفحة تسجيل الدخول إذا لم يكن المستخدم مصادقًا
  if (!isAuthenticated) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // عرض المحتوى المحمي إذا كان المستخدم مصادقًا
  return children;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <NotificationProvider>
          <Toaster />
          <Routes>
            {/* المسارات العامة */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            {/* المسارات المحمية */}
            <Route path="/" element={<MainLayout />}>
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <DashboardPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/strategic-mind"
                element={
                  <ProtectedRoute>
                    <StrategicMindPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/creative-spark"
                element={
                  <ProtectedRoute>
                    <CreativeSparkPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/transparent-mentor"
                element={
                  <ProtectedRoute>
                    <TransparentMentorPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/learning-loop"
                element={
                  <ProtectedRoute>
                    <LearningLoopPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/campaigns"
                element={
                  <ProtectedRoute>
                    <CampaignsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/settings"
                element={
                  <ProtectedRoute>
                    <SettingsPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <ProfilePage />
                  </ProtectedRoute>
                }
              />
            </Route>
            
            {/* مسار 404 */}
            <Route
              path="*"
              element={
                <div className="flex flex-col items-center justify-center h-screen">
                  <h1 className="text-4xl font-bold mb-4">404</h1>
                  <p className="text-xl mb-6">الصفحة غير موجودة</p>
                  <a href="/" className="text-primary hover:underline">
                    العودة إلى الصفحة الرئيسية
                  </a>
                </div>
              }
            />
          </Routes>
        </NotificationProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
