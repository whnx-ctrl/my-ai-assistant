from ai_backend import ask_qianfan

if __name__=="__main__":
    test_question = "你好，请用一句话介绍你自己。"
    print(f"提问：{test_question}")
    answer = ask_qianfan(test_question)
    print(f"回答：{answer}")
