from fastapi import APIRouter

from config import BaseConfig as Conf
from qa_app.views.qa_view import router as qa_router

api_router = APIRouter(responses=Conf.DEFAULT_API_RESPONSES)
api_router.include_router(qa_router, prefix="/qa", tags=["qa"])
