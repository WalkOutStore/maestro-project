import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { learningLoopService } from '../services/api';

const LearningLoopPage = () => {
  const [campaignId, setCampaignId] = useState('');
  const [days, setDays] = useState(30);
  const [recommendationId, setRecommendationId] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleStats = async () => {
    setLoading(true);
    setResult(null);
    try {
      const cid = campaignId === '' ? undefined : Number(campaignId);
      const res = await learningLoopService.getRecommendationFeedbackStats(cid);
      setResult({ type: 'stats', data: res.data });
    } catch (e) {
      setResult({ error: e?.response?.data?.detail || 'حدث خطأ أثناء جلب الإحصائيات' });
    } finally {
      setLoading(false);
    }
  };

  const handleSendFeedback = async () => {
    const rid = Number(recommendationId);
    if (!rid || Number.isNaN(rid)) {
      setResult({ error: 'الرجاء إدخال معرف توصية صالح' });
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const res = await learningLoopService.saveRecommendationFeedback(rid, { helpful: true });
      setResult({ type: 'save', data: res.data });
    } catch (e) {
      setResult({ error: e?.response?.data?.detail || 'حدث خطأ أثناء حفظ التغذية الراجعة' });
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeTrends = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await learningLoopService.analyzeFeedbackTrends(days);
      setResult({ type: 'trends', data: res.data });
    } catch (e) {
      setResult({ error: e?.response?.data?.detail || 'حدث خطأ أثناء تحليل الاتجاهات (يستلزم صلاحيات أعلى)' });
    } finally {
      setLoading(false);
    }
  };

  const renderResultItems = () => {
    if (!result || !result.data) {
      return (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🤷‍♂️</div>
          <p className="text-muted-foreground text-lg">لا توجد نتائج</p>
        </div>
      );
    }

    // عرض الإحصائيات والاتجاهات بشكل واضح
    if (result.type === 'stats' || result.type === 'trends') {
      const data = result.data;
      return (
        <div className="space-y-3">
          <Card className="bg-muted p-3">
            <p><strong>إجمالي التوصيات:</strong> {data.total_recommendations}</p>
            <p><strong>التوصيات المطبقة:</strong> {data.applied_recommendations}</p>
            <p><strong>التغذية الراجعة المستلمة:</strong> {data.feedback_received}</p>
            <p><strong>متوسط التقييم:</strong> {data.average_rating}</p>
            <p><strong>حسب النوع:</strong> {Object.keys(data.by_type).length > 0 ? JSON.stringify(data.by_type) : 'فارغ'}</p>
          </Card>
        </div>
      );
    }

    // عرض رسالة نجاح عند حفظ التغذية الراجعة
    if (result.type === 'save') {
      return (
        <Card className="bg-muted p-3">
          <p>تم حفظ التغذية الراجعة بنجاح!</p>
        </Card>
      );
    }

    // fallback لأي نوع بيانات غير متوقع
    return (
      <Card className="bg-muted p-3">
        <pre>{JSON.stringify(result.data, null, 2)}</pre>
      </Card>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">حلقة التعلم</h1>
        <p className="text-muted-foreground">إدارة التغذية الراجعة وتحليل الاتجاهات</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>مدخلات</CardTitle>
          <CardDescription>حدد الحقول المطلوبة حسب العملية</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          <div className="space-y-2">
            <Label>معرّف الحملة (اختياري)</Label>
            <Input
              type="text"
              value={campaignId}
              onChange={(e) => setCampaignId(e.target.value)}
              placeholder="اتركه فارغاً لإحصائيات عامة"
            />
          </div>
          <div className="space-y-2">
            <Label>الأيام (تحليل الاتجاهات)</Label>
            <Input
              type="number"
              value={days}
              onChange={(e) => setDays(parseInt(e.target.value || '0', 10))}
            />
          </div>
          <div className="space-y-2">
            <Label>معرّف التوصية (لحفظ التغذية الراجعة)</Label>
            <Input
              type="text"
              value={recommendationId}
              onChange={(e) => setRecommendationId(e.target.value)}
              placeholder="رقم توصية موجود فعلياً"
            />
          </div>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button onClick={handleStats} disabled={loading}>
          {loading ? 'جاري الجلب...' : 'عرض إحصائيات التغذية الراجعة'}
        </Button>
        <Button variant="outline" onClick={handleSendFeedback} disabled={loading}>
          {loading ? 'جاري الحفظ...' : 'حفظ تغذية راجعة'}
        </Button>
        <Button variant="secondary" onClick={handleAnalyzeTrends} disabled={loading}>
          {loading ? 'جاري التحليل...' : 'تحليل الاتجاهات'}
        </Button>
      </div>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>النتيجة</CardTitle>
            <CardDescription>مخرجات حلقة التعلم</CardDescription>
          </CardHeader>
          <CardContent>
            {result.error ? (
              <p className="text-destructive">{result.error}</p>
            ) : (
              renderResultItems()
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default LearningLoopPage;
