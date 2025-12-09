import aiohttp
import base64
import json
from typing import Dict, Any
from app.core.config import settings


class ClaudeClient:
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    async def analyze_photo(self, image_path: str, filename: str) -> Dict[str, Any]:
        """使用 Claude API 分析照片"""
        # 读取图片并转换为 base64
        with open(image_path, "rb") as f:
            image_data = f.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        
        # 构建 prompt
        prompt = self._build_prompt()
        
        # 构建请求体
        payload = {
            "model": "claude-3-opus-20240229",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 1000
        }
        
        # 发送请求
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=payload
            ) as response:
                response_data = await response.json()
                
                if response.status != 200:
                    raise Exception(f"Claude API 调用失败: {response_data}")
                
                # 解析响应
                content = response_data["content"][0]["text"]
                return self._parse_response(content)
    
    def _build_prompt(self) -> str:
        """构建用于分析照片的 prompt"""
        return """
你是一位专业的摄影导师，请从以下四个维度为这张照片进行评分和点评：

1. 技术 (Technical): 评分范围 0-100，评价要点包括曝光准确性、对焦精准度、景深运用、画面稳定性
2. 构图 (Composition): 评分范围 0-100，评价要点包括三分法/黄金分割、引导线、画面平衡、空间层次
3. 美学 (Aesthetic): 评分范围 0-100，评价要点包括色彩和谐、光影效果、氛围营造、视觉冲击力
4. 叙事 (Narrative): 评分范围 0-100，评价要点包括主题表达、情感传递、创意独特性、故事性

请按照以下严格的 JSON 格式输出结果，不要添加任何额外的文本或解释：
{
  "scores": {
    "technical": 85,
    "composition": 78,
    "aesthetic": 82,
    "narrative": 75
  },
  "analysis": {
    "highlights": ["构图运用三分法，主体突出", "色彩和谐，整体氛围统一"],
    "improvements": ["背景略显杂乱", "可尝试更低的拍摄角度"],
    "suggestions": ["后期适当提高对比度", "裁剪去除边缘干扰元素"]
  }
}

请注意：
- 分数必须是整数
- 评价要客观、具体、可操作
- 先肯定优点，再指出不足
- 建议要能立刻实践
- 语言要友好，鼓励为主
        """
    
    def _parse_response(self, content: str) -> Dict[str, Any]:
        """解析 API 响应，提取评分和分析结果"""
        # 清理响应内容，确保是纯 JSON
        import re
        import json
        
        # 移除可能的markdown格式
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        
        # 使用正则表达式提取JSON内容
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise Exception(f"无法解析 Claude API 响应: {content}")
        
        json_content = json_match.group(0)
        data = json.loads(json_content)
        
        # 确保analysis是字典格式
        analysis = data.get("analysis", {})
        if isinstance(analysis, str):
            try:
                analysis = json.loads(analysis)
            except json.JSONDecodeError:
                analysis = {}
        
        # 确保analysis包含必要的字段
        if "highlights" not in analysis:
            analysis["highlights"] = []
        if "improvements" not in analysis:
            analysis["improvements"] = []
        if "suggestions" not in analysis:
            analysis["suggestions"] = []
        
        # 计算综合评分
        scores = data["scores"]
        overall_score = int((scores["technical"] + scores["composition"] + scores["aesthetic"] + scores["narrative"]) / 4)
        
        return {
            "scores": scores,
            "overall_score": overall_score,
            "analysis": analysis
        }
