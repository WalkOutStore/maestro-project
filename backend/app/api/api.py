from fastapi import APIRouter

from app.api.endpoints import users, campaigns, strategic_mind, creative_spark, transparent_mentor, learning_loop, achievements
from app.api.api_integrations import router as api_integrations_router


api_router = APIRouter()

# إضافة مسارات API
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(strategic_mind.router, prefix="/strategic-mind", tags=["strategic-mind"])
api_router.include_router(creative_spark.router, prefix="/creative-spark", tags=["creative-spark"])
api_router.include_router(transparent_mentor.router, prefix="/transparent-mentor", tags=["transparent-mentor"])
api_router.include_router(learning_loop.router, prefix="/learning-loop", tags=["learning-loop"])
api_router.include_router(api_integrations_router, prefix="/api-integrations", tags=["api-integrations"])
