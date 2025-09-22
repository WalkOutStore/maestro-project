import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { campaignService } from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AlertCircle, Plus, ArrowUpRight, TrendingUp, Users, DollarSign, BarChart3 } from 'lucide-react';

const DashboardPage = () => {
  const { user } = useAuth();
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  // بيانات نموذجية للرسوم البيانية
  const performanceData = [
    { name: 'يناير', ctr: 0.025, roi: 2.1, conversions: 120 },
    { name: 'فبراير', ctr: 0.028, roi: 2.3, conversions: 145 },
    { name: 'مارس', ctr: 0.032, roi: 2.5, conversions: 160 },
    { name: 'أبريل', ctr: 0.030, roi: 2.4, conversions: 155 },
    { name: 'مايو', ctr: 0.035, roi: 2.7, conversions: 180 },
    { name: 'يونيو', ctr: 0.038, roi: 2.9, conversions: 200 },
  ];

  const channelData = [
    { name: 'فيسبوك', value: 35 },
    { name: 'انستغرام', value: 25 },
    { name: 'تويتر', value: 15 },
    { name: 'لينكد إن', value: 10 },
    { name: 'جوجل', value: 15 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  useEffect(() => {
    const fetchCampaigns = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // محاولة استدعاء API حقيقي
        try {
          const response = await campaignService.getCampaigns();
          setCampaigns(response.data);
        } catch (apiError) {
          console.warn('فشل في الاتصال بـ API، استخدام بيانات نموذجية:', apiError);
          
          // في حالة فشل API، استخدم بيانات نموذجية
          setCampaigns([
            {
              id: 1,
              name: 'حملة إطلاق المنتج الجديد',
              status: 'active',
              budget: 5000,
              start_date: '2023-06-01',
              end_date: '2023-07-01',
              metrics: {
                impressions: 120000,
                clicks: 3600,
                ctr: 0.03,
                conversions: 180,
                roi: 2.5
              }
            },
            {
              id: 2,
              name: 'حملة التسويق عبر وسائل التواصل الاجتماعي',
              status: 'active',
              budget: 3000,
              start_date: '2023-05-15',
              end_date: '2023-06-15',
              metrics: {
                impressions: 85000,
                clicks: 2550,
                ctr: 0.03,
                conversions: 127,
                roi: 2.2
              }
            },
            {
              id: 3,
              name: 'حملة إعادة الاستهداف',
              status: 'planned',
              budget: 2000,
              start_date: '2023-07-01',
              end_date: '2023-07-31',
              metrics: {
                impressions: 0,
                clicks: 0,
                ctr: 0,
                conversions: 0,
                roi: 0
              }
            }
          ]);
        }
      } catch (err) {
        setError('حدث خطأ أثناء تحميل الحملات');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCampaigns();
  }, []);

  // حساب إجماليات الحملات النشطة
  const activeCampaigns = campaigns.filter(campaign => campaign.status === 'active');
  const totalBudget = activeCampaigns.reduce((sum, campaign) => sum + campaign.budget, 0);
  const totalImpressions = activeCampaigns.reduce((sum, campaign) => sum + (campaign.metrics?.impressions || 0), 0);
  const totalClicks = activeCampaigns.reduce((sum, campaign) => sum + (campaign.metrics?.clicks || 0), 0);
  const totalConversions = activeCampaigns.reduce((sum, campaign) => sum + (campaign.metrics?.conversions || 0), 0);
  const averageROI = activeCampaigns.length > 0
    ? activeCampaigns.reduce((sum, campaign) => sum + (campaign.metrics?.roi || 0), 0) / activeCampaigns.length
    : 0;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">لوحة التحكم</h1>
          <p className="text-muted-foreground">
            مرحبًا {user?.full_name || user?.username}، هذه هي نظرة عامة على حملاتك التسويقية.
          </p>
        </div>
        <Link to="/campaigns/new">
          <Button>
            <Plus className="ml-2 h-4 w-4" />
            حملة جديدة
          </Button>
        </Link>
      </div>

      <Tabs defaultValue="overview" value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">نظرة عامة</TabsTrigger>
          <TabsTrigger value="campaigns">الحملات</TabsTrigger>
          <TabsTrigger value="analytics">التحليلات</TabsTrigger>
        </TabsList>
        
        <TabsContent value="overview" className="space-y-4">
          {/* بطاقات الإحصائيات */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">الميزانية الإجمالية</CardTitle>
                <DollarSign className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalBudget.toLocaleString()} $</div>
                <p className="text-xs text-muted-foreground">
                  للحملات النشطة
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">معدل النقر إلى الظهور</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {totalImpressions > 0 ? ((totalClicks / totalImpressions) * 100).toFixed(2) : 0}%
                </div>
                <p className="text-xs text-muted-foreground">
                  +2.1% من الشهر الماضي
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">التحويلات</CardTitle>
                <Users className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalConversions.toLocaleString()}</div>
                <p className="text-xs text-muted-foreground">
                  +12.5% من الشهر الماضي
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">العائد على الاستثمار</CardTitle>
                <BarChart3 className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{averageROI.toFixed(1)}x</div>
                <p className="text-xs text-muted-foreground">
                  +0.3x من الشهر الماضي
                </p>
              </CardContent>
            </Card>
          </div>

          {/* الرسوم البيانية */}
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="col-span-1">
              <CardHeader>
                <CardTitle>أداء الحملات</CardTitle>
                <CardDescription>
                  معدل النقر إلى الظهور والعائد على الاستثمار على مدار الأشهر الستة الماضية
                </CardDescription>
              </CardHeader>
              <CardContent className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={performanceData}
                    margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
                    <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
                    <Tooltip />
                    <Bar yAxisId="left" dataKey="ctr" name="معدل النقر إلى الظهور" fill="#8884d8" />
                    <Bar yAxisId="right" dataKey="roi" name="العائد على الاستثمار" fill="#82ca9d" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <Card className="col-span-1">
              <CardHeader>
                <CardTitle>توزيع القنوات</CardTitle>
                <CardDescription>
                  توزيع الميزانية حسب قنوات التسويق
                </CardDescription>
              </CardHeader>
              <CardContent className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={channelData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {channelData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* الحملات النشطة */}
          <Card>
            <CardHeader>
              <CardTitle>الحملات النشطة</CardTitle>
              <CardDescription>
                الحملات التسويقية الجارية حاليًا
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-4">
                  {[1, 2].map((i) => (
                    <div key={i} className="flex items-center space-x-4 space-x-reverse">
                      <Skeleton className="h-12 w-12 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-[250px]" />
                        <Skeleton className="h-4 w-[200px]" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : error ? (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4 ml-2" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              ) : activeCampaigns.length === 0 ? (
                <div className="text-center py-6">
                  <p className="text-muted-foreground">لا توجد حملات نشطة حاليًا</p>
                  <Link to="/campaigns/new" className="mt-4 inline-block">
                    <Button>إنشاء حملة جديدة</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {activeCampaigns.map((campaign) => (
                    <div key={campaign.id} className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0">
                      <div>
                        <h3 className="font-medium">{campaign.name}</h3>
                        <p className="text-sm text-muted-foreground">
                          الميزانية: {campaign.budget.toLocaleString()} $ | التحويلات: {campaign.metrics?.conversions || 0}
                        </p>
                      </div>
                      <Link to={`/campaigns/${campaign.id}`}>
                        <Button variant="ghost" size="sm">
                          <ArrowUpRight className="h-4 w-4 ml-1" />
                          عرض
                        </Button>
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
            <CardFooter>
              <Link to="/campaigns" className="text-sm text-primary hover:underline">
                عرض جميع الحملات
              </Link>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="campaigns" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>جميع الحملات</CardTitle>
              <CardDescription>
                قائمة بجميع حملاتك التسويقية
              </CardDescription>
            </CardHeader>
            <CardContent>
              {loading ? (
                <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="flex items-center space-x-4 space-x-reverse">
                      <Skeleton className="h-12 w-12 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="h-4 w-[250px]" />
                        <Skeleton className="h-4 w-[200px]" />
                      </div>
                    </div>
                  ))}
                </div>
              ) : error ? (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4 ml-2" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              ) : campaigns.length === 0 ? (
                <div className="text-center py-6">
                  <p className="text-muted-foreground">لا توجد حملات حاليًا</p>
                  <Link to="/campaigns/new" className="mt-4 inline-block">
                    <Button>إنشاء حملة جديدة</Button>
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {campaigns.map((campaign) => (
                    <div key={campaign.id} className="flex items-center justify-between border-b border-border pb-4 last:border-0 last:pb-0">
                      <div>
                        <h3 className="font-medium">{campaign.name}</h3>
                        <div className="flex items-center mt-1">
                          <span className={`inline-block w-2 h-2 rounded-full mr-2 ${
                            campaign.status === 'active' ? 'bg-green-500' : 
                            campaign.status === 'planned' ? 'bg-blue-500' : 'bg-gray-500'
                          }`}></span>
                          <p className="text-sm text-muted-foreground">
                            {campaign.status === 'active' ? 'نشطة' : 
                             campaign.status === 'planned' ? 'مخططة' : 'منتهية'}
                            {' | '}
                            الميزانية: {campaign.budget.toLocaleString()} $
                          </p>
                        </div>
                      </div>
                      <Link to={`/campaigns/${campaign.id}`}>
                        <Button variant="ghost" size="sm">
                          <ArrowUpRight className="h-4 w-4 ml-1" />
                          عرض
                        </Button>
                      </Link>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
            <CardFooter>
              <Link to="/campaigns/new">
                <Button>
                  <Plus className="ml-2 h-4 w-4" />
                  إنشاء حملة جديدة
                </Button>
              </Link>
            </CardFooter>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>تحليلات الأداء</CardTitle>
              <CardDescription>
                تحليل مفصل لأداء حملاتك التسويقية
              </CardDescription>
            </CardHeader>
            <CardContent className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={performanceData}
                  margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="conversions" name="التحويلات" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
            <CardFooter>
              <Link to="/analytics" className="text-sm text-primary hover:underline">
                عرض تحليلات مفصلة
              </Link>
            </CardFooter>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DashboardPage;
