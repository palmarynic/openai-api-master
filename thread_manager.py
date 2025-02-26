class ThreadManager:
    def __init__(self, openai_client):
        self.client = openai_client

    def create_thread(self):
        thread = self.client.beta.threads.create()
        return thread.id

    def add_message_to_thread(self, thread_id, role, content):
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content
        )

    def run_assistant(self, thread_id, assistant_id, model="gpt-4"):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
            model=model
        )

        if run.status == "completed":
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)
            return messages.data.content.text.value
        else:
            return None