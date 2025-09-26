import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { creativeSparkService } from '../services/api';

const CreativeSparkPage = () => {
  const [industry, setIndustry] = useState('technology');
  const [product, setProduct] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleGenerateCopy = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await creativeSparkService.generateAdCopy({ industry, product }, 'ad_copy');
      setResult({ type: 'copy', data: res.data });
    } catch (e) {
      setResult({ error: e?.response?.data?.detail || 'حدث خطأ أثناء توليد النص الإعلاني' });
    } finally {
      setLoading(false);
    }
  };

  const handleVisualSuggestions = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await creativeSparkService.generateVisualSuggestions({ industry, product });
      setResult({ type: 'visuals', data: res.data });
    } catch (e) {
      setResult({ error: e?.response?.data?.detail || 'حدث خطأ أثناء جلب الاقتراحات البصرية' });
    } finally {
      setLoading(false);
    }
  };

  const handleTemplates = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await creativeSparkService.getContentTemplates();
      setResult({ type: 'templates', data: res.data });
    } catch (e) {
      setResult({ error: e?.response?.data?.detail || 'حدث خطأ أثناء جلب النماذج' });
    } finally {
      setLoading(false);
    }
  };

  const renderResultItems = () => {
    if (!result || !Array.isArray(result.data)) return null;

    return (
      <div className="space-y-4">
        {result.data.map((item, index) => (
          <Card key={index} className="bg-muted p-3">
            <p>{item.text || JSON.stringify(item)}</p>
          </Card>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">الشرارة الإبداعية</h1>
        <p className="text-muted-foreground">توليد نصوص إعلانية واقتراحات بصرية ونماذج محتوى</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>مدخلات</CardTitle>
          <CardDescription>اختر الصناعة وأدخل اسم المنتج/الخدمة</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-3">
          <div className="space-y-2">
            <Label>الصناعة</Label>
            <Select value={industry} onValueChange={setIndustry}>
              <SelectTrigger>
                <SelectValue placeholder="اختر الصناعة" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="technology">التكنولوجيا</SelectItem>
                <SelectItem value="retail">التجزئة</SelectItem>
                <SelectItem value="finance">المالية</SelectItem>
                <SelectItem value="healthcare">الرعاية الصحية</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label>المنتج/الخدمة</Label>
            <Input value={product} onChange={(e) => setProduct(e.target.value)} placeholder="مثال: نظارات ذكية" />
          </div>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button onClick={handleGenerateCopy} disabled={loading}>
          {loading ? 'جاري التوليد...' : 'توليد نص إعلاني'}
        </Button>
        <Button variant="outline" onClick={handleVisualSuggestions} disabled={loading}>
          {loading ? 'جاري التحليل...' : 'اقتراحات بصرية'}
        </Button>
        <Button variant="secondary" onClick={handleTemplates} disabled={loading}>
          {loading ? '...جاري الجلب' : 'نماذج محتوى'}
        </Button>
      </div>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>النتيجة</CardTitle>
            <CardDescription>مخرجات الخدمة</CardDescription>
          </CardHeader>
          <CardContent>
            {result.error ? (
              <p className="text-destructive">{result.error}</p>
            ) : result.data && result.data.length === 0 ? (
              <div className="text-center py-8">
                <div className="text-6xl mb-4">🤷‍♂️</div>
                <p className="text-muted-foreground text-lg">لا توجد نتائج</p>
                <p className="text-sm text-muted-foreground mt-2">
                  جرّب تغيير الصناعة أو المنتج، أو تأكد من نوع المحتوى
                </p>
              </div>
            ) : (
              renderResultItems()
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default CreativeSparkPage;
