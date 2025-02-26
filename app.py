import os
from flask import Flask, request, jsonify, render_template, session
import logging
from dotenv import load_dotenv
from thread_manager import ThreadManager
import openai

# 載入環境變數
load_dotenv()
client = openai.OpenAI()
# 初始化 Flask 應用程式
app = Flask(__name__)

# 初始化 OpenAI 客戶端
openai.api_key = os.getenv("OPENAI_API_KEY")

# 助手 ID 和向量儲存庫 ID
ASSISTANT_ID = os.getenv("ASSISTANT_ID")
VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

# 檢查必要的環境變數
if not all([openai.api_key, ASSISTANT_ID, VECTOR_STORE_ID]):
    raise ValueError("缺少必要的環境變數")
# Flask route to render the HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assist', methods=['POST'])
def assist():
    try:
        # 取得使用者查詢
        data = request.get_json()
        query = data.get('query')

        # 使用 ThreadManager 處理執行緒
        thread_manager = ThreadManager(openai)
        thread_id = thread_manager.create_thread()
        thread_manager.add_message_to_thread(thread_id, "user", query)

        # 指定 GPT 模型
        model = "gpt-4o"  # 或其他可用的 GPT 模型
        response = thread_manager.run_assistant(thread_id, ASSISTANT_ID, model)

        if response:
            return jsonify({"response": response})
        else:
            return jsonify({"error": "助手執行失敗"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    assistant = client.beta.assistants.update(
        assistant_id=ASSISTANT_ID,
        tool_resources=[
            {
                "type": "file_search",
                "file_search": {
                    "vector_store_ids": [VECTOR_STORE_ID]
                }
            }
        ]
    )