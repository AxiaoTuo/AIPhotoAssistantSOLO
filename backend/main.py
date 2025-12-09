from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield


app = FastAPI(
    title="摄影初学者AI图片评价系统",
    description="利用AI大模型为摄影初学者提供图片评价和学习指导",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": "摄影初学者AI图片评价系统 API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
