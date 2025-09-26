import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { campaignService } from '../services/api';
import { Plus, Search, Edit, Trash2 } from 'lucide-react';

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const fetchCampaigns = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await campaignService.getCampaigns();
      setCampaigns(response.data);
    } catch (err) {
      setError('حدث خطأ أثناء جلب الحملات');
      console.error('Error fetching campaigns:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredCampaigns = campaigns.filter(campaign =>
    campaign.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    campaign.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status) => {
    const statusMap = {
      'active': { label: 'نشطة', variant: 'default' },
      'paused': { label: 'متوقفة', variant: 'secondary' },
      'completed': { label: 'مكتملة', variant: 'outline' },
      'draft': { label: 'مسودة', variant: 'destructive' }
    };
    const statusInfo = statusMap[status] || { label: status, variant: 'default' };
    return <Badge variant={statusInfo.variant}>{statusInfo.label}</Badge>;
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">الحملات</h1>
          <p className="text-muted-foreground">إدارة وتحليل حملاتك التسويقية</p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          حملة جديدة
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>البحث والتصفية</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center space-x-2">
            <Search className="h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="البحث في الحملات..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="max-w-sm"
            />
          </div>
        </CardContent>
      </Card>

      {error && (
        <Card>
          <CardContent className="pt-6">
            <p className="text-destructive">{error}</p>
            <Button onClick={fetchCampaigns} className="mt-2">
              إعادة المحاولة
            </Button>
          </CardContent>
        </Card>
      )}

      {loading ? (
        <div className="flex items-center justify-center h-32">
          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredCampaigns.length === 0 ? (
            <Card className="col-span-full">
              <CardContent className="pt-6 text-center">
                <p className="text-muted-foreground">
                  {campaigns.length === 0 ? 'لا توجد حملات حالياً' : 'لا توجد نتائج للبحث'}
                </p>
              </CardContent>
            </Card>
          ) : (
            filteredCampaigns.map((campaign) => (
              <Card key={campaign.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <CardTitle className="text-lg">{campaign.name || 'حملة بدون اسم'}</CardTitle>
                    {getStatusBadge(campaign.status)}
                  </div>
                  <CardDescription>
                    {campaign.description || 'لا يوجد وصف'}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">الميزانية:</span>
                      <span>{campaign.budget ? `$${campaign.budget.toLocaleString()}` : 'غير محدد'}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">تاريخ الإنشاء:</span>
                      <span>{campaign.created_at ? new Date(campaign.created_at).toLocaleDateString('ar-SA') : 'غير محدد'}</span>
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2 mt-4">
                    <Button variant="outline" size="sm">
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="outline" size="sm">
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default CampaignsPage;

