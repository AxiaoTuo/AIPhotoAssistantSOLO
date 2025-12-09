from datetime import datetime
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, Optional

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    thumbnail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    image_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # 存储原图片或压缩后的图片

    # 四维度评分
    score_tech: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    score_comp: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    score_aes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    score_story: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    overall_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # 分析结果
    analysis: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="photos")
