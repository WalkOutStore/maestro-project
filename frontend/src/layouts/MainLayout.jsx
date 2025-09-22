import { useState } from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import {
  BarChart3,
  BrainCircuit,
  Lightbulb,
  Eye,
  RefreshCcw,
  LayoutDashboard,
  Settings,
  LogOut,
  Menu,
  X,
  User,
} from 'lucide-react';
import logo from '../assets/images/maestro_logo.png';

const MainLayout = () => {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // التحقق مما إذا كان المسار الحالي يطابق الرابط
  const isActive = (path) => {
    return location.pathname === path;
  };

  // قائمة الروابط الرئيسية
  const mainLinks = [
    { path: '/dashboard', icon: <LayoutDashboard size={20} />, label: 'لوحة التحكم' },
    { path: '/campaigns', icon: <BarChart3 size={20} />, label: 'الحملات' },
    { path: '/strategic-mind', icon: <BrainCircuit size={20} />, label: 'العقل الاستراتيجي' },
    { path: '/creative-spark', icon: <Lightbulb size={20} />, label: 'الشرارة الإبداعية' },
    { path: '/transparent-mentor', icon: <Eye size={20} />, label: 'المرشد الشفاف' },
    { path: '/learning-loop', icon: <RefreshCcw size={20} />, label: 'حلقة التعلم' },
  ];

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden" dir="rtl">
      {/* الشريط الجانبي للجوال */}
      <div className="lg:hidden">
        <Button
          variant="ghost"
          size="icon"
          className="fixed top-4 right-4 z-50"
          onClick={toggleSidebar}
        >
          {sidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </Button>
      </div>

      {/* الشريط الجانبي */}
      <aside
        className={`bg-sidebar text-sidebar-foreground w-64 flex-shrink-0 border-l border-sidebar-border overflow-y-auto transition-transform duration-300 ease-in-out ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        } fixed lg:relative h-full z-40`}
      >
        <div className="p-4">
          <div className="flex items-center justify-center mb-8">
            <img src={logo} alt="Maestro Logo" className="h-10" />
            <h1 className="text-xl font-bold mr-2">Maestro</h1>
          </div>

          <nav className="space-y-1">
            {mainLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`flex items-center px-4 py-3 rounded-md transition-colors ${
                  isActive(link.path)
                    ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                    : 'hover:bg-sidebar-accent/10'
                }`}
              >
                <span className="ml-3">{link.icon}</span>
                <span>{link.label}</span>
              </Link>
            ))}
          </nav>

          <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-sidebar-border">
            {isAuthenticated ? (
              <div className="space-y-2">
                <Link
                  to="/settings"
                  className={`flex items-center px-4 py-3 rounded-md transition-colors ${
                    isActive('/settings')
                      ? 'bg-sidebar-accent text-sidebar-accent-foreground'
                      : 'hover:bg-sidebar-accent/10'
                  }`}
                >
                  <span className="ml-3">
                    <Settings size={20} />
                  </span>
                  <span>الإعدادات</span>
                </Link>
                <Button
                  variant="ghost"
                  className="w-full justify-start px-4 py-3 h-auto hover:bg-sidebar-accent/10"
                  onClick={handleLogout}
                >
                  <span className="ml-3">
                    <LogOut size={20} />
                  </span>
                  <span>تسجيل الخروج</span>
                </Button>
              </div>
            ) : (
              <div className="space-y-2">
                <Link to="/login">
                  <Button variant="outline" className="w-full">
                    تسجيل الدخول
                  </Button>
                </Link>
                <Link to="/register">
                  <Button className="w-full">إنشاء حساب</Button>
                </Link>
              </div>
            )}
          </div>
        </div>
      </aside>

      {/* المحتوى الرئيسي */}
      <main className="flex-1 overflow-y-auto bg-background">
        {isAuthenticated && (
          <header className="bg-card shadow-sm border-b border-border">
            <div className="px-4 py-3 flex items-center justify-between">
              <h2 className="text-lg font-medium">
                {mainLinks.find((link) => isActive(link.path))?.label || 'Maestro'}
              </h2>
              <div className="flex items-center">
                <Link to="/profile" className="flex items-center">
                  <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground">
                    <User size={16} />
                  </div>
                  {user && (
                    <span className="mr-2 text-sm font-medium">
                      {user.full_name || user.username}
                    </span>
                  )}
                </Link>
              </div>
            </div>
          </header>
        )}
        <div className="p-6">
          <Outlet />
        </div>
      </main>

      {/* طبقة التعتيم للجوال عند فتح الشريط الجانبي */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 lg:hidden"
          onClick={toggleSidebar}
        />
      )}
    </div>
  );
};

export default MainLayout;
