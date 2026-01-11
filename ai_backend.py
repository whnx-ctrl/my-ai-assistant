import os
import requests
import json

def ask_qianfan(question):
    #调用百度千帆API（使用qwen3-14b模型）
    api_key=os.getenv('BAIDU_API_KEY')
    if not api_key:
        return "错误：未设置 BAIDU_API_KEY 环境变量"
    url = "https://qianfan.baidubce.com/v2/responses"
    # 请求头：告诉API服务器“你是谁”“你发的是什么格式的数据”
    headers = {
        "Authorization": f"Bearer {api_key}",  # 身份验证：用API密钥证明你有权调用
        "Content-Type": "application/json"     # 告诉服务器：我发的请求体是JSON格式
    }
    # 请求体：发给API的具体数据（问题+要使用的模型）
    data = {
        "input": question,  # 你要问AI的问题
        "model": "qwen3-14b"  # 要调用的模型ID（从百度千帆官方文档查的）
    }
    try:
        #发送POST请求：向API地址发数据,超过时间30秒（防止服务器卡死）
        response = requests.post(url,headers=headers,json=data,timeout=120)
        response.raise_for_status() #检查请求是否成功
        result = response.json()

        # 直接提取文本
        raw_text = result['output'][0]['content'][0]['text']
        # 简单清理
        # 移除所有空白字符（空格、换行、制表符等），只保留一个空格分隔
        import re
        cleaned = ' '.join(raw_text.split())
        return cleaned

    except requests.exceptions.RequestException as e:
        return f"网络请求失败: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"解析响应失败: {e}，原始响应: {response.text}"
