from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.creative_spark.api_integrations import api_integrations

router = APIRouter()


@router.get("/status", response_model=Dict[str, Any])
async def get_api_status():
    """
    الحصول على حالة جميع الـ APIs المكونة
    """
    try:
        status = api_integrations.get_api_status()
        validation = api_integrations.validate_api_keys()

        return {
            "success": True,
            "message": "API status retrieved successfully",
            "data": {
                "api_status": status,
                "api_keys_validation": validation
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving API status: {str(e)}")


@router.get("/test-gemini")
async def test_gemini_api():
    """
    اختبار Google Gemini API
    """
    try:
        result = api_integrations.generate_text_with_gemini(
            "اكتب جملة قصيرة باللغة العربية عن الذكاء الاصطناعي",
            max_tokens=50
        )

        if result["success"]:
            return {
                "success": True,
                "message": "Gemini API test successful",
                "data": result["data"]
            }
        else:
            return {
                "success": False,
                "message": "Gemini API test failed",
                "error": result["error"]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing Gemini API: {str(e)}")


@router.get("/test-google-trends")
async def test_google_trends_api():
    """
    اختبار Google Trends API
    """
    try:
        result = api_integrations.get_google_trends_data(["ذكاء اصطناعي", "تكنولوجيا"])

        if result["success"]:
            return {
                "success": True,
                "message": "Google Trends API test successful",
                "data": {
                    "keywords": result["data"]["keywords"],
                    "source": result["data"]["source"],
                    "has_data": bool(result["data"].get("interest_over_time"))
                }
            }
        else:
            return {
                "success": False,
                "message": "Google Trends API test failed",
                "error": result.get("error", "Unknown error")
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing Google Trends API: {str(e)}")


@router.get("/test-twitter")
async def test_twitter_api():
    """
    اختبار Twitter API
    """
    try:
        result = api_integrations.get_twitter_data(["ذكاء اصطناعي", "تكنولوجيا"], days=3)

        if result["success"]:
            return {
                "success": True,
                "message": "Twitter API test successful",
                "data": {
                    "keywords": result["data"]["keywords"],
                    "total_tweets": result["data"]["total_tweets"],
                    "source": result["data"]["source"]
                }
            }
        else:
            return {
                "success": False,
                "message": "Twitter API test failed",
                "error": result.get("error", "Unknown error")
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing Twitter API: {str(e)}")
