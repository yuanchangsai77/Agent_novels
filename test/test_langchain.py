from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from agents.utils.config import load_api_key, MODEL_NAME

api_key = load_api_key()

# 初始化ChatGoogleGenerativeAI，设置transport为'rest'
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,  
    google_api_key=api_key,
    max_tokens=200,
    transport='rest'
)

prompt = PromptTemplate.from_template("""
你是一个智能机器人，负责回答用户提出的问题。
问题:{question}
""")

chain = prompt | llm
r = chain.invoke(input={'question':'什么是agent协作'})
print(r.content)