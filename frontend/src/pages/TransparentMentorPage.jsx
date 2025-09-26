import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { transparentMentorService } from '../services/api';

const TransparentMentorPage = () => {
  const [budget, setBudget] = useState(5000);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleExplainPrediction = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await transparentMentorService.explainPrediction({ features: { budget } }, 'model_v1');
      setResult({ type: 'explain', data: res.data });
    } catch (e) {
      setResult({ error: 'حدث خطأ أثناء تفسير التنبؤ' });
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateScenarios = async () => {
    setLoading(true);
    setResult(null);
    try {
      const res = await transparentMentorService.generateAlternativeScenarios({ base: { budget } }, 'ctr', 3);
      setResult({ type: 'scenarios', data: res.data });
    } catch (e) {
      setResult({ error: 'حدث خطأ أثناء توليد السيناريوهات' });
    } finally {
      setLoading(false);
    }
  };

  const renderResultItems = () => {
    if (!result || !Array.isArray(result.data) || result.data.length === 0) {
      return (
        <div className="text-center py-8">
          <div className="text-6xl mb-4">🤷‍♂️</div>
          <p className="text-muted-foreground text-lg">لا توجد نتائج</p>
        </div>
      );
    }

    return (
      <div className="space-y-4">
        {result.data.map((item, index) => (
          <Card key={index} className="bg-muted p-3">
            <p>
              {item.explanation || item.scenario || item.text || JSON.stringify(item)}
            </p>
          </Card>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">المرشد الشفاف</h1>
        <p className="text-muted-foreground">تفسير التنبؤات وتوليد سيناريوهات بديلة</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>مدخلات</CardTitle>
          <CardDescription>أدخل ميزانية افتراضية</CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <Label>الميزانية (دولار)</Label>
            <Input
              type="number"
              value={budget}
              onChange={(e) => setBudget(parseInt(e.target.value || '0', 10))}
            />
          </div>
        </CardContent>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Button onClick={handleExplainPrediction} disabled={loading}>
          {loading ? 'جاري التحليل...' : 'تفسير التنبؤ'}
        </Button>
        <Button variant="outline" onClick={handleGenerateScenarios} disabled={loading}>
          {loading ? 'جاري التوليد...' : 'توليد سيناريوهات بديلة'}
        </Button>
      </div>

      {result && (
        <Card>
          <CardHeader>
            <CardTitle>النتيجة</CardTitle>
            <CardDescription>مخرجات المرشد الشفاف</CardDescription>
          </CardHeader>
          <CardContent>{renderResultItems()}</CardContent>
        </Card>
      )}
    </div>
  );
};

export default TransparentMentorPage;
