import axios from 'axios';

// إعداد الإعدادات الافتراضية لـ axios
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة معترض للطلبات لإضافة رمز الوصول
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// إضافة معترض للاستجابات للتعامل مع الأخطاء
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // التعامل مع أخطاء المصادقة
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// خدمات المستخدمين
// خدمات المستخدمين
export const authService = {
  // login يحتاج x-www-form-urlencoded
  login: (credentials) =>
    api.post(
      '/users/login',
      new URLSearchParams({
        username: credentials.username,
        password: credentials.password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    ),

  // register عادي JSON
  register: (userData) => api.post('/users', userData),

  getCurrentUser: () => api.get('/users/me'),
  updateUser: (userData) => api.put('/users/me', userData),
};


// خدمات الحملات
export const campaignService = {
  getCampaigns: (params) => api.get('/campaigns', { params }),
  getCampaign: (id) => api.get(`/campaigns/${id}`),
  createCampaign: (campaignData) => api.post('/campaigns', campaignData),
  updateCampaign: (id, campaignData) => api.put(`/campaigns/${id}`, campaignData),
  deleteCampaign: (id) => api.delete(`/campaigns/${id}`),
  
  // المحتوى
  getContents: (campaignId, params) => api.get(`/campaigns/${campaignId}/contents`, { params }),
  createContent: (campaignId, contentData) => api.post(`/campaigns/${campaignId}/contents`, contentData),
  updateContent: (campaignId, contentId, contentData) => api.put(`/campaigns/${campaignId}/contents/${contentId}`, contentData),
  deleteContent: (campaignId, contentId) => api.delete(`/campaigns/${campaignId}/contents/${contentId}`),
  
  // التوصيات
  getRecommendations: (campaignId, params) => api.get(`/campaigns/${campaignId}/recommendations`, { params }),
  createRecommendation: (campaignId, recommendationData) => api.post(`/campaigns/${campaignId}/recommendations`, recommendationData),
  updateRecommendation: (campaignId, recommendationId, recommendationData) => api.put(`/campaigns/${campaignId}/recommendations/${recommendationId}`, recommendationData),
};

// خدمات العقل الاستراتيجي
export const strategicMindService = {
  predictCTR: (campaignData) => api.post('/strategic-mind/predict-ctr', campaignData),
  predictROI: (campaignData) => api.post('/strategic-mind/predict-roi', campaignData),
  recommendChannels: (campaignData) => api.post('/strategic-mind/recommend-channels', campaignData),
  getKnowledgeRules: (params) => api.get('/strategic-mind/knowledge-rules', { params }),
  evaluateRules: (context, ruleType) => api.post('/strategic-mind/evaluate-rules', { context, rule_type: ruleType }),
};

// خدمات الشرارة الإبداعية
export const creativeSparkService = {
  generateAdCopy: (campaignData, contentType) => api.post('/creative-spark/generate-ad-copy', { ...campaignData, content_type: contentType }),
  generateVisualSuggestions: (campaignData) => api.post('/creative-spark/generate-visual-suggestions', campaignData),
  analyzeImage: (formData) => api.post('/creative-spark/analyze-image', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  analyzeTrends: (campaignData) => api.post('/creative-spark/analyze-trends', campaignData),
  getContentTemplates: (params) => api.get('/creative-spark/content-templates', { params }),
};

// خدمات المرشد الشفاف
export const transparentMentorService = {
  explainPrediction: (predictionData, modelType) => api.post('/transparent-mentor/explain-prediction', { ...predictionData, model_type: modelType }),
  explainRecommendation: (recommendationData, recommendationType) => api.post('/transparent-mentor/explain-recommendation', { ...recommendationData, recommendation_type: recommendationType }),
  generateAlternativeScenarios: (baseData, scenarioType, numScenarios = 3) => api.post('/transparent-mentor/generate-alternative-scenarios', { ...baseData, scenario_type: scenarioType, num_scenarios: numScenarios }),
  generateVisualizationConfig: (data, visualizationType) => api.post('/transparent-mentor/generate-visualization-config', { ...data, visualization_type: visualizationType }),
  generateDecisionPathVisualization: (decisionPath) => api.post('/transparent-mentor/generate-decision-path-visualization', decisionPath),
  generateComparisonVisualization: (scenarios, metrics) => api.post('/transparent-mentor/generate-comparison-visualization', { scenarios, metrics }),
};

// خدمات حلقة التعلم
export const learningLoopService = {
  saveRecommendationFeedback: (recommendationId, feedbackData) => api.post(`/learning-loop/save-recommendation-feedback?recommendation_id=${recommendationId}`, feedbackData),
  getRecommendationFeedbackStats: (campaignId) => api.get('/learning-loop/recommendation-feedback-stats', { params: { campaign_id: campaignId } }),
  collectUserInteractions: (interactionData) => api.post('/learning-loop/collect-user-interactions', interactionData),
  analyzeFeedbackTrends: (days = 30) => api.get('/learning-loop/analyze-feedback-trends', { params: { days } }),
};

export default api;
