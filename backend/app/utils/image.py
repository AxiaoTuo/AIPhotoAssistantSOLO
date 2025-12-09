from PIL import Image
import io
import base64
from typing import Tuple, Optional


def compress_image(image_data: bytes, target_size: int = 1024 * 1024, quality: int = 85) -> Tuple[bytes, str]:
    """
    压缩图片，目标大小默认1MB
    :param image_data: 原始图片数据
    :param target_size: 目标大小（字节）
    :param quality: 初始质量
    :return: (压缩后的图片数据, 图片格式)
    """
    img = Image.open(io.BytesIO(image_data))
    
    # 获取原始格式
    img_format = img.format or 'JPEG'
    
    # 确保图片是RGB格式，JPEG不支持RGBA
    if img.mode == 'RGBA':
        # 将RGBA转换为RGB，使用白色作为背景
        img_rgb = Image.new('RGB', img.size, (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[3])  # 使用alpha通道作为遮罩
        img = img_rgb
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 如果已经小于目标大小，直接返回
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format=img_format, quality=quality)
    img_bytes = img_byte_arr.getvalue()
    
    if len(img_bytes) <= target_size:
        return img_bytes, img_format
    
    # 逐步降低质量直到满足大小要求
    while len(img_bytes) > target_size and quality > 10:
        quality -= 5
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img_format, quality=quality)
        img_bytes = img_byte_arr.getvalue()
    
    # 如果质量已经降到10%还是太大，就调整尺寸
    if len(img_bytes) > target_size:
        # 计算缩放比例
        scale = (target_size / len(img_bytes)) ** 0.5
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img_format, quality=quality)
        img_bytes = img_byte_arr.getvalue()
    
    return img_bytes, img_format


def generate_thumbnail(image_data: bytes, size: Tuple[int, int] = (100, 100)) -> str:
    """
    生成缩略图并转换为base64编码
    :param image_data: 原始图片数据
    :param size: 缩略图尺寸
    :return: base64编码的缩略图
    """
    img = Image.open(io.BytesIO(image_data))
    
    # 确保图片是RGB格式，JPEG不支持RGBA
    if img.mode == 'RGBA':
        # 将RGBA转换为RGB，使用白色作为背景
        img_rgb = Image.new('RGB', img.size, (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[3])  # 使用alpha通道作为遮罩
        img = img_rgb
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # 生成缩略图，保持宽高比
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    # 保存为JPEG
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=70)
    img_bytes = img_byte_arr.getvalue()
    
    # 转换为base64
    base64_thumbnail = base64.b64encode(img_bytes).decode('utf-8')
    
    return f"data:image/jpeg;base64,{base64_thumbnail}"


def get_image_metadata(image_data: bytes) -> Optional[dict]:
    """
    获取图片元数据
    :param image_data: 原始图片数据
    :return: 图片元数据字典
    """
    try:
        img = Image.open(io.BytesIO(image_data))
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode
        }
    except Exception:
        return None
