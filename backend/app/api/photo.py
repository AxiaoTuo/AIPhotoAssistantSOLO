import os
import json
import base64
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.photo import Photo
from app.schemas.photo import PhotoAnalyzeResponse, PhotoListResponse, PhotoListItem
from app.services.ai_service import AIService
from app.utils.image import compress_image, generate_thumbnail

router = APIRouter(prefix="/api/photo", tags=["photo"])

# 确保上传目录存在
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze", response_model=PhotoAnalyzeResponse)
async def analyze_photo(
    file: UploadFile = File(...),
    model: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    上传图片并进行AI分析
    :param file: 上传的图片文件
    :param model: 使用的AI模型，可选，默认使用配置中的模型
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 分析结果
    """
    # 检查文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请上传图片文件"
        )
    
    # 读取文件内容
    file_content = await file.read()
    
    # 压缩图片
    compressed_content, img_format = compress_image(file_content)
    
    # 生成缩略图
    thumbnail = generate_thumbnail(compressed_content)
    
    # 保存图片到临时目录
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(compressed_content)
    
    try:
        # 调用AI服务进行分析
        ai_service = AIService(model=model)
        analysis_result = await ai_service.analyze_photo(file_path, file.filename)
        
        # 将压缩后的图片转换为 base64 字符串
        image_base64 = base64.b64encode(compressed_content).decode('utf-8')
        img_format = 'jpeg'  # 压缩后统一为 jpeg 格式
        full_image_data = f'data:image/{img_format};base64,{image_base64}'
        
        # 创建图片记录
        photo = Photo(
            user_id=current_user.id,
            filename=file.filename,
            thumbnail=thumbnail,
            image_data=full_image_data,
            score_tech=analysis_result["scores"]["technical"],
            score_comp=analysis_result["scores"]["composition"],
            score_aes=analysis_result["scores"]["aesthetic"],
            score_story=analysis_result["scores"]["narrative"],
            overall_score=analysis_result["overall_score"],
            analysis=json.dumps(analysis_result["analysis"]),
            model_used=ai_service.model
        )
        
        db.add(photo)
        await db.commit()
        await db.refresh(photo)
        
        # 构建响应
        return {
            "id": photo.id,
            "filename": photo.filename,
            "thumbnail": photo.thumbnail,
            "image_data": photo.image_data,
            "scores": {
                "technical": photo.score_tech,
                "composition": photo.score_comp,
                "aesthetic": photo.score_aes,
                "narrative": photo.score_story
            },
            "overall_score": photo.overall_score,
            "analysis": json.loads(photo.analysis),
            "model_used": photo.model_used,
            "created_at": photo.created_at
        }
        
    finally:
        # 清理临时文件
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/history", response_model=PhotoListResponse)
async def get_history(
    page: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取历史记录列表
    :param page: 页码，默认1
    :param page_size: 每页数量，默认10
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 历史记录列表
    """
    # 计算偏移量
    offset = (page - 1) * page_size
    
    # 查询总数
    total_result = await db.execute(
        select(Photo).where(Photo.user_id == current_user.id)
    )
    total = len(total_result.scalars().all())
    
    # 查询分页数据
    result = await db.execute(
        select(Photo)
        .where(Photo.user_id == current_user.id)
        .order_by(Photo.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    photos = result.scalars().all()
    
    # 构建响应
    return {
        "total": total,
        "items": [{
            "id": photo.id,
            "filename": photo.filename,
            "thumbnail": photo.thumbnail,
            "overall_score": photo.overall_score,
            "created_at": photo.created_at
        } for photo in photos]
    }


@router.get("/{photo_id}", response_model=PhotoAnalyzeResponse)
async def get_photo_detail(
    photo_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取单条分析详情
    :param photo_id: 图片ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    :return: 分析详情
    """
    result = await db.execute(
        select(Photo).where(Photo.id == photo_id, Photo.user_id == current_user.id)
    )
    photo = result.scalar_one_or_none()
    
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图片不存在"
        )
    
    # 构建响应
    try:
        analysis_data = json.loads(photo.analysis) if photo.analysis else {
            "highlights": [],
            "improvements": [],
            "suggestions": []
        }
    except json.JSONDecodeError:
        analysis_data = {
            "highlights": [],
            "improvements": [],
            "suggestions": []
        }
    
    return {
        "id": photo.id,
        "filename": photo.filename,
        "thumbnail": photo.thumbnail,
        "image_data": photo.image_data,
        "scores": {
            "technical": photo.score_tech,
            "composition": photo.score_comp,
            "aesthetic": photo.score_aes,
            "narrative": photo.score_story
        },
        "overall_score": photo.overall_score,
        "analysis": analysis_data,
        "model_used": photo.model_used,
        "created_at": photo.created_at
    }


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_photo(
    photo_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    删除分析记录
    :param photo_id: 图片ID
    :param current_user: 当前登录用户
    :param db: 数据库会话
    """
    result = await db.execute(
        delete(Photo).where(Photo.id == photo_id, Photo.user_id == current_user.id)
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="图片不存在"
        )
    
    await db.commit()
    return None
