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
        response = requests.post(url,headers=headers,json=data,timeout=30)
        response.raise_for_status() #检查请求是否成功
        result = response.json()


        #调式后的代码
        # 方法1：使用链式.get()安全访问
        # 直接根据观察到的结构提取
        # 结构：result['output'][0]['content'][0]['text']
        answer = result.get('output', [{}])[0].get('content', [{}])[0].get('text', '')
        if answer:
            return answer
        else:
            # 如果上述方法失败，尝试其他可能的字段
            if 'output' in result:
                # 输出可能直接包含文本
                output_data = result['output']
                if isinstance(output_data, str):
                    return output_data
                elif isinstance(output_data, list) and len(output_data) > 0:
                    return str(output_data)
            return f"未能提取回答，可用字段: {list(result.keys())}"
        #解析AI的回答（最初用来调试用的代码，查询到放回的json形式后即可注销）
        #if 'output' in result:
        #    answer = result['output']
        #elif 'choices' in result and len(result['choices']) > 0:
        #    answer = result['choices'][0].get('message', {}).get('content', str(result))
        #elif 'result' in result:
        #    answer = result['result']
        #else:
            # 调试用：如果解析失败，返回原始响应（方便找问题）
        #    answer = f"（调试信息）未能解析标准答案，原始响应：{json.dumps(result, ensure_ascii=False)[:200]}"
        #return answer
    # 异常处理：工业化项目必须有，防止程序崩溃
    except requests.exceptions.RequestException as e:
        return f"网络请求失败: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"解析响应失败: {e}，原始响应: {response.text}"
