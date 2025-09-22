import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import MainLayout from './layouts/MainLayout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import StrategicMindPage from './pages/StrategicMindPage';
import './App.css';

// مكون حماية المسارات
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

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
                  <div className="p-4">
                    <h1 className="text-3xl font-bold">الشرارة الإبداعية</h1>
                    <p className="text-muted-foreground mt-2">
                      محرك إبداعي متطور يولد أفكارًا ومحتوى إبداعي يتناسب مع هوية العلامة التجارية واتجاهات السوق الحالية.
                    </p>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/transparent-mentor"
              element={
                <ProtectedRoute>
                  <div className="p-4">
                    <h1 className="text-3xl font-bold">المرشد الشفاف</h1>
                    <p className="text-muted-foreground mt-2">
                      نظام تفسير متقدم يوضح القرارات والتوصيات بطريقة سهلة الفهم، مما يعزز الثقة والتعلم.
                    </p>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/learning-loop"
              element={
                <ProtectedRoute>
                  <div className="p-4">
                    <h1 className="text-3xl font-bold">حلقة التعلم التشاركي</h1>
                    <p className="text-muted-foreground mt-2">
                      نظام تعلم مستمر يستفيد من تفاعلات المستخدمين لتحسين النماذج وقاعدة المعرفة بشكل تلقائي.
                    </p>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/campaigns"
              element={
                <ProtectedRoute>
                  <div className="p-4">
                    <h1 className="text-3xl font-bold">الحملات</h1>
                    <p className="text-muted-foreground mt-2">
                      إدارة وتحليل حملاتك التسويقية.
                    </p>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/settings"
              element={
                <ProtectedRoute>
                  <div className="p-4">
                    <h1 className="text-3xl font-bold">الإعدادات</h1>
                    <p className="text-muted-foreground mt-2">
                      إدارة إعدادات حسابك وتفضيلاتك.
                    </p>
                  </div>
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <div className="p-4">
                    <h1 className="text-3xl font-bold">الملف الشخصي</h1>
                    <p className="text-muted-foreground mt-2">
                      عرض وتعديل معلومات ملفك الشخصي.
                    </p>
                  </div>
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
      </AuthProvider>
    </Router>
  );
}

export default App;
