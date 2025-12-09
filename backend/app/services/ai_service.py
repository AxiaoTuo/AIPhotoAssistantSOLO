from typing import Dict, Any, Optional
from app.core.config import settings

# 导入不同模型的客户端
from app.services.deepseek_client import DeepSeekClient
from app.services.openai_client import OpenAIClient
from app.services.claude_client import ClaudeClient


class AIService:
    def __init__(self, model: Optional[str] = None):
        self.model = model or settings.DEFAULT_AI_MODEL
        self.client = self._get_client()
    
    def _get_client(self):
        """根据模型名称获取对应的客户端实例"""
        if self.model == "deepseek":
            return DeepSeekClient()
        elif self.model == "openai":
            return OpenAIClient()
        elif self.model == "claude":
            return ClaudeClient()
        else:
            raise ValueError(f"不支持的模型: {self.model}")
    
    async def analyze_photo(self, image_path: str, filename: str) -> Dict[str, Any]:
        """统一的图片分析接口"""
        return await self.client.analyze_photo(image_path, filename)
    
    def switch_model(self, model: str):
        """切换 AI 模型"""
        self.model = model
        self.client = self._get_client()
