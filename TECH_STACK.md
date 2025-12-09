# 摄影初学者AI图片评价系统 - 技术文档

## 项目概述
轻量级前后端分离个人项目，利用AI大模型为摄影初学者提供图片评价和学习指导。

---

## 技术栈

### 前端 (frontend/)
| 类别 | 技术选型 | 版本建议 | 说明 |
|------|---------|---------|------|
| 框架 | Vue 3 + Composition API | ^3.4 | 响应式、组件化 |
| 构建 | Vite | ^5.0 | 快速开发体验 |
| UI | Element Plus | ^2.5 | 企业级组件库 |
| 状态 | Pinia | ^2.1 | 轻量状态管理 |
| HTTP | Axios | ^1.6 | 请求封装 |
| 图表 | ECharts | ^5.4 | 雷达图展示 |
| 路由 | Vue Router | ^4.2 | 前端路由 |

### 后端 (backend/)
| 类别 | 技术选型 | 版本建议 | 说明 |
|------|---------|---------|------|
| 框架 | FastAPI | ^0.109 | 高性能、自动文档 |
| ORM | SQLAlchemy | ^2.0 | 数据库操作 |
| 数据库 | SQLite | 内置 | 轻量、无需安装 |
| 认证 | python-jose | ^3.3 | JWT Token |
| 密码 | passlib[bcrypt] | ^1.7 | 密码哈希 |
| 图片 | Pillow | ^10.0 | 图片预处理 |
| 环境 | python-dotenv | ^1.0 | 环境变量管理 |

### AI 模型层
统一接口抽象，支持切换：
- **OpenAI GPT-4V** - 视觉理解能力强
- **Anthropic Claude** - 擅长教育性解释
- **DeepSeek** - 性价比高，国内访问稳定

---

## 项目结构

```
AIPhotoAssistant/
├── frontend/                    # Vue 3 前端
│   ├── public/
│   ├── src/
│   │   ├── api/                # API 接口封装
│   │   │   ├── index.js        # Axios 实例
│   │   │   ├── auth.js         # 认证接口
│   │   │   └── photo.js        # 图片分析接口
│   │   ├── components/         # 公共组件
│   │   │   ├── ImageUpload.vue # 上传组件
│   │   │   ├── ScoreRadar.vue  # 雷达图
│   │   │   └── ResultCard.vue  # 结果卡片
│   │   ├── views/              # 页面视图
│   │   │   ├── Home.vue        # 首页/上传
│   │   │   ├── Login.vue       # 登录
│   │   │   ├── Register.vue    # 注册
│   │   │   ├── History.vue     # 历史记录
│   │   │   └── Detail.vue      # 分析详情
│   │   ├── stores/             # Pinia 状态管理
│   │   │   ├── user.js         # 用户状态
│   │   │   └── photo.js        # 图片状态
│   │   ├── router/             # 路由配置
│   │   │   └── index.js
│   │   ├── utils/              # 工具函数
│   │   │   └── image.js        # 图片压缩
│   │   ├── styles/             # 全局样式
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── backend/                     # FastAPI 后端
│   ├── app/
│   │   ├── __init__.py
│   │   ├── api/                # API 路由
│   │   │   ├── __init__.py
│   │   │   ├── auth.py         # 认证路由
│   │   │   └── photo.py        # 图片分析路由
│   │   ├── core/               # 核心配置
│   │   │   ├── __init__.py
│   │   │   ├── config.py       # 配置管理
│   │   │   ├── security.py     # JWT 认证
│   │   │   └── database.py     # 数据库连接
│   │   ├── models/             # 数据库模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── photo.py
│   │   ├── schemas/            # Pydantic 模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── photo.py
│   │   ├── services/           # 业务逻辑
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py   # AI 统一服务入口
│   │   │   ├── openai_client.py
│   │   │   ├── claude_client.py
│   │   │   └── deepseek_client.py
│   │   └── utils/              # 工具函数
│   │       ├── __init__.py
│   │       └── image.py        # 图片处理
│   ├── uploads/                # 上传文件临时目录
│   ├── main.py                 # 应用入口
│   ├── requirements.txt        # 依赖列表
│   └── .env.example            # 环境变量示例
│
├── TECH_STACK.md               # 本技术文档
├── README.md                   # 项目说明
└── .gitignore
```

---

## 核心功能

### 1. 用户认证（简单版）
- 账号密码注册/登录
- JWT Token 认证（有效期7天）
- 无需邮箱验证，简化流程

### 2. 图片上传与分析
- 前端 Canvas 压缩（目标 < 1MB）
- 支持 JPG/PNG/WebP 格式
- EXIF 信息提取（可选）
- 异步分析，支持流式返回

### 3. AI 四维度评价系统

| 维度 | 评分范围 | 评价要点 |
|------|---------|---------|
| 技术 | 0-100 | 曝光准确性、对焦精准度、景深运用、画面稳定性 |
| 构图 | 0-100 | 三分法/黄金分割、引导线、画面平衡、空间层次 |
| 美学 | 0-100 | 色彩和谐、光影效果、氛围营造、视觉冲击力 |
| 叙事 | 0-100 | 主题表达、情感传递、创意独特性、故事性 |

### 4. 历史记录
- 分页列表展示
- 缩略图预览
- 详情查看
- 成长曲线（可选）

### 5. 可视化展示
- **雷达图**: 四维度得分直观对比
- **详细点评**: 优缺点分析
- **改进建议**: 具体可操作的提升建议

---

## API 设计

### 认证接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 图片分析接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/photo/analyze` | 上传图片并分析 |
| GET | `/api/photo/history` | 获取历史记录列表 |
| GET | `/api/photo/{id}` | 获取单条分析详情 |
| DELETE | `/api/photo/{id}` | 删除分析记录 |

### 请求/响应示例

**登录请求**
```json
POST /api/auth/login
{
  "username": "photographer",
  "password": "secret123"
}
```

**登录响应**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**分析响应**
```json
{
  "id": 1,
  "scores": {
    "technical": 75,
    "composition": 82,
    "aesthetic": 68,
    "narrative": 71
  },
  "overall_score": 74,
  "analysis": {
    "highlights": ["构图运用三分法，主体突出", "色彩和谐"],
    "improvements": ["背景略显杂乱", "可尝试更低角度"],
    "suggestions": ["后期可适当提高对比度", "裁剪去除边缘干扰元素"]
  },
  "model_used": "deepseek",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 数据库设计

### users 表
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PK, AUTO | 主键 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希 |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |
| updated_at | DATETIME | ON UPDATE | 更新时间 |

### photos 表
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INTEGER | PK, AUTO | 主键 |
| user_id | INTEGER | FK → users.id | 用户ID |
| filename | VARCHAR(255) | NOT NULL | 原文件名 |
| thumbnail | TEXT | | 缩略图Base64 |
| score_tech | INTEGER | | 技术分 (0-100) |
| score_comp | INTEGER | | 构图分 (0-100) |
| score_aes | INTEGER | | 美学分 (0-100) |
| score_story | INTEGER | | 叙事分 (0-100) |
| overall_score | INTEGER | | 综合分 |
| analysis | TEXT | | 详细分析(JSON) |
| model_used | VARCHAR(50) | | 使用的AI模型 |
| created_at | DATETIME | DEFAULT NOW | 创建时间 |

---

## 环境变量配置

在 `backend/.env` 中配置：

```env
# ============ AI API Keys ============
# 至少配置一个即可使用
OPENAI_API_KEY=sk-xxxx
OPENAI_BASE_URL=https://api.openai.com/v1

ANTHROPIC_API_KEY=sk-ant-xxxx

DEEPSEEK_API_KEY=sk-xxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# 默认使用的模型: openai / claude / deepseek
DEFAULT_AI_MODEL=deepseek

# ============ JWT 配置 ============
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_DAYS=7

# ============ 数据库 ============
DATABASE_URL=sqlite:///./app.db

# ============ 应用配置 ============
DEBUG=true
CORS_ORIGINS=http://localhost:5173
```

---

## 快速开始

### 后端启动
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key

# 启动服务
python -m uvicorn main:app --reload --port 8000
```

### 前端启动
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问
- 前端: http://localhost:5173
- 后端 API 文档: http://localhost:8000/docs

---

## 开发规范

### Git 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

### 代码风格
- **前端**: ESLint + Prettier
- **后端**: Black + isort

---

## 后续扩展方向
- [ ] 多图批量分析
- [ ] 分析历史对比
- [ ] 学习路径推荐
- [ ] 社区分享功能
- [ ] 移动端适配
