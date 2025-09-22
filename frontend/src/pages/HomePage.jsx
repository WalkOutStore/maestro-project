import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '../contexts/AuthContext';
import heroBanner from '../assets/images/maestro_hero_banner.png';
import architectureImage from '../assets/images/maestro_architecture.png';
import {
  BrainCircuit,
  Lightbulb,
  Eye,
  RefreshCcw,
  LayoutDashboard,
  ArrowLeft,
} from 'lucide-react';

const HomePage = () => {
  const { isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('strategic-mind');

  const features = [
    {
      id: 'strategic-mind',
      icon: <BrainCircuit size={24} />,
      title: 'العقل الاستراتيجي',
      description:
        'قاعدة معرفة ديناميكية ومحرك استدلال هجين يجمع بين القواعد المنطقية والتعلم الآلي لتقديم تحليلات استراتيجية وتوصيات مدروسة.',
      benefits: [
        'تحليل بيانات السوق والمنافسين',
        'التنبؤ بأداء الحملات التسويقية',
        'توصيات مخصصة لتوزيع الميزانية',
        'تحديد الفرص والتهديدات',
      ],
    },
    {
      id: 'creative-spark',
      icon: <Lightbulb size={24} />,
      title: 'الشرارة الإبداعية',
      description:
        'محرك إبداعي متطور يولد أفكارًا ومحتوى إبداعي يتناسب مع هوية العلامة التجارية واتجاهات السوق الحالية.',
      benefits: [
        'توليد نصوص إعلانية جذابة',
        'اقتراحات بصرية مبتكرة',
        'تحليل اتجاهات المحتوى الرائج',
        'تخصيص المحتوى حسب الجمهور المستهدف',
      ],
    },
    {
      id: 'transparent-mentor',
      icon: <Eye size={24} />,
      title: 'المرشد الشفاف',
      description:
        'نظام تفسير متقدم يوضح القرارات والتوصيات بطريقة سهلة الفهم، مما يعزز الثقة والتعلم.',
      benefits: [
        'تفسير واضح للتنبؤات والتوصيات',
        'عرض مرئي لمسارات القرار',
        'توليد سيناريوهات بديلة للمقارنة',
        'تعزيز فهم العوامل المؤثرة',
      ],
    },
    {
      id: 'learning-loop',
      icon: <RefreshCcw size={24} />,
      title: 'حلقة التعلم التشاركي',
      description:
        'نظام تعلم مستمر يستفيد من تفاعلات المستخدمين لتحسين النماذج وقاعدة المعرفة بشكل تلقائي.',
      benefits: [
        'تحسين مستمر للتوصيات والتنبؤات',
        'التكيف مع تغيرات السوق',
        'الاستفادة من خبرات المستخدمين',
        'تحليل اتجاهات التغذية الراجعة',
      ],
    },
    {
      id: 'interactive-cockpit',
      icon: <LayoutDashboard size={24} />,
      title: 'قمرة القيادة التفاعلية',
      description:
        'لوحة تحكم شاملة تتيح للمستخدمين إدارة حملاتهم التسويقية ومراقبة أدائها بسهولة.',
      benefits: [
        'عرض مرئي للمؤشرات الرئيسية',
        'إدارة متكاملة للحملات',
        'تقارير تفصيلية قابلة للتخصيص',
        'تنبيهات ذكية للفرص والمخاطر',
      ],
    },
  ];

  const activeFeature = features.find((feature) => feature.id === activeTab);

  return (
    <div className="min-h-screen bg-background" dir="rtl">
      {/* قسم الترويسة */}
      <header className="bg-card shadow-sm border-b border-border">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <img src="/src/assets/images/maestro_logo.png" alt="Maestro Logo" className="h-10" />
            <h1 className="text-xl font-bold mr-2">Maestro</h1>
          </div>
          <nav className="hidden md:flex space-x-4 space-x-reverse">
            <Link to="/" className="px-3 py-2 rounded-md hover:bg-muted transition-colors">
              الرئيسية
            </Link>
            <Link to="/features" className="px-3 py-2 rounded-md hover:bg-muted transition-colors">
              المميزات
            </Link>
            <Link to="/pricing" className="px-3 py-2 rounded-md hover:bg-muted transition-colors">
              الأسعار
            </Link>
            <Link to="/about" className="px-3 py-2 rounded-md hover:bg-muted transition-colors">
              عن المنصة
            </Link>
          </nav>
          <div className="flex space-x-4 space-x-reverse">
            {isAuthenticated ? (
              <Link to="/dashboard">
                <Button>لوحة التحكم</Button>
              </Link>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline">تسجيل الدخول</Button>
                </Link>
                <Link to="/register">
                  <Button>إنشاء حساب</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* قسم البطل */}
      <section className="py-16 bg-gradient-to-b from-background to-muted">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-center">
            <div className="md:w-1/2 mb-8 md:mb-0">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">
                الذكاء الاصطناعي المتكامل للتسويق الرقمي
              </h1>
              <p className="text-lg mb-6 text-muted-foreground">
                منصة Maestro تجمع بين قوة الذكاء الاصطناعي والخبرة التسويقية لمساعدتك في تحقيق
                نتائج استثنائية لحملاتك التسويقية.
              </p>
              <div className="flex space-x-4 space-x-reverse">
                <Link to="/register">
                  <Button size="lg" className="px-6">
                    ابدأ الآن مجانًا
                  </Button>
                </Link>
                <Link to="/demo">
                  <Button size="lg" variant="outline" className="px-6">
                    طلب عرض توضيحي
                  </Button>
                </Link>
              </div>
            </div>
            <div className="md:w-1/2">
              <img
                src={heroBanner}
                alt="Maestro Platform"
                className="rounded-lg shadow-xl"
              />
            </div>
          </div>
        </div>
      </section>

      {/* قسم المميزات */}
      <section className="py-16 bg-card">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">المكونات الرئيسية</h2>
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
            {features.map((feature) => (
              <button
                key={feature.id}
                className={`flex flex-col items-center p-4 rounded-lg transition-colors ${
                  activeTab === feature.id
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-card hover:bg-muted'
                }`}
                onClick={() => setActiveTab(feature.id)}
              >
                <div className="mb-2">{feature.icon}</div>
                <h3 className="text-lg font-medium text-center">{feature.title}</h3>
              </button>
            ))}
          </div>
          {activeFeature && (
            <div className="bg-background rounded-lg p-6 shadow-lg border border-border">
              <div className="flex flex-col md:flex-row">
                <div className="md:w-2/3 mb-6 md:mb-0 md:ml-6">
                  <h3 className="text-2xl font-bold mb-4 flex items-center">
                    <span className="ml-2">{activeFeature.icon}</span>
                    {activeFeature.title}
                  </h3>
                  <p className="text-lg mb-6">{activeFeature.description}</p>
                  <h4 className="text-xl font-semibold mb-4">المزايا الرئيسية:</h4>
                  <ul className="space-y-2">
                    {activeFeature.benefits.map((benefit, index) => (
                      <li key={index} className="flex items-center">
                        <span className="ml-2 text-primary">✓</span>
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="md:w-1/3 flex items-center justify-center">
                  <div className="w-48 h-48 rounded-full bg-muted flex items-center justify-center">
                    <div className="text-6xl">{activeFeature.icon}</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      {/* قسم الهيكل */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-4">هيكل النظام المتكامل</h2>
          <p className="text-lg text-center mb-12 max-w-3xl mx-auto">
            تعمل مكونات Maestro معًا بتناغم لتوفير حل شامل للتسويق الرقمي المدعوم بالذكاء
            الاصطناعي.
          </p>
          <div className="flex justify-center">
            <img
              src={architectureImage}
              alt="Maestro Architecture"
              className="rounded-lg shadow-lg max-w-full"
            />
          </div>
        </div>
      </section>

      {/* قسم الدعوة للعمل */}
      <section className="py-16 bg-primary text-primary-foreground">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">جاهز لتحويل استراتيجيتك التسويقية؟</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            انضم إلى الآلاف من المسوقين الذين يستخدمون Maestro لتحقيق نتائج استثنائية في حملاتهم
            التسويقية.
          </p>
          <div className="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4 sm:space-x-reverse">
            <Link to="/register">
              <Button size="lg" variant="secondary" className="px-8">
                ابدأ الآن مجانًا
              </Button>
            </Link>
            <Link to="/contact">
              <Button size="lg" variant="outline" className="px-8 bg-transparent border-primary-foreground hover:bg-primary-foreground/10">
                تواصل معنا
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* التذييل */}
      <footer className="bg-card border-t border-border py-12">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <img src="/src/assets/images/maestro_logo.png" alt="Maestro Logo" className="h-8" />
                <h3 className="text-lg font-bold mr-2">Maestro</h3>
              </div>
              <p className="text-muted-foreground">
                منصة الذكاء الاصطناعي المتكاملة للتسويق الرقمي
              </p>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">المنتج</h4>
              <ul className="space-y-2">
                <li>
                  <Link to="/features" className="text-muted-foreground hover:text-foreground">
                    المميزات
                  </Link>
                </li>
                <li>
                  <Link to="/pricing" className="text-muted-foreground hover:text-foreground">
                    الأسعار
                  </Link>
                </li>
                <li>
                  <Link to="/roadmap" className="text-muted-foreground hover:text-foreground">
                    خارطة الطريق
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">الشركة</h4>
              <ul className="space-y-2">
                <li>
                  <Link to="/about" className="text-muted-foreground hover:text-foreground">
                    عن المنصة
                  </Link>
                </li>
                <li>
                  <Link to="/blog" className="text-muted-foreground hover:text-foreground">
                    المدونة
                  </Link>
                </li>
                <li>
                  <Link to="/careers" className="text-muted-foreground hover:text-foreground">
                    الوظائف
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="text-lg font-semibold mb-4">الدعم</h4>
              <ul className="space-y-2">
                <li>
                  <Link to="/contact" className="text-muted-foreground hover:text-foreground">
                    اتصل بنا
                  </Link>
                </li>
                <li>
                  <Link to="/docs" className="text-muted-foreground hover:text-foreground">
                    التوثيق
                  </Link>
                </li>
                <li>
                  <Link to="/faq" className="text-muted-foreground hover:text-foreground">
                    الأسئلة الشائعة
                  </Link>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-border mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-muted-foreground">
              &copy; {new Date().getFullYear()} Maestro. جميع الحقوق محفوظة.
            </p>
            <div className="flex space-x-4 space-x-reverse mt-4 md:mt-0">
              <Link to="/privacy" className="text-sm text-muted-foreground hover:text-foreground">
                سياسة الخصوصية
              </Link>
              <Link to="/terms" className="text-sm text-muted-foreground hover:text-foreground">
                شروط الاستخدام
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;
