# ChapterAgent.py

import os
import json
from agents.Agent_llm import initialize_llm, create_chapter_prompt

class ChapterAgent:
    def __init__(self, outline_file, memory_dir='output/memory', output_dir='output/chapters'):
       self.memory_dir = memory_dir
       self.output_dir = output_dir
       self.llm = initialize_llm()
       self.prompt_template = create_chapter_prompt()
       self.outline = self.load_outline(outline_file)
       self.ensure_dirs()
       
    def ensure_dirs(self):
       for dir in [self.memory_dir, self.output_dir]:
           if not os.path.exists(dir):
               os.makedirs(dir)

    def load_outline(self, outline_file):
       filepath = os.path.join(self.memory_dir, outline_file)
       with open(filepath, 'r', encoding='utf-8') as f:
           return f.read()

    def load_memory(self):
       memory = {}
       memory_files = os.listdir(self.memory_dir)
       for file in memory_files:
           if file.endswith('.json'):
               with open(os.path.join(self.memory_dir, file), 'r', encoding='utf-8') as f:
                   memory[file.replace('.json','')] = json.load(f)
       return memory

    def get_previous_chapters(self):
       chapters = []
       chapter_files = sorted(os.listdir(self.output_dir))
       for file in chapter_files:
           if file.endswith('.txt'):
               with open(os.path.join(self.output_dir, file), 'r') as f:
                   chapters.append(f.read())
       return chapters

    def generate_chapter(self, chapter_number):
        if chapter_number == 1:
            # 第一章只需要大纲信息
            input_data = {
                'outline': self.outline,
                'memory': {},  # 空字典
                'previous_chapters': [], # 空列表 
                'chapter_number': chapter_number
            }
        else:
            # 后续章节需要加载记忆和之前章节
            # memory = self.load_memory()
            # prev_chapters = self.get_previous_chapters()
            input_data = {
                'outline': self.outline,
                # 'memory': memory,
                'memory': {},
                # 'previous_chapters': prev_chapters,
                'chapter_number': chapter_number
            }
            
        chapter = self.prompt_template | self.llm
        response = chapter.invoke(input=input_data)
        return response.content

    def save_chapter(self, chapter_text, chapter_number):
       filename = f'chapter_{chapter_number:03d}.txt'
       filepath = os.path.join(self.output_dir, filename)
       with open(filepath, 'w', encoding='utf-8') as f:
           f.write(chapter_text)
       print(f"第{chapter_number}章已保存到 {filepath}")

    def run(self, chapter_number):
       print(f"正在生成第{chapter_number}章...")
       chapter_text = self.generate_chapter(chapter_number)
       print("章节生成完毕，正在保存...")
       self.save_chapter(chapter_text, chapter_number)
       print("章节生成流程完成。")

if __name__ == "__main__":
   agent = ChapterAgent('novel_outline.json')
   agent.run(chapter_number=1)
