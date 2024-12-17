import os

PROXY = os.getenv('PROXY')
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL', "postgresql+asyncpg://weiqun:123456@localhost:15432/ai-chat")
MAX_MESSAGE_CONTEXT_LENGTH = int(os.getenv('MAX_MESSAGE_CONTEXT_LENGTH', 50))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')