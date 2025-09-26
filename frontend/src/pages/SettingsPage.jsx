import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Separator } from '@/components/ui/separator';
import { authService } from '../services/api';
import { Settings, Bell, Shield, Palette, Globe } from 'lucide-react';
import { useNotification } from '../contexts/NotificationContext';

const SettingsPage = () => {
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      push: false,
      marketing: false,
    },
    privacy: {
      profileVisible: true,
      dataSharing: false,
    },
    preferences: {
      language: 'ar',
      theme: 'light',
      timezone: 'Asia/Riyadh',
    },
    api: {
      autoSave: true,
      cacheResults: true,
    }
  });
  
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const { showSuccess, showError, showInfo, showWarning } = useNotification();

  const handleSave = async () => {
    setLoading(true);
    setMessage(null);
    try {
      // حفظ الإعدادات في localStorage أو إرسالها للخادم
      localStorage.setItem('userSettings', JSON.stringify(settings));
      showSuccess('تم حفظ الإعدادات بنجاح');
    } catch (error) {
      showError('حدث خطأ أثناء حفظ الإعدادات');
    } finally {
      setLoading(false);
    }
  };

  const defaultSettings = {
    notifications: {
      email: true,
      push: false,
      marketing: false,
    },
    privacy: {
      profileVisible: true,
      dataSharing: false,
    },
    preferences: {
      language: 'ar',
      theme: 'light',
      timezone: 'Asia/Riyadh',
    },
    api: {
      autoSave: true,
      cacheResults: true,
    }
  };

  const handleReset = () => {
    setSettings(defaultSettings);
    showInfo('تم إعادة تعيين الإعدادات إلى القيم الافتراضية');
  };

  useEffect(() => {
    // تحميل الإعدادات المحفوظة
    const savedSettings = localStorage.getItem('userSettings');
    if (savedSettings) {
      try {
        setSettings(JSON.parse(savedSettings));
      } catch (error) {
        console.error('Error loading settings:', error);
      }
    }
  }, []);

  const updateSetting = (category, key, value) => {
    setSettings(prev => ({
      ...prev,
      [category]: {
        ...prev[category],
        [key]: value
      }
    }));
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">الإعدادات</h1>
        <p className="text-muted-foreground">إدارة إعدادات حسابك وتفضيلاتك</p>
      </div>

      {message && (
        <Card>
          <CardContent className="pt-6">
            <p className={`${
              message.type === 'success' ? 'text-green-600' : 
              message.type === 'error' ? 'text-red-600' : 
              'text-blue-600'
            }`}>
              {message.text}
            </p>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-6">
        {/* إعدادات الإشعارات */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              الإشعارات
            </CardTitle>
            <CardDescription>إدارة تفضيلات الإشعارات</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>إشعارات البريد الإلكتروني</Label>
                <p className="text-sm text-muted-foreground">تلقي إشعارات عبر البريد الإلكتروني</p>
              </div>
              <Switch
                checked={settings.notifications.email}
                onCheckedChange={(checked) => updateSetting('notifications', 'email', checked)}
              />
            </div>
            <Separator />
            <div className="flex items-center justify-between">
              <div>
                <Label>الإشعارات الفورية</Label>
                <p className="text-sm text-muted-foreground">تلقي إشعارات فورية في المتصفح</p>
              </div>
              <Switch
                checked={settings.notifications.push}
                onCheckedChange={(checked) => updateSetting('notifications', 'push', checked)}
              />
            </div>
            <Separator />
            <div className="flex items-center justify-between">
              <div>
                <Label>إشعارات التسويق</Label>
                <p className="text-sm text-muted-foreground">تلقي إشعارات حول العروض والميزات الجديدة</p>
              </div>
              <Switch
                checked={settings.notifications.marketing}
                onCheckedChange={(checked) => updateSetting('notifications', 'marketing', checked)}
              />
            </div>
          </CardContent>
        </Card>

        {/* إعدادات الخصوصية */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              الخصوصية والأمان
            </CardTitle>
            <CardDescription>إدارة إعدادات الخصوصية وحماية البيانات</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>إظهار الملف الشخصي</Label>
                <p className="text-sm text-muted-foreground">السماح للآخرين برؤية ملفك الشخصي</p>
              </div>
              <Switch
                checked={settings.privacy.profileVisible}
                onCheckedChange={(checked) => updateSetting('privacy', 'profileVisible', checked)}
              />
            </div>
            <Separator />
            <div className="flex items-center justify-between">
              <div>
                <Label>مشاركة البيانات</Label>
                <p className="text-sm text-muted-foreground">مشاركة البيانات لتحسين الخدمة</p>
              </div>
              <Switch
                checked={settings.privacy.dataSharing}
                onCheckedChange={(checked) => updateSetting('privacy', 'dataSharing', checked)}
              />
            </div>
          </CardContent>
        </Card>

        {/* التفضيلات العامة */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Palette className="h-5 w-5" />
              التفضيلات العامة
            </CardTitle>
            <CardDescription>إعدادات الواجهة واللغة</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label>اللغة</Label>
              <Select
                value={settings.preferences.language}
                onValueChange={(value) => updateSetting('preferences', 'language', value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="ar">العربية</SelectItem>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="fr">Français</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>المظهر</Label>
              <Select
                value={settings.preferences.theme}
                onValueChange={(value) => updateSetting('preferences', 'theme', value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="light">فاتح</SelectItem>
                  <SelectItem value="dark">داكن</SelectItem>
                  <SelectItem value="system">حسب النظام</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="grid gap-2">
              <Label>المنطقة الزمنية</Label>
              <Select
                value={settings.preferences.timezone}
                onValueChange={(value) => updateSetting('preferences', 'timezone', value)}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Asia/Riyadh">الرياض</SelectItem>
                  <SelectItem value="Asia/Dubai">دبي</SelectItem>
                  <SelectItem value="Africa/Cairo">القاهرة</SelectItem>
                  <SelectItem value="UTC">UTC</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* إعدادات API */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="h-5 w-5" />
              إعدادات API
            </CardTitle>
            <CardDescription>إعدادات متقدمة للواجهة البرمجية</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label>الحفظ التلقائي</Label>
                <p className="text-sm text-muted-foreground">حفظ التغييرات تلقائياً</p>
              </div>
              <Switch
                checked={settings.api.autoSave}
                onCheckedChange={(checked) => updateSetting('api', 'autoSave', checked)}
              />
            </div>
            <Separator />
            <div className="flex items-center justify-between">
              <div>
                <Label>تخزين النتائج مؤقتاً</Label>
                <p className="text-sm text-muted-foreground">تحسين الأداء عبر التخزين المؤقت</p>
              </div>
              <Switch
                checked={settings.api.cacheResults}
                onCheckedChange={(checked) => updateSetting('api', 'cacheResults', checked)}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="flex gap-4">
        <Button onClick={handleSave} disabled={loading}>
          {loading ? 'جاري الحفظ...' : 'حفظ الإعدادات'}
        </Button>
        <Button variant="outline" onClick={handleReset}>
          إعادة تعيين
        </Button>
      </div>
    </div>
  );
};

export default SettingsPage;
