import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { authService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { User, Mail, Phone, MapPin, Calendar, Edit, Save, X } from 'lucide-react';

const ProfilePage = () => {
  const { user } = useAuth();
  const [profile, setProfile] = useState({
    full_name: '',
    email: '',
    phone: '',
    company: '',
    position: '',
    location: '',
    bio: '',
    website: '',
    linkedin: '',
    twitter: ''
  });
  
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    if (user) {
      setProfile({
        full_name: user.full_name || '',
        email: user.email || '',
        phone: user.phone || '',
        company: user.company || '',
        position: user.position || '',
        location: user.location || '',
        bio: user.bio || '',
        website: user.website || '',
        linkedin: user.linkedin || '',
        twitter: user.twitter || ''
      });
    }
  }, [user]);

  const handleSave = async () => {
    setLoading(true);
    setMessage(null);
    try {
      await authService.updateUser(profile);
      setMessage({ type: 'success', text: 'تم تحديث الملف الشخصي بنجاح' });
      setIsEditing(false);
    } catch (error) {
      setMessage({ 
        type: 'error', 
        text: error.response?.data?.detail || 'حدث خطأ أثناء تحديث الملف الشخصي' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (user) {
      setProfile({
        full_name: user.full_name || '',
        email: user.email || '',
        phone: user.phone || '',
        company: user.company || '',
        position: user.position || '',
        location: user.location || '',
        bio: user.bio || '',
        website: user.website || '',
        linkedin: user.linkedin || '',
        twitter: user.twitter || ''
      });
    }
    setIsEditing(false);
    setMessage(null);
  };

  const handleInputChange = (field, value) => {
    setProfile(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const getInitials = (name) => {
    return name
      .split(' ')
      .map(word => word.charAt(0))
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">الملف الشخصي</h1>
          <p className="text-muted-foreground">عرض وتعديل معلومات ملفك الشخصي</p>
        </div>
        <div className="flex gap-2">
          {isEditing ? (
            <>
              <Button onClick={handleSave} disabled={loading}>
                <Save className="mr-2 h-4 w-4" />
                {loading ? 'جاري الحفظ...' : 'حفظ'}
              </Button>
              <Button variant="outline" onClick={handleCancel}>
                <X className="mr-2 h-4 w-4" />
                إلغاء
              </Button>
            </>
          ) : (
            <Button onClick={() => setIsEditing(true)}>
              <Edit className="mr-2 h-4 w-4" />
              تعديل
            </Button>
          )}
        </div>
      </div>

      {message && (
        <Card>
          <CardContent className="pt-6">
            <p className={`${
              message.type === 'success' ? 'text-green-600' : 'text-red-600'
            }`}>
              {message.text}
            </p>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-6 md:grid-cols-3">
        {/* معلومات أساسية */}
        <Card className="md:col-span-1">
          <CardHeader className="text-center">
            <Avatar className="w-24 h-24 mx-auto mb-4">
              <AvatarImage src={user?.avatar} />
              <AvatarFallback className="text-lg">
                {getInitials(profile.full_name || 'مستخدم')}
              </AvatarFallback>
            </Avatar>
            <CardTitle>{profile.full_name || 'غير محدد'}</CardTitle>
            <CardDescription>{profile.position || 'لا يوجد منصب محدد'}</CardDescription>
            {profile.company && (
              <Badge variant="secondary">{profile.company}</Badge>
            )}
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center gap-2 text-sm">
              <Mail className="h-4 w-4 text-muted-foreground" />
              <span>{profile.email || 'غير محدد'}</span>
            </div>
            {profile.phone && (
              <div className="flex items-center gap-2 text-sm">
                <Phone className="h-4 w-4 text-muted-foreground" />
                <span>{profile.phone}</span>
              </div>
            )}
            {profile.location && (
              <div className="flex items-center gap-2 text-sm">
                <MapPin className="h-4 w-4 text-muted-foreground" />
                <span>{profile.location}</span>
              </div>
            )}
            {user?.created_at && (
              <div className="flex items-center gap-2 text-sm">
                <Calendar className="h-4 w-4 text-muted-foreground" />
                <span>انضم في {new Date(user.created_at).toLocaleDateString('ar-SA')}</span>
              </div>
            )}
          </CardContent>
        </Card>

        {/* تفاصيل الملف الشخصي */}
        <Card className="md:col-span-2">
          <CardHeader>
            <CardTitle>معلومات شخصية</CardTitle>
            <CardDescription>تفاصيل حسابك ومعلوماتك الشخصية</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <Label>الاسم الكامل</Label>
                {isEditing ? (
                  <Input
                    value={profile.full_name}
                    onChange={(e) => handleInputChange('full_name', e.target.value)}
                    placeholder="أدخل اسمك الكامل"
                  />
                ) : (
                  <p className="text-sm p-2 bg-muted rounded">{profile.full_name || 'غير محدد'}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label>البريد الإلكتروني</Label>
                {isEditing ? (
                  <Input
                    type="email"
                    value={profile.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    placeholder="أدخل بريدك الإلكتروني"
                  />
                ) : (
                  <p className="text-sm p-2 bg-muted rounded">{profile.email || 'غير محدد'}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label>رقم الهاتف</Label>
                {isEditing ? (
                  <Input
                    value={profile.phone}
                    onChange={(e) => handleInputChange('phone', e.target.value)}
                    placeholder="أدخل رقم هاتفك"
                  />
                ) : (
                  <p className="text-sm p-2 bg-muted rounded">{profile.phone || 'غير محدد'}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label>الموقع</Label>
                {isEditing ? (
                  <Input
                    value={profile.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                    placeholder="أدخل موقعك"
                  />
                ) : (
                  <p className="text-sm p-2 bg-muted rounded">{profile.location || 'غير محدد'}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label>الشركة</Label>
                {isEditing ? (
                  <Input
                    value={profile.company}
                    onChange={(e) => handleInputChange('company', e.target.value)}
                    placeholder="أدخل اسم شركتك"
                  />
                ) : (
                  <p className="text-sm p-2 bg-muted rounded">{profile.company || 'غير محدد'}</p>
                )}
              </div>
              <div className="space-y-2">
                <Label>المنصب</Label>
                {isEditing ? (
                  <Input
                    value={profile.position}
                    onChange={(e) => handleInputChange('position', e.target.value)}
                    placeholder="أدخل منصبك"
                  />
                ) : (
                  <p className="text-sm p-2 bg-muted rounded">{profile.position || 'غير محدد'}</p>
                )}
              </div>
            </div>

            <Separator />

            <div className="space-y-2">
              <Label>نبذة شخصية</Label>
              {isEditing ? (
                <Textarea
                  value={profile.bio}
                  onChange={(e) => handleInputChange('bio', e.target.value)}
                  placeholder="اكتب نبذة عن نفسك"
                  rows={3}
                />
              ) : (
                <p className="text-sm p-2 bg-muted rounded min-h-[80px]">
                  {profile.bio || 'لا توجد نبذة شخصية'}
                </p>
              )}
            </div>

            <Separator />

            <div className="space-y-4">
              <Label>روابط اجتماعية</Label>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-2">
                  <Label className="text-sm">الموقع الشخصي</Label>
                  {isEditing ? (
                    <Input
                      value={profile.website}
                      onChange={(e) => handleInputChange('website', e.target.value)}
                      placeholder="https://example.com"
                    />
                  ) : (
                    <p className="text-sm p-2 bg-muted rounded">
                      {profile.website ? (
                        <a href={profile.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                          {profile.website}
                        </a>
                      ) : (
                        'غير محدد'
                      )}
                    </p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label className="text-sm">LinkedIn</Label>
                  {isEditing ? (
                    <Input
                      value={profile.linkedin}
                      onChange={(e) => handleInputChange('linkedin', e.target.value)}
                      placeholder="https://linkedin.com/in/username"
                    />
                  ) : (
                    <p className="text-sm p-2 bg-muted rounded">
                      {profile.linkedin ? (
                        <a href={profile.linkedin} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                          {profile.linkedin}
                        </a>
                      ) : (
                        'غير محدد'
                      )}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ProfilePage;

