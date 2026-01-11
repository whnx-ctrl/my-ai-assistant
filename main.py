# 1. 导入依赖：把需要的工具包拿过来
from fastapi import FastAPI  # 导入FastAPI框架（核心工具，用来创建后端服务）
import uvicorn  # 导入uvicorn（FastAPI的运行服务器，负责把服务跑起来）
from fastapi.middleware.cors import CORSMiddleware  # <-- 新增导入
from ai_backend import ask_qianfan


# 2. 创建服务实例：相当于“启动一个后端服务”
app = FastAPI()  # app就是咱们的后端服务对象，后续所有接口都挂在这个对象上



# 添加CORS中间件 -- 关键！
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应改为你的前端域名，如 ["http://你的IP"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ CORS 中间件已配置")


# 3. 定义第一个接口：根路径 / 
@app.get("/")  # @app.get("/") 是“装饰器”，表示定义一个GET请求的接口，路径是 /
def read_root():  # 这个函数是接口的“处理逻辑”，访问 / 时会执行这个函数
    # 返回一个JSON数据（FastAPI会自动把字典转成JSON，前端能直接解析）
    return {"message": "我的AI助手后端服务已上线！", "status": "running"}

# 4. 定义第二个接口：聊天接口 /chat
@app.get("/chat")  # 定义GET请求的接口，路径是 /chat
def chat(q: str = "你好"):  # q是接口的“参数”，str表示参数类型，"你好"是默认值
    # 模拟AI回复（后续替换成真实大模型调用逻辑即可）
    ai_answer = ask_qianfan(q)
    return {"question": q, "answer": ai_answer}

print("✅ 正在启动服务...")
# 5. 运行服务：让服务在服务器上“跑起来”
if __name__ == "__main__":
    # uvicorn.run 启动服务：
    # app → 要运行的服务对象；
    # host="0.0.0.0" → 允许外网访问（关键！否则只有服务器自己能访问）；
    # port=8000 → 服务运行在8000端口
    print("✅ 正在调用 uvicorn.run()")
    uvicorn.run(app, host="0.0.0.0", port=8000)
