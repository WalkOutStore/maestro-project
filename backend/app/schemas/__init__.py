from app.schemas.user import (
    User, UserCreate, UserUpdate, UserInDB,
    Token, TokenPayload
)
from app.schemas.campaign import (
    Campaign, CampaignCreate, CampaignUpdate, CampaignWithDetails,
    Content, ContentCreate, ContentUpdate,
    Recommendation, RecommendationCreate, RecommendationUpdate
)
from app.schemas.knowledge_base import (
    KnowledgeRule, KnowledgeRuleCreate, KnowledgeRuleUpdate,
    MLModel, MLModelCreate, MLModelUpdate,
    TrendData, TrendDataCreate,
    ContentTemplate, ContentTemplateCreate, ContentTemplateUpdate
)
