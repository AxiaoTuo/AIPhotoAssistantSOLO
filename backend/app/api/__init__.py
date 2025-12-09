from fastapi import APIRouter
from app.api import auth, photo

# 创建主路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(auth.router)
api_router.include_router(photo.router)
