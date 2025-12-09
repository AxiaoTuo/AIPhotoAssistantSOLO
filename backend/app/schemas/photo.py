from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ScoreDetail(BaseModel):
    technical: int
    composition: int
    aesthetic: int
    narrative: int


class AnalysisDetail(BaseModel):
    highlights: List[str]
    improvements: List[str]
    suggestions: List[str]


class PhotoAnalyzeResponse(BaseModel):
    id: int
    filename: str
    thumbnail: Optional[str]
    image_data: Optional[str]
    scores: ScoreDetail
    overall_score: int
    analysis: AnalysisDetail
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True


class PhotoListItem(BaseModel):
    id: int
    filename: str
    thumbnail: Optional[str]
    overall_score: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class PhotoListResponse(BaseModel):
    total: int
    items: List[PhotoListItem]
