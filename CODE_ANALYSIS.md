# AI学习助手 - 代码深度分析
分析时间: $(date)

## 1. 项目结构概览
my_ai_assistant/
├── 📦 后端核心
│ ├── main.py # FastAPI应用主文件
│ ├── ai_backend.py # 百度千帆API集成
│ ├── test_api.py # API测试脚本
│ └── pycache/ # Python字节码缓存
│
├── 🎨 前端界面 (frontend/)
│ ├── index.html # 主页面HTML结构
│ ├── style.css # CSS样式设计
│ └── app.js # JavaScript交互逻辑
│
├── 📊 运维文件
│ ├── server.log # 服务运行日志
│ └── .bashrc # 环境变量配置
│
└── 📚 项目文档
├── PROJECT_STRUCTURE.md # 项目结构说明
└── CODE_ANALYSIS.md # 代码分析文档



## 2. 各文件职责分析

### 2.1 main.py - 后端服务器
职责:
- 创建FastAPI应用实例
- 配置CORS跨域支持
- 定义API路由端点
- 提供静态文件服务
- 启动HTTP服务器

关键组件:
1. FastAPI() - Web框架
2. CORSMiddleware - 跨域处理
3. 路由装饰器 (@app.get)
4. uvicorn - ASGI服务器

### 2.2 ai_backend.py - AI集成层
职责:
- 封装百度千帆API调用
- 处理API认证和请求
- 解析API返回的JSON数据
- 错误处理和降级

技术要点:
1. requests库 - HTTP客户端
2. 环境变量读取 - os.getenv()
3. JSON解析 - response.json()
4. 异常处理 - try/except

### 2.3 index.html - 前端界面
职责:
- 用户交互界面
- 发送请求到后端API
- 显示AI回答
- 响应式设计

技术栈:
1. HTML5 - 页面结构
2. CSS3 - 样式和布局
3. JavaScript - 交互逻辑
4. Fetch API - 异步请求

## 3. 数据流向
用户输入 → 前端JS → HTTP请求 → FastAPI路由 → AI集成 → 百度API → 解析响应 → 返回JSON → 前端显示

## 4. 关键技术点
