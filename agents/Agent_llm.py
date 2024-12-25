from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from agents.utils.config import load_api_key, MODEL_NAME

def initialize_llm():
    api_key = load_api_key()
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0.3,
        max_tokens=2000,
        api_key=api_key,
        transport='rest'
    )

def create_outline_prompt():
    template = """
    你是一个经验丰富的小说故事生成器。根据以下初始提示和关键词提示，生成一个详细的小说故事大纲，包括主要内容、章节划分和主要人物描述。

    初始提示:{initial_prompt}
    关键词提示:{keyword_prompts}
    章节总数:{total_chapters}

    返回格式化信息:
    '故事整体大纲':故事整体大纲,
    '第1章主要内容':XXX,
    '第2章主要内容':XXX,
    ...
    '第10章主要内容':XXX,
    '主要人物和其特征介绍':XXX

    请确保内容结构清晰，格式化良好，便于后续使用和参考。
    """
    return PromptTemplate.from_template(template)

def create_chapter_prompt():
    template = """
    基于以下信息生成当前章节号的小说内容:
    
    大纲信息: {outline}
    当前章节号: {chapter_number}
    
    请生成符合上下文连贯性、情节发展合理、小说第一人称、剧情循序渐进、字数1000以上的这一当前章节号的内容。
    """
    return PromptTemplate.from_template(template)

def create_memory_prompt():
    template = """
    从以下章节内容中提取关键信息:
    
    章节内容: {chapter_text}
    章节编号: {chapter_number} 
    
    请提取并返回格式化信息:
    '章节号': 章节号,
    '关键词列表': [大量可以凸显章节内容细节的词],
    '事件1: [包含时间、地点、人物、起因、经过、结果或者进展],
    '事件2: [包含时间、地点、人物、起因、经过、结果或者进展],
    ...
    '事件n: [包含时间、地点、人物、起因、经过、结果或者进展],
    """
    return PromptTemplate.from_template(template)
