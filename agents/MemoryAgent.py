# MemoryAgent.py

import os
import json
from agents.Agent_llm import initialize_llm, create_memory_prompt

class MemoryAgent:
    def __init__(self, memory_dir='output/memory'):
        self.memory_dir = memory_dir
        self.llm = initialize_llm()  
        self.prompt_template = create_memory_prompt()
        self.ensure_memory_dir()

    def ensure_memory_dir(self):
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
            
    def extract_memory(self, chapter_text, chapter_number):
        input_data = {
            'chapter_text': chapter_text,
            'chapter_number': chapter_number
        }
        
        memory = self.prompt_template | self.llm
        response = memory.invoke(input=input_data)
        return response.content

    def save_memory(self, memory_data, chapter_number, filename=None):
        if not filename:
            filename = f'chapter_memory_{chapter_number:03d}.json'
        filepath = os.path.join(self.memory_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, ensure_ascii=False, indent=4)
            
    def run(self, chapter_text, chapter_number):
        print(f"正在从第{chapter_number}章提取记忆...")
        memory_data = self.extract_memory(chapter_text, chapter_number)
        print("记忆提取完毕，正在保存...")
        self.save_memory(memory_data, chapter_number)
        print("记忆保存完成。")

if __name__ == "__main__":
    agent = MemoryAgent()
    with open('data/chapters/chapter_001.txt', 'r', encoding='utf-8') as f:
        chapter_text = f.read()
    agent.run(chapter_text, 1)