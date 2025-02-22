import os
from dotenv import load_dotenv
import openai
load_dotenv()
class AssistantManager:

    assistant_id = None

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = openai
        self.model = model

        # 使用已存在的 Assistant ID
        AssistantManager.assistant_id = os.getenv("ASSISTANT_ID")  # 替換為你的 Assistant ID
        # Retrieve existing assistant if ID is already set
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(assistant_id=AssistantManager.assistant_id)
        else:
            self.create_assistant(
                name="assist' Assistant",
                instructions="""你是大光長榮的AI助手，你只回答文件內的資訊。""",
                tools=[
                    {"type": "file_search"}
                ],

            )

    def create_assistant(self, name, instructions, tools):
        assistant_obj = self.client.beta.assistants.create(name=name, instructions=instructions, tools=tools,  model=self.model)
        AssistantManager.assistant_id = assistant_obj.id
        self.assistant = assistant_obj
